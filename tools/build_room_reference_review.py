#!/usr/bin/env python3
"""Package an already reframed near-16:9 artwork in a small offline review.

Creative editing happens upstream. This only encodes the supplied result into
an exact 1600x900 JPG and readable HTML with a native image-download link.
"""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]

def main():
    from PIL import Image
    args=argparse.ArgumentParser(description=__doc__)
    args.add_argument('--input',type=Path,default=ROOT/'build/checks/room-cutaway/room-reframed-source.png')
    args.add_argument('--output',type=Path,default=ROOT/'visual-preview/maziss-room-16x9.html')
    opts=args.parse_args()
    source=opts.input.resolve();out=ROOT/'build/checks/room-cutaway';out.mkdir(parents=True,exist_ok=True)
    with Image.open(source) as image:width,height=image.size
    assert abs(width/height-16/9)<.02,'Reframe the artwork before packaging; this helper does not crop it'
    jpg=out/'maziss-room-16x9.jpg'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf','scale=1600:900','-frames:v','1','-q:v','8',str(jpg)],check=True)
    uri='data:image/jpeg;base64,'+base64.b64encode(jpg.read_bytes()).decode()
    html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Maziss — room in 16:9</title><style>body{margin:0;background:#20282e;color:#f2e8d8;font:17px/1.5 system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:20px}img{display:block;width:100%;height:auto;border-radius:6px}a{display:inline-block;color:#ffe4a3;padding:14px 0}p{max-width:950px}</style></head><body><main>
<h1>Room reference — 16:9</h1><p>Your cutaway-room image reframed as a rectangular game view: white surround and pointed lower floor removed. No character is included.</p>
<img id="room" src="__IMAGE__" width="1600" height="900" alt="Painted apartment with red sofa, green door, cyan city window, repair desk and a straight rectangular floor view">
<a id="download" href="__IMAGE__" download="maziss-room-16x9.jpg">Download the room image — 1600 × 900 JPG</a>
<p>This is a separate image-assisted reframing proposal. The supplied image and earlier approved artwork are retained. The artwork provides a depth reference; walkable floor geometry, furniture obstacles and character scale still need to be aligned beneath it.</p>
</main></body></html>'''.replace('__IMAGE__',uri)
    opts.output.parent.mkdir(parents=True,exist_ok=True);opts.output.write_text(html);opts.output.chmod(0o644);opts.output.parent.chmod(0o755)
    assert opts.output.stat().st_size<1_000_000,'Review exceeds compact delivery target'
    report={'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceSize':[width,height],
            'downloadSize':[1600,900],'jpgBytes':jpg.stat().st_size,'htmlBytes':opts.output.stat().st_size,
            'htmlSHA256':hashlib.sha256(opts.output.read_bytes()).hexdigest(),
            'method':'Imagegen reframing followed by JPG encoding; not a literal pixel crop or a3Dmesh'}
    (out/'delivery-manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
