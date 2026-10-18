#!/usr/bin/env python3
"""Independent real-browser walking checks; serves the offline file internally."""
import functools
import base64
import hashlib
import http.server
import json
import math
from pathlib import Path
import threading
import time

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'build/checks/walking-revision'


def distance_to_edge(p, a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]
    t = max(0, min(1, ((p['x']-a[0])*dx+(p['y']-a[1])*dy)/(dx*dx+dy*dy)))
    return math.hypot(p['x']-a[0]-t*dx, p['y']-a[1]-t*dy)


def inside(p, polygon):
    result = False
    for a, b in zip(polygon, polygon[1:]+polygon[:1]):
        if (a[1] > p['y']) != (b[1] > p['y']):
            if p['x'] < (b[0]-a[0])*(p['y']-a[1])/(b[1]-a[1])+a[0]:
                result = not result
    return result


def legal(p, room):
    polygons = [room['walkable']] + [o['polygon'] for o in room['obstacles']]
    return (inside(p, polygons[0]) and not any(inside(p, q) for q in polygons[1:])
            and all(distance_to_edge(p, a, b) >= room['clearance']-0.0001
                    for q in polygons for a, b in zip(q, q[1:]+q[:1])))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    html = ROOT / 'visual-preview/maziss-walking.html'
    room = json.loads((ROOT/'walking/room.json').read_text())
    checks, errors, requests, frame_states = [], [], [], []
    def check(condition, label):
        assert condition, label
        checks.append(label)
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1450, 'height': 1000})
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('request', lambda r: requests.append(r.url))
            page.goto(f'http://127.0.0.1:{server.server_port}/visual-preview/maziss-walking.html')
            page.wait_for_function('() => window.mazissWalk && mazissWalk.getState().ready')
            state = lambda: page.evaluate('mazissWalk.getState()')
            check(legal(state()['position'], room), 'Initial feet are legal by independent Python geometry')
            page.screenshot(path=str(OUTPUT/'idle.png'), full_page=True)
            assets = page.evaluate('''async () => {
              const result=[];
              for (const [name,url] of [['background',BACKGROUND_URL],['rig',RIG_ATLAS_URL]]) {
                if(!url)continue;
                const img=new Image();img.src=url;await img.decode();
                const c=document.createElement('canvas');c.width=img.width;c.height=img.height;
                const ctx=c.getContext('2d');ctx.drawImage(img,0,0);const d=ctx.getImageData(0,0,c.width,c.height).data;
                let transparent=0,opaque=0;for(let i=3;i<d.length;i+=4){if(d[i]===0)transparent++;if(d[i]>200)opaque++;}
                result.push({name,width:img.width,height:img.height,transparent,opaque,dataURL:url.startsWith('data:')});
              } return {images:result,rig:RIG};
            }''')
            check(all(a['dataURL'] and a['opaque'] > 100 for a in assets['images']), 'Embedded artwork decodes and has visible pixels')
            check(all(a['transparent'] > a['width']*a['height']*.1 for a in assets['images'] if a['name'] != 'background'), 'Character atlases contain substantial transparent space')

            def walk(x, y, screenshot=None):
                result = page.evaluate('p => mazissWalk.goTo(p[0],p[1])', [x,y])
                assert result['status'] != 'unreachable', (x,y,result)
                observed=[]
                for i in range(160):
                    page.wait_for_timeout(60)
                    s=state(); s['observed_at']=time.monotonic(); observed.append(s)
                    frame_states.append({k:s.get(k) for k in ('position','pose','moving','direction','speed')})
                    if screenshot and i==4: page.screenshot(path=str(OUTPUT/screenshot), full_page=True)
                    if not s['path']: break
                assert not s['path'], f'Route did not finish: {(x,y)}'
                assert math.hypot(s['position']['x']-result['target']['x'],s['position']['y']-result['target']['y']) < .1
                assert all(legal(p,room) for p in s['samples']), 'Recorded feet violated independently checked geometry'
                # A 60ms polling interval can span several frames, but not a teleport.
                assert all(math.hypot(b['position']['x']-a['position']['x'],b['position']['y']-a['position']['y']) <= 500*(b['observed_at']-a['observed_at'])+15
                           for a,b in zip(observed,observed[1:])), 'Abrupt movement between observed browser frames'
                return result, observed

            # Observe one uninterrupted, straight pass; separate it from turns,
            # resets and stop/settle contacts when evaluating alternating strikes.
            walk(500,700)
            gait_start = page.evaluate('mazissWalk.getGaitSamples().length')
            page.evaluate('mazissWalk.goTo(1450,700)')
            phase_images=[]
            for i in range(60):
                page.wait_for_timeout(70)
                s=state()
                if s['moving'] and 2<=i<=20 and i%3==2:
                    # Freeze through the real pause control before clipping, so
                    # screenshot latency cannot move the character out of frame.
                    page.evaluate("document.getElementById('pause').click()")
                    page.wait_for_timeout(20)
                    s=state()
                    box=page.locator('#room').bounding_box();scale=box['width']/room['width']
                    clip={'x':box['x']+(s['position']['x']-160)*scale,
                          'y':max(box['y'],box['y']+(s['position']['y']-490)*scale),
                          'width':320*scale,'height':520*scale}
                    name=f'gait-phase-{len(phase_images)+1}.png'
                    page.screenshot(path=str(OUTPUT/name),clip=clip)
                    phase_images.append(name)
                    page.evaluate("document.getElementById('pause').click()")
                if not s['path']:break
            check(not state()['path'], 'Uninterrupted faster horizontal pass completes')
            gait_history=page.evaluate('mazissWalk.getGaitSamples()')[gait_start:]
            (OUTPUT/'gait-samples.json').write_text(json.dumps(gait_history)+'\n')
            strikes=[];seen={(l['id'],l['contactId']) for l in gait_history[0]['pose']['legs']};last_contacts={};drift=0;max_lift=0
            lead={'left':[],'right':[]};knee={'left':[],'right':[]};stance_counts={'left':0,'right':0}
            for sample in gait_history:
                pose=sample['pose'];root=sample['position']
                for leg in pose['legs']:
                    key=(leg['id'],leg['contactId'])
                    lead[leg['id']].append(leg['ground']['x']-root['x'])
                    knee[leg['id']].append(leg['knee']['x']-leg['hip']['x'])
                    max_lift=max(max_lift,leg['lift'])
                    if leg['stance']:
                        stance_counts[leg['id']]+=1
                        check_ground=legal(leg['ground'],room)
                        assert check_ground, 'Planted foot violates room clearance'
                        if key in last_contacts:
                            previous=last_contacts[key]
                            drift=max(drift,math.hypot(previous['x']-leg['ground']['x'],previous['y']-leg['ground']['y']))
                        last_contacts[key]=leg['ground']
                        if key not in seen:
                            strikes.append(leg['id'])
                            seen.add(key)
                    assert inside(leg['ground'],room['walkable']) and not any(inside(leg['ground'],o['polygon']) for o in room['obstacles']), 'Boot projection enters solid geometry'
            check(len(strikes)>=5 and all(a!=b for a,b in zip(strikes,strikes[1:])), 'Actual rendered left/right stance contact identities alternate')
            check(all(min(values)<-25 and max(values)>25 for values in lead.values()), 'The same left and right legs each travel ahead of and behind the body')
            check(drift<1e-6 and min(stance_counts.values())>5, 'Each stance boot remains planted at its own world contact')
            check(max_lift>10 and all(max(v)-min(v)>15 for v in knee.values()), 'Swing feet lift and both rendered knees articulate')
            check(max(s['speed'] for s in gait_history)>330, 'Measured browser movement exceeds old 260 px/s ceiling')
            check(all(abs(s['pose']['torso']['angle'])<.04 for s in gait_history), 'Anatomical gait solver stays stable independently of the painted torso transform')
            renders=[s['render'] for s in gait_history if s.get('render')]
            arm_limit=math.radians(6)+1e-6
            check(bool(renders) and all(len(r['armAngles'])==2 and abs(sum(r['armAngles']))<1e-8 and max(abs(a) for a in r['armAngles'])<=arm_limit for r in renders), 'Actual renderer uses opposing arm rotations bounded to six degrees')
            check(min(r['armAngles'][0] for r in renders)<-.03 and max(r['armAngles'][0] for r in renders)>.03, 'Rendered arms swing modestly in both directions rather than staying rigid')
            check(all(math.radians(5)<=abs(r['torsoAngle'])<=math.radians(7) for r in renders), 'Actual side-view torso lean stays between five and seven degrees')
            check(max(r['torsoAngle'] for r in renders)-min(r['torsoAngle'] for r in renders)>.01, 'Actual painted torso has small nonzero walking motion')
            upper_fraction=assets['rig']['bodyHeight']*assets['rig']['beltAnchor']/(.45+assets['rig']['bodyHeight']*assets['rig']['beltAnchor'])
            check(.48<=upper_fraction<=.50, 'Nominal head-to-pelvis versus pelvis-to-floor split is approximately 49/51')
            cuff_error=max(math.hypot(j['shinEnd']['x']-j['bootCuff']['x'],j['shinEnd']['y']-j['bootCuff']['y']) for r in renders for j in r['joins'])
            check(cuff_error<1e-6, 'Rendered shin endpoints equal the transformed boot cuffs')
            (OUTPUT/'contact-sheet.html').write_text('<!doctype html><meta charset="utf-8"><title>Actual rendered gait phases</title><style>body{background:#20202a;color:white;font:16px sans-serif}section{display:flex;flex-wrap:wrap}figure{margin:5px}img{max-width:200px}</style><h1>Actual browser-rendered gait phases</h1><section>'+''.join('<figure><img src="data:image/png;base64,'+base64.b64encode((OUTPUT/n).read_bytes()).decode()+'"><figcaption>'+n+'</figcaption></figure>' for n in phase_images)+'</section>')
            sheet=browser.new_page(viewport={'width':1600,'height':700})
            sheet.goto(f'http://127.0.0.1:{server.server_port}/build/checks/walking-revision/contact-sheet.html')
            sheet.screenshot(path=str(OUTPUT/'contact-sheet.png'),full_page=True)
            sheet.close()

            walk(1030,563)
            result, observed = walk(1460,598,'chest-detour.png')
            check(len(result['path'])>2, 'Actual chest traversal uses a genuine bent route')
            check(any(s['moving'] for s in observed), 'Movement actually occurs over browser frames')
            for x,y in [(1650,670),(1510,730),(600,700),(720,620),(1000,745),(450,680),(1200,620),(1460,598)]:
                walk(x,y)
            check(True, 'Ten completed browser traversals preserve legal feet, endpoints and continuous movement')
            before=state()['position']
            rejected=page.evaluate('mazissWalk.goTo(900,100)')
            page.wait_for_timeout(150)
            check(rejected['status']=='unreachable' and state()['position']==before, 'High wall target is rejected without moving')
            adjusted,_=walk(1300,545)
            check(adjusted['status']=='adjusted', 'Furniture click redirects to legal floor')

            page.evaluate('mazissWalk.goTo(500,700)');page.wait_for_timeout(150)
            redirect=page.evaluate('''() => {const before=mazissWalk.getState().position;
              const result=mazissWalk.goTo(1550,720);
              return {before,result,after:mazissWalk.getState().position};}''')
            check(redirect['before']==redirect['after'] and len(redirect['result']['path'])>=2, 'Mid-walk redirection preserves actual feet instead of snapping')
            for p in [[800,650],[1450,700],[650,710],[1300,650]]:
                page.evaluate('p=>mazissWalk.goTo(...p)',p);page.wait_for_timeout(45)
            walk(1040,690)
            check(all(legal(p,room) for p in state()['samples']), 'Rapid redirections keep all recorded positions legal')

            page.evaluate('mazissWalk.goTo(500,700)');page.wait_for_timeout(180)
            page.click('#pause');paused=state()['position'];paused_pose=state()['pose'];paused_render=state()['render'];page.wait_for_timeout(250)
            check(state()['position']==paused and state()['paused'], 'Pause freezes character position')
            check(state()['pose']==paused_pose, 'Pause freezes articulated legs and torso as well as position')
            check(state()['render']==paused_render, 'Pause freezes arm and painted torso transforms')
            resume_index=page.evaluate("() => {document.getElementById('pause').click();return mazissWalk.getGaitSamples().length;}")
            page.wait_for_timeout(90)
            resumed=page.evaluate('mazissWalk.getGaitSamples()')[resume_index:]
            check(bool(resumed) and all(math.hypot(b['position']['x']-a['position']['x'],b['position']['y']-a['position']['y'])<20 for a,b in zip([{'position':paused}]+resumed,resumed)), 'Resume has no catch-up jump in actual rendered frames')
            # Simulate an unresponsive frame; dt must remain bounded on recovery.
            blocked=page.evaluate('''() => {const position=mazissWalk.getState().position,index=mazissWalk.getGaitSamples().length;
              const end=performance.now()+700;while(performance.now()<end){};return {position,index};}''')
            page.wait_for_timeout(70)
            recovered=page.evaluate('mazissWalk.getGaitSamples()')[blocked['index']:]
            check(bool(recovered) and all(math.hypot(b['position']['x']-a['position']['x'],b['position']['y']-a['position']['y'])<20 for a,b in zip([{'position':blocked['position']}]+recovered,recovered)), 'Long blocked frame has no catch-up jump in actual rendered frames')
            page.evaluate('mazissWalk.reset()')
            page.set_viewport_size({'width': 650,'height': 850})
            box=page.locator('#room').bounding_box();target=(1000,740)
            page.mouse.click(box['x']+target[0]/room['width']*box['width'],box['y']+target[1]/room['height']*box['height'])
            command=state()['commands'][-1]
            check(abs(command['x']-target[0])<2 and abs(command['y']-target[1])<2, 'Scaled canvas maps a real mouse click to correct room coordinates')
            page.wait_for_function('() => !mazissWalk.getState().path.length')
            page.locator('#debug').check()
            page.screenshot(path=str(OUTPUT/'narrow-debug.png'),full_page=True)
            page.locator('#debug').uncheck()
            page.screenshot(path=str(OUTPUT/'narrow.png'),full_page=True)
            page.wait_for_timeout(400)
            idle=state();page.wait_for_timeout(150)
            check(not idle['moving'] and idle['pose']==state()['pose'], 'Settled idle holds the complete articulated pose')
            all_gait=page.evaluate('mazissWalk.getGaitSamples()')
            check(all(legal(l['ground'],room) for s in all_gait for l in s['pose']['legs']), 'Both planted and airborne boot projections preserve clearance across traversals and turns')
            check(not errors,'No browser page errors')
            check(len(requests)==1,'No external asset or network requests after the HTML document')
            result={'checks':checks,'errors':errors,'browser':browser.version,'assets':assets,
                    'html_sha256':hashlib.sha256(html.read_bytes()).hexdigest(),
                    'recorded_samples':len(state()['samples']),'observed_animation_states':len(frame_states),
                    'gait_metrics':{'samples':len(gait_history),'strikes':strikes,'max_stance_drift':drift,'max_swing_lift':max_lift,'max_speed':max(s['speed'] for s in gait_history),'max_arm_degrees':max(math.degrees(abs(a)) for r in renders for a in r['armAngles']),'torso_degrees_range':[math.degrees(min(r['torsoAngle'] for r in renders)),math.degrees(max(r['torsoAngle'] for r in renders))],'nominal_upper_fraction':upper_fraction,'max_shin_cuff_endpoint_error':cuff_error},
                    'generated_at_unix':time.time()}
            (OUTPUT/'browser-results.json').write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps({'checks':len(checks),'samples':result['recorded_samples'],'browser':browser.version}))
            browser.close()
    finally:
        server.shutdown()


if __name__=='__main__':
    main()
