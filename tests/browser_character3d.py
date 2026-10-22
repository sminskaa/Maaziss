#!/usr/bin/env python3
"""Focused offline construction-study QA, not final character-art approval.

The private model and supplied-FBX poses remain in ignored build/checks/.
Verify closed geometry, actual skinned positions, camera occlusion and controls;
capture the rendered result for visual review rather than infer appearance from
the existence of objects alone.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
GARMENTS = {'Shirt', 'Jacket', 'Belt', 'Pants', 'Boots', 'Bag'}
GROUPS = {'Head and neck', 'Eyes', 'Mouth', 'Upper arms', 'Lower arms', 'Hands',
          'Upper legs', 'Lower legs', 'Feet', *GARMENTS}


def closed_mesh(item):
    """Weld coincident export vertices before counting triangle incidence."""
    positions = np.asarray(item['positions']).reshape(-1, 3)
    keys, ids = {}, []
    for position in positions:
        key = tuple(round(float(value), 5) for value in position)
        ids.append(keys.setdefault(key, len(keys)))
    edges = Counter()
    adjacency = {}
    for triangle in np.asarray(item['indices']).reshape(-1, 3):
        a, b, c = (ids[index] for index in triangle)
        if len({a, b, c}) < 3:
            continue
        for x, y in ((a, b), (b, c), (c, a)):
            edges[tuple(sorted((x, y)))] += 1
            adjacency.setdefault(x, set()).add(y)
            adjacency.setdefault(y, set()).add(x)
    visited, components = set(), 0
    for vertex in adjacency:
        if vertex in visited:
            continue
        components += 1
        pending = [vertex]
        visited.add(vertex)
        while pending:
            for neighbor in adjacency[pending.pop()] - visited:
                visited.add(neighbor)
                pending.append(neighbor)
    return {'name': item['name'], 'boundary': sum(n == 1 for n in edges.values()),
            'nonmanifold': sum(n > 2 for n in edges.values()), 'components': components}


def image_from_url(url, path):
    path.write_bytes(base64.b64decode(url.split(',', 1)[1]))
    return np.asarray(Image.open(path).convert('RGB'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html', type=Path, default=ROOT/'visual-preview/maziss-3d-study.html')
    parser.add_argument('--manifest', type=Path, default=ROOT/'build/checks/character3d/build-manifest.json')
    parser.add_argument('--output', type=Path, default=ROOT/'build/checks/character3d/qa')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    source = args.html.read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    manifest = json.loads(args.manifest.read_text())
    data = json.loads((ROOT/'build/checks/character3d/model-private.json').read_text())
    passed, failed, warnings, errors, requests = [], [], [], [], []

    def check(value, label, evidence=None):
        (passed if value else failed).append({'check': label, 'evidence': evidence})

    def source_match():
        return all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected
                   for name, expected in manifest['source_sha256'].items())

    check(digest == manifest['output_sha256'], 'Actual HTML matches the frozen build manifest')
    check(source_match(), 'Actual model and viewer sources match the frozen manifest')
    check(GROUPS <= {item['group'] for item in data['objects']},
          'Requested anatomy, garments and equipment have independently inspectable geometry')
    topology = [closed_mesh(item) for item in data['objects']]
    defects = [item for item in topology if item['boundary'] or item['nonmanifold']]
    check(not defects, 'Every exported object has closed, two-triangle-edge geometry after coordinate welding', defects)
    principal = [item for item in topology if item['name'] in ('Shirt', 'Pants', 'Jacket')]
    check(len(principal) == 3 and all(item['components'] == 1 for item in principal),
          'Shirt, pants and jacket each form one connected garment surface', principal)
    malformed = []
    for item in data['objects']:
        vertex_count = len(item['positions'])//3
        weights = np.asarray(item['skinWeights']).reshape(-1, 4)
        indices = np.asarray(item['skinIndices'])
        if (not np.isfinite(item['positions']).all() or not np.isfinite(item['normals']).all()
                or len(item['normals']) != vertex_count*3 or len(weights) != vertex_count
                or not np.allclose(weights.sum(axis=1), 1, atol=3e-6)
                or np.min(weights) < 0 or np.max(indices) >= len(data['bones'])
                or max(item['indices']) >= vertex_count):
            malformed.append(item['name'])
    check(not malformed, 'All actual vertices have finite normals and valid normalized skin weights', malformed)
    lengths = np.array([[math.dist(bone['head'], bone['tail']) for bone in frame]
                        for frame in data['motion']['frames']])
    drift = float(np.max(np.ptp(lengths, axis=0)))
    check(drift < 1e-6, 'All FBX-retargeted bone segment lengths remain fixed through the cycle', drift)
    endpoint = max(math.dist(a[key], b[key])
                   for a, b in zip(data['motion']['frames'][0], data['motion']['frames'][-1])
                   for key in ('head', 'tail'))
    check(endpoint < 1e-5, 'Private walking cycle repeats at its actual endpoints', endpoint)
    for group in ('Eyes', 'Mouth'):
        rigid = all(all(data['bones'][index]['name'] == 'Head'
                        for index, weight in zip(item['skinIndices'], item['skinWeights']) if weight > 0)
                    for item in data['objects'] if item['group'] == group)
        check(rigid, group+' geometry remains attached to the shared head bone')
    bag_bones = {data['bones'][index]['name'] for item in data['objects'] if item['group'] == 'Bag'
                 for index, weight in zip(item['skinIndices'], item['skinWeights']) if weight > 0}
    check(bag_bones == {'Spine'}, 'Bag shell, strap, fastenings and tools share one rigid transform without fragment detachment', sorted(bag_bones))

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path='/usr/bin/chromium',
                  args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        context = browser.new_context(offline=True, viewport={'width': 1450, 'height': 1150})
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda request: requests.append(request.url))
        page.set_content(source.decode(), wait_until='load')
        page.wait_for_function('window.maziss3d && maziss3d.ready', timeout=30000)
        state = page.evaluate('maziss3d.getState()')
        check(state['objects'] == len(data['objects']), 'Every exported object is present in the actual renderer', state['objects'])
        check(page.locator('#fallback').is_hidden(), 'Successful viewer hides its loading/fallback message')
        depth = page.evaluate('maziss3d.meshes.every(({mesh})=>mesh.material.depthTest && mesh.material.depthWrite)')
        check(depth, 'All actual body and garment materials use camera depth occlusion')
        opaque = page.evaluate('maziss3d.meshes.every(({mesh})=>!mesh.material.map && !mesh.material.transparent && mesh.material.opacity===1 && mesh.material.alphaTest===0)')
        check(opaque, 'Actual construction uses opaque geometry without image cutouts or alpha masks')
        page.click('#pause')
        frozen = page.evaluate('maziss3d.getState().phase')
        page.wait_for_timeout(150)
        check(page.evaluate('maziss3d.getState().phase') == frozen, 'Actual Pause control freezes the walking pose')
        page.click('#step')
        step = page.evaluate('maziss3d.getState()')
        expected = 1/30/data['motion']['cycleSeconds']
        check(abs((step['phase']-frozen) % 1-expected) < 1e-8 and not step['playing'],
              'Actual frame-step control uses the FBX cycle timing')
        page.click('#idle')
        check(not page.evaluate('maziss3d.getState().walk'), 'Actual Stand still control selects the authored neutral pose')
        page.click('#anatomy')
        visibility = page.evaluate('maziss3d.getState().visible')
        check(all(not visibility[group] for group in GARMENTS)
              and all(visible for group, visible in visibility.items() if group not in GARMENTS),
              'Body only hides clothing while retaining complete underlying anatomy')
        anatomy = []
        for angle in (0, 90, 180, 270):
            page.evaluate('(a)=>maziss3d.setView(a)', angle)
            file = args.output/f'anatomy-idle-{angle}.png'
            image_from_url(page.evaluate('maziss3d.snapshot()'), file)
            anatomy.append(file)
        page.click('#dressed')
        check(all(page.evaluate('maziss3d.getState().visible').values()), 'Dressed restores all independently modeled parts')

        # Measure the actual shader-equivalent skinned vertex positions, including
        # every boot vertex, instead of inferring geometry health from bone names.
        geometry = page.evaluate('''()=>{
          const out=[];
          for(let i=0;i<24;i++){
            maziss3d.setPhase(i/24);
            let bad=0,minZ=Infinity,maxZ=-Infinity,minBootZ=Infinity,maxRadius=0;
            for(const{mesh,item}of maziss3d.meshes){
              const v=new THREE.Vector3();
              for(let k=0;k<mesh.geometry.attributes.position.count;k++){
                mesh.getVertexPosition(k,v);
                if(!Number.isFinite(v.x+v.y+v.z))bad++;
                minZ=Math.min(minZ,v.z);maxZ=Math.max(maxZ,v.z);
                maxRadius=Math.max(maxRadius,Math.hypot(v.x,v.y));
                if(item.group==='Boots')minBootZ=Math.min(minBootZ,v.z);
              }
            }
            out.push({frame:i,bad,minZ,maxZ,minBootZ,maxRadius});
          }
          return out;
        }''')
        check(not any(sample['bad'] for sample in geometry), 'Actual skinned vertices remain finite across 24 walking poses')
        check(all(sample['maxRadius'] < 1 and 1.5 < sample['maxZ'] < 2.5 for sample in geometry),
              'Actual skinned meshes remain within a human-sized body envelope')
        floor_min = min(sample['minBootZ'] for sample in geometry)
        if floor_min < -.005:
            warnings.append({'limitation': 'Boot geometry intersects the floor during some poses', 'minimum_z_metres': floor_min})
        (args.output/'geometry-results.json').write_text(json.dumps(geometry, indent=2)+'\n')

        # Facial details must visibly occlude behind the head from the rear.
        # Suppress cast shadows only for this comparison: otherwise removing an
        # occluded eye can legitimately change its shadow on a visible shoulder.
        page.evaluate('()=>{maziss3d.renderer.shadowMap.enabled=false;maziss3d.draw()}')
        facial_pixels = {}
        for angle in (0, 180):
            page.evaluate('(a)=>{maziss3d.setView(a);maziss3d.setPhase(.25)}', angle)
            for group in ('Eyes', 'Mouth'):
                before = image_from_url(page.evaluate('maziss3d.snapshot()'), args.output/f'occlusion-{angle}-{group}-on.png')
                page.locator(f'input[data-group="{group}"]').uncheck()
                after = image_from_url(page.evaluate('maziss3d.snapshot()'), args.output/f'occlusion-{angle}-{group}-off.png')
                facial_pixels[f'{angle}-{group}'] = int(np.count_nonzero(np.max(np.abs(before.astype(int)-after.astype(int)), axis=2) > 10))
                page.locator(f'input[data-group="{group}"]').check()
        for group in ('Eyes', 'Mouth'):
            check(facial_pixels[f'0-{group}'] > 3 and facial_pixels[f'180-{group}'] == 0,
                  group+' renders on the face and is actually occluded by the head from behind',
                  {key: value for key, value in facial_pixels.items() if group in key})
        page.evaluate('()=>{maziss3d.renderer.shadowMap.enabled=true;maziss3d.draw()}')

        captures = []
        for angle in range(0, 360, 45):
            page.locator('#dressed').click()
            for frame in range(4):
                phase = frame/4
                page.evaluate('([a,p])=>{maziss3d.setView(a);maziss3d.setPhase(p)}', [angle, phase])
                file = args.output/f'dressed-{angle}-{frame}.png'
                pixels = image_from_url(page.evaluate('maziss3d.snapshot()'), file)
                captures.append({'angle': angle, 'phase': phase, 'file': file.name,
                                 'unique_colors': len(np.unique(pixels.reshape(-1, 3), axis=0))})
        check(all(capture['unique_colors'] > 100 for capture in captures),
              'Actual rendered character frames contain visible shaded geometry at eight camera angles', len(captures))
        sheet = Image.new('RGB', (1200, 8*270), '#20262c')
        draw = ImageDraw.Draw(sheet)
        for index, capture in enumerate(captures):
            im = Image.open(args.output/capture['file']).convert('RGBA')
            backdrop = Image.new('RGBA', im.size, '#68717a')
            backdrop.alpha_composite(im)
            im = backdrop.convert('RGB');im.thumbnail((300, 240))
            x, y = index % 4*300, index//4*270
            sheet.paste(im, (x, y+25))
            draw.text((x+5, y+5), f"{capture['angle']} degrees / phase {capture['phase']}", fill='white')
        sheet.save(args.output/'walking-sheet.png')
        page.click('#wire')
        check(page.evaluate('maziss3d.meshes.every(({mesh})=>mesh.material.wireframe)'), 'Wireframe exposes every mesh for geometry inspection')
        page.click('#wire')
        page.click('button[data-angle="90"]')
        check(abs(page.evaluate('maziss3d.getState().angle')-math.pi/2) < 1e-8,
              'Actual side-view camera button orients the 3D model')
        box = page.locator('#model').bounding_box()
        initial_angle = page.evaluate('maziss3d.getState().angle')
        page.mouse.move(box['x']+400, box['y']+300);page.mouse.down()
        page.mouse.move(box['x']+470, box['y']+300);page.mouse.up()
        check(abs(page.evaluate('maziss3d.getState().angle')-initial_angle) > .1,
              'Actual drag gesture orbits to an intermediate camera angle')
        check(not errors, 'No JavaScript runtime errors', errors)
        check(not requests, 'Self-contained viewer runs with browser networking disabled', requests)
        browser_version = browser.version
        browser.close()

    check(hashlib.sha256(args.html.read_bytes()).hexdigest() == digest,
          'HTML did not change during the focused run')
    check(source_match(), 'Model and runtime sources did not change during the focused run')
    result = {'build': manifest['build'], 'html_sha256': digest, 'passed': passed,
              'failed': failed, 'warnings': warnings, 'closed_objects': len(topology),
              'walking_captures': len(captures), 'anatomy_captures': len(anatomy),
              'browser': browser_version, 'seconds': round(time.monotonic()-started, 2),
              'limits': ['Closed meshes can still intersect each other or stretch under skinning.',
                         'This is preliminary construction geometry, not final Maziss art or clothing approval.',
                         'No native Windows or Godot execution is covered; software WebGL is not player performance evidence.']}
    (args.output/'browser-results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'build': manifest['build'][:12], 'passed': len(passed),
                      'failed': failed, 'warnings': warnings, 'seconds': result['seconds']}))
    raise SystemExit(bool(failed))


if __name__ == '__main__':
    main()
