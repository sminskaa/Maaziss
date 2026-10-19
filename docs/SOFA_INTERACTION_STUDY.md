# First interactive sofa sitting study

The owner requested a first environmental interaction: move Maziss around the
room, select **Use**, click the sofa and sit on one fixed spot without pillows.
The clear right cushion is the target. Original art, the supplied sculpt and the
previous walking source remain unchanged.

## Construction

`tools/character_sitting_pose.py` authors a two-second stand-to-sit action on the
existing 14-bone skeleton. Both complete feet stay planted while fixed-length
two-bone IK bends the knees. The hips move back/down, the torso leans forward
before descent and settles near upright. The bag-side arm follows its joined bag
region; independent bag/hand topology is still unfinished. Standing reverses this
first authored action rather than claiming a separately captured stand-up motion.

`tools/render_sofa_sit.py` uses the actual model, current toon lighting, a fixed
camera pitched toward the floor and a presentation heading. Hidden cuboid seat,
floor and back proxies establish real local-space contact landmarks. The cushion
top is 0.43 authoring units high. They guide this authored interaction; they are
not a recovered sofa mesh or a dynamic physics simulation.

The proxy seat contact projects onto source-art point (430,610) in the 1672×941
reframed room. Fixed world scale and the camera's projected floor point determine
placement; no animation frame is normalized to changing silhouette bounds. The
first scene test uses 250 source pixels per authoring unit at this seat. Other
floor depths use one proportional scale rule. The pillows are not moved or edited.

## Interactive review

`tools/build_sofa_sit_review.py` packs the actual 288×360 motion renders into
transparent VP9 clips, with a WebP atlas for idle/turn poses, inside an offline
Canvas page at `visual-preview/maziss-sofa-sit.html`. This compact encoding was
checked in Chromium for the owner's Chrome/Brave review workflow. The controller
source is `tools/sofa_interaction.js`. This is a review delivery format, not a
decision about the final Godot animation format.

- Clicking clear floor walks Maziss there through a visibility graph inside the
  calibrated concave floor outline. Sofa, desk and walls are outside that outline.
- **Use** plus a click anywhere on the sofa approaches the same clear cushion,
  turns, lowers onto it and stays seated. The pillows are never separate seats.
- A new floor click stands him up, then walks to the target. Reset restores the
  initial position. Right-click examines; Look at does not trigger sitting.
- Seat guide optionally shows the projected proxy. It is a review aid.

The soft sole/seat contact cues and a small near-arm occlusion region are scene
compositing. Walking uses a broad root contact cue, avoiding detached shadows at
rest-foot positions. These are not physically cast room shadows or full furniture geometry.
Floor navigation is bounded to this one image/seat. No inventory, dialogue or main
Godot game state is modified. The final game target remains offline desktop.

## Reproduce privately

```sh
blender -b --python tools/render_sofa_sit.py -- --test
blender -b --python tools/render_sofa_sit.py
python3 tools/build_sofa_sit_review.py
```

The renderer reads the retained private supplied rig and FBX-derived walking
curves in `build/checks/supplied-character/`. Actual pose renders, scene proxies,
manifests and packed assets remain ignored in `build/checks/sofa-sit/`. Generated
HTML remains private. The renderer saves a separate authoring scene, leaving the
source `.blend`, `.glb`, motion and approved images intact.

Art and QA must open actual pose frames and interactive room captures to judge
support, proportions, cloth continuity, depth order and human motion. Finite
coordinates or passing click tests alone cannot establish those qualities. Their
scoped results are in `production/ART_SOFA_SIT.md` and `production/QA_SOFA_SIT.md`.

## Resume checkpoint

The private deliverable is `visual-preview/maziss-sofa-sit.html`, with its exact
size and hash in `build/checks/sofa-sit/delivery-manifest.json`. The separate
`sofa-sit.blend` contains the seated authoring scene and hidden seat/floor/back
proxies; `character_sitting_pose.py` remains the reproducible action definition.
The supplied model, approved drawings and earlier walking source are preserved.
The owner still decides whether the acting, scale and contact feel convincing.
