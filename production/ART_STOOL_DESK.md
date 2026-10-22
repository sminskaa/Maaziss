# ART-014 desk-facing stool action

The owner requested a continuation of the existing stool action: Maziss passes
behind the pulled stool and sits facing the actual desk at the right of the room,
ready for a future writing action. This increment contains no writing animation.

`tools/stool_desk_pose.py` is a separate, import-safe Blender pose module. It
imports the retained `stool_interaction_pose` baseline and returns its exact full
state dictionary for every time before4.6seconds. Original source models, accepted
pull, framing, scene and prior reports remain unchanged.

The new action is11.5seconds at20fps. After releasing the rim, Maziss takes short
paired planted steps around the west/back and north side of the stool, then aligns
on its northeast side at9.5seconds. Descent ends at11.5seconds. The final yaw is
135degrees: local front-Y becomes world+X,+Y, toward the right desk rather than
the window. Root is computed as stool minus the rotated(.005,.365,0) seat marker,
so the final pelvis remains at.698m above the original.568m seat. The original
Right arm and joined bag geometry remain quiet relative to the torso. The free
Left arm relaxes toward the thigh in the final local heading.

The route uses preserved-pitch feet, independent planted swing transfers and
fixed-length two-bone leg solutions. Lead foot changes after the west/north
corner to avoid an unnecessarily broad split stance. The renderer's nonapproach
whole-foot Z-yaw correction should remain enabled for these new phases. A3.5cm
transfer pelvis dip is sufficient for reachability and avoids repeating the prior
deep alignment crouch.

Private `build/checks/stool-desk-facing/art/pose-validation.json` records1151
samples: maximum bone-length error3.63e-7m, maximum route ankle separation.49205m,
and minimum ankle lift-2.98e-8m (float precision). Every complete state in460
samples at100Hz before4.6seconds compares exactly equal with the retained baseline.
`prefix-equivalence.json` binds that claim to both source hashes. These numerical
construction checks do not establish deformed-mesh clearance or natural motion.
The baseline's inherited approach contact limit remains outside this change.

Actual accepted full-room endpoint `build/checks/stool-interaction/composite/frame-156.png`
was inspected before authoring. Its front/room-facing torso confirms the owner's
requested change is material. New combined-render keys have now been inspected
as recorded below; the final continuous-playback verdict remains pending.

## Stabilized actual room-key review

Inspected all eight actual new combined room images, `room-key-113.png`,
`127`, `141`, `155`, `169`, `183`, `210` and `230` under
`build/checks/stool-desk-facing/`, against source SHA-256
`e925600b2691e9ec342e151f0e3b7e05bf938e9ca27470a08d10dd4e22044436`.
The first provisional key pass predates the final pelvis-dip refinement and is
superseded; only the stabilized second pass supports this recommendation.

The complete stool remains visible as Maziss passes its west side and then
behind it. Midstep silhouettes show compact bent legs without the earlier deep
split/kneel. The last approach steps remain separate from the stool legs at room
view scale; there is no obvious leg-through-seat defect in these samples. The
seated endpoint visibly supports the hips on the stool, with bent thighs and
floor-supported boots. Clothing, silhouette and joined hand/bag stay continuous.
The back/three-quarter torso faces the desktop and radio on the right. It no
longer faces into the room, and its heading is visibly distinct from facing
straight toward the window. Room composition and painted furniture are preserved.

Art recommends proceeding with continuous rendering. These eight stills do not
establish smooth step pacing across the whole detour; the deliberate paired
shuffling and descent must still be watched in the actual native clip before the
final recommendation. Independent baked geometry audit remains QA's evidence.

## Final actual native-playback review

Opened the final compact HTML in offline Chromium, activated its Use-stool action
and let the native video play continuously to the end. Captured25 actual decoded
playback images from4.50 to12.54seconds without seeking, including the entire
new detour, alignment, descent and held endpoint. The recorded video clock reached
12.55seconds and the player ended at `Seated facing the desk`. Evidence:
`art/native-playback-review.json`, all `art/playback-*.png` images and the assembled
`art/native-playback-sheet.jpg`, under the private new output folder. Reviewed
those actual playback captures alongside the eight full-room keys. Final HTML
SHA-256 is `8212067b1806a5b9b158079195118dfe85737ae30f941dae21b170702384ce0f`.

The new route reads as a deliberate sequence of short repositioning shuffles
around the stool rather than passing through it. The feet alternate during each
transfer, the torso stays coherent, and the character does not drop into a deep
lunge or jump between the detour and descent. The circling is cautious and a little
staged because each paired step settles before the next; it is acceptable for
this bounded study, with naturalistic gait polish still open. No new obvious
boot/stool intersection, bag tearing, duplicated prop or background hole appears
in these reviewed captures. The endpoint consistently reads as seated at the
right desk, with the stool supporting the hips and boots on the floor. The future
writing surface is ahead of his torso; no writing motion is claimed.

Art recommends this corrected action for owner review. This is scoped to the
actual rendered candidate, with QA's independent deformed-scene/contact evidence
and the inherited early approach boot-floor limit retained. It is not a final
character/gait art approval or main-game integration.
