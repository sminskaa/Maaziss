#!/usr/bin/env python3
"""Compose real character-lighting captures at calibrated room scale.

Original images/model/motion are read only. Outputs stay in ignored folders.
This is a 2.5D presentation study, not a reconstructed 3D room or navigation system.
"""
from pathlib import Path
import base64
import hashlib
import json
import subprocess
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'build/checks/supplied-character'
STYLE=ROOT/'build/checks/style-match/character'
OUT=ROOT/'build/checks/style-match/delivery';OUT.mkdir(parents=True,exist_ok=True)
PREVIEW=ROOT/'visual-preview';PREVIEW.mkdir(exist_ok=True)
manifest=json.loads((STYLE/'manifest.json').read_text())
assert len(manifest['walk'])==24,'Capture a continuous walk before packaging motion'

def media(path,kind='image/png'):
    return 'data:'+kind+';base64,'+base64.b64encode(path.read_bytes()).decode()

def jpeg(source,target):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-frames:v','1','-q:v','8',str(target)],check=True)

# Calibrated against the accepted composition: approximately 596px from hair to
# boots at original floor (1125,698). This uses fixed model/camera units, never
# the changing image bounding box of a walking frame.
calibration={'referenceFoot':[1125,698],'referenceCharacterHeightPixels':596,
             'referenceCharacterHeightWorld':2.0,'perspectiveHorizonY':130,
             'roomSize':[1932,814],
             'scope':'Two-dimensional perspective proposal; final 3D room camera is not reconstructed'}
movement=json.loads((SOURCE/'motion-private.json').read_text())
stride=0
for side in ('Left','Right'):
    p=[f[side+'Foot']['head'][1] for f in movement['frames']];stride+=max(p)-min(p)
inputs={'room':media(ROOT/'art/walking/apartment-background.png'),
        'original':media(ROOT/'art/proposals/apartment-cartoon-v2.png'),
        'baseline':media(SOURCE/'renders/idle-0.png'),
        'styled':{str(v['angle']):media(STYLE/v['idle']) for v in manifest['views']},
        'walk':[media(STYLE/name) for name in manifest['walk']],
        'ground':manifest['views'][0]['groundPixel'],'ortho':manifest['cameraOrthoScale'],
        'calibration':calibration,'stride':stride}
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(offline=True)
    page.set_content('<canvas width="960" height="405"></canvas>')
    page.evaluate('''async input=>{
      const load=src=>new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>resolve(i);i.onerror=reject;i.src=src;});
      const room=await load(input.room),original=await load(input.original),baseline=await load(input.baseline),styled={},walk=await Promise.all(input.walk.map(load));
      for(const [angle,src] of Object.entries(input.styled))styled[angle]=await load(src);
      const c=document.querySelector('canvas'),ctx=c.getContext('2d'),k=960/1932,cal=input.calibration;
      const blank=()=>{ctx.clearRect(0,0,960,405);ctx.drawImage(room,0,0,960,405);};
      const height=y=>cal.referenceCharacterHeightPixels*(y-cal.perspectiveHorizonY)/(cal.referenceFoot[1]-cal.perspectiveHorizonY);
      const place=(image,x,y)=>{
        const ppm=height(y)/cal.referenceCharacterHeightWorld;
        const scale=ppm/(640/input.ortho)*k;
        const left=x*k-input.ground[0]*scale,top=y*k-input.ground[1]*scale;
        ctx.fillStyle='rgba(39,20,30,.22)';ctx.beginPath();ctx.ellipse(x*k,y*k,53*scale,8*scale,0,0,2*Math.PI);ctx.fill();
        ctx.drawImage(image,left,top,480*scale,640*scale);
        return {foot:[x,y],characterHeight:height(y),renderScale:scale};
      };
      const output=()=>c.toDataURL('image/png');
      window.scene=(kind)=>{
        blank();
        if(kind==='original')ctx.drawImage(original,0,0,960,405);
        else if(kind==='baseline')place(baseline,...cal.referenceFoot);
        else if(kind==='styled')place(styled['0'],...cal.referenceFoot);
        else if(kind==='side')place(styled['90'],...cal.referenceFoot);
        else if(kind==='scale'){
          const anchors=[[900,560],[1280,690],[1610,780]];
          window.scaleEvidence=anchors.map(a=>place(styled['0'],...a));
        }
        return output();
      };
      window.walkFrame=n=>{
        blank();const progress=n/71;
        const travel=3*input.stride*cal.referenceCharacterHeightPixels/cal.referenceCharacterHeightWorld;
        place(walk[n%24],1600-progress*travel,698);return output();
      };
    }''',inputs)
    for kind in ('original','baseline','styled','side','scale'):
        url=page.evaluate('scene',kind);(OUT/f'{kind}.png').write_bytes(base64.b64decode(url.split(',')[1]))
        jpeg(OUT/f'{kind}.png',OUT/f'{kind}.jpg')
    evidence=page.evaluate('scaleEvidence')
    frames=OUT/'frames';frames.mkdir(exist_ok=True)
    for n in range(72):
        url=page.evaluate('walkFrame',n);(frames/f'{n:04}.png').write_bytes(base64.b64decode(url.split(',')[1]))
    browser.close()

video=OUT/'walk.mp4';fps=24/manifest['cycleSeconds']
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate',str(fps),'-i',str(frames/'%04d.png'),'-c:v','libx264','-crf','29','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(video)],check=True)
picture=lambda name:media(OUT/f'{name}.jpg','image/jpeg')
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Maziss — lighting and room scale</title><style>body{margin:0;background:#20282e;color:#f2e8d8;font:17px/1.5 system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:20px}img,video{display:block;width:100%;height:auto;border-radius:7px}details{margin:20px 0}summary{cursor:pointer}h2{font-size:21px;margin-bottom:10px}a{color:#ffe4a3}</style></head><body><main>
<h1>Matching Maziss to the room</h1><p>The same model and motion, with warmer room lighting, cooler window fill and drawn contours. The room artwork is unchanged.</p>
<h2>Proposed character treatment</h2><img src="__STYLED__" width="960" height="405" alt="Actual newly shaded Maziss model placed in the original room at calibrated scale">
<details><summary>Previous shading at the same position and scale</summary><img src="__BASELINE__" width="960" height="405" alt="Previous shaded model at exactly the same room position and scale"></details>
<details><summary>Original approved drawing for comparison</summary><img src="__ORIGINAL__" width="960" height="405" alt="Original approved room and illustrated Maziss"></details>
<details><summary>Side view with the same room lighting</summary><img src="__SIDE__" width="960" height="405" alt="Actual side-view render with a fixed camera and room lights"></details>
<h2>Walking at a consistent room depth</h2><video controls playsinline muted preload="metadata"><source src="__VIDEO__" type="video/mp4">Use the still comparisons above.</video>
<p>His floor position controls his size. This pass keeps the same depth and scale throughout; body and limbs are not resized separately.</p>
<h2>Near, middle and back: three separate placements</h2><img src="__SCALE__" width="960" height="405" alt="The same model at back, middle and foreground floor positions, scaled using one perspective rule">
<p>The door and the original drawing guide this initial perspective calibration. A modeled room will let us replace this proposal with one shared 3D camera and floor.</p>
<p>This is a lighting and scale study. The face, clothing wear, hands and final painted finish still need work. The bag-side arm retains its earlier resting constraint. Room placement is composited review footage, not a new playable movement system.</p>
<p><a href="maziss-room-reference.html">Clean room reference and download</a></p>
</main></body></html>'''
for token,name in [('STYLED','styled'),('BASELINE','baseline'),('ORIGINAL','original'),('SIDE','side'),('SCALE','scale')]:html=html.replace('__'+token+'__',picture(name))
html=html.replace('__VIDEO__',media(video,'video/mp4'))
target=PREVIEW/'maziss-style-match.html';target.write_text(html);target.chmod(0o644)
assert target.stat().st_size<1_000_000,'Review exceeds compact delivery target'
report={'modelSHA256':hashlib.sha256((SOURCE/'maziss-supplied-rig.glb').read_bytes()).hexdigest(),
        'renderManifestSHA256':hashlib.sha256((STYLE/'manifest.json').read_bytes()).hexdigest(),
        'htmlSHA256':hashlib.sha256(target.read_bytes()).hexdigest(),'htmlBytes':target.stat().st_size,
        'calibration':calibration,'depthPlacements':evidence,'sceneStrideMetres':stride,
        'walkFloorY':698,'walkScaleConstant':True,'walkFrames':72}
(OUT/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
