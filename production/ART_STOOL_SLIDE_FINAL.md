# ART-016 — revised right-hand stool action

20 October 2026. Resumed the saved 8.8-second action and existing independent
right-arm/bag candidate. No model reconstruction or additional research. The source
character remains the private prepared candidate SHA-256
`0b4f0fd6c7f180c3c71bab70dae384cac5341d5c6ccc23b615896631907352b2`.

## Current correction ready for frozen key review

Pose SHA-256:
`95f60d2ef89f423a123c696d809495e0ca6026c41e5cac500cac07708b82c2ec`.
The single pull-foot adjustment moves anatomical Right by (.29, .04, 0) m,
4 cm farther along world positive Y than the saved starting candidate. No new
step or circular route is added. A smooth mid-pull pelvis rise peaks at 1.8 cm;
a simultaneous 2 cm world-negative-X root adjustment retains the hand's reach.
Both corrections return to zero at pull endpoints. The held right-hand targets,
short boarding transfer, occupied slide and final desktop targets are preserved.

During the final desktop reach only, the elbow pole blends smoothly from the
existing outboard pole to local (sign*.12, .05, -.8), completing its transition
at 75% of that reach. This lowers both elbows toward the torso. Pull and occupied
seat-grip elbow poles are unchanged. Final hand tips/Z targets remain unchanged.

Private reproducible probes/results:
`build/checks/stool-slide/art-resume/equivalent.py`,
`equivalent-verify.py`, `equivalent-whole.json`,
`equivalent-dense-pull.json`, and matching logs. The probe imports the renderer's
shared `apply_sample` directly: actor location/heading, actor-local bone targets,
exact planted Foot Z roll, and authored stool location. Actor/rig/stool animations
are cleared first. Both evaluated feet are checked against actual stool surfaces.

- Across all 177 authored 20 fps samples: zero boot/stool edge/triangle crossing
  pairs and zero sampled bag vertices inside the solid seat. Maximum target
  bone-length discrepancy is 0.000000344 m; held Right-grip error is zero.
- Across 181 samples spaced 0.01 seconds from 2.4–4.2 s: zero boot/stool crossing
  pairs, zero boot vertices inside stool solids, and zero bag vertices inside the
  seat. Bone lengths remain within 0.000000344 m and held grip is exact.

Boot checks combine evaluated triangle edge crossings and closed-surface ray
parity. Bag identity uses the original source bag's retained Y/Z coordinates,
avoiding mistaken selection after its authorized outward shift. These are sampled
geometric checks, not continuous physical simulation or visual acceptance.

## Superseded probe mismatch and correction

The earlier proposed pose `5418f084…` was independently rejected: baked-scene QA
found 709 crossing pairs and a Right boot vertex 16.34 mm inside stool leg 3.
The initial `verify.py` omitted the renderer's exact planted Foot roll and used a
cached rig inverse. Its zero-crossing assertion was invalid and is withdrawn.
The corrected pipeline reproduces that 16.34076 mm penetration before searching.
Current `equivalent-*` results above supersede the earlier `candidate-*` results;
old files are retained as diagnostic history, not acceptance evidence.

## Actual-image elbow diagnostic

Opened the ten actual raw keys from superseded scene
`9e16256b39a083efbc88dc15be6a43b0b1775c27db2e970353d91b7a87423e68`,
retained in `art-resume/raw-keys-sheet.jpg`. The compact pull/boarding, character,
satchel and stool remain recognizable. These are raw keys, not current room proof.

Opened fresh `art-resume/final-palm-contact.png`: the anatomical Left upper arm
projected almost horizontally sideways, reading as a raised wing. Root authorized
an in-memory downward-pole test. Opened its actual alternate-camera result,
`art-resume/down-pole-palm-contact.png`: both elbows now hang near the torso and
below the desk edge, improving the relaxed seated working silhouette. Evaluated
hand minimum Z stays .931226 m Left and .933096 m Right, 1.23/3.10 mm above the
.93 m support. Hand tips remain unchanged. The source hands are coarse mitten-like
forms; no articulated finger pose is claimed. The alternate camera uses a plain
support material and hidden desk items only for this read-only diagnostic.

The coordinator must now rebake the current frozen source. Independent QA must
bind its checks to that scene/source pair. Fresh actual before/during/after room
images, an unobscured final palm view from the new bake, and the actual native movie
remain mandatory. No final Art recommendation or owner approval is claimed yet.

## Corrected frozen key gate — ready for full motion

Corrected scene SHA-256:
`e3df556e2207972d8f346d6b0ae8e59624b0995aae64611cbeec7e507bf46ba3`.
Opened all eight refreshed actual painted-room composites at 2.8, 3.05, 3.2,
3.4, 4.25, 6.85, 8.1 and 8.8 seconds. Their hashes are retained in
`art-resume/corrected-room-sheet-manifest.json`; full-room and enlarged actual
image sheets are `corrected-room-keys-sheet.jpg` and
`corrected-room-keys-details.jpg`. Also opened full room frames at 3.05 and 8.8 s.

The compact pull/boarding, continuous satchel and complete stool read coherently.
The corrected boot is visibly separated from the stool leg; the pulled hand stays
at the rim. The clean room patch remains intact, with no duplicated stool, painted
remnant, old shadow or hole observed. The 8.1 s arm reaches forward, and the final
seated desk-facing posture keeps the elbows lower and close to the torso.

Opened `art-resume/corrected-final-palm-contact.png` rendered directly from this
new bake. The relaxed elbow pose is retained. Actual hand vertices with >.65 Hand
weight, inside the tabletop's XY footprint, number 122 Left and 129 Right; their
minimum Z values are .931226/.933096 m. None penetrates the .93 m support plane.
Evidence: `corrected-palm-skin-contact.json` and fresh view manifest.

Art recommends proceeding to the full continuous render once independent QA
clears this frozen geometry. This is a key-stage recommendation; actual native
movie playback, motion/transition judgment, and final Art recommendation remain
pending. No owner approval is inferred.
