#!/usr/bin/env python3
"""Capture actual rendered walking-study phases into an offline HTML review.

Uses Playwright and the internal test browser; never embeds the private footage.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import http.server,functools,threading,base64,json
r=Path(__file__).resolve().parents[1];out=r/'build/checks/clothing-walk/coordinator';out.mkdir(parents=True,exist_ok=True)
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*_):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(r)));threading.Thread(target=server.serve_forever,daemon=True).start()
rows=[];parts=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1450,'height':1050})
 page.goto(f'http://127.0.0.1:{server.server_port}/visual-preview/maziss-walking-v8.html');page.wait_for_function('()=>window.mazissWalk&&mazissWalk.getState().ready')
 for view in ['right','front','back','left']:
  page.click(f'[data-view={view}]')
  if page.evaluate('mazissWalk.getState().paused'):page.click('#pause')
  page.wait_for_timeout(700);page.click('#pause');page.wait_for_timeout(30)
  while page.evaluate('mazissWalk.getState().pose.phase')>.035:page.evaluate("document.getElementById('step').click()")
  images=[]
  for i in range(8):
   for _ in range(4):page.evaluate("document.getElementById('step').click()")
   s=page.evaluate('mazissWalk.getState()');box=page.locator('#room').bounding_box();scale=box['width']/1932
   clip={'x':box['x']+(s['position']['x']-220)*scale,'y':box['y']+(s['position']['y']-490)*scale,'width':440*scale,'height':515*scale}
   data=page.screenshot(clip=clip);(out/f'{view}-{i}.png').write_bytes(data)
   images.append('<figure><img src="data:image/png;base64,'+base64.b64encode(data).decode()+'"><figcaption>Phase '+str(round(s['pose']['phase'],2))+'</figcaption></figure>')
  rows.append('<h2>'+view+'</h2><section>'+''.join(images)+'</section>')
 for item in page.evaluate('''()=>{const out=[];for(const [view,cache]of Object.entries(mazissWalk.getPainter().cache))for(const key of ['head','body','bag','pants','otherPants','boot','otherBoot']){const L=cache[key];if(!L)continue;const c=document.createElement('canvas');c.width=180;c.height=210;const ctx=c.getContext('2d'),s=Math.min(160/L.w,190/L.h);ctx.translate((180-L.w*s)/2,(210-L.h*s)/2);ctx.scale(s,s);ctx.drawImage(L.canvas,0,0);out.push({view,key,png:c.toDataURL()});}return out;}'''):
  parts.append('<figure><img src="'+item['png']+'"><figcaption>'+item['view']+' — '+item['key']+'</figcaption></figure>')
 b.close()
server.shutdown()
html='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Maziss FBX walk poses</title><style>body{background:#1c2029;color:#f5e7d5;font:16px system-ui;margin:20px}section{display:flex;gap:8px;overflow-x:auto}figure{margin:0}img{width:220px;height:auto}figcaption{padding:8px}.parts{flex-wrap:wrap;overflow:visible}.parts img{width:180px;background:#888}</style><h1>Actual rendered walking poses — revision 8</h1><p>Eight phase samples per direction from the interactive character. These are visual review captures, not an approval of naturalness. Use the interactive page for normal playback, slow playback and frame stepping.</p>'+''.join(rows)+'<h2>Separate drawing layers</h2><p>Actual cached artwork used by the renderer, shown before animation. These are 2D painted layers, not 3D clothing models. The jacket has complete backing beneath moving arms; the bag is a complete separate layer. Original head/face and original tailoring details are retained. Each leg is then deformed continuously along the animated bones.</p><section class="parts">'+''.join(parts)+'</section></html>'
target=r/'visual-preview/maziss-walking-v8-poses.html';target.write_text(html);target.chmod(0o644)
# A separate local screenshot of the HTML contact sheet for coordinator inspection.
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1900,'height':1900});page.set_content(html);page.screenshot(path=str(out/'sheet.png'),full_page=True);b.close()
print('Captured32 rendered poses and built HTML pose review.')
