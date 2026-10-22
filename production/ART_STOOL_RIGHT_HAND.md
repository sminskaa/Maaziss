# ART-015 — independent anatomical right arm

20 October 2026. Bounded preparation for the owner's revised stool action: Maziss
stands left of the stool, pulls with anatomical right hand, briefly sits, grips the
seat with right hand while occupied stool slides toward the desk, then places both
hands on the desktop. This report covers the arm preparation, not approval of that
whole motion or main-game integration.

## Actual diagnosis and local construction

The supplied right hand/forearm and bag share surface vertices. The retained source
weights intentionally hold the bag-side arm quiet. Assigning those shared vertices
to Right bones would tear/stretch the satchel. The original private supplied rig is
unchanged.

`tools/prepare_stool_right_arm.py` creates the ignored
`build/checks/stool-slide/character-right-arm.blend`. It preserves `MazissRig` and
`Maziss supplied sculpt` for renderer compatibility. A capped portion of the actual
free supplied left sleeve/forearm/hand is mirrored into a closed `Right arm` mesh,
with weights only to `RightUpperArm`, `RightForeArm`, `RightHand`. This keeps the
supplied sculpt's chunky sleeve/hand design and anatomical palm/thumb chirality.

The retired outer fused right arm is removed locally; its body and original bag
boundary is capped. The bag's inner shell remains the supplied geometry; the new
outer side receives bag colour and stays with Spine. No moving mesh shares bag
vertices. The face, hair, body proportions and original opposite arm remain intact.
Upper shoulder overlap was corrected after the first actual render exposed a gap.

## Checked evidence

Private evidence in `build/checks/stool-slide/art/`:

- `right-arm-topology.json`: body 4,566 vertices / 9,240 faces; Right arm 429 / 716.
  Both have zero boundary edges and zero nonmanifold edges.
- `right-arm-deformation.json`: body maximum displacement under the isolated arm
  reach is 0.00000264 m (matrix numerical noise); right arm displacement is 0.769 m.
  All original body coordinates above 1.50 m remain exactly retained, including the
  face and hair. No original head/face features were rebuilt.
- Actual Cycles renders: `arm-rest-0.png`, `arm-rest-65.png`, `arm-rest-135.png`,
  `arm-reach-0.png`, `arm-reach-65.png`, `arm-reach-135.png`. Inspected all six.
  Right hand visibly reaches forward while satchel keeps its shape; no source
  stretched shelf, old hanging hand, open shoulder hole or floating arm was seen.
  A fine shoulder junction remains visible in a front view and needs assessment at
  the final room scale. Source hand detail remains coarse; no finger grasp rig was
  invented.

Candidate SHA256:
`8c682c0c5c9def8d564696f34264c8af7fa5a2f74c6709246f2b75958f80ff77`.
Source SHA256:
`570cae56315de4b0dffeffbff681c4179887c3eeda5accf7bc5dbba77ae2cfd7`.

## Scoped recommendation

Ready for coordinator's combined character/stool/desk contact renders. This is a
usable closed local arm candidate; the six isolated diagnostic views do not certify
seat grip, bag/seat clearance while sitting, desk contact or all interpolated poses.
Art and QA must inspect the same combined before/during/after actual images before
recommending the revised stool action. No final artistic or owner approval claimed.

## Combined stool/desk keys — revision hold

Later on 20 October, inspected all eight actual raw keys (2.4, 3.4, 4.25,
5.8, 6.3, 6.85, 7.4, 8.8 s), and painted-room composites at 2.4, 6.3, 8.8 s.
The right arm stays recognizable, with no visible open shoulder or stretched bag.
The authored compact step avoids the earlier circling route. The hand/seat and
bag/seat contacts nevertheless need correction before a scoped recommendation.

Read-only evaluated-skin evidence is retained privately in `art/contact-art.json`,
`art/bag-seat.json`, `art/exact-contact.json`, and their scripts. These calculations
use the actual separate right mesh, original-body left hand vertices with hand
weight above .65, and original bag vertices with bag influence above .7. Signed
nearest distance to the actual closed seat confirms intersections rather than
merely comparing bone tips or height extrema.

- Initial scene `f52e1159e2b314240215939b8ead7d5d14043f21d83f3bc8d696e7bce41ab46e`:
  final left/right hand skins reach .89764/.90410 m over a .93 m desktop. Both
  penetrate the tabletop. The coordinator raised the final targets and rebaked.
- Corrected scene `b48d21eedfe7c69ab396a55621d0b1382b97f0642d959d879934f7164e591d6f`:
  right hand minimum .93310 m, approximately 3 mm above desk. Left minimum is
  .92298 m; two actual hand vertices within the desktop footprint still penetrate
  over 0.5 mm, deepest about 7 mm. Further left adjustment/retest required.
- At pull 2.4/3.4 s, 42 right-hand vertices are inside the actual solid seat,
  deepest about 30 mm. At seated grip/slide 6.3–7.4 s, 46 are inside, also about
  30 mm. This is solid penetration rather than fingers wrapped outside the rim.
  Move the grasp toward the outer rim and fit the evaluated skin.
- Actual bag/seat intersections persist: 14–17 bag vertices during pull,
  3–5 during sit/slide, deepest about 24–29 mm. The bag remains visually stable,
  but stability does not establish clearance. Adjust bag/stool/body spacing.
- QA independently identified boot/ring/leg crossings during the occupied slide;
  that evidence and movement correction remain with QA/coordinator.

Current combined recommendation: **hold for contact corrections and actual-image
retest**. The local arm topology is usable; it does not make the current combined
stool action acceptable. The painted desktop obscures much of the final palm from
the game camera, so a diagnostic unobscured/contact view is needed alongside the
room view to support any later palm-support claim. No full-motion acceptance yet.

## Bounded bag clearance candidate

Coordinator authorized an outboard bag adjustment before the next combined bake.
The preparation script now shifts the retained bag shell toward anatomical Right
(local negative X) by at most .10 m, using the existing smooth bag field and an
additional upper fade from .99 to 1.23 m to soften the strap/hip transition. The
651 affected local vertices keep their existing topology/colours; both meshes
remain closed manifold. Face, hair, hands, limbs and original source are unchanged.

New private candidate SHA256:
`0b4f0fd6c7f180c3c71bab70dae384cac5341d5c6ccc23b615896631907352b2`.
The six actual rest/reach diagnostic renders were refreshed and inspected. Bag
silhouette is broader, continuous and stable; neutral right hand remains visible
beside it, with close overlap in the hanging pose. No gap or stretched shelf was
seen. This is readiness for combined retest, not proof that the seat interference
is fixed. Previous combined-scene blockers remain open until a newly baked scene
using this candidate is measured and rendered.

## Revised bag/stance/contact key retest

Inspected the revised nine raw keys after `keys-revised.log` recorded COMPLETE.
Baked scene SHA256:
`e37b80b727f50e896b9b21993217849fcf443eb6430e8d8d965407b18190d68a`.
This scene uses the outboard bag candidate above and the wider advancing stance.
The previously retained room composites predate this bake, so they are not claimed
as revised painted-room evidence.

Closed-seat/surface retest at 2.4, 3.4, 5.8, 6.3, 6.85, 7.4, 8.8 s finds no bag
vertices inside the seat; nearest bag/seat distances are 15.5–77.9 mm. The outboard
bag correction succeeds for those samples. Final hand skins over the actual desk
footprint now lie at least 1.23 mm (left) and 3.10 mm (right) above its surface,
with no penetrating selected hand vertices. Final palm/desk support is now within
a few millimetres, subject to actual-image review with the desktop exposed.

The revised pull grip overshoots outward: nearest actual hand/seat gap is 35.6 mm
and the raw key visibly floats. Seated grip still puts eight selected hand vertices
inside the seat, deepest 9.52 mm. A read-only radial search with the actual rig and
mesh gives these minimal fitted targets, sent to the coordinator:

- Pull: `(-.14707, .17975, .590)`; nearest skin/seat distance .752 mm,
  no selected hand vertices inside.
- Seated grip: `q135 @ (-.18697, -.22851, .590)`; nearest .448 mm,
  no selected hand vertices inside.

The search did not save a modified pose or scene. Coordinator must apply/rebake,
render and independently retest; this section is a measured proposal, not final
contact acceptance. Current hold is narrowed to the actual grasp fit and full
combined motion/room evidence. Source sleeve/hand are still coarse and do not have
articulated fingers; contact must be judged as a stylized existing hand shape.
