# Character lighting and room-scale checkpoint

19 October 2026. Owner prefers the supplied-model reconstruction over earlier
sprite projection, while requesting closer colours, shadows and cartoon style.
The original room remains the reference. A subtle room redesign is held while
the owner explores supplying a modeled room; no approved art is replaced.

## Saved owner deliverable

`visual-preview/maziss-room-reference.html` is a 642,530-byte self-contained page
showing the existing character-free room at 1932×814 with a JPG download button.
The actual image decoded and downloaded in offline Chromium. Independent QA also
opened desktop/mobile captures with no errors, network requests or overflow.
The original PNG is `art/walking/apartment-background.png`, unchanged.

## Current bounded work

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
