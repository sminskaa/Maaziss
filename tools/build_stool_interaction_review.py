#!/usr/bin/env python3
"""Composite actual 3D action over a local repaired plate; pack an offline review.

Use --keys to compose key renders only, otherwise package the complete sequence.
The generated background patch is a retained private image-tool output, not a
runtime network dependency. Original room and previous reviews stay unchanged.
"""
from pathlib import Path
import argparse
import base64
import hashlib
import io
import json
import subprocess

from PIL import Image, ImageDraw, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/checks/stool-interaction'
SOURCE=ROOT/'build/checks/room-cutaway/room-reframed-source.png'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def uri(raw,mime):
    return 'data:'+mime+';base64,'+base64.b64encode(raw).decode()


def jpeg(image,width=960,quality=76):
    image=image.convert('RGB');image.thumbnail((width,width),Image.Resampling.LANCZOS)
    stream=io.BytesIO();image.save(stream,'JPEG',quality=quality,optimize=True)
    return uri(stream.getvalue(),'image/jpeg')


def clean_background():
    source=Image.open(SOURCE).convert('RGB')
    patch=Image.open(OUT/'clean-patch-generated.png').convert('RGB').resize((260,250),Image.Resampling.LANCZOS)
    mask=Image.new('L',(260,250))
    ImageDraw.Draw(mask).polygon([(85,43),(139,40),(176,52),(183,83),(168,105),(184,177),(171,191),(145,182),(119,184),(88,188),(64,175),(61,152),(75,130),(88,95),(77,83),(77,58)],fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(2.5))
    source.paste(patch,(1320,570),mask);source.save(OUT/'room-clean.png')
    source.crop((1320,570,1580,820)).save(OUT/'clean-crop.png')
    mask.save(OUT/'repair-mask.png')
    return source


def main():
    global OUT
    parser=argparse.ArgumentParser();parser.add_argument('--keys',action='store_true')
    parser.add_argument('--output',type=Path,default=OUT)
    parser.add_argument('--html',type=Path,default=ROOT/'visual-preview/maziss-stool-interaction.html')
    parser.add_argument('--contact-view',type=Path,help='Optional actual alternate-camera hand contact image')
    args=parser.parse_args();OUT=args.output.resolve()
    m=json.loads((OUT/('key-manifest.json' if args.keys else 'render-manifest.json')).read_text())
    assert digest(ROOT/m.get('poseScriptPath','tools/stool_interaction_pose.py'))==m['poseScriptSHA256']
    assert all(digest(ROOT/path)==sha for path,sha in m.get('poseDependencies',{}).items())
    background=clean_background().convert('RGBA')
    scale=m['roomPixelsPerMetre']/(m['height']/m['orthoScale'])
    offset=tuple(round(m['roomFloorAnchor'][i]-m['groundPixel'][i]*scale) for i in (0,1))
    frames=OUT/'composite';frames.mkdir(exist_ok=True)
    first=None;last=None
    for r in m['renders']:
        actor=Image.open(OUT/r['name']).convert('RGBA')
        assert digest(OUT/r['name'])==r['sha256']
        canvas=background.copy()
        canvas.alpha_composite(actor.resize((round(actor.width*scale),round(actor.height*scale)),Image.Resampling.LANCZOS),offset)
        if args.keys:
            canvas.convert('RGB').save(OUT/('room-'+r['name']))
        else:
            index=round(r['seconds']*m['fps'])
            canvas.resize((1120,630),Image.Resampling.LANCZOS).convert('RGB').save(frames/f'frame-{index:03}.png')
        if first is None:first=canvas.copy()
        last=canvas
    if args.keys:
        print('Composited',len(m['renders']),'actual keyframes',offset,scale);return
    assert len(m['renders'])==round(m['duration']*m['fps'])+1
    original=Image.open(SOURCE).crop((1320,570,1580,820))
    repaired=Image.open(OUT/'clean-crop.png')
    template='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Maziss — use the desk stool</title>
<style>*{box-sizing:border-box}body{margin:0;background:#24232b;color:#f4e6cf;font:17px/1.5 system-ui,sans-serif}main{max-width:1120px;margin:auto;padding:18px}h1{line-height:1.2}video,img{display:block;width:100%;height:auto;border-radius:6px}.scene{position:relative}.controls{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0}button{font:inherit;background:#4d493b;color:#f4e6cf;border:1px solid #a68e6a;border-radius:5px;padding:8px 17px;cursor:pointer}button[aria-pressed=true]{background:#dfbd73;color:#252027}#hotspot{position:absolute;left:78%;top:60%;width:15%;height:24%;padding:0;border:2px dashed #f3ce7d;background:transparent}#hotspot[hidden]{display:none}#status{min-height:1.6em}small{color:#cebea9}.proof{display:grid;grid-template-columns:1fr 1fr;gap:16px}.proof img{max-width:400px}figure{margin:12px 0}figcaption{padding:8px 0}details{margin:20px 0}@media(max-width:600px){.proof{grid-template-columns:1fr}}</style>
<main><h1>Use the desk stool</h1><p>Select <strong>Use</strong>, then click the highlighted stool beside the desk. Maziss approaches, pulls it toward himself and sits. You can also use the video controls to watch or inspect any moment.</p>
<div class="controls"><button id="use" aria-pressed="false">Use</button><button id="reset">Reset</button></div>
<div class="scene"><video id="action" controls playsinline preload="auto" poster="__POSTER__"><source src="__MOVIE__" type="video/webm"></video><button id="hotspot" hidden aria-label="Use the stool beside the desk"></button></div>
<p id="status" role="status" aria-live="polite">Ready. Select Use and click the stool.</p>
<details><summary>Check the background beneath the stool</summary><p>The original painted stool and its shadow are removed locally. The 3D stool moves over the repaired rug and floor.</p><div class="proof"><figure><img src="__ORIGINAL__" alt="Original painted stool and surrounding desk/rug"><figcaption>Original artwork</figcaption></figure><figure><img src="__CLEAN__" alt="Repaired background with the painted stool removed and an intact rug"><figcaption>Repaired background</figcaption></figure></div></details>
<details><summary>Still: seated on the moved 3D stool</summary><img src="__STILL__" alt="Actual final render of Maziss seated on the moved stool"></details>
<p><small>First desk-stool interaction study. Character and stool are rendered together as real 3D geometry, with a fixed camera and floor shadow catcher. The room remains painted art with a local background repair. Surface detail, the mitten-like free hand and joined bag-side hand remain unfinished. This is one authored action, separate from the main Godot room.</small></p>
<script>const video=document.querySelector('#action'),use=document.querySelector('#use'),hotspot=document.querySelector('#hotspot'),status=document.querySelector('#status');
use.onclick=()=>{use.setAttribute('aria-pressed','true');hotspot.hidden=false;status.textContent='Click the highlighted stool to use it.'};
hotspot.onclick=()=>{hotspot.hidden=true;video.currentTime=0;video.play().catch(e=>{status.textContent='Use the video Play control to watch the action.';console.error(e)})};
document.querySelector('#reset').onclick=()=>{video.pause();video.currentTime=0;hotspot.hidden=true;use.setAttribute('aria-pressed','false');status.textContent='Ready. Select Use and click the stool.'};
function phase(t){return t<1.2?'Approaching the desk':t<2.5?'Reaching for the stool':t<4?'Pulling the stool':t<4.6?'Releasing the stool':t<5.8?'Moving into position':t<7.8?'Sitting down':'Seated'}
video.addEventListener('timeupdate',()=>{if(!hotspot.hidden)return;if(video.currentTime>0)status.textContent=phase(video.currentTime)});
Object.defineProperty(window,'stoolReview',{value:Object.freeze({snapshot:()=>({time:video.currentTime,duration:video.duration,paused:video.paused,ended:video.ended,readyState:video.readyState,phase:phase(video.currentTime),useSelected:use.getAttribute('aria-pressed')==='true',hotspotVisible:!hotspot.hidden})})});</script></main></html>'''
    if m.get('phaseBoundaries'):
        template=template.replace('pulls it toward himself and sits.', 'pulls it toward himself, steps around the back of the stool and sits facing the desk.')
        old=template[template.index('function phase(t)'):template.index("\nvideo.addEventListener")]
        cases=':'.join('t<'+str(end)+'?'+json.dumps(label) for end,label in m['phaseBoundaries'])+':'+json.dumps(m.get('finalLabel','Seated facing the desk'))
        template=template.replace(old,'function phase(t){return '+cases+'}')
    if m.get("reviewDescription"):
        template=template.replace("Maziss approaches, pulls it toward himself, steps around the back of the stool and sits facing the desk.",m["reviewDescription"])
    if m.get('deskGeometry'):
        template=template.replace('Surface detail, the mitten-like free hand and joined bag-side hand remain unfinished.', 'The right arm moves independently of the satchel. Fitted 3D desk and object volumes provide contact and depth while retaining the painted appearance. Surface detail and hand shapes remain unfinished.')
    if args.contact_view:
        contact=jpeg(Image.open(args.contact_view),width=640,quality=74)
        proof='<details><summary>Alternate view: both hands at the desktop</summary><img src="'+contact+'" alt="Actual alternate-camera render showing both rounded hands supported at the desk"><p>This diagnostic view uses a plain desk surface to expose hand contact. The room view retains the painted artwork. Hand and finger detail is still preliminary.</p></details>'
        template=template.replace('<p><small>First desk-stool interaction study.',proof+'<p><small>First desk-stool interaction study.')
    for crf in (33,36,39):
        movie=OUT/'desk-stool-action.webm'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate',str(m['fps']),'-i',str(frames/'frame-%03d.png'),'-vf','tpad=stop_mode=clone:stop_duration=1','-c:v','libvpx-vp9','-b:v','0','-crf',str(crf),'-row-mt','1','-threads','4','-pix_fmt','yuv420p','-an',str(movie)],check=True)
        html=template.replace('__POSTER__',jpeg(first,width=1120,quality=72)).replace('__MOVIE__',uri(movie.read_bytes(),'video/webm')).replace('__ORIGINAL__',jpeg(original,width=260,quality=88)).replace('__CLEAN__',jpeg(repaired,width=260,quality=88)).replace('__STILL__',jpeg(last,width=960,quality=73))
        print('PACK',crf,len(html.encode()),flush=True)
        if len(html.encode())<1_000_000:break
    target=args.html.resolve()
    target.write_text(html);target.chmod(0o644);target.parent.chmod(0o755)
    report={'htmlBytes':target.stat().st_size,'htmlSHA256':digest(target),
            'contactViewSHA256':digest(args.contact_view) if args.contact_view else None,
            'movieSHA256':digest(movie),'movieCRF':crf,'renderManifestSHA256':digest(OUT/'render-manifest.json'),
            'cleanRoomSHA256':digest(OUT/'room-clean.png'),'sourceRoomSHA256':digest(SOURCE),
            'scope':m['scope'],'renders':len(m['renders']),'nativeVideoSize':[1120,630],
            'actorScale':scale,'actorOffset':offset}
    (OUT/'delivery-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
