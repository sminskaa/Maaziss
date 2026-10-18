"""Encode retained, verified rendered frames for a small no-script HTML review."""
from pathlib import Path
import base64,hashlib,json,subprocess
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/checks/preview-delivery'
OUT.mkdir(parents=True,exist_ok=True)
rendered=(ROOT/'visual-preview/maziss-painted-rendered.html').read_text()
start=rendered.index('const FILM=')+len('const FILM=')
film,_=json.JSONDecoder().raw_decode(rendered[start:])
chosen=[0,45,90,180]
views=[v for v in film['views'] if v['angle'] in chosen]
def source(path):return 'data:image/png;base64,'+base64.b64encode((ROOT/path).read_bytes()).decode()
inputs={'views':views,'room':source('art/walking/apartment-background.png'),
        'front':source('art/walking/maziss-depth-atlas.png'),
        'side':source('art/walking/maziss-side-atlas.png')}
frames=OUT/'frames';frames.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(offline=True)
    page.set_content('<!doctype html><html><body><canvas id="review" width="960" height="600"></canvas></body></html>')
    page.evaluate('''async inputs=>{
      const load=src=>new Promise((resolve,reject)=>{let i=new Image();i.onload=()=>resolve(i);i.onerror=reject;i.src=src;});
      const art={room:await load(inputs.room),front:await load(inputs.front),side:await load(inputs.side)};
      const views=[];for(const v of inputs.views)views.push({angle:v.angle,frames:await Promise.all(v.frames.map(load))});
      const canvas=document.querySelector('canvas'),ctx=canvas.getContext('2d');
      window.paintFrame=(view,frame)=>{
        const v=views[view],room=art.room;
        const ratio=Math.max(960/room.width,600/room.height),w=room.width*ratio,h=room.height*ratio;
        ctx.drawImage(room,(960-w)/2,(600-h)/2,w,h);
        ctx.fillStyle='rgba(20,24,28,.80)';ctx.fillRect(0,0,960,42);ctx.fillRect(0,564,960,36);
        ctx.font='bold 19px sans-serif';ctx.fillStyle='#fff1d4';ctx.fillText('Original drawing',40,28);ctx.fillText('Actual animated model',450,28);
        ctx.font='16px sans-serif';ctx.fillText(v.angle+'° · First painting study — face and tailoring still need work',40,588);
        const back=v.angle===180,side=v.angle===90;
        ctx.save();if(side){ctx.translate(310,0);ctx.scale(-1,1);}
        ctx.drawImage(side?art.side:art.front,side?590:153,back?444:0,side?200:192,440,50,76,218,500);ctx.restore();
        ctx.drawImage(v.frames[frame],390,35,480,600);
        return canvas.toDataURL('image/png');
      };
    }''',inputs)
    n=0
    for index,view in enumerate(views):
        for frame in range(24):
            url=page.evaluate('([v,f])=>paintFrame(v,f)',[index,frame]);(frames/f'{n:04}.png').write_bytes(base64.b64decode(url.split(',',1)[1]));n+=1
        print('Prepared actual frames',view['angle'],flush=True)
    browser.close()

fps=24/film['cycle'];video=ROOT/'visual-preview/maziss-review-small.mp4'
# Repeat each camera's existing cycle twice. Encoding is a presentation change;
# character geometry, paintings and walking poses remain untouched.
listing=OUT/'sequence.txt'
names=[]
for view in range(4):
    for repeat in range(2):names.extend(frames/f'{view*24+i:04}.png' for i in range(24))
listing.write_text(''.join(f"file '{p}'\nduration {1/fps:.10f}\n" for p in names)+f"file '{names[-1]}'\n")
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-r',str(fps),'-c:v','libx264','-preset','medium','-crf','27','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(video)],check=True)
poster=OUT/'poster.jpg'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(frames/'0000.png'),'-frames:v','1','-q:v','4',str(poster)],check=True)
encoded='data:video/mp4;base64,'+base64.b64encode(video.read_bytes()).decode()
still='data:image/jpeg;base64,'+base64.b64encode(poster.read_bytes()).decode()
html='''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Maziss — small review</title>
<style>
body{margin:0;background:#20282e;color:#f2e8d8;font:17px/1.5 system-ui,sans-serif}
main{max-width:1000px;margin:auto;padding:20px}video,img{display:block;width:100%;height:auto;border-radius:8px}
details{margin-top:18px}summary{cursor:pointer}small{color:#c9c2b4}
</style>
</head>
<body>
<main>
<h1>Maziss: painted walking review</h1>
<p>Press Play for front, angled, side and back views. This is the same model and walking test, in a smaller video.</p>
<video controls playsinline muted loop preload="metadata" poster="__POSTER__">
<source src="__VIDEO__" type="video/mp4">
Your viewer cannot play this video. The still comparison is below.
</video>
<details open><summary>Still comparison</summary><img src="__POSTER__" width="960" height="600" alt="Original cartoon drawing at left and actual painted model render at right"></details>
<p><small>First surface-painting study. Face likeness and shoulder tailoring remain unfinished. All media is included in this file; no internet connection or live 3D support is required after download.</small></p>
</main>
</body>
</html>
'''.replace('__POSTER__',still).replace('__VIDEO__',encoded)
target=ROOT/'visual-preview/maziss-review-small.html';target.write_text(html)
for p in (target,video):p.chmod(0o644)
report={'source_build':json.loads((ROOT/'build/checks/painted-character/build-manifest.json').read_text())['build'],
        'source_html_sha256':hashlib.sha256((ROOT/'visual-preview/maziss-painted-rendered.html').read_bytes()).hexdigest(),
        'angles':chosen,'unique_frames':96,'repeated_frames':192,'cycle_seconds':film['cycle'],
        'html_bytes':target.stat().st_size,'video_bytes':video.stat().st_size,
        'html_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
(OUT/'compact-manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
