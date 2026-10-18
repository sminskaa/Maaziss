#!/usr/bin/env python3
"""Create an offline review page with embedded artwork and actual UI screenshots."""
from pathlib import Path
import base64
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def embedded_jpeg(source: str, target: Path) -> str:
    # Delivery encoding only: keep the original image and its dimensions unchanged.
    with Image.open(ROOT / source) as image:
        image.convert("RGB").save(target, quality=85, optimize=True)
    target.chmod(0o644)
    return 'data:image/jpeg;base64,' + base64.b64encode(target.read_bytes()).decode('ascii')


def main() -> None:
    preview = ROOT / 'visual-preview'
    preview.mkdir(exist_ok=True)
    preview.chmod(0o755)
    art = embedded_jpeg('art/proposals/apartment-cartoon-v2.png', preview / 'apartment-cartoon.jpg')
    screenshot = embedded_jpeg('build/checks/controls-inventory.png', preview / 'game-controls.jpg')
    target = preview / 'maziss-style-review.html'
    target.write_text('''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Maziss — cartoon art and controls review</title>
<style>body{margin:0;padding:24px;background:#172128;color:#f5e8ce;font:18px system-ui}main{max-width:1280px;margin:auto}img{display:block;width:100%;height:auto;border:1px solid #aa9161}p{line-height:1.5;max-width:950px}h2{margin-top:48px}a{color:#f1c778}nav{display:flex;gap:24px;flex-wrap:wrap}.note{color:#bfcac6}</style>
<main><h1>Maziss — art and controls review</h1>
<nav><a href="#art">Revised art with Maziss</a><a href="#controls">Implemented controls</a></nav>
<section id="art"><h2>1. Revised apartment and Maziss</h2>
<p>Revision 2: straighter door and window frames, with Maziss now visible. The painted texture, colours, lighting, sofa and workshop details are retained.</p>
<p class="note">Art proposal for your feedback. This composition includes a proposed design for Maziss; it is not yet installed as separate background and animated character assets in the playable game.</p>
<img alt="Revised art with Maziss: a slumped burgundy sofa, crooked green door, skewed window, cluttered repair desk and warm wooden floor." src="''' + art + '''"></section>
<section id="controls"><h2>2. Actual prototype with the new controls</h2>
<p>The game now has the nine verbs, graphical inventory, right-click examination, and basic click-to-walk movement. This screenshot still uses the older placeholder background and character.</p>
<img alt="Actual playable room with nine verb buttons and graphical metal-strip and leaflet inventory icons." src="''' + screenshot + '''">
<p>Give · Pick up · Use · Look at · Talk to · Pull · Push · Close · Open</p>
<p class="note">There are no NPCs in the first room yet. Walking currently moves the placeholder sprite; the walking animation is still to come. No external files, account, scripts or network connection are required to view this page.</p>
</section></main></html>''', encoding='utf-8')
    target.chmod(0o644)
    # A stable, simple entry point alongside the named review file.
    entry = preview / 'index.html'
    entry.write_bytes(target.read_bytes())
    entry.chmod(0o644)
    revision = preview / 'maziss-art-revision-2.html'
    revision.write_bytes(target.read_bytes())
    revision.chmod(0o644)
    print(f'Created {target.relative_to(ROOT)} ({target.stat().st_size:,} bytes)')


if __name__ == '__main__':
    main()
