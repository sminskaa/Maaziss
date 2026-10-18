# Walking study — FBX revision 7

Open `visual-preview/maziss-walking-v7.html`, or the latest `maziss-walking.html`.
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

The original room and character PNGs are unchanged. `walking/character-renderer.js`
uses runtime masks and a continuous trouser mesh rather than separate cuff scraps.
Side boots use a flat planted drawing; neutral front/back boots remain upright.
Boot tops sit under the actual trouser endpoints. The far arm is drawn before the
torso and the near arm after it. Source-mask cleanup and final connected-component
cleanup remove small detached image fragments. Overlapping triangle clips prevent
thin transparent cracks between trouser sections.

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

`visual-preview/maziss-walking-v7-poses.html` contains actual rendered phase captures.
Use moving playback as well as still poses to judge the result.

## Validation and limits

Frozen build `9d7c3a14af4f` passed 54 focused browser/pixel checks, including
52 actual rendered poses in four directions with no detached alpha components.
The final source/output identity is recorded in
`build/checks/fbx-walk/build-manifest.json`. Independent results and visual findings
are in `production/QA_FBX_WALK.md`. Technical checks do not establish that the
animation looks natural; owner review remains necessary.

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
python3 tests/browser_fbx_walk.py
python3 tools/capture_fbx_walk.py
```

Extraction requires the retained owner-supplied FBX and ignored intake manifest.
The builder requires the extracted `private/motion/fbx-motion.json` (or `--motion`
path), Python and Pillow. The browser tools use Playwright and Chromium. A public
checkout alone cannot reproduce this private-input study. Raw FBX, extracted curves
and generated previews remain excluded from Git while reference licence evidence
is unresolved. The extraction helper and reports contain no motion arrays.

The self-contained HTML embeds art, code and the private derived motion for the
owner's local review; do not publish or package it as a release. Preview files use
0644 permissions inside a 0755 folder. They need no runtime network or AI service.
Previous revisions remain historical rejected candidates, not approved animation.
The final target stays an installed offline desktop Godot game.
