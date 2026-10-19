#!/usr/bin/env python3
"""Package actual stool renders and a GLB download into a compact offline page."""
from pathlib import Path
import base64
import hashlib
import io
import json

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'build/checks/stool-study'


def data(raw, mime):
    return 'data:'+mime+';base64,'+base64.b64encode(raw).decode()


def picture(path, width=640):
    with Image.open(path) as image:
        image = image.convert('RGB')
        if image.width > width:
            image.thumbnail((width, width), Image.Resampling.LANCZOS)
        stream = io.BytesIO()
        image.save(stream, 'JPEG', quality=86, optimize=True)
    return data(stream.getvalue(), 'image/jpeg')


def main():
    manifest = json.loads((OUT/'model-manifest.json').read_text())
    assert len(manifest['views']) == 3
    for view in manifest['views']:
        assert hashlib.sha256((OUT/(view['name']+'.png')).read_bytes()).hexdigest() == view['imageSHA256']
    model = (OUT/'maziss-stool.glb').read_bytes()
    assert hashlib.sha256(model).hexdigest() == manifest['modelSHA256']
    source = ROOT/'build/checks/room-cutaway/room-reframed-source.png'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == manifest['sourceRoomSHA256']
    with Image.open(source) as image:
        image.crop(tuple(manifest['sourceCrop'])).save(OUT/'stool-reference.png')
    labels = {
        'room-angle': 'Reference-view estimate · 23° above the floor',
        'rear-angle': 'Rear view · complete rear legs and bracing',
        'underside': 'Underside · solid seat and leg attachment areas',
    }
    cards = ''.join('<figure><img src="'+picture(OUT/(v['name']+'.png'))+'" width="640" height="640" alt="Actual Blender stool render: '+v['name']+'"><figcaption>'+labels[v['name']]+'</figcaption></figure>' for v in manifest['views'])
    html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Maziss — first complete stool model</title><style>
*{box-sizing:border-box}body{margin:0;background:#24212c;color:#f1e3cc;font:17px/1.5 system-ui,sans-serif}main{max-width:1060px;margin:auto;padding:20px}h1{line-height:1.2}a{color:#f2c97f}figure{margin:0;background:#342d38;border:1px solid #78635b;border-radius:7px;overflow:hidden}figure img{display:block;width:100%;height:auto}figcaption{padding:10px 14px}.views{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.reference{display:grid;grid-template-columns:180px minmax(0,1fr);gap:20px;align-items:center;margin:20px 0}.reference img{width:145px;height:175px}details{margin-top:20px}details img{width:100%;height:auto}.download{display:inline-block;padding:9px 16px;background:#5a4738;border:1px solid #b19067;border-radius:6px}small{color:#d2bfa9}@media(max-width:650px){.views{grid-template-columns:1fr}.reference{grid-template-columns:1fr}}
</style><main><h1>First complete stool model</h1>
<p>A small geometry study based on the stool beside Maziss’s desk. These are actual renders of one complete 3D model: a rounded solid seat, four splayed legs and a closed footrest ring.</p>
<section class="reference"><figure><img src="__REFERENCE__" width="145" height="175" alt="Unchanged crop of the painted stool beside the desk"><figcaption>Original room detail</figcaption></figure><div><p>Compare the seat thickness, leg spread, bracing and overall proportions with the three model views below.</p><p><strong>Preliminary colour only.</strong> Painted grain, wear, room lighting and precise camera matching belong to the next pass. Model dimensions are estimates.</p><a class="download" download="maziss-stool.glb" href="__MODEL__">Download the 3D stool (.glb)</a></div></section>
<section class="views">__CARDS__</section>
<details><summary>Show the unchanged room reference</summary><img src="__ROOM__" width="900" height="507" alt="The unchanged room with its original painted stool beside the desk"></details>
<p><small>The room image is unchanged. This review does not replace the painted stool, reconstruct its background or animate Maziss. The model is saved separately in Blender and GLB formats. Views share the same geometry and scale; the underside view omits the studio floor to expose construction.</small></p></main></html>'''
    html = html.replace('__REFERENCE__', picture(OUT/'stool-reference.png'))
    html = html.replace('__MODEL__', data(model, 'model/gltf-binary'))
    html = html.replace('__CARDS__', cards).replace('__ROOM__', picture(source,900))
    target = ROOT/'visual-preview/maziss-stool-study.html'
    target.parent.mkdir(exist_ok=True)
    target.write_text(html)
    target.chmod(0o644)
    target.parent.chmod(0o755)
    for name in ('maziss-stool.blend','maziss-stool.glb'):
        (OUT/name).chmod(0o644)
    result = {'htmlBytes':target.stat().st_size,
              'htmlSHA256':hashlib.sha256(target.read_bytes()).hexdigest(),
              'modelSHA256':manifest['modelSHA256'],
              'views':manifest['views'],'scope':manifest['scope']}
    assert result['htmlBytes'] < 1_000_000
    (OUT/'delivery-manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
