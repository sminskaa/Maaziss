#!/usr/bin/env python3
"""Pack the walking study into a portable, offline HTML file with embedded artwork."""
from pathlib import Path
from datetime import datetime, timezone
from io import BytesIO
import base64
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art/walking'


def embedded_image(path: Path, transparent: bool) -> str:
    image = Image.open(path)
    out = BytesIO()
    if transparent:
        image.convert('RGBA').save(out, format='WEBP', quality=88, method=6)
        mime='image/webp'
    else:
        image.convert('RGB').save(out, format='WEBP', quality=84, method=6)
        mime='image/webp'
    return f'data:{mime};base64,'+base64.b64encode(out.getvalue()).decode('ascii')


def main() -> None:
    room = json.loads((ROOT/'walking/room.json').read_text())
    sprites=json.loads((ROOT/'walking/original-sprites.json').read_text())
    replacements = {
        '__ROOM_DATA__':json.dumps(room,separators=(',',':')),
        '__REFERENCE_DATA__':(ROOT/'walking/reference-motion.json').read_text(),
        '__RIG_DATA__':json.dumps(sprites,separators=(',',':')),
        '__BACKGROUND_URL__':embedded_image(ART/'apartment-background.png',False),
        '__RIG_ATLAS_URL__':embedded_image(ART/'maziss-side-atlas.png',True),
        '__DEPTH_ATLAS_URL__':embedded_image(ART/'maziss-depth-atlas.png',True),
        '__NAVIGATION_JS__':(ROOT/'walking/navigation.js').read_text(),
        '__GAIT_JS__':(ROOT/'walking/reference-gait.js').read_text(),
        '__DEMO_JS__':(ROOT/'walking/demo.js').read_text(),
    }
    html = (ROOT/'walking/index.template.html').read_text()
    for key,value in replacements.items():
        if html.count(key)!=1:
            raise ValueError(f'Expected exactly one {key} placeholder')
        html=html.replace(key,value)
    source_paths=['walking/room.json','walking/navigation.js','walking/reference-gait.js','walking/reference-motion.json','walking/demo.js',
                  'walking/index.template.html','tools/build_walking_demo.py',
                  'art/walking/apartment-background.png','art/walking/maziss-side-atlas.png',
                  'art/walking/maziss-depth-atlas.png', 'walking/original-sprites.json']
    hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in source_paths}
    identity=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
    html=html.replace('<head>','<head>\n<meta name="maziss-build" content="'+identity+'">',1)
    target=ROOT/'visual-preview/maziss-walking.html'
    target.parent.mkdir(exist_ok=True)
    target.parent.chmod(0o755)
    target.write_text(html)
    target.chmod(0o644)
    revision=target.parent/'maziss-walking-v5.html'
    revision.write_bytes(target.read_bytes())
    revision.chmod(0o644)
    evidence=ROOT/'build/checks/reference-walk'
    evidence.mkdir(parents=True,exist_ok=True)
    (evidence/'build-manifest.json').write_text(json.dumps({'built_at':datetime.now(timezone.utc).isoformat(),'build':identity,'source_sha256':hashes,'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size},indent=2)+'\n')
    print(f'Created {target.relative_to(ROOT)} ({target.stat().st_size:,} bytes); build {identity[:12]}')


if __name__=='__main__':
    main()
