#!/usr/bin/env python3
"""Package actual supplied-rig renders as a compact, offline native-video review.

Run after render_supplied_character.py. All artwork, captures and output remain
ignored/private; this helper never alters the approved originals.
"""
from pathlib import Path
import base64
import hashlib
import json
import subprocess

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'build/checks/supplied-character'
OUT = BUILD / 'delivery'
OUT.mkdir(exist_ok=True)
FRAMES = OUT / 'frames'
FRAMES.mkdir(exist_ok=True)
manifest = json.loads((BUILD / 'render-manifest.json').read_text())
model_hash = hashlib.sha256((BUILD / 'maziss-supplied-rig.glb').read_bytes()).hexdigest()
assert manifest['modelSHA256'] == model_hash, 'Render/model mismatch'


def embedded(path, kind='image/png'):
    return 'data:' + kind + ';base64,' + base64.b64encode(path.read_bytes()).decode()


views = manifest['views']
movement=json.loads((BUILD/'motion-private.json').read_text())
# Match scene travel to the rig's measured ankle excursion and render scale.
# A cycle contains two steps; do not slide the pose at an arbitrary pixel speed.
excursions=[]
for side in ('Left','Right'):
    positions=[frame[side+'Foot']['head'][1] for frame in movement['frames']]
    excursions.append(max(positions)-min(positions))
stride_metres=sum(excursions)
travel_pixels=3*stride_metres*(333/2.23)
inputs = {'room': embedded(ROOT / 'art/walking/apartment-background.png'),
          'travelPixels':travel_pixels,
          'front': embedded(ROOT / 'art/walking/maziss-depth-atlas.png'),
          'side': embedded(ROOT / 'art/walking/maziss-side-atlas.png'),
          'views': [{**v, 'idle': embedded(BUILD / 'renders' / v['idle']),
                     'frames': [embedded(BUILD / 'renders' / f) for f in v['frames']]}
                    for v in views]}
selected = [0, 90, 180, 270]
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = browser.new_page(offline=True)
    page.set_content('<canvas width="960" height="600"></canvas>')
    page.evaluate('''async input=>{
      const load=src=>new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>resolve(i);i.onerror=reject;i.src=src;});
      const art={room:await load(input.room),front:await load(input.front),side:await load(input.side)};
      const views=[];for(const v of input.views)views.push({angle:v.angle,idle:await load(v.idle),frames:await Promise.all(v.frames.map(load))});
      const c=document.querySelector('canvas'),ctx=c.getContext('2d');
      const room=()=>{const r=art.room,s=Math.max(960/r.width,600/r.height);ctx.drawImage(r,(960-r.width*s)/2,(600-r.height*s)/2,r.width*s,r.height*s);};
      const title=(left,right,footer)=>{
        ctx.fillStyle='rgba(20,24,28,.86)';ctx.fillRect(0,0,960,42);ctx.fillRect(0,562,960,38);
        ctx.fillStyle='#fff1d4';ctx.font='bold 18px sans-serif';ctx.fillText(left,30,28);ctx.fillText(right,465,28);
        ctx.font='16px sans-serif';ctx.fillText(footer,30,587);
      };
      window.frame=(angle,n,travel=null)=>{
        const v=views.find(v=>v.angle===angle);room();
        if(travel===null){
          title('Original drawing','Actual supplied-model render',angle+'° · Geometry and walking study');
          const side=angle===90||angle===270,back=angle===180;
          ctx.save();if(angle===90){ctx.translate(330,0);ctx.scale(-1,1);}
          ctx.drawImage(side?art.side:art.front,side?590:153,back?444:0,side?200:192,440,55,75,218,500);ctx.restore();
          ctx.fillStyle='rgba(45,24,12,.30)';ctx.beginPath();ctx.ellipse(679,550,84,12,0,0,Math.PI*2);ctx.fill();
          ctx.drawImage(v.frames[n],470,20,420,560);
        }else{
          title('Maziss in the room','Actual model renders','Walking placement study · bag-side arm stays quiet');
          const x=70+travel*input.travelPixels,y=240;
          ctx.fillStyle='rgba(45,24,12,.30)';ctx.beginPath();ctx.ellipse(x+125,y+307,53,8,0,0,Math.PI*2);ctx.fill();
          ctx.drawImage(v.frames[n],x,y,250,333);
        }
        return c.toDataURL('image/png');
      };
      window.turnaround=()=>{
        c.width=960;c.height=640;ctx.fillStyle='#d6cbb6';ctx.fillRect(0,0,960,640);
        views.forEach((v,i)=>{let x=(i%4)*240,y=Math.floor(i/4)*320;ctx.drawImage(v.idle,x+15,y+3,210,280);ctx.fillStyle='#302c29';ctx.font='18px sans-serif';ctx.fillText(v.angle+'°',x+98,y+307);});
        return c.toDataURL('image/png');
      };
    }''', inputs)
    number = 0
    for angle in selected:
        for n in range(24):
            url = page.evaluate('([a,n])=>frame(a,n)', [angle,n])
            (FRAMES / f'{number:04}.png').write_bytes(base64.b64decode(url.split(',')[1]))
            number += 1
    # Three cycles of translation in each direction; source poses remain intact.
    for angle, reverse in [(270,False),(90,True)]:
        for n in range(72):
            progress=n/71
            url=page.evaluate('([a,n,t])=>frame(a,n,t)',[angle,n%24,1-progress if reverse else progress])
            (FRAMES/f'{number:04}.png').write_bytes(base64.b64decode(url.split(',')[1]));number+=1
    url = page.evaluate('turnaround()')
    (OUT/'turnaround.png').write_bytes(base64.b64decode(url.split(',')[1]))
    browser.close()

fps = 24/manifest['cycleSeconds']
sequence = OUT/'sequence.txt'
names=[]
for view in range(4):
    for repeat in range(2):names.extend(FRAMES/f'{view*24+n:04}.png' for n in range(24))
names.extend(FRAMES/f'{n:04}.png' for n in range(96,240))
sequence.write_text(''.join(f"file '{p}'\nduration {1/fps:.10f}\n" for p in names)+f"file '{names[-1]}'\n")
video=ROOT/'visual-preview/maziss-rebuilt-review.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(sequence),'-r',str(fps),'-c:v','libx264','-preset','medium','-crf','29','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(video)],check=True)
for source,target in [(FRAMES/'0000.png',OUT/'poster.jpg'),(OUT/'turnaround.png',OUT/'turnaround.jpg')]:
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-frames:v','1','-q:v','8',str(target)],check=True)
poster=embedded(OUT/'poster.jpg','image/jpeg');turnaround=embedded(OUT/'turnaround.jpg','image/jpeg')
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Maziss — rebuilt model review</title>
<style>body{margin:0;background:#20282e;color:#f2e8d8;font:17px/1.5 system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:20px}video,img{display:block;width:100%;height:auto;border-radius:8px}details{margin:20px 0}summary{cursor:pointer}small{color:#d0c6b5}</style></head><body><main>
<h1>Maziss: supplied-model walking study</h1>
<p>Press Play for front, both sides and back, followed by walking across the room. These are actual renders of your supplied model.</p>
<video controls playsinline muted loop preload="metadata" poster="__POSTER__"><source src="__VIDEO__" type="video/mp4">The still comparison and turnaround are below.</video>
<details><summary>Still comparison with the original drawing</summary><img src="__POSTER__" width="960" height="600" alt="Original Maziss drawing beside the actual rebuilt model"></details>
<details open><summary>Eight viewing angles</summary><img src="__TURNAROUND__" width="960" height="640" alt="Actual model rendered from eight viewing angles"></details>
<p>The bag-side arm stays quiet because the supplied sculpt joins the hand and bag. Separating those surfaces is needed before independent arm movement.</p>
<p><small>This is a model and motion study. The original painted face, clothing wear and inked finish still need a dedicated art pass. The room traversal is a rendered placement study, not the playable Godot scene. Everything in this page works offline; no live 3D support is required.</small></p>
</main></body></html>'''.replace('__POSTER__',poster).replace('__TURNAROUND__',turnaround).replace('__VIDEO__',embedded(video,'video/mp4'))
target=ROOT/'visual-preview/maziss-rebuilt-review.html';target.write_text(html)
assert target.stat().st_size<1_000_000,'Compact delivery exceeded the tested size target'
for path in [target,video]:path.chmod(0o644)
target.parent.chmod(0o755)
report={'modelSHA256':model_hash,'renderedAngles':[v['angle'] for v in views],
        'sceneStrideMetres':stride_metres,'sceneTravelPixels':travel_pixels,
        'uniqueCompositeFrames':number,'encodedFrames':len(names),'fps':fps,
        'htmlBytes':target.stat().st_size,'videoBytes':video.stat().st_size,
        'htmlSHA256':hashlib.sha256(target.read_bytes()).hexdigest()}
(OUT/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
