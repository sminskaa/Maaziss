# Walking study — clothing continuity revision 8

Open `visual-preview/maziss-walking-v8.html`, or the latest `maziss-walking.html`.
HTML works in the owner's panel; embedded chat pictures do not. This remains a
separate motion study, not the playable Godot apartment.

## Motion source

Blender 4.3.2 imported three supplied FBX walks. The selected ordinary walking loop
uses frames 234–269 of `02-walkforward.fbx`, at 30 fps: a 1.166667-second cycle.
Both legs and both arms were extracted independently. The setup T-pose is excluded
from walking. See `production/FBX_MOTION_REVIEW.md` for actual import observations,
loop fitting, inferred stride and reference limitations.

`walking/fbx-gait.js` interpolates those private joint trajectories and retargets
normalized bone directions onto fixed original-art leg lengths. It uses
`image-gait.js` for route phase and start/stop state only; the previous authored
image poses are not the source of this walking cycle. Idle is separately authored,
with relaxed knees and neutral boots. Foot pitch comes from the walk only while
moving. Modest arm and torso motion accompany the legs.

## Rendering corrections

Revision 7's cutout approach left holes when arms uncovered the torso or bag.
Revision 8 adds complete painted jacket backing and a separate intact satchel,
while retaining original opaque collar/torso detail, head/face and arm art. Neither
jacket nor bag has an arm-shaped or hand-shaped transparent cutout. The bag is
attached rigidly to the torso, not fragmented across moving arm masks. The original
room and original character PNGs remain unchanged. New repair art/provenance is in
`art/walking/CLOTHING_REPAIR.md`.

Depth views now use distinct observer-left/right trouser and boot drawings.
Previously both shoes used observer-left art, even when programmed rotation was
zero. Previously the trouser cuff was displaced from the skeletal ankle to match
a fixed shoe height; that reached about 14–15 pixels at 440-pixel character height.
Both trouser meshes now terminate at the actual animated cuffs. Boot projection
adapts below that attachment, rather than moving the cloth end independently.
Real perspective shortening of a bent leg remains; the FBX gait is unchanged.

The continuous trouser meshes and camera-depth arm ordering are retained. The
pose-review HTML also displays actual separate runtime drawing layers. These are
2D painted assets, not individually modeled 3D garments or cloth physics.

## Review controls

- Click floor to walk; another click changes the route. Existing obstacle routing
  and root clearance are retained.
- Left, Right, Toward camera and Away from camera show an in-place cycle.
- The live close-up uses the same character renderer at a larger scale.
- Stand still exits the study/route and lets the transition to idle finish. Reset
  restores the initial resting pose.
- Pause freezes motion. Next frame advances 1/30 second; half/quarter playback helps
  examine knees, shoe roll and the loop boundary.
- Footsteps and walkable-area overlays are optional review aids.

`visual-preview/maziss-walking-v8-poses.html` contains actual rendered phase captures.
Use moving playback as well as still poses to judge the result.

## Validation and limits

Frozen build `5c3d7d3fcda2` passed 44 focused checks, covering 100 whole-character
poses and 80 isolated item renders. This is scoped technical evidence, not creative
acceptance.

The source/output identity is recorded in
`build/checks/clothing-walk/build-manifest.json`. Independent actual-pixel,
per-garment and attachment results are in `production/QA_CLOTHING_WALK.md`.
Revision 7's component and geometric checks missed interior clothing gaps and
same-handed shoe artwork. Revision 8 checks isolated garment layers as well as
whole characters; technical checks still do not establish owner acceptance.

This is a 2D retarget of a 3D reference. Front/back foot roll and directional drawing
changes during turns remain approximations. Fixed bone lengths and smooth joint
curves do not guarantee world-space planted feet: some sliding can remain during
travel and transitions. The room checks navigation-root clearance, not full-body
3D collision or foreground occlusion. Linux Chromium checks do not establish a
native Windows run. Main Godot graphics and animation remain unchanged; accepted
art integration is a later increment.

## Reproduction and private inputs

```sh
blender -b --python tools/extract_fbx_walk.py -- --intake private/motion/fbx-intake.json
python3 tools/build_walking_demo.py
python3 tests/browser_clothing_walk.py
python3 tools/capture_fbx_walk.py
```

Extraction requires the retained owner-supplied FBX and ignored intake manifest.
The builder requires the extracted `private/motion/fbx-motion.json` (or `--motion`
path), Python and Pillow. Browser tools use Playwright and Chromium; the clothing
test also uses NumPy and SciPy (already present in this workspace). A public
checkout alone cannot reproduce this private-input study. Raw FBX, extracted curves
and generated previews remain excluded from Git while reference licence evidence
is unresolved. The extraction helper and reports contain no motion arrays.

The self-contained HTML embeds art, code and the private derived motion for the
owner's local review; do not publish or package it as a release. Preview files use
0644 permissions inside a 0755 folder. They need no runtime network or AI service.
Previous revisions remain historical rejected candidates, not approved animation.
The final target stays an installed offline desktop Godot game.
