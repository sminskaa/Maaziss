#!/usr/bin/env python3
"""Embed procedural model and private motion in an offline local HTML review."""
from pathlib import Path
import hashlib,json,gzip,base64
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/checks/painted-character';PREVIEW=ROOT/'visual-preview';PREVIEW.mkdir(exist_ok=True)
paths=['tools/build_character_3d.py','tools/character3d_body.py','tools/character3d_fit.py','tools/character3d_textures.py','tools/build_character_3d_preview.py','character3d/preview.js','character3d/painted.template.html','character3d/vendor/three.min.js','art/walking/maziss-side-atlas.png','art/walking/maziss-depth-atlas.png','art/walking/maziss-clean-garment-reference.png','art/walking/apartment-background.png']
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths};hashes['private/motion/fbx-motion.json']=hashlib.sha256((ROOT/'private/motion/fbx-motion.json').read_bytes()).hexdigest();hashes['build/checks/painted-character/model-private.json']=hashlib.sha256((OUT/'model-private.json').read_bytes()).hexdigest();identity=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
def embedded(path):return 'data:image/png;base64,'+base64.b64encode((ROOT/path).read_bytes()).decode()
sources={key:embedded(path) for key,path in [('side','art/walking/maziss-side-atlas.png'),('depth','art/walking/maziss-depth-atlas.png'),('garment','art/walking/maziss-clean-garment-reference.png')]}
html=(ROOT/'character3d/painted.template.html').read_text().replace('__THREE_JS__',(ROOT/'character3d/vendor/three.min.js').read_text()).replace('__PREVIEW_JS__',(ROOT/'character3d/preview.js').read_text()).replace('__MODEL_DATA__',base64.b64encode(gzip.compress((OUT/'model-private.json').read_bytes(),mtime=0)).decode()).replace('__PAINT_SOURCES__',json.dumps(sources,separators=(',',':'))).replace('__ROOM_IMAGE__',embedded('art/walking/apartment-background.png')).replace('<head>','<head><meta name="maziss-build" content="'+identity+'">',1)
target=PREVIEW/'maziss-painted-3d.html';target.write_text(html);target.chmod(0o644);PREVIEW.chmod(0o755)
(OUT/'build-manifest.json').write_text(json.dumps({'built_at':datetime.now(timezone.utc).isoformat(),'build':identity,'source_sha256':hashes,'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2)+'\n');print('Built',target.name,'bytes',target.stat().st_size,'identity',identity[:12])
