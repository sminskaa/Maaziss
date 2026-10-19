#!/usr/bin/env python3
"""Pack actual rendered poses into an offline interactive sofa review."""
from pathlib import Path
import base64, hashlib, io, json, math, subprocess
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/checks/sofa-sit';ASSETS=OUT/'assets';ASSETS.mkdir(exist_ok=True)
manifest=json.loads((OUT/'render-manifest.json').read_text())
assert len(manifest['sit'])==41 and len(manifest['walk'])==8
assert min(c['minimumZ'] for c in manifest['contacts'])>-.001

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def url(raw,kind):return 'data:'+kind+';base64,'+base64.b64encode(raw).decode()

def sheet(files,cell,columns,quality):
    image=Image.new('RGBA',(columns*cell[0],math.ceil(len(files)/columns)*cell[1]),(0,0,0,0))
    for i,name in enumerate(files):
        with Image.open(OUT/name) as frame:
            image.paste(frame.resize(cell,Image.Resampling.BICUBIC),((i%columns)*cell[0],(i//columns)*cell[1]))
    data=io.BytesIO();image.save(data,'WEBP',quality=quality,alpha_quality=50,method=5)
    return data.getvalue()

# Pixel scale is fitted to the clear right cushion, not to each frame's bounds.
ppu=250;render_ppm=manifest['height']/manifest['orthoScale'];ratio=ppu/render_ppm
seat_contact=[430,610];ground=manifest['groundPixel'];contact=manifest['seatContactPixel']
origin=[seat_contact[i]-(contact[i]-ground[i])*ratio for i in (0,1)]

def project_local(point):
    angle=math.radians(manifest['sitHeadingDegrees']);x,y,z=point
    x,y=x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle)
    cam=manifest['cameraPosition'];target=manifest['cameraTarget']
    depth=math.hypot(cam[1]-target[1],cam[2]-target[2]);sine=(cam[2]-target[2])/depth;cosine=abs(cam[1]-target[1])/depth
    return [origin[0]+x*ppu,origin[1]-(y*sine+z*cosine)*ppu]
seat_guide=[project_local((x,y,manifest['seatHeight'])) for x,y in [(-.36,.065),(.36,.065),(.36,.665),(-.36,.665)]]
cam=manifest['cameraPosition'];target=manifest['cameraTarget'];foreshortening=(cam[2]-target[2])/math.hypot(cam[1]-target[1],cam[2]-target[2])
motion=json.loads((ROOT/'build/checks/supplied-character/motion-private.json').read_text())
stride=0
for side in ('Left','Right'):
    values=[f[side+'Foot']['head'][1] for f in motion['frames']];stride+=max(values)-min(values)
room_image=Image.open(ROOT/'build/checks/room-cutaway/room-reframed-source.png').convert('RGB')
room_bytes=io.BytesIO();room_image.resize((1280,720),Image.Resampling.LANCZOS).save(room_bytes,'JPEG',quality=74,optimize=True)
idle=[]
for i in range(16):
    angle=i*22.5;key=str(int(angle)) if angle.is_integer() else str(angle)
    idle.append(manifest['idle'][key] if i%2==0 else manifest['turn'][key])
floor=[[0,941],[1672,941],[1672,835],[1425,795],[1350,615],[625,615],[575,655],[495,695],[400,750],[0,805]]
script=(ROOT/'tools/sofa_interaction.js').read_text()
template='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Maziss — try the sofa</title>
<style>body{margin:0;background:#20282e;color:#f2e8d8;font:17px/1.5 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:18px}canvas,img{display:block;width:100%;height:auto;border-radius:6px}canvas{touch-action:manipulation;cursor:crosshair}.controls{display:flex;flex-wrap:wrap;align-items:center;gap:9px;margin:12px 0}button{font:inherit;color:#f9edd6;background:#3b4c4b;border:1px solid #958767;border-radius:5px;padding:7px 16px;cursor:pointer}button[aria-pressed=true]{color:#282318;background:#e4c57b}#status{min-height:3em;margin:8px 0}details{margin-top:18px}small{color:#cfc4b3}</style></head><body><main>
<h1>Try sitting on the sofa</h1><p>Click clear floor to walk. Select <strong>Use</strong>, then click the sofa: Maziss will use the same empty right cushion. Click the floor again to stand up and walk there.</p>
<p id="loading">Loading the room and animation…</p><canvas id="room" width="1672" height="941" role="img" aria-label="Interactive room: click the floor to walk, or choose Use and click the sofa to sit"></canvas>
<div class="controls"><button data-verb="Walk" aria-pressed="true">Walk</button><button data-verb="Use" aria-pressed="false">Use</button><button data-verb="Look at" aria-pressed="false">Look at</button><button id="reset">Reset</button><label><input id="guide" type="checkbox"> Seat guide</label></div><p id="status" role="status" aria-live="polite">Loading…</p>
<details><summary>Still: seated on the clear cushion</summary><img src="__STILL__" width="960" height="540" alt="Maziss seated on the right cushion with the pillows left in place"></details>
<p><small>First interaction study. Actual model poses use a fitted seat and floor proxy; the room remains painted artwork. Bag-side arm limitations and unfinished face/material detail remain. Contact shadows and the near sofa arm are composited. This review runs offline; it is not yet installed in the main Godot game.</small></p>
<script>window.SOFA_DATA=__DATA__;</script><script>__SCRIPT__</script></main></body></html>'''

# The fallback is composed from the same final real model render, at exactly
# the same anchor and scale as the interactive view.
still=room_image.convert('RGBA');actor=Image.open(OUT/manifest['sit'][-1]).convert('RGBA')
placed=actor.resize((round(manifest['width']*ratio),round(manifest['height']*ratio)),Image.Resampling.LANCZOS)
still.alpha_composite(placed,(round(origin[0]-ground[0]*ratio),round(origin[1]-ground[1]*ratio)))
still.resize((960,540),Image.Resampling.LANCZOS).convert('RGB').save(ASSETS/'seated-fallback.jpg',quality=68,optimize=True)
fallback=(ASSETS/'seated-fallback.jpg').read_bytes()

movies={}
for name,pattern,fps,reverse in [('sit','sit-%02d.png',20,False),('stand','sit-%02d.png',20,True)]+[('walk-'+a,'walk-'+a+'-%02d.png',24/manifest['cycleSeconds'],False) for a in manifest['walk']]:
    target_movie=ASSETS/(name+'.webm')
    command=['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate',str(fps),'-i',str(OUT/pattern)]
    if reverse:command+=['-vf','reverse']
    command+=['-c:v','libvpx-vp9','-pix_fmt','yuva420p','-b:v','0','-crf','34','-auto-alt-ref','0','-an',str(target_movie)]
    subprocess.run(command,check=True)
    movies[name]={'kind':'video','src':url(target_movie.read_bytes(),'video/webm')}
for cell,quality in [((288,360),76),((240,300),70),((216,270),65)]:
    entries={}
    groups={'idle':idle}
    for name,files in groups.items():
        columns=7 if name=='sit' else 4 if name=='idle' else 6
        raw=sheet(files,cell,columns,quality);(ASSETS/f'{name}.webp').write_bytes(raw)
        entries[name]={'src':url(raw,'image/webp'),'frames':len(files),'columns':columns}
    entries.update(movies)
    data={'room':url(room_bytes.getvalue(),'image/jpeg'),'sheets':entries,'cell':cell,
          'renderSize':[manifest['width'],manifest['height']],'renderPixelsPerMetre':render_ppm,
          'groundPixel':ground,'footShadows':manifest['footShadows'],'seatGuide':seat_guide,
          'seat':{'origin':origin,'contact':seat_contact,'height':manifest['seatHeight'],'pixelsPerMetre':ppu,'singleSpot':True},
          'sitFrames':len(manifest['sit']),'sitSeconds':manifest['sitSeconds'],'floor':floor,
          'routeNodes':[[1450,850],[1280,660],[680,660],[580,720],[450,790],[280,850]],
          'nearArm':[[555,550],[578,535],[592,570],[575,620],[555,647],[550,618]],
          'floorForeshortening':foreshortening,'strideMetres':stride,
          'sourceModelSHA256':manifest['sourceGLBSHA256']}
    html=template.replace('__STILL__',url(fallback,'image/jpeg')).replace('__DATA__',json.dumps(data,separators=(',',':'))).replace('__SCRIPT__',script)
    print('PACK',cell,quality,len(html.encode()),flush=True)
    if len(html.encode())<1_000_000:break
else:raise RuntimeError('Interactive review exceeds compact delivery budget')
target=ROOT/'visual-preview/maziss-sofa-sit.html';target.write_text(html);target.chmod(0o644);target.parent.chmod(0o755)
report={'sourceModelSHA256':manifest['sourceGLBSHA256'],'renderManifestSHA256':digest(OUT/'render-manifest.json'),
        'htmlSHA256':digest(target),'htmlBytes':target.stat().st_size,'cell':cell,'webpQuality':quality,
        'animationEncoding':'Full288×360 alphaVP9 clips; high-resolution WebP idle poses; Chrome/Brave review format',
        'seat':data['seat'],'seatGuide':seat_guide,'floor':floor,'sourceRoomSHA256':digest(ROOT/'build/checks/room-cutaway/room-reframed-source.png'),
        'scope':'Interactive HTML study with actual3Dpose renders, seat/floor proxy and2Dfloor routing; no main Godot scene changes'}
(OUT/'delivery-manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
