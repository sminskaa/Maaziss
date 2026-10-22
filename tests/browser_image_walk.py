#!/usr/bin/env python3
"""Scoped image-guided animation checks and actual browser pose captures.

Numerical continuity is evidence about glitches, not a score for naturalness.
This suite imports no FBX, video, personal footage or reference-image pixels.
"""
from __future__ import annotations

import base64
import functools
import hashlib
import http.server
import json
import math
from pathlib import Path
import threading
import time

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'build/checks/image-walk'
HTML = ROOT / 'visual-preview/maziss-walking-v6.html'


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    manifest = json.loads((OUTPUT / 'build-manifest.json').read_text())
    initial_hash = hashlib.sha256(HTML.read_bytes()).hexdigest()
    passed, failed, errors, requests, captures = [], [], [], [], []
    metrics = {}

    def check(ok, label, evidence=None):
        entry = label if evidence is None else {'check': label, 'evidence': evidence}
        (passed if ok else failed).append(entry)

    check(initial_hash == manifest['output_sha256'], 'Preview matches its build manifest')
    check(all(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
              for name, digest in manifest['source_sha256'].items()), 'Reviewed source hashes match the build')
    authored = json.loads((ROOT / 'walking/image-motion.json').read_text())
    check(authored['used_fbx'] is False and authored['used_video_tracking'] is False
          and authored['source_images_embedded'] is False,
          'Candidate explicitly uses an authored image-only method without embedded supplied media')

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1450, 'height': 1050})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('request', lambda request: requests.append(request.url))
            page.goto(f'http://127.0.0.1:{server.server_port}/visual-preview/maziss-walking-v6.html')
            page.wait_for_function('() => window.mazissWalk && mazissWalk.getState().ready')
            state = lambda: page.evaluate('mazissWalk.getState()')

            def capture(name, view):
                sample = state()
                box = page.locator('#room').bounding_box()
                scale = box['width'] / 1932
                page.screenshot(path=str(OUTPUT / name), clip={
                    'x': box['x'] + (sample['position']['x'] - 210) * scale,
                    'y': box['y'] + (sample['position']['y'] - 510) * scale,
                    'width': 420 * scale, 'height': 535 * scale})
                captures.append({'name': name, 'view': view, 'phase': sample['pose']['phase'], 'mode': sample['pose']['mode']})
                return sample

            initial = capture('idle.png', 'idle')
            h = initial['render']['baseHeight']
            rest_forward = max(abs(leg['base']['x'] - initial['pose']['pelvis']['x']) for leg in initial['pose']['legs'])
            check(initial['pose']['mode'] == 'idle' and rest_forward < .03 * h,
                  'Resting side-view soles sit under the pelvis rather than a stride ahead', rest_forward)
            check(max(abs(leg['heel']['y'] - leg['toe']['y']) for leg in initial['pose']['legs']) < 1e-7,
                  'Both neutral side-view heel-to-toe sole lines are level')

            # The test constructs an independent instance of the embedded runtime
            # class so sampling is deterministic and does not depend on browser FPS.
            deterministic = page.evaluate('''() => {
              const g=new MazissImageGait.Gait(IMAGE_MOTION),h=440,p={x:1000,y:700};
              g.reset(p,h);const poses=[];
              for(let i=0;i<660;i++){
                const active=i<480, t=i/120;
                const v=active?Math.min(200,1000*t,Math.max(0,(4-t)*1000)):0;
                p.x+=v/120;
                poses.push(g.update(p,h,1/120,active,{x:1,y:0},false));
              }
              const steady=new MazissImageGait.Gait(IMAGE_MOTION);steady.reset({x:0,y:0},h);
              for(let i=0;i<120;i++)steady.update({x:0,y:0},h,1/120,true,{x:1,y:0},true);
              const cycle=[];
              for(let i=0;i<520;i++)cycle.push(steady.update({x:0,y:0},h,1/240,true,{x:1,y:0},true));
              const resume=new MazissImageGait.Gait(IMAGE_MOTION),rp={x:0,y:0};resume.reset(rp,h);
              for(let i=0;i<120;i++){rp.x+=1.5;resume.update(rp,h,1/120,true,{x:1,y:0},false);}
              resume.update(rp,h,1/120,false,{x:1,y:0},false);
              for(let i=0;i<14;i++)resume.update(rp,h,1/120,false,{x:1,y:0},false);
              const settlingWeight=resume.pose.blend;
              rp.x+=1.5;const resumedWeight=resume.update(rp,h,1/120,true,{x:1,y:0},false).blend;
              for(let i=0;i<60;i++){rp.x+=1.5;resume.update(rp,h,1/120,true,{x:1,y:0},false);}
              const roomWeight=resume.pose.blend;
              const studyWeight=resume.update(rp,h,1/120,false,{x:1,y:0},true).blend;
              rp.x+=1.5;const roomAgainWeight=resume.update(rp,h,1/120,true,{x:1,y:0},false).blend;
              return {poses,cycle,transitions:{settlingWeight,resumedWeight,roomWeight,studyWeight,roomAgainWeight}};
            }''')
            poses, cycle = deterministic['poses'], deterministic['cycle']
            max_transition_cuff_step = max(math.hypot(b['cuff']['x']-a['cuff']['x'], b['cuff']['y']-a['cuff']['y'])
                                           for before, after in zip(poses, poses[1:]) for a, b in zip(before['legs'], after['legs']))
            max_transition_knee_step = max(abs((b['thigh']-b['shin'])-(a['thigh']-a['shin']))*180/math.pi
                                           for before, after in zip(poses, poses[1:]) for a, b in zip(before['legs'], after['legs']))
            max_cycle_knee_speed = max(abs((b['thigh']-b['shin'])-(a['thigh']-a['shin']))*240*180/math.pi
                                       for before, after in zip(cycle, cycle[1:]) for a, b in zip(before['legs'], after['legs']))
            min_knee_flex = min(abs(leg['thigh']-leg['shin'])*180/math.pi for pose in cycle for leg in pose['legs'])
            modes = list(dict.fromkeys(pose['mode'] for pose in poses))
            check(modes == ['starting', 'walking', 'settling', 'idle'], 'Deterministic traversal includes start, walk, settle and idle', modes)
            check(max_transition_cuff_step < 440*.03 and max_transition_knee_step < 10,
                  'Start/stop traversal has no cuff teleport or knee-angle jump at 120 Hz',
                  {'max_cuff_step_pixels': max_transition_cuff_step, 'max_knee_step_degrees': max_transition_knee_step})
            check(min_knee_flex > 5, 'Steady cycle avoids the straight-leg IK singularity', min_knee_flex)
            check(max_cycle_knee_speed < 450, 'Steady knee-angle motion avoids the rejected rapid-extension envelope', max_cycle_knee_speed)
            check(all(math.isfinite(leg['knee']['x']) and math.isfinite(leg['cuff']['y'])
                      for pose in poses + cycle for leg in pose['legs']), 'Sampled joint positions remain finite')
            transitions = deterministic['transitions']
            check(0 < transitions['settlingWeight'] < 1
                  and transitions['settlingWeight'] <= transitions['resumedWeight']
                  < transitions['settlingWeight']+.01,
                  'Interrupted settling resumes from current arm/torso blend without relaxing to zero', transitions)
            check(transitions['roomWeight'] == transitions['studyWeight'] == transitions['roomAgainWeight'] == 1,
                  'Room/study switching preserves a fully active arm/torso blend', transitions)
            metrics.update({'transition_max_cuff_step_at_120hz': max_transition_cuff_step,
                            'transition_max_knee_angle_step_at_120hz': max_transition_knee_step,
                            'steady_max_knee_degrees_per_second': max_cycle_knee_speed,
                            'steady_min_knee_flex_degrees': min_knee_flex,
                            'interruption_blends': transitions})

            for view, desired in {'right': (1, 0), 'front': (0, 1), 'back': (0, -1), 'left': (-1, 0)}.items():
                page.click(f'[data-view="{view}"]')
                if state()['paused']:
                    page.click('#pause')
                page.wait_for_timeout(450)
                page.click('#pause')
                phases = []
                for i in range(8):
                    phases.append(capture(f'{view}-phase-{i+1}.png', view))
                    page.evaluate('() => {for(let i=0;i<4;i++)document.getElementById("step").click();}')
                check(all(s['render']['source'] == 'first-proposal' and len(s['render']['joins']) == 2 for s in phases),
                      f'{view}: actual rendered poses retain original artwork and two boot/trouser joins')
                check(phases[-1]['pose']['yaw']['x']*desired[0]+phases[-1]['pose']['yaw']['y']*desired[1] > .999,
                      f'{view}: requested direction is used')
                check(all(abs(((s['pose']['legs'][1]['phase']-s['pose']['legs'][0]['phase'])%1)-.5) < 1e-9 for s in phases),
                      f'{view}: legs alternate half a cycle apart')
                if view in ('front', 'back'):
                    lane_error = max(abs(leg['knee']['x']-leg['hip']['x']) for s in phases for leg in s['pose']['legs'])
                    check(lane_error < 2, f'{view}: knees remain in their depth-view leg lanes', lane_error)
                phase_before = state()['pose']['phase']
                page.evaluate('() => {for(let i=0;i<162;i++)document.getElementById("step").click();}')
                check(abs(((state()['pose']['phase']-phase_before+.5)%1)-.5) < 1e-8,
                      f'{view}: frame stepping preserves the authored 1.08-second timing across five cycles')
            frozen = state()
            page.wait_for_timeout(250)
            check(state()['pose'] == frozen['pose'] and state()['render'] == frozen['render'],
                  'Paused study freezes painted transforms and the full pose')
            page.click('#pause')
            page.select_option('#playback', '0.5')
            phase_before = state()['pose']['phase']; clock_before = time.monotonic()
            page.wait_for_timeout(430)
            phase_delta = (state()['pose']['phase']-phase_before)%1
            elapsed = time.monotonic()-clock_before
            check(abs(phase_delta-elapsed/authored['cycle_seconds']*.5) < .05,
                  'Half-speed playback follows authored timing', {'phase_delta': phase_delta, 'elapsed': elapsed})
            page.select_option('#playback', '1')
            page.click('#stand')
            page.wait_for_function('()=>mazissWalk.getState().pose.mode==="idle"', timeout=3000)
            standing = capture('stand-after-study.png', 'standing')
            check(not standing['study'] and not standing['path']
                  and max(abs(leg['base']['x']-standing['pose']['pelvis']['x'])
                          for leg in standing['pose']['legs']) < .03*standing['render']['baseHeight'],
                  'Stand control settles the cycle into feet-under-pelvis rest')
            page.evaluate('mazissWalk.reset()')

            # Capture actual painted start/stop frames in addition to evaluating
            # deterministic geometry. These expose source-mask or drawing jumps
            # that joint-coordinate checks alone cannot detect.
            page.evaluate('mazissWalk.goTo(1450,690)')
            for i in range(6):
                page.wait_for_timeout(40)
                capture(f'starting-{i+1}.png', 'starting')
            page.wait_for_function('()=>mazissWalk.getState().pose.mode==="settling"', timeout=15000)
            for i in range(6):
                capture(f'settling-{i+1}.png', 'settling')
                page.wait_for_timeout(70)
            page.wait_for_function('()=>mazissWalk.getState().pose.mode==="idle"', timeout=3000)
            page.evaluate('mazissWalk.reset()')

            def walk(x, y):
                route = page.evaluate('p=>mazissWalk.goTo(...p)', [x, y])
                assert route['target'], route
                page.wait_for_function('()=>!mazissWalk.getState().path.length', timeout=15000)
                page.wait_for_function('()=>mazissWalk.getState().pose.mode==="idle"', timeout=3000)
                s = state()
                check(math.hypot(s['position']['x']-route['target']['x'], s['position']['y']-route['target']['y']) < .1,
                      f'Room traversal {x},{y} reaches the resolved destination')
                return route

            walk(500, 700)
            first = len(page.evaluate('mazissWalk.getGaitSamples()'))
            walk(1450, 700)
            straight = page.evaluate('mazissWalk.getGaitSamples()')[first:]
            # Only flat-sole loaded stance is fixed. Heel/toe rollover is allowed
            # to move its other painted points; its pivot is not the sole centre.
            contacts = {}; max_flat_drift = 0; pairs = 0
            for sample in straight:
                if sample['pose']['mode'] != 'walking' or sample['pose']['yaw']['x'] < .999999:
                    continue
                for leg in sample['pose']['legs']:
                    if not leg['stance'] or abs(leg['bootAngle']) > 1e-8:
                        continue
                    key = (leg['id'], leg['contactId'])
                    painted = next(j for j in sample['render']['joins'] if j['id'] == leg['id'])['paintedContact']
                    if key in contacts:
                        pairs += 1
                        old = contacts[key]
                        max_flat_drift = max(max_flat_drift, math.hypot(painted['x']-old['x'], painted['y']-old['y']))
                    contacts[key] = painted
            check(pairs > 5 and max_flat_drift < .01, 'Painted flat loaded soles stay fixed during aligned room walking',
                  {'observed_pairs': pairs, 'max_drift': max_flat_drift})
            capture('settled-after-route.png', 'settled')
            settled = state(); page.wait_for_timeout(150)
            check(state()['pose'] == settled['pose'], 'Arrived character holds a stable idle pose')
            walk(1030, 563)
            detour = walk(1460, 598)
            check(len(detour['path']) > 2, 'Furniture detour uses a genuine multi-segment route')
            check(all(page.evaluate('p=>mazissWalk.navigation.isWalkable(p)', p) for p in state()['samples']),
                  'Recorded root substeps remain on walkable buffered floor')
            before = state()['position']; rejected = page.evaluate('mazissWalk.goTo(900,100)')
            page.wait_for_timeout(80)
            check(rejected['status'] == 'unreachable' and state()['position'] == before,
                  'High wall click is rejected without moving')
            page.evaluate('mazissWalk.goTo(500,700)'); page.wait_for_timeout(120)
            page.click('#pause'); page.wait_for_timeout(40)
            frozen = state(); page.wait_for_timeout(200)
            check(state()['position'] == frozen['position'] and state()['pose'] == frozen['pose'], 'Room pause freezes navigation and the full pose')
            page.click('#pause')
            page.wait_for_function('()=>!mazissWalk.getState().path.length')
            check(not errors, 'No JavaScript runtime errors', errors)
            check(len(requests) == 1, 'Preview makes no separate asset or external-network requests', requests)
            offline_context = browser.new_context(offline=True)
            offline = offline_context.new_page(); offline.set_content(HTML.read_text(), wait_until='load')
            offline.wait_for_function('()=>window.mazissWalk&&mazissWalk.getState().ready')
            offline.click('[data-view="right"]')
            before = offline.evaluate('mazissWalk.getState().pose.phase')
            offline.wait_for_timeout(120)
            check(offline.evaluate('mazissWalk.getState().pose.phase') != before,
                  'Embedded preview animates with browser networking disabled')
            offline_context.close()
            browser_version = browser.version
            browser.close()
    finally:
        server.shutdown()

    check(hashlib.sha256(HTML.read_bytes()).hexdigest() == initial_hash, 'Preview did not change during QA')
    check(all(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
              for name, digest in manifest['source_sha256'].items()), 'Reviewed sources did not change during QA')
    sheet = ('<!doctype html><meta charset="utf-8"><title>Image walk QA poses</title>'
             '<style>body{background:#20202a;color:white;font:16px sans-serif}section{display:flex;flex-wrap:wrap}figure{margin:5px}img{width:220px}</style>'
             '<h1>Actual image-guided revision 6 browser poses</h1><p>Animation continuity evidence; creative approval remains with the owner.</p>')
    for view in ('idle', 'right', 'front', 'back', 'left', 'standing', 'starting', 'settling', 'settled'):
        sheet += '<h2>'+view+'</h2><section>'
        for item in captures:
            if item['view'] == view:
                sheet += '<figure><img src="data:image/png;base64,'+base64.b64encode((OUTPUT/item['name']).read_bytes()).decode()+'"><figcaption>'+f"{item['mode']}, phase {item['phase']:.3f}"+'</figcaption></figure>'
        sheet += '</section>'
    (OUTPUT/'qa-contact-sheet.html').write_text(sheet)
    result = {'passed': passed, 'failed': failed, 'errors': errors, 'metrics': metrics,
              'html_sha256': initial_hash, 'build': manifest['build'], 'browser': browser_version,
              'captures': captures, 'seconds': round(time.monotonic()-started, 2),
              'limits': ['Continuity checks do not establish naturalness. Actual poses require visual inspection.',
                         'Direct file:// opening is blocked by managed Chromium policy; offline embedded execution was tested.',
                         'Godot integration and FBX processing are outside this image-only study.']}
    (OUTPUT/'browser-results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'passed': len(passed), 'failed': failed, 'metrics': metrics, 'build': manifest['build']}))
    raise SystemExit(bool(failed))


if __name__ == '__main__':
    main()
