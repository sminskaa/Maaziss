#!/usr/bin/env python3
"""Pack the walking study into a portable, offline HTML file with embedded artwork."""
from pathlib import Path
from datetime import datetime, timezone
from io import BytesIO
import argparse
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
        image.convert('RGBA').save(out, format='WEBP', lossless=True, method=6)
        mime='image/webp'
    else:
        image.convert('RGB').save(out, format='WEBP', quality=84, method=6)
        mime='image/webp'
    return f'data:{mime};base64,'+base64.b64encode(out.getvalue()).decode('ascii')


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--motion',type=Path,default=ROOT/'private/motion/fbx-motion.json')
    args=parser.parse_args()
    if not args.motion.is_file():
        parser.error('Private FBX motion is missing. Run tools/extract_fbx_walk.py with the owner-provided animation first; see docs/WALKING_DEMO.md.')
    room = json.loads((ROOT/'walking/room.json').read_text())
    sprites=json.loads((ROOT/'walking/original-sprites.json').read_text())
    replacements = {
        '__ROOM_DATA__':json.dumps(room,separators=(',',':')),
        '__FBX_MOTION_DATA__':args.motion.read_text(),
        '__RIG_DATA__':json.dumps(sprites,separators=(',',':')),
        '__BACKGROUND_URL__':embedded_image(ART/'apartment-background.png',False),
        '__RIG_ATLAS_URL__':embedded_image(ART/'maziss-side-atlas.png',True),
        '__DEPTH_ATLAS_URL__':embedded_image(ART/'maziss-depth-atlas.png',True),
        '__CLOTHING_ATLAS_URL__':embedded_image(ART/'maziss-clothing-repair.png',True),
        '__NAVIGATION_JS__':(ROOT/'walking/navigation.js').read_text(),
        '__GAIT_JS__':(ROOT/'walking/image-gait.js').read_text(),
        '__DEMO_JS__':(ROOT/'walking/demo.js').read_text(),
        '__FBX_GAIT_JS__':(ROOT/'walking/fbx-gait.js').read_text(),
        '__CHARACTER_JS__':(ROOT/'walking/character-renderer.js').read_text(),
    }
    html = (ROOT/'walking/index.template.html').read_text()
    for key,value in replacements.items():
        if html.count(key)!=1:
            raise ValueError(f'Expected exactly one {key} placeholder')
        html=html.replace(key,value)
    source_paths=['walking/room.json','walking/navigation.js','walking/image-gait.js','walking/fbx-gait.js','walking/character-renderer.js','walking/demo.js',
                  'walking/index.template.html','tools/build_walking_demo.py',
                  'art/walking/apartment-background.png','art/walking/maziss-side-atlas.png',
                  'art/walking/maziss-depth-atlas.png','art/walking/maziss-clothing-repair.png', 'walking/original-sprites.json']
    hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in source_paths}
    hashes['private/motion/fbx-motion.json']=hashlib.sha256(args.motion.read_bytes()).hexdigest()
    identity=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
    html=html.replace('<head>','<head>\n<meta name="maziss-build" content="'+identity+'">',1)
    target=ROOT/'visual-preview/maziss-walking.html'
    target.parent.mkdir(exist_ok=True)
    target.parent.chmod(0o755)
    target.write_text(html)
    target.chmod(0o644)
    revision=target.parent/'maziss-walking-v8.html'
    revision.write_bytes(target.read_bytes())
    revision.chmod(0o644)
    evidence=ROOT/'build/checks/clothing-walk'
    evidence.mkdir(parents=True,exist_ok=True)
    (evidence/'build-manifest.json').write_text(json.dumps({'built_at':datetime.now(timezone.utc).isoformat(),'build':identity,'source_sha256':hashes,'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size},indent=2)+'\n')
    print(f'Created {target.relative_to(ROOT)} ({target.stat().st_size:,} bytes); build {identity[:12]}')


if __name__=='__main__':
    main()
