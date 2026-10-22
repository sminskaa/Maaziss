# Desk stool approach, pull and sit study

Owner authorization: replace the painted stool with its complete 3D candidate,
have Maziss approach in front of the desk, pull it toward himself and sit. This
explicitly resumes character motion for this bounded task. Other backlog changes
and the main Godot room are outside this increment.

## Construction and sources

- `tools/stool_interaction_pose.py`: world-space action, 7.8 seconds at20fps,
  retained FBX walking directions with distance-based phase; fixed-length limbs,
  Left-hand rim contact, release, staged turn/step and supported descent.
- `tools/render_stool_interaction.py`: original supplied complete rig and original
  six-part stool rendered together, real floor shadow catcher, fixed23° camera,
  fixed200 source-room pixels/metre. No per-frame silhouette resizing.
- `tools/build_stool_interaction_review.py`: locally repaired room, fixed-frame
  compositing, native video with an offline Use-stool control and still evidence.
- Private authoring scene: `build/checks/stool-interaction/stool-interaction.blend`.
  Character/root/stool animation is baked before rendering and saved separately.
- Private action/plate/renders/manifests: `build/checks/stool-interaction/`.
  Original character, stool model, room image and earlier previews are preserved.

The old painted stool and its shadow are removed with an image-tool local repair.
Its retained output is `clean-patch-generated.png`. Only a feathered local mask in
source crop(1320,570)–(1580,820) is composited into the room; the source itself is
unchanged. Art and QA inspected the stool-free rug/floor/desk region for holes,
old fragments and coherent seams. `room-clean.png` is the resulting clean plate.

Stool starts at world(0,0,0), mapped to roomfloor(1445,744), and is pulled to
(-.38,-.32,0), about half a metre toward Maziss. Seat top is .568m. Final pelvis
is .698m; final25° heading and root(-.2302759,-.6529154,0) place the seat landmark
exactly over the stool. The bag-side Right arm remains quiet relative to the torso
because its hand and bag share original geometry. The Left hand performs the pull.

## Corrections driven by actual review

The rig helper uses bone directions and cannot infer twist about a nearly vertical
spine. The renderer therefore carries world heading/position on an actual actor
root and inverse-transforms the authored targets into actor-local coordinates.
This avoids a frontal torso remaining behind while limbs turn around it.

Art and QA found the initial frontal endpoint hard to read as sitting. Turning
25° reveals the bent thigh and stool edge without moving the seat contact. They
also identified an overly wide alignment step. Leading with the Right foot reduces
maximum ankle separation from1.001m to.479m and allows a smaller.15m transfer
crouch instead of.26m. Exact pose comparison verifies460 full states before4.6s
remain unchanged, so verified prefix renders can be reused with recorded hashes.

QA measured a2.06cm boot-floor intersection during the pivot. Preserving foot-vector
pitch alone did not fix it: direction-based rotation still lost sole roll. During
non-walking phases, the renderer now explicitly applies the whole foot's Z-yaw
relative to its original basis. The5.2s actual corrected keyframe has minimum mesh
height about+.00094m; the final endpoint is within floating-point floor tolerance.
Final independent scene and continuous-motion checks are recorded separately.

## Review status and limits

Final full-motion review is complete. Art inspected eight composed keyframes and
20 native playback captures; independent QA inspected final images, audited all157
baked scene samples and frame hashes, and passed11 offline browser checks including
actual decoded time/phase progression, Use-hotspot activation, endpoint, reset,
repeat and mobile layout. Both recommend owner review of this first candidate.
Final reports: `production/ART_STOOL_FINAL.md` and `production/QA_STOOL_FINAL.md`.
Earlier authoring and defect history remains in `ART_STOOL_INTERACTION.md` and
`QA_STOOL_INTERACTION.md`; those provisional findings are not the final verdict.

The compact review is `visual-preview/maziss-stool-interaction.html`,930920bytes,
SHA-256 `29e45f1274caf82099af98cd29aa6e91a865aa0cdd14e8bb5d4ad67dcb8e6f24`.
It contains the1120×630 actual action video and embedded before/after/still evidence.
The native video is8.85seconds including the one-second held endpoint.

The final independent audit verifies corrected pivot clearance and finite meshes,
with maximum joint error2.90e-6m. It also identifies inherited approach boot-floor
penetration up to1.633cm at1.05s. That remaining first-pass walking/contact defect
is disclosed; do not claim zero penetration or finished natural acting. Art also
notes a stiff/deep preparation and limited seat visibility as polish items. These
are recorded alongside the scoped owner-review recommendation, not concealed by
passing browser tests.

The preview is one authored action, not a free walking controller or runtime
physics simulation. Character face/hands, clothing wear and prop textures remain
preliminary. A1second held endpoint is added to the video after actual rendered
frames. The final game direction remains offline Godot; no external service is
required by the review or player runtime. No stool reset/return animation, writing
or other room interaction is claimed.

## Reproduce in the retained private workspace

```sh
blender -b --python tools/render_stool_interaction.py -- --keys
python3 tools/build_stool_interaction_review.py --keys
blender -b --python tools/render_stool_interaction.py
python3 tools/build_stool_interaction_review.py
```

The image-tool patch must already exist privately. No generation/network calls
are hidden in these commands. Source/model/pose/render/frame hashes and output
placement live in the private manifests. Explicit reuse flags require retained
prior manifests and, for changed pose definitions, the exact prefix-equivalence
proof; regular reproduction works without those caches.

## Subsequent owner-directed revision

The owner requested boarding around the back and sitting toward the desk after
reviewing this first candidate. `STOOL_DESK_FACING_STUDY.md` records the separate
revision. This original preview, poses and private assets remain intact.
