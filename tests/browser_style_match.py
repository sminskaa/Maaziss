#!/usr/bin/env python3
"""Check delivery and retained-source identity for the lighting/style study.

This cannot judge artistic likeness. Actual still/video inspection is documented
separately in production/QA_STYLE_MATCH.md. Captures and generated media stay private.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINES = {
    'art/walking/apartment-background.png': '489f564dbdd85d44695ac010f164547a274e4df7fea4435cb36c8d0f9be233f2',
    'art/proposals/apartment-cartoon-v2.png': '1df8148642288823ae6123f9551fe33288a975f696e637017ffb4360f4b2b710',
    'art/walking/maziss-depth-atlas.png': '0a16ef505caf1f5b761d57401cf9832bca05a0c95dad94edee3c57bf5ebca88c',
    'art/walking/maziss-side-atlas.png': '4cbf9432159d8a59695dbfad88cf1b234628df84a6aa1397f656c2427a3ba18b',
    'build/checks/supplied-character/maziss-supplied-rig.glb': 'eb3c9fb665f186221378cbe25bcc5739cc14c1b86259e11bae8d28f0debd1b06',
    'build/checks/supplied-character/motion-private.json': '55145ab633384f5d1e2de9c9bc771b0fd7cf3fdb2e8712ac1ea73d38d79e3131',
}


def audit(html: Path, output: Path):
    from playwright.sync_api import sync_playwright
    result = {'html': str(html.relative_to(ROOT)), 'bytes': html.stat().st_size,
              'sha256': hashlib.sha256(html.read_bytes()).hexdigest(), 'viewports': []}
    assert result['bytes'] <= 1_000_000, 'Compact review exceeds its one-MB delivery budget'
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        result['browser'] = browser.version
        for name, width, height in [('desktop', 1280, 1000), ('mobile', 390, 844)]:
            errors, external = [], []
            context = browser.new_context(offline=True, viewport={'width': width, 'height': height})
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('request', lambda request: external.append(request.url)
                    if request.url.startswith(('http:', 'https:')) else None)
            page.set_content(html.read_text(), wait_until='load')
            page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
            assert page.locator('img').count() > 0, 'Native still fallback is missing'
            assert page.locator('script').count() == 0, 'Review requires application JavaScript'
            videos = []
            for number in range(page.locator('video').count()):
                video = page.locator('video').nth(number)
                video.scroll_into_view_if_needed()
                page.wait_for_function('(n)=>document.querySelectorAll("video")[n].readyState>=2', arg=number)
                metadata = video.evaluate('(v)=>({width:v.videoWidth,height:v.videoHeight,duration:v.duration,controls:v.controls})')
                assert metadata['width'] > 0 and metadata['height'] > 0 and metadata['controls']
                assert metadata['duration'] > 0
                video.evaluate('(v)=>{v.muted=true;v.currentTime=0;return v.play()}')
                page.wait_for_function('(n)=>document.querySelectorAll("video")[n].currentTime>.15', arg=number)
                video.evaluate('(v)=>v.pause()')
                metadata['playbackAdvanced'] = True
                videos.append(metadata)
            page.evaluate('window.scrollTo(0,0)')
            overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth+1')
            assert not overflow, f'{name}: horizontal page overflow'
            assert not errors, errors
            assert not external, external
            capture = f'review-{name}.png'
            page.screenshot(path=str(output/capture), full_page=True)
            result['viewports'].append({'name': name, 'videos': videos, 'imageCount': page.locator('img').count(),
                                        'horizontalOverflow': overflow, 'errors': errors,
                                        'externalRequests': external, 'capture': capture})
            context.close()
        browser.close()
    return result


def render_audit(manifest_path: Path):
    from PIL import Image
    manifest = json.loads(manifest_path.read_text())
    source = ROOT/'build/checks/supplied-character/maziss-supplied-rig.blend'
    assert manifest['sourceBlendSHA256'] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert manifest['geometryChanged'] is False and manifest['motionChanged'] is False
    assert manifest['imageProjectionUsed'] is False
    assert 'Fixed camera' in manifest['headingConvention']
    assert len(manifest['views']) >= 3
    assert len(manifest['walk']) == 24, 'Final review requires the full sampled walking cycle'
    names = [view['idle'] for view in manifest['views']] + manifest['walk']
    images = []
    for name in names:
        path = manifest_path.parent/name
        with Image.open(path) as im:
            assert im.size == (480, 640) and im.mode == 'RGBA'
            assert im.getchannel('A').getbbox(), f'{name}: empty model render'
        images.append({'name': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    return {'manifestSHA256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
            'sourceBlendSHA256': manifest['sourceBlendSHA256'], 'images': images,
            'cycleSeconds': manifest['cycleSeconds'], 'headingConvention': manifest['headingConvention']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html', type=Path, required=True)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT/'build/checks/style-match/qa')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    retained = {name: {'expected': expected, 'actual': hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}
                for name, expected in BASELINES.items()}
    assert all(item['expected'] == item['actual'] for item in retained.values()), 'A retained model, motion or approved drawing changed'
    result = {'retainedSources': retained, 'delivery': audit(args.html.resolve(), args.output),
              'scope': 'Source preservation and actual offline native-media playback; artistic verdict requires image inspection.',
              'deliveryLimit': 'Internal Chromium success does not establish host-panel availability.'}
    if args.manifest:
        result['renderManifest'] = render_audit(args.manifest)
    (args.output/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
