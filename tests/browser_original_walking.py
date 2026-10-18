#!/usr/bin/env python3
"""Focused regression for first-proposal artwork with the accepted gait solver."""
from pathlib import Path
import functools,http.server,threading,json,hashlib,math
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/checks/walking-original-legs'
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*_):pass

def main():
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    checks=[];errors=[];requests=[]
    def check(ok,label):
        assert ok,label
        checks.append(label)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1450,'height':1000})
        page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda req:requests.append(req.url))
        page.goto(f'http://127.0.0.1:{server.server_port}/visual-preview/maziss-walking-v4.html')
        page.wait_for_function('window.mazissWalk && mazissWalk.getState().ready')
        state=lambda:page.evaluate('mazissWalk.getState()')
        check(state()['render']['source']=='first-proposal' and state()['render']['initial'],'Initial character uses the first source atlas')
        page.screenshot(path=str(OUT/'idle.png'))
        original=(ROOT/'visual-preview/maziss-walking-v1.html').read_text()
        sprites=json.loads(original.split('const SPRITES=',1)[1].split(';const BACKGROUND_URL=',1)[0])
        check(page.evaluate('SPRITES')==sprites,'All original frame rectangles and anchors retained')
        # Upper-body pixels must be exactly the original painted frame at the
        # original size/anchor. This catches a replacement torso or extra lean.
        def upper_pixel_check():
            return page.evaluate('''async()=>{
              const s=mazissWalk.getState(),r=s.render,side=s.direction==='left'||s.direction==='right';
              const f=(side?SPRITES.frames:SPRITES.depthFrames)[r.originalFrame];
              const h=r.baseHeight,scale=h/f.h,w=f.w*scale;
              const bg=new Image();bg.src=BACKGROUND_URL;await bg.decode();
              const art=new Image();art.src=side?ATLAS_URL:DEPTH_ATLAS_URL;await art.decode();
              const c=document.createElement('canvas');c.width=ROOM.width;c.height=ROOM.height;
              const ctx=c.getContext('2d');ctx.drawImage(bg,0,0,ROOM.width,ROOM.height);
              ctx.save();ctx.translate(s.position.x,s.position.y);if(side)ctx.scale(s.facing,1);
              ctx.drawImage(art,f.x,f.y,f.w,f.h,-w*f.footX,-h,w,h);ctx.restore();
              const x=Math.floor(s.position.x-w),y=Math.ceil(s.position.y-h+3),cw=Math.ceil(w*2),ch=Math.floor(h*.50-6);
              const a=ctx.getImageData(x,y,cw,ch).data,b=document.querySelector('#room').getContext('2d').getImageData(x,y,cw,ch).data;
              let mismatch=0,maxDelta=0,examples=[];for(let i=0;i<a.length;i++)if(a[i]!==b[i]){mismatch++;maxDelta=Math.max(maxDelta,Math.abs(a[i]-b[i]));if(examples.length<8)examples.push({x:x+Math.floor(i/4)%cw,y:y+Math.floor(i/4/cw),a:a[i],b:b[i]});}
              return {mismatch,maxDelta,examples,pixels:cw*ch};}''')
        def walk(x,y):
            result=page.evaluate('p=>mazissWalk.goTo(...p)',[x,y]);check(bool(result.get('target')),'Route accepted')
            page.wait_for_function('()=>!mazissWalk.getState().path.length',timeout=15000)
            page.wait_for_timeout(180)
            s=state();check(math.hypot(s['position']['x']-result['target']['x'],s['position']['y']-result['target']['y'])<.1,'Arrives without teleport')
        walk(500,700)
        start=page.evaluate('mazissWalk.getGaitSamples().length')
        page.evaluate('mazissWalk.goTo(1450,700)')
        for i in range(5):
            page.wait_for_timeout(220);page.click('#pause');page.wait_for_timeout(30)
            s=state();before=s['pose'];page.wait_for_timeout(45)
            check(state()['pose']==before,'Pause preserves accepted gait pose')
            pixel=upper_pixel_check()
            check(pixel['maxDelta']<=1 and pixel['mismatch']<pixel['pixels']*.004,'Original painted head/torso retained, allowing one-channel raster rounding at sparse edges')
            page.screenshot(path=str(OUT/f'phase-{i+1}.png'))
            page.click('#pause')
        page.wait_for_function('()=>!mazissWalk.getState().path.length',timeout=10000)
        history=page.evaluate('mazissWalk.getGaitSamples()')[start:]
        contacts={};strikes=[];drift=0
        for frame in history:
            for leg in frame['pose']['legs']:
                if not leg['stance']:continue
                key=(leg['id'],leg['contactId']);point=leg['ground']
                if key in contacts:drift=max(drift,math.hypot(point['x']-contacts[key]['x'],point['y']-contacts[key]['y']))
                else:
                    contacts[key]=point
                    if frame['moving']:strikes.append(leg['id'])
        check(drift<1e-6,'Planted contacts do not slide')
        # Discard the existing support contact at the pass entry.
        strikes=strikes[1:]
        check(len(strikes)>=4 and all(a!=b for a,b in zip(strikes,strikes[1:])),'Left and right legs alternate contacts')
        check(all(math.hypot(j['shinEnd']['x']-j['bootCuff']['x'],j['shinEnd']['y']-j['bootCuff']['y'])<1e-6 for f in history for j in f['render'].get('joins',[])),'Original boots and shins share transformed cuff')
        for x,y,label in [(1050,610,'away'),(1050,740,'toward'),(500,700,'left')]:
            page.evaluate('p=>mazissWalk.goTo(...p)',[x,y]);page.wait_for_timeout(350);page.click('#pause');page.wait_for_timeout(30)
            page.screenshot(path=str(OUT/f'{label}.png'));page.click('#pause');page.wait_for_function('()=>!mazissWalk.getState().path.length',timeout=15000)
        bad=page.evaluate('mazissWalk.goTo(900,100)');check(not bad.get('target'),'Wall click rejected')
        page.evaluate('mazissWalk.reset()');check(state()['render']['source']=='first-proposal','Reset retains original character')
        check(not errors,'No browser errors');check(len(requests)==1,'No external requests after document')
        result={'checks':checks,'errors':errors,'strikes':strikes,'stance_drift':drift,'html_sha256':hashlib.sha256((ROOT/'visual-preview/maziss-walking-v4.html').read_bytes()).hexdigest()}
        (OUT/'browser-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':len(checks),'strikes':strikes,'drift':drift}));browser.close()
    server.shutdown()
if __name__=='__main__':main()
