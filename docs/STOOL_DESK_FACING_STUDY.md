# Desk-facing stool revision

The owner accepted the first pull-and-sit study as a starting point, then requested
that Maziss pass around the back of the stool and sit toward the writing desk.
This revision keeps the first4.6 seconds of approach, reach, pull and release
unchanged and replaces only the subsequent boarding and seating.

## Construction

`tools/stool_desk_pose.py` imports the preserved original pose module. Seven small
paired foot transfers take Maziss around the west/back and north side of the stool,
then align him diagonally toward the actual far-right desk. The final heading is
135 degrees in the retained world coordinates (front +X,+Y), rather than the
original25 degrees toward the room or180 degrees toward the window bench.

The final root position is calculated from the stool centre and rotated local
seat marker. Hips descend onto the same real seat while the boots remain planted.
The complete character mesh, clothing/bag geometry, six-part stool, floor scale,
camera and repaired room plate are retained. The joined bag-side arm stays quiet.
The free hand rests near the thigh; no writing or desktop hand contact is animated.

The authored sequence lasts11.5seconds at20fps, followed by a one-second video
hold. The918447-byte `visual-preview/maziss-stool-desk-facing.html` keeps the earlier
preview intact (SHA-256 `8212067b1806a5b9b158079195118dfe85737ae30f941dae21b170702384ce0f`). Select
**Use**, then click the highlighted stool; native video controls also work.
This remains an authored review action, not the main Godot room or arbitrary
walking, collision avoidance or desk use at runtime.

## Evidence and review

Private retained files: `build/checks/stool-desk-facing/`, including the baked
Blender scene, actual transparent/composited frames, prefix-equivalence proof,
render and delivery manifests and reviewer evidence. The exact460 states sampled
from0 through4.59seconds equal the earlier version; the92 corresponding rendered
frames are reused only after checking their retained hashes. Remaining frames are
new actual renders. Source files and dependency hashes are recorded to distinguish
this revision from the original preserved study.

Art and QA inspected the same actual route midpoint, descent and final room images,
then native playback. Both recommend owner review: Art inspected25decoded playback
captures; QA passed11offline controls/playback/mobile checks and all231frame hashes.
A139sample evaluated boot/stool surface check detected no crossings; scene joint
error is at most2.90e-6m. The cautious, slightly mechanical circling pace remains
an acting polish item, along with the unchanged initial approach floor overlap. See `production/ART_STOOL_DESK.md` and
`production/QA_STOOL_DESK.md` for their final scoped recommendations and limits.
Original room and model assets remain private and unchanged. Palette, texture,
face/hands and earlier approach boot-floor overlap remain separate polish work.
The new facing supports the requested desk orientation; future writing still
needs a fitted desk surface, arm reach and pen/paper contact work.

## Reproduce in the retained workspace

```sh
blender -b --python tools/render_stool_interaction.py -- --pose-module stool_desk_pose --output build/checks/stool-desk-facing
python3 tools/build_stool_interaction_review.py --output build/checks/stool-desk-facing --html visual-preview/maziss-stool-desk-facing.html
```

The retained clean-background patch must exist in the selected output directory.
Add `--keys` to both commands for a small still review. Optional
`--reuse-verified-prefix build/checks/stool-interaction/render-manifest.json`
requires the retained old frames and matching `art/prefix-equivalence.json` proof;
regular rendering does not require the reuse cache. No paid or runtime network
service is needed.
