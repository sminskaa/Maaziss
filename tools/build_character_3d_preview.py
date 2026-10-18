#!/usr/bin/env python3
"""Embed procedural model and private motion in an offline local HTML review."""
from pathlib import Path
import hashlib,json,gzip,base64
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/checks/character3d';PREVIEW=ROOT/'visual-preview';PREVIEW.mkdir(exist_ok=True)
paths=['tools/build_character_3d.py','tools/character3d_body.py','tools/build_character_3d_preview.py','character3d/preview.js','character3d/index.template.html','character3d/vendor/three.min.js']
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths};hashes['private/motion/fbx-motion.json']=hashlib.sha256((ROOT/'private/motion/fbx-motion.json').read_bytes()).hexdigest();hashes['build/checks/character3d/model-private.json']=hashlib.sha256((OUT/'model-private.json').read_bytes()).hexdigest();identity=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
html=(ROOT/'character3d/index.template.html').read_text().replace('__THREE_JS__',(ROOT/'character3d/vendor/three.min.js').read_text()).replace('__PREVIEW_JS__',(ROOT/'character3d/preview.js').read_text()).replace('__MODEL_DATA__',base64.b64encode(gzip.compress((OUT/'model-private.json').read_bytes(),mtime=0)).decode()).replace('<head>','<head><meta name="maziss-build" content="'+identity+'">',1)
target=PREVIEW/'maziss-3d-study.html';target.write_text(html);target.chmod(0o644);PREVIEW.chmod(0o755)
(OUT/'build-manifest.json').write_text(json.dumps({'built_at':datetime.now(timezone.utc).isoformat(),'build':identity,'source_sha256':hashes,'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2)+'\n');print('Built',target.name,'bytes',target.stat().st_size,'identity',identity[:12])
