#!/usr/bin/env python3
"""Actual offline browser interactions and captures for the fixed-sofa review.

This checks the public controls and records actual canvas screenshots. It does
not approve the art, assert full room physics or certify a production rig.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCENE = (1672, 941)


def render_audit(path: Path):
    """Check declared actual images, preserving visual judgement as a separate step."""
    manifest = json.loads(path.read_text())
    checked = []
    for key, source in [('sourceBlendSHA256', ROOT/'build/checks/supplied-character/maziss-supplied-rig.blend'),
                        ('sourceGLBSHA256', ROOT/'build/checks/supplied-character/maziss-supplied-rig.glb'),
                        ('poseScriptSHA256', ROOT/'tools/character_sitting_pose.py'),
                        ('renderScriptSHA256', ROOT/'tools/render_sofa_sit.py')]:
        assert hashlib.sha256(source.read_bytes()).hexdigest() == manifest[key], key+' mismatch'
    names = list(manifest['sit']) + list(manifest['idle'].values()) + list(manifest.get('turn', {}).values())
    for samples in manifest['walk'].values(): names.extend(samples)
    assert len(manifest['sit']) == 41 and len(manifest['walk']) == 8 and len(manifest['turn']) == 8
    assert all(len(v) == 24 for v in manifest['walk'].values())
    for name in names:
        source = path.parent/name
        with Image.open(source) as image:
            assert image.size == (manifest['width'], manifest['height'])
            assert image.mode == 'RGBA' and image.getchannel('A').getbbox()
        checked.append({'name':name, 'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
    assert len(manifest['contacts']) == 41
    assert all(c['finite'] and c['bodyVertices'] == 4906 and abs(c['minimumZ']) < .00001
               for c in manifest['contacts'])
    assert manifest['groundPixel'][1] > 300, 'Camera projection was captured before transform update'
    return {'manifestSHA256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'images':checked, 'contacts':manifest['contacts'],
            'groundPixel':manifest['groundPixel'], 'seatContactPixel':manifest['seatContactPixel']}


def browser_audit(html: Path, output: Path, focused=False):
    raw = html.read_bytes()
    report = {'html': str(html.relative_to(ROOT)), 'bytes': len(raw),
              'sha256': hashlib.sha256(raw).hexdigest(), 'checks': [],
              'states': [], 'captures': [], 'viewports': [], 'focused':focused}
    def check(ok, label, evidence=None):
        report['checks'].append({'check': label, 'passed': bool(ok), 'evidence': evidence})
        if not ok:
            (output/'results.json').write_text(json.dumps(report, indent=2)+'\n')
            raise AssertionError(f'{label}: {evidence}')
    check(len(raw) <= 1_050_000, 'Compact interactive review stays near one MB', len(raw))
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        report['browser'] = browser.version
        errors = []; requests = []
        context = browser.new_context(offline=True, viewport={'width': 1280, 'height': 1000})
        page = context.new_page()
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('request', lambda r: requests.append(r.url) if r.url.startswith(('http:', 'https:')) else None)
        page.set_content(raw.decode(), wait_until='load')
        page.wait_for_function('window.mazissReview && typeof mazissReview.snapshot === "function"')
        page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
        state = lambda: page.evaluate('mazissReview.snapshot()')
        canvas = page.locator('canvas').first
        def capture(name):
            path = output/(name+'.png')
            canvas.screenshot(path=str(path))
            report['captures'].append(path.name)
            report['states'].append({'capture': name, 'state': state()})
        def click(x, y, button='left'):
            box = canvas.bounding_box()
            assert box
            page.mouse.click(box['x']+x/SCENE[0]*box['width'],
                             box['y']+y/SCENE[1]*box['height'], button=button)
        def sample(seconds):
            started = time.monotonic(); seen = []
            while time.monotonic()-started < seconds:
                snap = state(); seen.append(snap)
                page.wait_for_timeout(60)
            return seen
        capture('initial')
        report['initialState'] = state()
        report['canvas'] = canvas.evaluate('(c)=>({width:c.width,height:c.height})')
        check(report['canvas'] == {'width':1672,'height':941},
              'Actual canvas uses the calibrated room coordinates', report['canvas'])
        check(state()['loaded'] and state()['mode'] == 'idle', 'Starts in a loaded neutral idle state')
        position0 = state()['position']
        click(900, 150); page.wait_for_timeout(160)
        check(state()['position'] == position0 and state()['mode'] == 'idle',
              'Wall click does not move Maziss')
        click(1530, 600); page.wait_for_timeout(160)
        check(state()['position'] == position0 and state()['mode'] == 'idle',
              'Desk/furniture click does not move Maziss')
        page.get_by_role('button', name='Use', exact=True).click()
        click(430, 590, 'right'); page.wait_for_timeout(100)
        check(state()['selectedVerb'] == 'Use' and state()['mode'] == 'idle',
              'Right-click examines sofa while preserving Use; it does not sit')
        click(430, 590)
        approach = sample(.6)
        check(any(s['mode'] == 'walking' and s['pendingSit'] for s in approach),
              'Use plus sofa click starts an actual approach before sitting')
        capture('approaching')
        observed = approach[:]
        descent_captured = False
        started = time.monotonic()
        while state()['mode'] != 'seated' and time.monotonic()-started < 14:
            snap = state(); observed.append(snap)
            if snap['mode'] == 'sitting' and .35 < snap['sitProgress'] < .7 and not descent_captured:
                capture('descending'); descent_captured = True
            page.wait_for_timeout(45)
        check(state()['mode'] == 'seated', 'Approach, turn and descent finish in seated state')
        modes = list(dict.fromkeys(s['mode'] for s in observed))
        check(all(v in modes for v in ['walking','turning','sitting']),
              'Observed a walk, turn and authored sit transition', modes)
        check(descent_captured, 'Captured an actual intermediate sitting frame')
        seated = state(); capture('seated')
        check(seated['sitProgress'] == 1 and seated['renderFrame'] == 40,
              'Final seated pose uses the complete authored descent')
        check(math.dist([seated['position']['x'],seated['position']['y']], seated['seat']['origin']) < 1,
              'Sitting uses its calibrated fixed floor/seat anchor')
        # Clicking any part of the sofa selects the same empty cushion. The
        # pillows are room art and do not become additional seating positions.
        click(290, 510); page.wait_for_timeout(160)
        check(state()['mode'] == 'seated' and state()['position'] == seated['position'],
              'A pillow-side sofa click keeps the one fixed clear seat')
        page.locator('#guide').check(); capture('seated-guide'); page.locator('#guide').uncheck()
        click(1230, 820)
        check(state()['mode'] == 'standing', 'Floor click while seated starts standing first')
        standing = sample(.55); capture('standing')
        check(any(s['mode'] == 'standing' and 0 < s['sitProgress'] < 1 for s in standing),
              'Standing reverses the authored descent instead of teleporting')
        page.wait_for_function('mazissReview.snapshot().mode === "walking"', timeout=4000)
        capture('walking-after-stand')
        route_samples = sample(3.6)
        page.wait_for_function('mazissReview.snapshot().mode === "idle"', timeout=7000)
        walked = state(); capture('arrived')
        check(math.dist([walked['position']['x'],walked['position']['y']], [1230,820]) < 1.5,
              'After standing, actual walking reaches the clicked floor')
        check(walked['walkDistance'] > seated['walkDistance'], 'Walk cycle advances with floor travel')
        def inside(point, polygon):
            hit = False; j = len(polygon)-1
            for i, a in enumerate(polygon):
                b = polygon[j]
                if (a[1]>point['y']) != (b[1]>point['y']) and point['x'] < (b[0]-a[0])*(point['y']-a[1])/(b[1]-a[1])+a[0]: hit = not hit
                j = i
            return hit
        check(all(inside(s['position'], walked['floor']) for s in observed+route_samples),
              'Recorded approach and departure positions stay inside the furniture-buffered floor')
        scales = [s['scalePixelsPerMetre'] for s in observed+route_samples]
        check(all(math.isfinite(v) and 170 < v < 310 for v in scales),
              'Scale remains finite and tied to calibrated floor depth', {'minimum':min(scales),'maximum':max(scales)})
        detour_samples = []
        if not focused:
            # A long cross-room trip exercises a concave-floor detour instead of
            # only the direct line between the centre and sofa approach point.
            click(250, 875)
            check(state()['mode'] == 'walking', 'Far floor click starts a cross-room walk')
            detour_samples = sample(4.8)
            page.wait_for_function('mazissReview.snapshot().mode === "idle"', timeout=7000)
            check(all(inside(s['position'], walked['floor']) for s in detour_samples),
                  'Cross-room route remains on floor around furniture')
            check(math.dist([state()['position']['x'],state()['position']['y']], [250,875]) < 1.5,
                  'Cross-room walk reaches its destination')
            capture('cross-room')
        page.get_by_role('button', name='Reset', exact=True).click()
        check(state()['mode'] == 'idle' and state()['position'] == position0 and state()['selectedVerb'] == 'Walk',
              'Reset restores the initial place and selected verb')
        if not focused:
            # Resizing changes CSS presentation but not source-space pointer targets.
            for width,height in [(960,800),(390,844)]:
                page.set_viewport_size({'width':width,'height':height}); page.wait_for_timeout(120)
                page.get_by_role('button', name='Use', exact=True).click(); click(430,590)
                page.wait_for_function('mazissReview.snapshot().mode === "seated"', timeout=16000)
                current = state(); capture('seated-'+str(width))
                overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth+1')
                check(not overflow, str(width)+': no horizontal page overflow')
                check(current['position'] == seated['position'], str(width)+': pointer conversion reaches the same seat')
                report['viewports'].append({'width':width,'height':height,'horizontalOverflow':overflow,
                                            'seatPosition':current['position']})
                page.get_by_role('button', name='Reset', exact=True).click()
        check(not errors, 'No JavaScript errors during interaction and resize', errors)
        check(not requests, 'No network requests with networking disabled', requests)
        report['observedModes'] = modes
        report['approachSamples'] = observed
        report['routeSamples'] = route_samples+detour_samples
        context.close(); browser.close()
    check(hashlib.sha256(html.read_bytes()).hexdigest() == report['sha256'],
          'Review HTML stayed unchanged during this QA pass')
    (output/'results.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


def media_decode_audit(report):
    """Inspect recorded actual media clocks, rather than desired sprite indices."""
    records = report['approachSamples'] + report['routeSamples']
    groups = []
    for mode, prefix in [('walking','walk-'), ('sitting','sit')]:
        media = [s.get('media',{}) for s in records if s['mode'] == mode
                 and s.get('media',{}).get('activeSheet','').startswith(prefix)
                 and s.get('media',{}).get('currentTime') is not None]
        assert media, mode+': no decoded media observations'
        times = [m['currentTime'] for m in media]
        assert max(times)-min(times) > .2, mode+': decoded media did not advance'
        assert any(m['readyState'] >= 2 and not m['paused'] for m in media)
        groups.append({'mode':mode, 'samples':len(media),
                       'currentTimeRange':[min(times),max(times)],
                       'readyStates':sorted(set(m['readyState'] for m in media))})
    seated = next(s['state']['media'] for s in report['states'] if s['capture'] == 'seated')
    assert seated['paused'] and abs(seated['currentTime']-seated['duration']) < .1
    return {'htmlSHA256':report['sha256'], 'observedDecodedMedia':groups,
            'seated':seated, 'scope':'Actual media advancement and held endpoint; alpha/composite appearance requires image inspection.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--focused', action='store_true', help='Repeat the key sit/stand workflow after an encoding-only change')
    parser.add_argument('--html', type=Path, default=ROOT/'visual-preview/maziss-sofa-sit.html')
    parser.add_argument('--manifest', type=Path, default=ROOT/'build/checks/sofa-sit/render-manifest.json')
    parser.add_argument('--output', type=Path, default=ROOT/'build/checks/sofa-sit/qa')
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    render_report = render_audit(args.manifest.resolve())
    (args.output/'render-audit.json').write_text(json.dumps(render_report, indent=2)+'\n')
    result = browser_audit(args.html.resolve(), args.output.resolve(), args.focused)
    media_report = media_decode_audit(result)
    (args.output/'media-decode.json').write_text(json.dumps(media_report, indent=2)+'\n')
    print(json.dumps({'checks':len(result['checks']), 'bytes':result['bytes'],
                      'sha256':result['sha256']}, indent=2))


if __name__ == '__main__': main()
