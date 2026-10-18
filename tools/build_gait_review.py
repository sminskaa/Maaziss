#!/usr/bin/env python3
"""Package actual final browser gait captures into an offline HTML pose review."""
from pathlib import Path
from io import BytesIO
import base64
import hashlib
import json
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

def main():
    evidence=ROOT/'build/checks/walking-revision'
    results=json.loads((evidence/'browser-results.json').read_text())
    assert results['html_sha256']==hashlib.sha256((ROOT/'visual-preview/maziss-walking-v3.html').read_bytes()).hexdigest(), 'Run QA on current HTML before packaging pose evidence'
    cards=[]
    for i,path in enumerate(sorted(evidence.glob('gait-phase-*.png')),1):
        encoded=BytesIO()
        with Image.open(path) as image:image.convert('RGB').save(encoded,format='WEBP',quality=85,method=6)
        data=base64.b64encode(encoded.getvalue()).decode('ascii')
        cards.append(f'<figure><img alt="Actual rendered walking pose {i}" src="data:image/webp;base64,{data}"><figcaption>Pose {i}</figcaption></figure>')
    assert cards, 'Missing rendered phase captures'
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Maziss walking poses</title><style>body{font:18px/1.5 system-ui;background:#18232b;color:#f5e7c9;margin:24px}main{max-width:1400px;margin:auto}section{display:flex;flex-wrap:wrap;gap:12px}figure{margin:0;background:#24333b;padding:8px;border-radius:6px}img{display:block;width:180px;max-width:100%;height:auto}figcaption{padding:8px}p{max-width:900px}</style><main><h1>Revised walking: actual rendered poses</h1><p>These consecutive samples come from the revised interactive example. Compare the knees and boots as the same legs move from behind to ahead. Use the walking example to judge motion; these static samples do not establish naturalness.</p><section>'''+''.join(cards)+'</section></main></html>'
    target=ROOT/'visual-preview/maziss-walking-poses.html'
    target.write_text(page);target.chmod(0o644)
    print(f'Created {len(cards)}-pose HTML review ({target.stat().st_size:,} bytes).')

if __name__=='__main__':main()
