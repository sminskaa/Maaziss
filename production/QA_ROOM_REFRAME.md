# QA-015: rectangular room-reference proposal

19 October 2026. **Suitable for owner review as a separate image-assisted 16:9
reframing proposal. This is not approval of a replacement background, an exact
pixel crop, a three-dimensional room model or a playable room.**

## Actual image inspection

QA opened the actual `build/checks/room-cutaway/room-reframed-source.png` and both
desktop/mobile browser captures of `visual-preview/maziss-room-16x9.html`, then
compared their appearance with the earlier `art/walking/apartment-background.png`.
The user's inline cutaway image has no local source file available to this QA
worker. QA therefore makes no exact-pixel comparison or preservation claim about
that input, and cannot attribute every difference to either the input or generation.

The delivered view is fully rectangular, with no white surrounding canvas, pointed
lower-floor extension or visible character. The red patched sofa, coats and wall
sink, notice board, green door with circular grille, turquoise city window, books,
containers, repair desk, green lamp and stool are readily recognizable. Amber
interior light, cooler turquoise window light, purple floor shadows, dark drawn
contours and painted timber/plaster remain consistent with the established style.
Door and window frames remain mostly straight. The image reads clearly as a
painted cartoon room rather than a neutral blockout or photorealistic render.

Relative to the earlier wide background, this view has a more elevated perspective,
a broader exposed foreground floor, visible upper beams and no large dark bottle
silhouettes framing the bottom corners. The sofa and desk are framed differently;
outer furniture/side-wall portions meet the left/right edges. The doorway rug,
sill details, papers and small props also differ from that earlier image. These
observations must not be summarized as an unchanged original or a literal crop.
The page correctly calls the result a separate image-assisted proposal and says
walkable floor, furniture obstacles and character scale still need alignment.

No Maziss is present, as requested for the room-only reference. Consequently this
image cannot by itself establish his scale, furniture occlusion, foot contact,
animated lighting coherence or compatibility with a final shared 3D camera.

## Delivery and retained-source evidence

The generated source PNG is 1672×941. The actual embedded/downloadable JPEG is
1600×900, exactly 16:9, and 202,626 bytes. QA clicked the native download link in
offline Chromium, saved the resulting `maziss-room-16x9.jpg`, decoded it as JPEG
and verified its bytes exactly match the retained delivery JPEG. This validates
the local page/download implementation, not the host chat's separate file service.

The self-contained HTML is 541,572 bytes, SHA-256
`fad7f9afcbcdac538fa2e4d93e3d41aa6cef2bc861e2e5d697486abbedcaff7d`.
At desktop 1280×1000 and mobile 390×844 with browser networking disabled, the
embedded native image decoded without scripts, external requests, page errors or
horizontal overflow. QA opened both actual screenshots; the image, explanatory
text and download control remain visible. No live WebGL or application JavaScript
is required. Internal Chromium success cannot guarantee the host panel displays it.

The existing model, motion data, approved room composition, original clean-room PNG
and both character atlases still match the retained hashes from QA-014. This room
proposal does not modify those files. The reused source/delivery check is
`tests/browser_style_match.py`; private browser results, screenshots and the actual
download check are under `build/checks/room-cutaway/qa/`. Owner visual approval and
later scene integration remain separate decisions.
