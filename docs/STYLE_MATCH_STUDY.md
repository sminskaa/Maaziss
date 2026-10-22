# Character lighting and room-scale checkpoint

19 October 2026. Owner prefers the supplied-model reconstruction over earlier
sprite projection, while requesting closer colours, shadows and cartoon style.
The original room remains the reference. A subtle room redesign is held while
the owner explores supplying a modeled room; no approved art is replaced.

Resumed after the allowance reset. The captured lighting study is complete:
three idle views and 24 actual walking frames, rendered in 147.66 seconds on CPU.
`visual-preview/maziss-style-match.html` is 633,890 bytes and contains the original,
previous and proposed treatments, a constant-depth walking pass and three separate
perspective-scale placements. Art and QA opened actual images and five video
moments; final scoped recommendations are recorded in their reports. Offline
desktop/mobile playback and retained-source hashes passed. This is a Blender look
target; the equivalent Godot shader and real room shadows are not implemented.

The owner then supplied a dimensional cutaway **image**, not a room mesh, and
clarified that the desired viewport is 16:9. A separate image-assisted reframing
proposal removes the white surround and lower floor point. It is available at
`visual-preview/maziss-room-16x9.html` with a 1600×900 JPG download. Its source is
retained privately in `build/checks/room-cutaway/`; original approved art is unchanged.
The image-generation edit is not an exact pixel crop or a reconstructed 3D room.
Do not reuse the old room's floor coordinates or horizon without recalibrating to
this new view. See the room Art/QA reports for the reviewed scope.

The final room HTML is 541,572 bytes, with a 202,626-byte 1600×900 JPG. Art and QA
opened the actual output and prior room references. QA also clicked the native
download, saved and decoded the JPG offline, and inspected desktop/mobile captures
without scripts, network requests, page errors or horizontal overflow. The new
framing preserves recognizable furniture and palette, but changes some props,
floorboard detail and edge framing. This is a separate review proposal; the new
view has not received character-scale, obstacle or navigation validation.

Room review reports: `production/ART_ROOM_REFRAME.md` and
`production/QA_ROOM_REFRAME.md`. Repackage the retained image-generated output with
`python3 tools/build_room_reference_review.py`. Its default input is the private
`build/checks/room-cutaway/room-reframed-source.png`; it only encodes the already
reframed result, not an automatic crop of arbitrary images.

## Saved owner deliverable

`visual-preview/maziss-room-reference.html` is a 642,530-byte self-contained page
showing the existing character-free room at 1932×814 with a JPG download button.
The actual image decoded and downloaded in offline Chromium. Independent QA also
opened desktop/mobile captures with no errors, network requests or overflow.
The original PNG is `art/walking/apartment-background.png`, unchanged.

## Historical allowance-saving checkpoint

- ART-008 `/root/art_style_match`: actual Cycles CPU toon shading, warm upper-left
  key, cooler window fill and brown Freestyle outlines. The fixed camera and
  room lights stay in place; only the character's presentation root rotates.
  Three idle views plus a 24-frame side walk are being captured privately.
- QA-014 `/root/style_qa`: opens actual references, renders, composites and offline
  browser screenshots. Initial actual front/profile/oblique and four-phase views
  show a clearer warm/cool palette, coherent garments and a single modeled face.
  Final full-cycle scene-scale review is pending at this checkpoint.
- Coordinator: `tools/build_style_match_review.py` packages actual output in
  `visual-preview/maziss-style-match.html`, with original/previous/new comparisons,
  a constant-depth walking pass and three depth-scale placements.

The owner reports only 10% allowance remaining. Finish the already running capture,
package and review if possible, then save. Do not start new reconstruction,
room generation, research, broad tests or another modeling iteration this turn.

That pause ended with the owner's explicit reset/resume instruction. The final
findings above supersede the historical pending statuses in this section.

## Perspective contract

Preserve the model's fixed two-metre authoring height and body proportions. The
approved scene is initially calibrated at original-image foot point (1125,698)
and approximately 596 pixels of standing character height. A provisional horizon
at Y=130 controls scale linearly with floor depth. This is a 2.5D placement proposal,
not a recovered physical camera or a final navigation solution.

The same-depth walk uses identical world-to-image scale in all frames. Near/back
placements must compare with the original door, sofa and desk. Do not scale boots,
legs or torso separately or normalize each frame's changing pixel bounds. The
future modeled room should provide one shared camera, floor and real shadows.

## Reproduce and resume

```sh
blender -b --python tools/render_character_style.py -- --walk-frames 24
python3 tools/build_style_match_review.py
python3 tests/browser_style_match.py --html visual-preview/maziss-style-match.html
```

Retained source files are the final supplied rig `.blend`/`.glb` and motion in
`build/checks/supplied-character/`. New actual captures are in
`build/checks/style-match/character/`, composites/manifests in `delivery/`, and
independent browser/image evidence in `qa/`. All generated files remain ignored.
Read `production/ART_STYLE_MATCH.md` and `production/QA_STYLE_MATCH.md` for the
latest executed findings; do not infer completion from this preliminary checkpoint.

For future characters, owner-supplied 3D is helpful but not invariably required.
This specific result depended substantially on the supplied sculpt. A single 2D
image does not determine unseen surfaces, clothing construction or rig-ready
topology; front/profile/back references improve a geometry-first attempt. Do not
claim equivalent automatic quality from one drawing has already been demonstrated.
