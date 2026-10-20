#!/usr/bin/env python3
"""Composite retained actual pose renders and package an offline review."""
from pathlib import Path
from PIL import Image,ImageDraw
import base64,io,json,html,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/checks/stool-feedback'
manifest=json.loads((OUT/'manifest.json').read_text())
assert hashlib.sha256((ROOT/'tools/stool_feedback_pose.py').read_bytes()).hexdigest()==manifest['poseSHA256']
background=Image.open(ROOT/'build/checks/stool-slide/room-clean.png').convert('RGBA')
scale=manifest['roomPixelsPerMetre']/(640/manifest['orthoScale'])
offset=tuple(round(manifest['roomFloorAnchor'][i]-manifest['groundPixel'][i]*scale) for i in (0,1))
def uri(im,width=500):
 im=im.convert('RGB');im.thumbnail((width,width));b=io.BytesIO();im.save(b,format='JPEG',quality=78,optimize=True)
 return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
labels={0:'A1 · Seated, before moving either foot',65:'A2 · Right foot moved; left foot and torso stay',145:'A3 · Left foot follows; torso still faces upper right',240:'A4 · Torso and head now face screen right',305:'B1 · Separate test: seated at the desk before reaching',370:'B2 · Hands retract below the edge',450:'B3 · Hands lift outside the desk edge',540:'B4 · Hands travel above the desktop',600:'B5 · Hands lower onto the desktop'}
rows=[];sheet=[]
for record in manifest['renders']:
 n=round(record['seconds']*100);room=background.copy();actor=Image.open(OUT/record['name']).convert('RGBA')
 room.alpha_composite(actor.resize((round(640*scale),round(640*scale)),Image.Resampling.LANCZOS),offset)
 room.convert('RGB').save(OUT/f'room-{n:03}.jpg',quality=90)
 crop=room.crop((1120,345,1672,900));crop.save(OUT/f'crop-{n:03}.png')
 diag=Image.open(OUT/f'diagnostic-{n:03}.png').convert('RGBA');plain=Image.new('RGBA',diag.size,(63,73,81,255));plain.alpha_composite(diag)
 tile=Image.new('RGB',(600,350),(28,39,48));a=crop.convert('RGB');a.thumbnail((290,310));tile.paste(a,(0,35));b=plain.convert('RGB');b.thumbnail((300,310));tile.paste(b,(300,35));ImageDraw.Draw(tile).text((6,8),labels[n],fill='white');sheet.append(tile)
 rows.append(f'<figure id="frame-{n}"><h3>{html.escape(labels[n])}</h3><div class="pair"><div><img src="{uri(crop)}" alt="{html.escape(labels[n])}, real rendered pose in the room"><p>Room view · desk-area crop</p></div><div><img src="{uri(plain)}" alt="{html.escape(labels[n])}, alternate real camera with diagnostic desk"><p>Diagnostic camera · same pose, neutral desk</p></div></div></figure>')
contact=Image.new('RGB',(1200,350*5),(28,39,48))
for i,tile in enumerate(sheet):contact.paste(tile,((i%2)*600,(i//2)*350))
contact.save(OUT/'review-contact-sheet.jpg',quality=90)
sections='<h2>A · Right foot → left foot → torso and head</h2>'+''.join(rows[:4])+'<h2>B · Separate hand-to-desk test</h2><p>The stool and character start closer to the desk in this second test. The intervening slide is not animated here.</p>'+''.join(rows[4:])
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Maziss — corrected stool poses</title><style>*{box-sizing:border-box}body{margin:0;background:#17232b;color:#f8ecd8;font:16px/1.5 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:18px}h1{font-size:26px}h2{margin-top:28px;color:#ffe196}h3{font-size:19px;margin:0 0 10px}figure{margin:16px 0;background:#23343f;border:1px solid #68818e;padding:12px;border-radius:8px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}img{width:100%;height:auto;display:block;border-radius:5px}.pair p,.hint{color:#cbdbe3;font-size:14px}label{display:block;margin:14px 0 5px}textarea,select,button{font:inherit;padding:9px;background:#243d4b;color:#fff3d8;border:1px solid #a0a9a7;border-radius:5px}textarea{width:100%;min-height:110px}button{cursor:pointer;background:#785b26}a{color:#ffe196}nav{display:flex;gap:15px;flex-wrap:wrap}p{margin:8px 0}@media(max-width:650px){.pair{grid-template-columns:1fr}main{padding:10px}}</style></head><body><main>
<h1>Corrected stool poses · small movement study</h1><p>Two isolated tests based on your feedback: ordered foot placement and seated turn; then a clear hand route onto the desk.</p>
<p><strong>The existing model is still unfinished.</strong> These are actual posed renders, not drawings of intended contacts. This page does not demonstrate continuous animation, natural timing, click-to-walk or Godot integration.</p><nav><a href="#frame-0">A · Seated turn</a><a href="#frame-305">B · Hand reach</a><a href="#feedback">Leave feedback</a></nav>
<p class="hint">The alternate camera uses a plain desk surface to expose contact. It is a diagnostic view, not a proposed replacement for the original room. No new character appearance is being proposed.</p>
__SECTIONS__
<section id="feedback"><h2>Your feedback on these two tests</h2><p>No need to review the unchanged approach, pull or slide again. Note the frame label if a pose needs changing.</p><label for="turn">A · Foot order and seated turn</label><select id="turn"><option value="unreviewed">Not reviewed</option><option value="matches-intent">Matches my intention for these poses</option><option value="revise">Needs correction</option></select><label for="reach">B · Hand route and placement</label><select id="reach"><option value="unreviewed">Not reviewed</option><option value="matches-intent">Matches my intention for these poses</option><option value="revise">Needs correction</option></select><label for="comments">Corrections / frame labels</label><textarea id="comments" placeholder="For example: in A3 the left foot should be closer to …"></textarea><button id="save">Save pose feedback</button><p id="status" role="status">Attach the downloaded JSON in chat, or reply with your comments directly.</p></section>
<p class="hint">Pose acceptance is separate from final character appearance, motion fluidity and game integration. The hand and facial detail in this rig remain limited.</p>
<script>const ids=['turn','reach','comments'],KEY='maziss-feedback-pose-v1';let saved={};try{saved=JSON.parse(localStorage.getItem(KEY))||{};}catch(e){}for(const id of ids){const el=document.getElementById(id);if(typeof saved[id]==='string')el.value=saved[id];el.oninput=()=>{saved[id]=el.value;try{localStorage.setItem(KEY,JSON.stringify(saved));}catch(e){}};}document.getElementById('save').onclick=()=>{const data={format:'maziss-stool-pose-feedback',version:1,poseSHA256:'__HASH__',exportedAt:new Date().toISOString()};for(const id of ids)data[id]=document.getElementById(id).value;const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download='maziss-stool-pose-feedback.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);document.getElementById('status').textContent='Download requested. Attach maziss-stool-pose-feedback.json in chat.';};</script></main></body></html>'''.replace('__SECTIONS__',sections).replace('__HASH__',manifest['poseSHA256'])
out=ROOT/'visual-preview/maziss-stool-pose-test.html';out.write_text(page);out.chmod(0o644);assert out.stat().st_size<1000000,out.stat().st_size
(OUT/'delivery.json').write_text(json.dumps({'htmlBytes':out.stat().st_size,'poseSHA256':manifest['poseSHA256'],'htmlSHA256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2));print(out,out.stat().st_size)
