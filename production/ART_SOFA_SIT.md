# Sofa sitting study — ART-010

The owner requests one fixed sitting position on the clear right-hand sofa
cushion, away from the pillows. This is an interaction and placement study,
not approval to remodel the room or to move its cushions and pillows.

## Pose and actual image inspection

`tools/character_sitting_pose.py` provides `targets_at(t)` for the original
14-bone supplied-mesh rig. It leaves body proportions and full geometry intact.
The feet remain at their original planted rest transforms throughout a smooth
two-second descent. A short anticipatory forward lean precedes the hips moving
back and down, followed by a quiet near-upright seated posture. Both leg chains
use fixed-length two-bone IK, with continuous knee bends. The free arm eases
toward the thigh. The other arm follows the body because its hand and bag still
share source geometry; independent bag-side hand acting needs topology work.

World landmarks use the existing front=-Y, up=+Z convention. Seat top is 0.43,
final skeletal pelvis height is 0.56, and the final pelvis is behind the feet
at Y=0.365. These are physical scene coordinates rather than per-frame image
bounding boxes. The source mesh, source animation and approved drawings remain
unchanged.

Opened the actual new 16:9 room image and actual Blender Workbench renders from
front, oblique and profile cameras at stand, intermediate descent and seated
times. Evidence is private under `build/checks/sofa-sit/art/pose-*.png`.
The inspected poses retain a recognizable clothed character, joined knees/cuffs
and boots, a single face and continuous jacket/bag silhouette. The final pose
has bent knees, approximately horizontal thighs and a near-upright chest over
a real proxy seat. The free hand is mitten-like, reflecting the supplied sculpt,
and the bag hangs below the seat top outside the central pelvis footprint.

This neutral material inspection establishes a useful pose candidate. Final
acceptance still requires inspection of the actual toon render composited at
the chosen empty cushion, including cushion overlap, boot-floor contact, room
scale and perspective. It does not certify a finished production rig, independent
bag topology, polished facial likeness or complete room geometry.

## First actual room composite

Opened `build/checks/sofa-sit/first-composite.png`, made from the actual toon
render against the new 1672 × 941 room. The pelvis lands on the exposed right
cushion, with the knees ahead of its edge and both boots meeting the floor in
front. The painted pillows remain behind and to the left; neither pillow has
been moved or used as the sitting surface. The bag and its joined hand hang
beside the near thigh, without visibly passing through a pillow. Body size is
plausible against the sofa seat/back and adjacent furnishings in this first
placement. No detached clothing, repeated face or missing limb is visible in
the checked final-pose composite.

The 288 × 360 test render is visibly softer than the room when enlarged for this
placement; I asked the coordinator to use higher-resolution final sitting frames
and add a subtle floor contact shadow. Its pale character colours retain the
earlier study's limitations, already acknowledged by the owner. Recommendation:
proceed with this fixed-seat interaction candidate and inspect the final actual
interactive capture before presentation. This is a scoped staging recommendation,
not finished art approval.

## Final interactive image review

Opened the actual browser captures `build/checks/sofa-sit/root/final-seated.png`,
`final-lowering.png` and `final-walking.png`. This review used visible output,
compared with the room painting and retained supplied-character appearance,
rather than treating source code or passing contact checks as art evidence.

The seated capture preserves the intended empty right cushion. Both painted
pillows remain visible behind and to the left. The pelvis reads as supported by
the seat, knees and boots remain in front of its edge, and the soft floor shadow
helps ground the soles. The near sofa arm stays in the foreground where needed.
The intermediate capture reads as a forward lean and knee bend before settling,
without visible missing trouser sections, detached bag fragments or duplicate
facial features. The walking capture retains a complete recognizable costume,
bag and boots at a plausible foreground room scale. No per-pose change in body
proportions is apparent across these three different sampled states.

The final preview's full-resolution animation improves the earlier coarse
sprite test. The character remains softer and simpler than the room painting;
his comparatively pale palette, young rounded face, mitten hands and limited
cloth detail remain unfinished, as already recorded. The quiet bag-side arm
still reflects fused source geometry. These are continuing production/art
limitations rather than a new blocker for this first fixed-seat interaction.

Scoped recommendation: **show this candidate to the owner as a first sofa-sit
interaction study**. No art blocker was visible in these inspected final
captures. This is not owner approval, finished likeness, complete collision
validation or certification of every animation frame; behavioral playback and
state checks belong to the separate QA report.
