#!/usr/bin/env python3
"""Create a compact, offline intent storyboard from the owner's directions.
Diagrams are contact/position annotations, not rendered poses or animation.
"""
from pathlib import Path
import base64,io,json,html
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'private/directions/seat-at-desk-original.json'
d=json.loads(source.read_text());notes=d['notes']
im=Image.open(ROOT/'build/checks/room-cutaway/room-reframed-source.png').convert('RGB');im.thumbnail((1280,720));buf=io.BytesIO();im.save(buf,format='JPEG',quality=82)
uri='data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()
beats=[
 ('Turn, then approach','Turn toward the desk while still at the start. Then walk to the left of the stool, close enough to reach it with the right hand.','Turn before translation. No route points were supplied: the game must calculate a valid route.', 'approach'),
 ('Right-hand grip','Stand beside the stool and grasp its top with the anatomical right hand at your marked location.','Maintain a plausible shoulder/elbow/wrist alignment; keep the hand clear of the bag.', 'grip'),
 ('Pull the stool back','Pull the stool away from the desk until its seat and right-hand grip reach your third mark.','Right hand stays attached during the pull. Keep body repositioning small; no circling or repeated tiny steps.', 'pull'),
 ('Turn and sit','Turn head and torso toward the upper right to sit on the pulled-out stool. Once seated, turn head and torso toward screen right.','Your mark identifies the intended seated area. Exact hip height and seat contact still need a posed visual test.', 'sit'),
 ('Slide forward together','While seated and facing right, grasp the stool with the right hand and move forward with the stool to your fifth mark.','Character and stool travel together. The desk should hide the right foot, as you requested.', 'slide'),
 ('Hands on the desk','Finish seated toward the desk and place both hands on its surface at the marked area.','No writing action yet. Exact left/right palm locations need a posed visual test.', 'finish')]
# Shared image is embedded once, then referenced by every inline SVG.
def marker(p,label,color='#ffdc85'):
 x,y=p['x']*1280,p['y']*720
 return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="#14232c" stroke="{color}" stroke-width="4"/><text x="{x-6:.1f}" y="{y+6:.1f}" fill="white" font-size="19" font-weight="bold">{label}</text>'
def arrow(a,b):
 return f'<path d="M {a["x"]*1280:.1f} {a["y"]*720:.1f} L {b["x"]*1280:.1f} {b["y"]*720:.1f}" stroke="#ffe196" stroke-width="5" stroke-dasharray="10 7" marker-end="url(#arrow)"/>'
cards=[]
for i,(title,interpret,checks,kind) in enumerate(beats):
 overlay=marker(notes[i],str(i+1))
 if i==0:overlay+=marker(d['start'],'S','#8df4df')+marker(d['end'],'D','#8df4df')+arrow(d['start'],d['end'])
 if i==2:overlay+=marker(notes[1],'2','#8df4df')+arrow(notes[1],notes[2])
 if i==3:overlay+='<text x="925" y="465" fill="#fff4d6" stroke="#14232c" stroke-width="5" paint-order="stroke" font-size="23">Face upper-right, then right</text>'
 if i==4:overlay+=marker(notes[3],'4','#8df4df')+arrow(notes[3],notes[4])
 svg=f'<svg viewBox="0 0 1280 720" role="img" aria-label="Beat {i+1} contact and position diagram"><use href="#room-picture"/>{overlay}</svg>'
 cards.append(f'''<article><h2>{i+1}. {html.escape(title)}</h2>{svg}<p>{html.escape(interpret)}</p><p class="hint">Check: {html.escape(checks)}</p><details><summary>Your original note</summary><p>{html.escape(notes[i]['text'])}</p></details><label for="status{i}">My interpretation of beat {i+1} is</label><select id="status{i}" data-status="{i}"><option value="unreviewed">Not reviewed yet</option><option value="intent-agreed">Correct intention</option><option value="revise">Needs correction</option></select><label for="note{i}">Your correction, if any</label><textarea id="note{i}" data-note="{i}" placeholder="For example: turn the other way before sitting."></textarea></article>''')
payload=json.dumps({'format':'maziss-storyboard-feedback','version':1,'sourceExportedAt':d.get('exportedAt'),'sourceFile':source.name,'beats':[{'number':i+1,'title':b[0],'interpretation':b[1],'status':'unreviewed','correction':''}for i,b in enumerate(beats)]})
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Maziss — stool action storyboard</title><style>
*{box-sizing:border-box}body{margin:0;background:#17232b;color:#f8ecd8;font:16px/1.5 system-ui,sans-serif}main{max-width:1350px;margin:auto;padding:20px}h1{font-size:27px;margin:0}h2{font-size:20px;margin:0 0 10px}.hint{color:#c7d9e4;font-size:14px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}article{background:#23343f;padding:14px;border:1px solid #567482;border-radius:8px}svg{display:block;width:100%;height:auto;border-radius:5px}label{display:block;margin-top:10px}textarea,select,button{font:inherit}textarea,select{width:100%;background:#14232c;color:#fff1dd;border:1px solid #78909b;border-radius:5px;padding:8px}textarea{min-height:75px}button{background:#735926;color:#fff7e9;padding:12px;border:1px solid #ffe196;border-radius:6px;cursor:pointer}button:focus-visible,textarea:focus-visible,select:focus-visible{outline:3px solid #ffe196;outline-offset:2px}.bar{position:sticky;bottom:0;background:#17232bf5;padding:14px 0;display:flex;gap:12px;align-items:center;flex-wrap:wrap}summary{cursor:pointer}p{margin:8px 0}#msg{font-size:14px;color:#ffe196}@media(max-width:800px){.grid{grid-template-columns:1fr}main{padding:12px}}
</style></head><body>
<svg aria-hidden="true" width="0" height="0" style="position:absolute"><defs><image id="room-picture" href="__IMAGE__" width="1280" height="720"/><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="#ffe196" stroke-width="1.3"/></marker></defs></svg>
<main><h1>Stool action · six-beat interpretation</h1>
<p>Check whether these six steps describe what you mean. Choose “Correct intention” or “Needs correction” under each, then save your feedback.</p>
<p class="hint">These are position/contact diagrams over the unchanged painting, not character poses or an animation. The painted stool does not move here. Gold numbered circles reproduce your marks; turquoise circles identify the related start point. Dashed lines indicate intended displacement, not a calculated walkable path. Character size and physical contacts remain unapproved.</p>
<div class="grid">__CARDS__</div><div class="bar"><button id="save">Save feedback for all six beats</button><span id="msg" role="status">Feedback is not automatically sent to chat.</span></div>
<p class="hint">Attach the saved JSON file in chat, or simply reply with the beat numbers you want changed. “Correct intention” approves the interpretation only; it does not approve animation, character appearance or timing.</p></main>
<script>const defaults=__PAYLOAD__;let review=structuredClone(defaults);const KEY='maziss-stool-storyboard-v1';try{const s=JSON.parse(localStorage.getItem(KEY));if(s&&s.sourceExportedAt===defaults.sourceExportedAt&&Array.isArray(s.beats)&&s.beats.length===6)review=s;}catch(e){}
function persist(){try{localStorage.setItem(KEY,JSON.stringify(review));document.getElementById('msg').textContent='Saved in this browser. Download and attach the file to share.';}catch(e){document.getElementById('msg').textContent='Use Save feedback before closing; browser storage is unavailable.';}}
document.querySelectorAll('[data-status]').forEach(el=>{const b=review.beats[+el.dataset.status];el.value=b.status;el.onchange=()=>{b.status=el.value;persist();};});
document.querySelectorAll('[data-note]').forEach(el=>{const b=review.beats[+el.dataset.note];el.value=b.correction;el.oninput=()=>{b.correction=el.value;persist();};});
document.getElementById('save').onclick=()=>{const data={...review,exportedAt:new Date().toISOString()},url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='maziss-stool-storyboard-feedback.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);document.getElementById('msg').textContent='Download requested. Attach maziss-stool-storyboard-feedback.json in chat.';};
</script></body></html>'''.replace('__IMAGE__',uri).replace('__CARDS__','\n'.join(cards)).replace('__PAYLOAD__',payload)
out=ROOT/'visual-preview/maziss-stool-storyboard.html';out.write_text(page);out.chmod(0o644);assert out.stat().st_size<1000000
print(f'{out}: {out.stat().st_size:,} bytes')
if __name__=='__main__':pass
