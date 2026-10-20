# ART-012 stool interaction pose study

Scope: actual supplied sculpt approaches the desk stool, grips its near-left rim
with the free Left hand, pulls the complete stool toward himself, releases, turns
and sits facing into the room. This is a first bounded action, not final art
approval or a walkability controller. Existing source mesh and bone lengths remain
unchanged; the joined Right hand/bag retains the torso transform throughout.

## Renderer contract

`tools/stool_interaction_pose.py` is an import-safe Blender Python module. Import
performs no scene edits. `DURATION=7.8`, `FPS=20`, `KEY_TIMES` supplies phase bounds.
`state_at(seconds)` clamps its argument and returns:

- `targets`: all 14 JOINTS names, each with world-space `head` and `tail` XYZ lists;
  pass directly to `build_supplied_character.pose`, without a second root transform.
- `stool_position`: worldXYZ translation of the complete original stool.
- `phase`: approach/reach/pull/release/align/sit/seated.
- `root`: floor position and `yaw_degrees` about +Z; metadata already applied to targets.
- `seconds`: clamped sample time.

World +Z is up, front is -Y. Floor translation mapping is 200px/m, anchor(1445,744)
with Y depth projected by the coordinator's fixed 23-degree-down camera. No pose
uses image bounds for scale.

| Seconds | Action | Root floor XYZ | Stool XYZ |
| --- | --- | --- | --- |
|0 | Start approach |(-1.7,-.9,0) |(0,0,0) |
|1.2 | Arrive,80-degree heading |(-.63,-.55,0) |(0,0,0) |
|2.5 | Free fingertip reaches rim |(-.63,-.55,0) |(0,0,0) |
|4.0 | Pull completes |(-.88,-.72,0) |(-.38,-.32,0) |
|4.6 | Release and straighten |(-.88,-.72,0) |(-.38,-.32,0) |
|5.8 | Front alignment,25-degree heading |(-.230276,-.652915,0) |(-.38,-.32,0) |
|7.8 | Seated |(-.230276,-.652915,0) |(-.38,-.32,0) |

The original stool seat is .568m. Final pelvis height is .698m, seat+.13m,
with .365m rear travel. Sitting uses fixed boot targets and continuous two-bone
IK. Repositioning alternates lifted feet and lowers the pelvis by .15m at midstep
for reachability. Final yaw is 25 degrees; the root is offset by the rotated
seat marker(.005,.365,0), retaining exact support at the moved stool center.
Reach/pull has a 32-degree preparation lean and .66m pelvis. Finger tip target is
(-.17,-.12,.56)+stool translation during contact. The retained FBX walk is used
for approach legs with its original floor correction and length-preserving
interpolated directions. Gait phase follows actual traveled distance divided by
the retained measured stride of 1.271577865 m. Start/stop and phase transitions use quintic easing.

## Numeric evidence

`build/checks/stool-interaction/art/pose-validation.json` records 781 samples at
100 Hz, all phase-boundary poses, bone lengths, moving rim contact and fixed sit
feet. Measured maximum bone-length error is 3.13e-7 m, held rim fingertip error is 2.99e-8 m,
and final sit boot movement is 0 m. Numeric contact is
only a construction check: source surface, boots, clothing, fingertip/seat contact,
room occlusion and perceived motion still require review of actual room renders.

## Actual image review

Inspected corrected actor-root room composites `room-key-000.png`,
`room-key-050.png`, and `room-key-156.png` (0, 2.5, 7.8 seconds). The renderer
carries actual actor heading, while converting world targets back to actor-local
space for the skeletal pose. Earlier captures with lost upright-bone twist were
superseded and are not review evidence.

- Approach: scale, complete silhouette and relationship to the desk/stool read
  coherently. Feet appear floor-supported.
- Rim contact: the Left free hand visibly meets the near seat edge. Deep squat
  and forward preparation lean read as a deliberate reach; Right arm/bag remain
  quiet. Complete stool geometry is visible.
- Final front view: boots appear grounded and bag/clothing stay continuous.
  However the thigh bend and stool seat are hidden by the frontal body/legs,
  making the static seated pose look close to standing. Recommended resolution
  before full rendering: turn the final seated heading 20–25 degrees into the room,
  compensating root position so the same seat marker remains over the stool.
- No obvious original stool duplication or open background hole in these three
  room samples. Midpull and after movement must expose the vacated floor patch
  before the background/old-shadow claim is complete.

The coordinator requested and the pose now implements the 25-degree final
heading with exact seat-marker compensation. The new final pose and coherent
rotated foot transition passed the same 781-sample numerical validation.
Current recommendation: inspect the changed seated room view and midpull frame,
then review the actual continuous clip. No final visual approval from these three stills. Source sculpt's simplified
mitten hands, pale surfaces and unfinished face remain existing art limitations.


QA's full-scene audit identified roughly 2 cm sole burial during alignment. The
cause was interpolation between foot vectors at different headings: normalized
XYZ lerp increased downward pitch. `_step_feet` now rotates the original foot
vector only about +Z while separately lifting/translating the ankle. Across the
781-sample check, transfer vertical foot-vector error is below 4.5e-8 m and minimum
ankle lift is -3e-8 m (float precision). Actual deformed-sole validation remains with
QA, and updated alignment imagery must be checked. Approach phase now follows
traveled distance using the existing measured-stride convention, so slowing the
root also slows the retained gait. This improves phase registration without
claiming a full contact-constrained walking controller.

### Staged corrected-heading review

Inspected actual corrected 25-degree `room-key-065.png` (midpull 3.25 s) and
`room-key-156.png` (seated 7.8 s), composited from the coordinator's historical
valid key manifest. These held-rim/final poses were unchanged by the subsequent
foot-yaw and distance-phase corrections; they are staged still evidence, not the
final clip's provenance.

The revised final now reads as sitting: visible bent thighs, stool near leg and
footrest behind the legs, and apparently supported hips. Boots look grounded;
complete character silhouette and clothing remain intact. Midpull keeps the free
hand visibly on the rim while the complete stool moves. The exposed rug/floor
shows no obvious duplicate stool, old shape or open hole at room-view scale.

Art recommendation from these actual stills: proceed to final continuous-motion
and native-player capture review. No new still-image blocker. Final source is
frozen for rendering; final motion/contact recommendation remains pending.


### Actual alignment blocker and bounded correction

Actual `room-key-104.png` showed a deep kneeling/split lunge during alignment;
this superseded the still-only recommendation to proceed. The default Left-leading
step put the feet up to 1.00146 m apart. Alignment now leads with Right, while the
pull retains its original Left lead. Maximum alignment ankle spacing is .47871m;
the preparation crouch is reduced from .26m to .15m (minimum pelvis height .76m).
Smaller .12/.14m variants overextended a shin and were discarded.

Before editing, source was retained privately as
`art/stool_pose_before_align.py`. Complete state dictionaries for 460 samples at
100Hz over 0–4.59 seconds compare exactly equal before/after. Only alignment changes;
the renderer can reuse the proven-identical approach/reach/pull/release prefix.
`art/align-revision-validation.json` records the comparison, displacement samples
and exact 5.2-second poses. All 781 pose samples again preserve bone lengths within
3.13e-7 m, held rim contact within 2.99e-8 m, and final seat/foot landmarks exactly.
The new actual alignment still and continuous clip require visual review.
