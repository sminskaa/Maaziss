#!/usr/bin/env python3
"""Capture the actual painted rig; HTML playback needs no WebGL or network."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,json,hashlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/checks/painted-character'
HTML=ROOT/'visual-preview/maziss-painted-3d.html'
N=24
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',
                             args=['--no-sandbox','--enable-unsafe-swiftshader'])
    page=browser.new_page(viewport={'width':1200,'height':1000},offline=True)
    page.set_content(HTML.read_text())
    page.wait_for_function('window.maziss3d&&maziss3d.ready',timeout=60000)
    page.evaluate('''()=>{const a=maziss3d;a.setPhase(0);a.setBackdrop('room');
      a.renderer.setPixelRatio(1);a.renderer.setSize(480,600,false);
      a.camera.aspect=.8;a.camera.updateProjectionMatrix();a.draw();}''')
    views=[]
    for angle in range(0,360,45):
        page.evaluate('a=>maziss3d.setView(a)',angle)
        frames=[]
        for frame in range(N):
            frames.append(page.evaluate('p=>{maziss3d.setPhase(p);return maziss3d.renderer.domElement.toDataURL("image/webp",.90)}',frame/N))
        page.evaluate('maziss3d.setWalking(false)')
        idle=page.evaluate('maziss3d.renderer.domElement.toDataURL("image/webp",.90)')
        page.evaluate('maziss3d.setWalking(true)')
        views.append({'angle':angle,'frames':frames,'idle':idle})
        print('Captured actual painted rig',angle,'degrees',flush=True)
    cycle=page.evaluate('maziss3d.data.motion.cycleSeconds')
    browser.close()

def embedded(path):
    return 'data:image/png;base64,'+base64.b64encode((ROOT/path).read_bytes()).decode()

template=(ROOT/'character3d/painted-film.template.html').read_text()
values={'__FILM__':json.dumps({'views':views,'cycle':cycle},separators=(',',':')),
        '__DEPTH__':embedded('art/walking/maziss-depth-atlas.png'),
        '__SIDE__':embedded('art/walking/maziss-side-atlas.png'),
        '__ROOM__':embedded('art/walking/apartment-background.png')}
for key,value in values.items():template=template.replace(key,value)
target=ROOT/'visual-preview/maziss-painted-rendered.html';target.write_text(template);target.chmod(0o644)
report={'source_html_sha256':hashlib.sha256(HTML.read_bytes()).hexdigest(),
        'capture_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'template_sha256':hashlib.sha256((ROOT/'character3d/painted-film.template.html').read_bytes()).hexdigest(),
        'frames':N*len(views),'angles':len(views),'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
        'bytes':target.stat().st_size}
(OUT/'rendered-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
print('Created',target.name,target.stat().st_size,'bytes',flush=True)
