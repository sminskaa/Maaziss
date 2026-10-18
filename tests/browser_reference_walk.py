#!/usr/bin/env python3
"""Focused browser checks and actual rendered phase captures for reference walk.

Geometry/continuity assertions are technical evidence, not a naturalness score.
No private recording or recording frame is copied to the deliverables.
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

from PIL import Image
from playwright.sync_api import Error, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'build/checks/reference-walk'
HTML = ROOT / 'visual-preview/maziss-walking-v5.html'


def edge_distance(point, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0, min(1, ((point['x'] - a[0]) * dx + (point['y'] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(point['x'] - a[0] - t * dx, point['y'] - a[1] - t * dy)


def inside(point, polygon):
    result = False
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        if (a[1] > point['y']) != (b[1] > point['y']):
            if point['x'] < (b[0] - a[0]) * (point['y'] - a[1]) / (b[1] - a[1]) + a[0]:
                result = not result
    return result


def legal(point, room):
    polygons = [room['walkable']] + [obstacle['polygon'] for obstacle in room['obstacles']]
    return (inside(point, polygons[0]) and not any(inside(point, poly) for poly in polygons[1:])
            and all(edge_distance(point, a, b) >= room['clearance'] - 1e-4
                    for poly in polygons for a, b in zip(poly, poly[1:] + poly[:1])))


def pose_numeric_delta(before, after, key=''):
    """Allow floating-point roundoff, never changed identities or structure."""
    if isinstance(before, bool) or isinstance(after, bool):
        return 0 if type(before) is type(after) and before == after else math.inf
    if key in ('id', 'contactId'):
        return 0 if type(before) is type(after) and before == after else math.inf
    if isinstance(before, (int, float)) and isinstance(after, (int, float)):
        return abs(before - after) if math.isfinite(before) and math.isfinite(after) else math.inf
    if isinstance(before, dict) and isinstance(after, dict):
        if before.keys() != after.keys():
            return math.inf
        return max((pose_numeric_delta(before[name], after[name], name) for name in before), default=0)
    if isinstance(before, list) and isinstance(after, list):
        if len(before) != len(after):
            return math.inf
        return max((pose_numeric_delta(a, b, key) for a, b in zip(before, after)), default=0)
    return 0 if type(before) is type(after) and before == after else math.inf


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    started = time.time()
    initial_hash = hashlib.sha256(HTML.read_bytes()).hexdigest()
    manifest = json.loads((OUTPUT / 'build-manifest.json').read_text())
    room = json.loads((ROOT / 'walking/room.json').read_text())
    reference = json.loads((ROOT / 'walking/reference-motion.json').read_text())
    checks, failures, errors, requests, captures, measurements, limitations = [], [], [], [], [], {}, []

    def check(condition, label, detail=None):
        (checks if condition else failures).append(label if detail is None else {'check': label, 'detail': detail})

    check(initial_hash == manifest['output_sha256'], 'Revision 5 output matches recorded build manifest')
    check(all(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
              for name, digest in manifest['source_sha256'].items()), 'Build source hashes match the files under review')
    check(len(reference['samples']) >= 25 and reference['source']['frames'] == [36, 78]
          and math.isclose(reference['cycle_seconds'], 1.4),
          'Reference records a full measured 42-frame / 1.4-second owner-footage cycle')
    check(reference['source']['private_footage_embedded'] is False,
          'Motion data explicitly excludes private recording pixels')

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1450, 'height': 1050})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('request', lambda request: requests.append(request.url))
            page.goto(f'http://127.0.0.1:{server.server_port}/visual-preview/maziss-walking-v5.html')
            page.wait_for_function('() => window.mazissWalk && mazissWalk.getState().ready')
            state = lambda: page.evaluate('mazissWalk.getState()')
            check(legal(state()['position'], room), 'Initial root position is legal by independent geometry')
            check(state()['render']['source'] == 'first-proposal', 'Initial character uses the first proposal artwork')
            page.screenshot(path=str(OUTPUT / 'idle.png'), full_page=True)

            # Each view is exercised for a complete real-time cycle. Pause through
            # the actual UI before capturing, so screenshots and pose data agree.
            expected = {'right': (1, 0), 'left': (-1, 0), 'front': (0, 1), 'back': (0, -1)}
            view_stats = {}
            for view, desired in expected.items():
                page.click(f'[data-view="{view}"]')
                page.wait_for_timeout(650)
                start_index = page.evaluate('mazissWalk.getGaitSamples().length')
                phase_states = []
                page.click('#pause')
                page.wait_for_timeout(30)
                for phase_index in range(8):
                    sample = state()
                    phase_states.append(sample)
                    box = page.locator('#room').bounding_box()
                    scale = box['width'] / room['width']
                    clip = {'x': box['x'] + (sample['position']['x'] - 230) * scale,
                            'y': max(box['y'], box['y'] + (sample['position']['y'] - 520) * scale),
                            'width': 460 * scale, 'height': 550 * scale}
                    name = f'{view}-phase-{phase_index + 1}.png'
                    page.screenshot(path=str(OUTPUT / name), clip=clip)
                    captures.append({'name': name, 'view': view, 'phase': sample['pose']['phase']})
                    page.evaluate("() => {for(let i=0;i<6;i++)document.getElementById('step').click();}")
                    page.wait_for_timeout(25)
                step_start = state()['pose']['phase']
                page.evaluate("() => {for(let i=0;i<42;i++)document.getElementById('step').click();}")
                step_end = state()['pose']['phase']
                check(abs(((step_end-step_start+.5)%1)-.5)<1e-8, f'{view}: 42 frame-step clicks reproduce exactly one measured reference cycle')
                page.click('#pause')
                history = page.evaluate('mazissWalk.getGaitSamples()')[start_index:]
                poses = [sample['pose'] for sample in history]
                check(bool(history) and all(sample['study'] if 'study' in sample else True for sample in phase_states), f'{view}: cycle study renders actual animation frames')
                yaw = poses[-1]['yaw']
                check(yaw['x'] * desired[0] + yaw['y'] * desired[1] > .995, f'{view}: character actually faces the requested direction', yaw)
                check(all(sample['render']['source'] == 'first-proposal' and len(sample['render'].get('joins', [])) == 2
                          for sample in phase_states), f'{view}: both articulated legs render from the first proposal artwork')
                cuff_error = max(math.hypot(joint['shinEnd']['x'] - joint['bootCuff']['x'], joint['shinEnd']['y'] - joint['bootCuff']['y'])
                                 for sample in phase_states for joint in sample['render']['joins'])
                check(cuff_error < 1e-6, f'{view}: renderer joins shin endpoints to transformed boot cuffs', cuff_error)
                # This is 2D sagittal projection evidence, not a naturalness metric.
                lateral = max(abs(leg['knee']['x'] - leg['hip']['x']) for pose in poses for leg in pose['legs'])
                if view in ('front', 'back'):
                    check(lateral < 2, f'{view}: projected knees stay in their leg lanes instead of kicking sideways', lateral)
                arm = [sample['render']['armAngles'] for sample in phase_states]
                check(any(max(values) - min(values) > .01 for values in zip(*arm)), f'{view}: rendered arms have nonzero cycle motion')
                check(all(abs(((pose['legs'][1]['phase'] - pose['legs'][0]['phase']) % 1) - .5) < 1e-9 for pose in poses),
                      f'{view}: left and right leg cycles are half a cycle apart')
                view_stats[view] = {'frames': len(history), 'max_knee_lateral_pixels': lateral,
                                    'max_shin_cuff_error': cuff_error, 'final_yaw': yaw,
                                    'phase_states': [{'phase': sample['pose']['phase'], 'pose': sample['pose'], 'render': sample['render']} for sample in phase_states]}

            # Pause must freeze an in-place study too, including all painted arms.
            page.click('#pause')
            page.wait_for_timeout(60)
            frozen = state()
            page.wait_for_timeout(300)
            later = state()
            check(frozen['pose'] == later['pose'] and frozen['render'] == later['render'], 'Pause freezes complete study pose and painted arm transforms')
            page.click('#pause')
            page.select_option('#playback', '.5') if page.locator('#playback option[value=".5"]').count() else page.select_option('#playback', '0.5')
            page.wait_for_timeout(150)
            before = state()['pose']['phase']; t0 = time.monotonic(); page.wait_for_timeout(450)
            half_delta = (state()['pose']['phase'] - before) % 1
            half_elapsed = time.monotonic() - t0
            check(abs(half_delta - half_elapsed / reference['cycle_seconds'] * .5) < .055,
                  'Half-speed cycle follows the measured reference timing', {'phase_delta': half_delta, 'seconds': half_elapsed})
            page.select_option('#playback', '1')
            page.locator('#study').uncheck()
            page.evaluate('mazissWalk.reset()')

            def walk(x, y, screenshot=None):
                route = page.evaluate('p => mazissWalk.goTo(...p)', [x, y])
                assert route['target'], (x, y, route)
                observed = []
                for _ in range(220):
                    page.wait_for_timeout(40)
                    sample = state(); observed.append(sample)
                    if not sample['path']:
                        break
                assert not sample['path'], f'Route did not finish {(x, y)}'
                check(math.hypot(sample['position']['x'] - route['target']['x'], sample['position']['y'] - route['target']['y']) < .1,
                      f'Route to {x},{y} reaches its resolved destination')
                if screenshot:
                    page.screenshot(path=str(OUTPUT / screenshot), full_page=True)
                return route, observed

            walk(500, 700)
            start_index = page.evaluate('mazissWalk.getGaitSamples().length')
            _, horizontal = walk(1450, 700)
            gait_history = page.evaluate('mazissWalk.getGaitSamples()')[start_index:]
            (OUTPUT / 'horizontal-gait-samples.json').write_text(json.dumps(gait_history) + '\n')
            # Compare loaded toe contacts only: ankle/heel movement during toe-off
            # is intended, while the grounded toe must remain planted.
            contact_points, painted_points, max_toe_drift, max_painted_drift, max_registration_error, strikes = {}, {}, 0, 0, 0, []
            ink_contacts = set()
            seen = {(leg['id'], leg['contactId']) for leg in gait_history[0]['pose']['legs']}
            for sample in gait_history:
                # The route reverses the prior heading; its initial turn is not
                # a stationary-contact interval. Evaluate planting after yaw has
                # aligned with the uninterrupted horizontal direction.
                if sample['pose']['yaw']['x'] < .999999:
                    continue
                for leg in sample['pose']['legs']:
                    if not leg['stance'] or sample['pose']['blend'] < .99:
                        continue
                    key = (leg['id'], leg['contactId'])
                    toe = leg['toe']
                    joint = next(joint for joint in sample['render']['joins'] if joint['id'] == leg['id'])
                    painted = joint['paintedContact']
                    ink_contacts.add(tuple(joint['sourceContact']))
                    max_registration_error = max(max_registration_error, math.hypot(painted['x'] - toe['x'], painted['y'] - toe['y']))
                    if key in painted_points:
                        previous_painted = painted_points[key]
                        max_painted_drift = max(max_painted_drift, math.hypot(painted['x'] - previous_painted['x'], painted['y'] - previous_painted['y']))
                    painted_points[key] = painted
                    if key in contact_points:
                        previous = contact_points[key]
                        max_toe_drift = max(max_toe_drift, math.hypot(toe['x'] - previous['x'], toe['y'] - previous['y']))
                    contact_points[key] = toe
                    if key not in seen:
                        strikes.append(leg['id']); seen.add(key)
            check(len(strikes) >= 4 and all(a != b for a, b in zip(strikes, strikes[1:])), 'Completed straight traverse shows alternating new left/right contacts', strikes)
            check(max_toe_drift < 1e-5, 'Loaded logical toes remain planted during an aligned straight traverse', max_toe_drift)
            check(max_painted_drift < 1e-5 and max_registration_error < 1e-5,
                  'Actual painted forefoot source points remain registered to those planted contacts',
                  {'max_drift': max_painted_drift, 'max_registration_error': max_registration_error})
            side_image = Image.open(ROOT / 'art/walking/maziss-side-atlas.png')
            check(bool(ink_contacts) and all(side_image.getpixel(point)[3] >= 128 for point in ink_contacts),
                  'Painted contact registration uses opaque original sole artwork rather than transparent source pixels', sorted(ink_contacts))
            check(max(leg['lift'] for sample in gait_history for leg in sample['pose']['legs']) > 5,
                  'Actual rendered swing feet lift above the floor')
            walk(1030, 563)
            route, _ = walk(1460, 598, 'chest-detour.png')
            check(len(route['path']) > 2, 'Chest detour takes a genuine bent route')
            walk(600, 700)
            walk(1650, 670)
            check(all(legal(point, room) for point in state()['samples']), 'All recorded root substeps respect walls, obstacles and clearance')
            before = state()['position']
            rejected = page.evaluate('mazissWalk.goTo(900,100)')
            page.wait_for_timeout(100)
            check(rejected['status'] == 'unreachable' and state()['position'] == before, 'High wall click is rejected without moving')
            route, _ = walk(1300, 545)
            check(route['status'] == 'adjusted', 'Furniture click resolves to nearby clear floor')
            page.evaluate('mazissWalk.goTo(500,700)'); page.wait_for_timeout(150)
            page.click('#pause'); page.wait_for_timeout(50)
            frozen = state(); page.wait_for_timeout(250); later = state()
            check(frozen['position'] == later['position'] and frozen['pose'] == later['pose'] and frozen['render'] == later['render'],
                  'Room-movement pause freezes position, leg pose and painted transforms')
            page.click('#pause')
            page.wait_for_function('() => !mazissWalk.getState().path.length')
            page.wait_for_function('() => {const s=mazissWalk.getState();return !s.moving && s.pose.blend===0;}')
            page.wait_for_timeout(100)
            idle = state(); page.wait_for_timeout(150); idle_after = state()
            idle_delta = pose_numeric_delta(idle['pose'], idle_after['pose'])
            check(idle_delta < 1e-9 and not idle['moving'] and not idle_after['moving'], 'Settled idle holds the complete pose within numerical precision',
                  {'blend_before': idle['pose']['blend'], 'blend_after': idle_after['pose']['blend'], 'max_numeric_delta': idle_delta})
            page.evaluate('mazissWalk.reset()')
            page.set_viewport_size({'width': 650, 'height': 850})
            box = page.locator('#room').bounding_box()
            clicked = (1000, 740)
            page.mouse.click(box['x'] + clicked[0] / room['width'] * box['width'],
                             box['y'] + clicked[1] / room['height'] * box['height'])
            command = state()['commands'][-1]
            check(abs(command['x'] - clicked[0]) < 2 and abs(command['y'] - clicked[1]) < 2,
                  'Actual mouse click on a narrow display maps to the correct room floor point')
            page.wait_for_function('() => !mazissWalk.getState().path.length')
            page.screenshot(path=str(OUTPUT / 'narrow.png'), full_page=True)
            check(not errors, 'No browser JavaScript errors', errors)
            check(len(requests) == 1, 'Self-contained preview issues no asset or external-network requests', requests)
            # Verify the deliverable also opens as a local file, independently of
            # the internal test server and with no network permission needed.
            offline = browser.new_page()
            try:
                offline.goto(HTML.as_uri())
                offline.wait_for_function('() => window.mazissWalk && mazissWalk.getState().ready')
                check(offline.evaluate('mazissWalk.getState().ready'), 'The HTML deliverable loads through file:// without a server')
            except Error as error:
                if 'ERR_BLOCKED_BY_ADMINISTRATOR' not in str(error):
                    raise
                limitations.append('Direct file:// opening could not be verified: managed Chromium blocks local-file navigation with ERR_BLOCKED_BY_ADMINISTRATOR. The internally served HTML did load with no asset or external-network requests.')
            offline.close()
            offline_context = browser.new_context(offline=True)
            offline_document = offline_context.new_page()
            offline_document.set_content(HTML.read_text(), wait_until='load')
            offline_document.wait_for_function('() => window.mazissWalk && mazissWalk.getState().ready')
            offline_document.click('[data-view="right"]')
            before_offline_phase = offline_document.evaluate('mazissWalk.getState().pose.phase')
            offline_document.wait_for_timeout(150)
            check(offline_document.evaluate('mazissWalk.getState().pose.phase') != before_offline_phase,
                  'Embedded HTML and animation execute with browser networking disabled')
            offline_context.close()
            measurements.update({'views': view_stats, 'straight_contacts': strikes, 'max_loaded_toe_drift': max_toe_drift, 'max_painted_contact_drift': max_painted_drift,
                                 'max_painted_contact_registration_error': max_registration_error,
                                 'max_settled_idle_numeric_delta': idle_delta, 'root_samples': len(state()['samples']), 'straight_gait_frames': len(gait_history)})
            browser_version = browser.version
            browser.close()
    finally:
        server.shutdown()

    final_hash = hashlib.sha256(HTML.read_bytes()).hexdigest()
    check(final_hash == initial_hash, 'Reviewed HTML remained unchanged throughout the browser run')
    check(all(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
              for name, digest in manifest['source_sha256'].items()), 'Reviewed sources remained unchanged throughout the browser run')
    sheet = ('<!doctype html><meta charset="utf-8"><title>Maziss reference walk phases</title>'
             '<style>body{background:#20202a;color:white;font:16px sans-serif}section{display:flex;flex-wrap:wrap}figure{margin:5px}img{width:230px}h2{width:100%}</style>'
             '<h1>Actual rendered phases: reference walk revision 5</h1><p>Private footage is not embedded. These are actual paused browser frames.</p>')
    for view in ('right', 'left', 'front', 'back'):
        sheet += '<h2>' + view + '</h2><section>'
        for capture in captures:
            if capture['view'] == view:
                sheet += ('<figure><img src="data:image/png;base64,' + base64.b64encode((OUTPUT / capture['name']).read_bytes()).decode()
                          + '"><figcaption>phase ' + f"{capture['phase']:.3f}" + '</figcaption></figure>')
        sheet += '</section>'
    (OUTPUT / 'contact-sheet.html').write_text(sheet)
    result = {'checks': checks, 'failures': failures, 'errors': errors, 'browser': browser_version,
              'html_sha256': initial_hash, 'build': manifest['build'], 'source_sha256': manifest['source_sha256'],
              'captures': captures, 'metrics': measurements, 'limitations': limitations, 'elapsed_seconds': round(time.time() - started, 2),
              'scope': 'Technical continuity and routing checks. Human naturalness needs visual review and owner approval.'}
    (OUTPUT / 'browser-results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'passed': len(checks), 'failed': failures, 'elapsed_seconds': result['elapsed_seconds']}))
    raise SystemExit(bool(failures))


if __name__ == '__main__':
    main()
