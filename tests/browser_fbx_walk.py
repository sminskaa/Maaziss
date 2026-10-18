#!/usr/bin/env python3
"""Focused browser/painted-pixel evidence for the private-input FBX study.

No FBX trajectory or owner reference image is copied into this test or report.
Checks establish rendering invariants, not creative acceptance or naturalness.
"""
from __future__ import annotations
import base64
import hashlib
import json
import math
from pathlib import Path
import time
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT/'visual-preview/maziss-walking-v7.html'
OUTPUT = ROOT/'build/checks/fbx-walk/qa'


def components(path, threshold=64):
    image=Image.open(path).convert('RGBA'); w,h=image.size
    alpha=image.getchannel('A'); pixels=alpha.load()
    todo={(x,y) for y in range(h) for x in range(w) if pixels[x,y]>threshold}
    result=[]
    while todo:
        q=[todo.pop()]; size=0; xmin=w; ymin=h; xmax=ymax=0
        while q:
            x,y=q.pop(); size+=1; xmin=min(xmin,x); ymin=min(ymin,y); xmax=max(xmax,x); ymax=max(ymax,y)
            for point in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if point in todo: todo.remove(point); q.append(point)
        result.append({'pixels':size,'bounds':[xmin,ymin,xmax,ymax]})
    return sorted(result,key=lambda x:x['pixels'],reverse=True)


CAPTURE_JS = '''async()=>{
 const load=url=>new Promise(resolve=>{const im=new Image();im.onload=()=>resolve(im);im.src=url;});
 const c=new MazissPaintedCharacter.Character(await load(ATLAS_URL),await load(DEPTH_ATLAS_URL));
 const gait=new MazissFbxGait.Gait(FBX_MOTION),out=[];
 for(const[name,yaw]of Object.entries({right:{x:1,y:0},front:{x:0,y:1},back:{x:0,y:-1},left:{x:-1,y:0}})){
  gait.reset({x:320,y:570},440);gait.yaw=yaw;
  for(const mode of ['idle','walking'])for(let i=0;i<(mode==='idle'?1:12);i++){
   gait.weight=mode==='idle'?0:1;gait.mode=mode;gait.cycle=i/12;
   const pose=gait.getPose(),canvas=document.createElement('canvas');canvas.width=640;canvas.height=620;
   const metrics=c.draw(canvas.getContext('2d'),pose,440);
   out.push({name:name+'-'+mode+'-'+i,view:name,mode,png:canvas.toDataURL(),pose,metrics});
  }
 }
 return out;
}'''


def main():
    OUTPUT.mkdir(parents=True,exist_ok=True)
    started=time.monotonic(); manifest=json.loads((OUTPUT.parent/'build-manifest.json').read_text())
    html=HTML.read_bytes(); initial_hash=hashlib.sha256(html).hexdigest()
    passed=[]; failed=[]; errors=[]; requests=[]; metrics={}
    def check(ok,label,evidence=None):
        (passed if ok else failed).append({'check':label,'evidence':evidence})
    def sources_match():
        return all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest for name,digest in manifest['source_sha256'].items())
    check(initial_hash==manifest['output_sha256'],'HTML matches the declared build')
    check(sources_match(),'Source files and private motion input match the declared build')
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        context=browser.new_context(offline=True,viewport={'width':1450,'height':1050})
        page=context.new_page(); page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('request',lambda request:requests.append(request.url))
        page.set_content(html.decode(),wait_until='load')
        page.wait_for_function('()=>window.mazissWalk&&mazissWalk.getState().ready')
        state=lambda:page.evaluate('mazissWalk.getState()')
        check(state()['pose']['mode']=='idle','Preview initially holds a neutral idle pose')
        captures=page.evaluate(CAPTURE_JS)
        pixel_components={}
        for sample in captures:
            path=OUTPUT/(sample['name']+'.png')
            path.write_bytes(base64.b64decode(sample.pop('png').split(',')[1]))
            pixel_components[sample['name']]=components(path)
        (OUTPUT/'poses.json').write_text(json.dumps(captures,indent=2)+'\n')
        for view in ('right','front','back','left'):
            group=[s for s in captures if s['view']==view]
            idle=next(s for s in group if s['mode']=='idle')
            check(all(abs(f['rotation'])<1e-9 for f in idle['metrics']['feet']),view+': neutral boots have no inherited walking roll')
            if view in ('left','right'):
                check(all(abs(f['heel']['y']-f['toe']['y'])<1e-8 for f in idle['metrics']['feet']),view+': painted neutral sole registration is horizontal')
                # Inspect the real lowest opaque sole, excluding the curved
                # toe/heel tips. Metadata alone missed revision 6's tilted art.
                f=max(idle['metrics']['feet'],key=lambda foot:foot['heel']['y'])
                xs=sorted([f['heel']['x'],f['toe']['x']]); span=xs[1]-xs[0]
                alpha=Image.open(OUTPUT/(idle['name']+'.png')).getchannel('A')
                bottoms=[]
                for x in range(round(xs[0]+span*.15),round(xs[1]-span*.15)):
                    ys=[y for y in range(round(f['heel']['y'])-12,round(f['heel']['y'])+10)
                        if alpha.getpixel((x,y))>128]
                    if ys: bottoms.append(max(ys))
                visible_range=max(bottoms)-min(bottoms) if bottoms else float('inf')
                check(len(bottoms)>35 and visible_range<=5,
                      view+': actual opaque neutral sole stays visibly flat across its central span',
                      {'columns':len(bottoms),'vertical_range_pixels':visible_range})
            else:
                check(all(f['rotation']==0 for s in group for f in s['metrics']['feet']),view+': directional boot artwork is kept upright')
            check(all(s['metrics']['layers'][0]=='far-arm' and s['metrics']['layers'][-1]=='near-arm'
                      and s['metrics']['layers'].index('body')>0 for s in group),view+': far arm is painted behind the body and near arm in front')
            check(all(s['metrics']['continuousPants'] and len(s['metrics']['joins'])==2
                      and all(j['pantContinuous'] and j['shinEnd']==j['bootCuff'] for j in s['metrics']['joins']) for s in group),
                      view+': continuous trouser skin meets both boot tops')
            islands=[{'pose':s['name'],'islands':pixel_components[s['name']][1:]} for s in group
                     if any(c['pixels']>16 for c in pixel_components[s['name']][1:])]
            check(not islands,view+': actual transparent character has no detached painted islands above 16 pixels',islands)
        metrics['actual_pixel_components']=pixel_components
        continuity=page.evaluate('''()=>{
          const g=new MazissFbxGait.Gait(FBX_MOTION);g.reset({x:0,y:0},440);g.weight=1;g.mode='walking';
          const poses=[];for(let i=0;i<=240;i++){g.cycle=i/240;poses.push(g.getPose());}
          const loop=[poses[0],poses[240]], transitions=[];g.reset({x:0,y:0},440);const p={x:0,y:0};
          for(let i=0;i<500;i++){const active=i<360;if(active)p.x+=1.1;transitions.push(g.update(p,440,1/120,active,{x:1,y:0},false));}
          return {poses,loop,transitions,cycleSeconds:FBX_MOTION.cycleSeconds,source:FBX_MOTION.source.filename};
        }''')
        poses=continuity['poses']; a,b=continuity['loop']
        loop_error=max(math.hypot(x[k]['x']-y[k]['x'],x[k]['y']-y[k]['y'])
                       for x,y in zip(a['legs'],b['legs']) for k in ('hip','knee','cuff','sole'))
        check(loop_error<1e-7,'FBX loop closes without a joint-coordinate teleport',loop_error)
        check(all(math.isfinite(leg[k][axis]) for p in poses+continuity['transitions'] for leg in p['legs']
                  for k in ('hip','knee','cuff','sole') for axis in ('x','y')),'Sampled cycle and start/stop joints remain finite')
        mode_order=list(dict.fromkeys(p['mode'] for p in continuity['transitions']))
        check(mode_order==['starting','walking','settling','idle'],'Actual FBX gait visits start/walk/settle/idle states',mode_order)
        lengths=[]
        for p in poses:
            for leg in p['legs']:
                local=leg['local']; lengths.append([math.dist(local['hip'],local['knee']),math.dist(local['knee'],local['cuff'])])
        ranges=[max(x[i] for x in lengths)-min(x[i] for x in lengths) for i in range(2)]
        check(max(ranges)<1e-7,'Retargeting preserves fixed original-character thigh/shin lengths',ranges)
        metrics['loop_error_pixels']=loop_error;metrics['cycle_seconds']=continuity['cycleSeconds']
        metrics['fbx_source_filename']=continuity['source'];metrics['bone_length_range_pixels']=ranges
        # Verify actual owner controls, not just independently constructed poses.
        for view in ('right','front','back','left'):
            page.click('[data-view="'+view+'"]');page.wait_for_timeout(340)
            if not state()['paused']:page.click('#pause')
            frozen=state();page.wait_for_timeout(100)
            check(state()['pose']==frozen['pose'],view+': pause freezes the complete FBX pose')
            page.click('#step');after=state()
            expected=1/30/continuity['cycleSeconds']
            check(abs(((after['pose']['phase']-frozen['pose']['phase'])%1)-expected)<1e-7,
                  view+': frame stepping advances FBX clip timing')
            page.click('#pause');page.click('#stand')
            page.wait_for_function('()=>mazissWalk.getState().pose.mode==="idle"',timeout=3000)
            check(not state()['study'] and not state()['path'],view+': Stand still exits study and settles')
            page.locator('#detail').screenshot(path=str(OUTPUT/(view+'-actual-idle.png')))
        page.evaluate('mazissWalk.reset()')
        def walk(x,y):
            route=page.evaluate('p=>mazissWalk.goTo(...p)',[x,y]);assert route['target'],route
            page.wait_for_function('()=>!mazissWalk.getState().path.length',timeout=18000)
            page.wait_for_function('()=>mazissWalk.getState().pose.mode==="idle"',timeout=3000)
            check(math.hypot(state()['position']['x']-route['target']['x'],state()['position']['y']-route['target']['y'])<.1,
                  f'Navigation reaches the resolved destination {x},{y}')
            return route
        walk(500,700);walk(1450,700);walk(1030,563);detour=walk(1460,598)
        check(len(detour['path'])>2,'Furniture route has a genuine multi-segment detour')
        check(page.evaluate('()=>mazissWalk.getState().samples.every(p=>mazissWalk.navigation.isWalkable(p))'),
              'Recorded route substeps stay on buffered walkable floor')
        before=state()['position'];rejected=page.evaluate('mazissWalk.goTo(900,100)');page.wait_for_timeout(100)
        check(rejected['status']=='unreachable' and state()['position']==before,'Wall click is rejected without moving')
        page.evaluate('mazissWalk.goTo(500,700)');page.wait_for_timeout(120);page.click('#pause');page.wait_for_timeout(50)
        frozen=state();page.wait_for_timeout(150)
        check(state()['pose']==frozen['pose'] and state()['position']==frozen['position'],'Room pause freezes both root navigation and pose')
        page.click('#reset');check(state()['position']==page.evaluate('ROOM.start'),'Reset restores the room starting point')
        check(not errors,'No JavaScript runtime errors',errors)
        check(not requests,'Embedded HTML runs with networking disabled and issues no asset/network requests',requests)
        browser_version=browser.version;browser.close()
    check(hashlib.sha256(HTML.read_bytes()).hexdigest()==initial_hash,'HTML did not change during QA')
    check(sources_match(),'Reviewed sources did not change during QA')
    sheet='<!doctype html><meta charset="utf-8"><title>FBX walk QA poses</title><style>body{background:#aaa;color:#111;font:16px sans-serif}section{display:flex;flex-wrap:wrap}figure{margin:4px}img{width:220px}</style><h1>Revision 7: actual transparent browser renders</h1><p>Grey reveals detached pixels and mesh seams. These captures are evidence, not creative approval.</p>'
    for view in ('right','front','back','left'):
        sheet+='<h2>'+view+'</h2><section>'
        for s in captures:
            if s['view']==view:
                sheet+='<figure><img src="data:image/png;base64,'+base64.b64encode((OUTPUT/(s['name']+'.png')).read_bytes()).decode()+'"><figcaption>'+s['name']+'</figcaption></figure>'
        sheet+='</section>'
    (OUTPUT/'qa-contact-sheet.html').write_text(sheet)
    result={'build':manifest['build'],'html_sha256':initial_hash,'passed':passed,'failed':failed,'metrics':metrics,
            'browser':browser_version,'seconds':round(time.monotonic()-started,2),
            'limits':['Creative acceptance and human naturalness require owner review.',
                      'Direct file:// loading is blocked by managed Chromium; offline set_content execution is covered.',
                      'Godot integration and Windows execution are outside this HTML test.']}
    (OUTPUT/'browser-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'build':manifest['build'][:12],'passed':len(passed),'failed':failed,'seconds':result['seconds']}))
    raise SystemExit(bool(failed))


if __name__=='__main__':main()
