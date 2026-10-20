#!/usr/bin/env python3
"""Build an offline, self-contained visual direction board; no game assets changed."""
from pathlib import Path
from PIL import Image
import base64, io, json
ROOT = Path(__file__).resolve().parents[1]
def data(image, fmt='JPEG'):
    out=io.BytesIO()
    image.save(out, format=fmt, **({'quality':83} if fmt=='JPEG' else {}))
    return 'data:image/'+('jpeg' if fmt=='JPEG' else 'png')+';base64,'+base64.b64encode(out.getvalue()).decode()
def main():
    room=Image.open(ROOT/'build/checks/room-cutaway/room-reframed-source.png').convert('RGB');room.thumbnail((1280,720))
    original=Image.open(ROOT/'art/proposals/apartment-cartoon-v2.png').convert('RGB');original.thumbnail((1100,600))
    background=Image.open(ROOT/'art/walking/apartment-background.png').convert('RGB');background.thumbnail((1280,720))
    # Existing painted reference only. This is not a new character/animation proposal.
    atlas=Image.open(ROOT/'art/walking/maziss-depth-atlas.png')
    actor=atlas.crop((0,0,atlas.width//4,atlas.height//2));actor=actor.crop(actor.getbbox());actor.thumbnail((170,320))
    assets={'room':data(room),'original':data(original),'background':data(background),'actor':data(actor,'PNG')}
    html=(ROOT/'tools/director_board/index.html').read_text().replace('__ASSETS__',json.dumps(assets)).replace('__SCRIPT__',(ROOT/'tools/director_board/director.js').read_text())
    output=ROOT/'visual-preview/maziss-director.html';output.write_text(html);output.chmod(0o644)
    assert output.stat().st_size<1_000_000
    print(f'{output}: {output.stat().st_size:,} bytes')
if __name__=='__main__':main()
