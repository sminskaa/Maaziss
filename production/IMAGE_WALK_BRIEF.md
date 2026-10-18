# Image-only walking brief — ART-005

Reviewed the three image sheets supplied in this conversation and read the current
`walking/reference-gait.js` and `walking/demo.js`. No FBX, video, video tracking or
new motion capture was opened or used for this brief. Static sheets show poses;
they do not establish frame durations, joint velocities or a measured human cycle.

## What the sheets support

- The twelve-pose boy sheet reads as stylized running: high recovery knee, markedly
  raised trailing foot and apparent flight poses. Use its alternating limb and
  overlapping silhouette ideas, not its stride, lift or contact schedule for Maziss.
- The two adult side-view sheets provide clearer straight/loaded-leg, recovery,
  foot-passing and opposing-arm silhouettes. Their very similar layouts are not
  independent measurements. Their ground heights, apparent limb lengths and contact
  relationships vary; the stretched fifth pose is an exaggerated illustration.
  Do not trace all poses or assign equal time to every illustration.
- None supplies reliable front/back anatomy or an idle-to-walk transition. These
  must be authored conservatively and labelled as interpretation.

## Proposed adult walk construction

The following is an animator-authored starting schedule, not timing extracted from
the images. One full cycle contains two steps. Mirror the first half for the other
leg, while keeping physical left/right identities stable.

| Full-cycle phase | Pose intention | Contact and weight |
| --- | --- | --- |
| 0.00 | First heel meets ground; opposite leg trails | Brief double support; avoid a locked leading knee |
| 0.08–0.12 | Down/recoil | Leading foot settles; leading knee absorbs weight; rear heel rises |
| 0.23–0.27 | Passing | Loaded foot beneath pelvis; recovering ankle passes close to it, toe clear |
| 0.37–0.42 | Up/recovery | Support heel lifts; recovery knee advances, then shin opens progressively |
| 0.50 | Opposite contact | Transfer load smoothly; repeat with sides exchanged |
| 0.58–0.62 | Opposite down | Mirror first recoil |
| 0.73–0.77 | Opposite passing | Mirror first passing |
| 0.87–0.92 | Opposite up | Mirror first up |
| 1.00 | Original contact | Identical pose and velocity to phase zero |

Start with approximately 60–62% stance per leg, creating short double-support
windows and no flight. Choose a comfortable adult cadence by visual review rather
than treating the sheets as a stopwatch. Keep recovery ankle clearance low and
avoid the boy sheet's running kick. A modest knee bend may remain at maximum
extension; the knee must not flick from bent to locked and back.

Use continuous positions and velocities through contact, toe-off, passing and loop
wrap. A cubic curve is useful only when its tangents are controlled: an overshooting
cubic can introduce new joint reversals. For a planted side foot, roll from heel
contact to flat support to forefoot/toe support; do not pin the toe through all of
stance while rotating a heel-first landing around it. On the swing leg, let the
shin unfold gradually before landing rather than straightening at a phase boundary.

Keep pelvis motion small, with two gentle rises/falls per stride. Retain the original
slight forward lean and painted proportions. Opposing arms should have quiet arcs
and soft changes of direction, with a small upper-body response. Do not stretch
limbs or change the face, jacket, bag, boots or overall design to achieve a pose.

## Specific implementation risks in revision 5

These are source-level explanations consistent with the owner's symptoms, not a
claim that static code inspection proves every rendered defect's cause.

1. `sample()` linearly interpolates joint angles. Its slope changes at every sample
   boundary, so a continuous angle can still produce visibly abrupt velocity changes.
2. The knee solve contains `sqrt(limb² - halfReach²)` close to full extension.
   The slope becomes very large near maximum reach; clipping reach and pelvis height
   creates further changes of slope. Maintain a smooth reach margin and verify knee
   angular velocity, rather than solving into the singularity and then clamping it.
3. Hard `stance` changes, separate support/swing ankle formulas and the late-stance
   pitch rule can disagree at toe-off. Match pose and tangent on both sides of the
   transition. Contact release must not replace one target with an unrelated one.
4. The rendered boot is repositioned after anatomical ankle solving. Its derived cuff
   then becomes the rendered shin endpoint. This means a geometrically valid knee/
   ankle can still yield a visually distorted leg. Define one consistent painted
   boot-to-cuff calibration and solve against the endpoint actually drawn.
5. A single neutral angle does not establish visible standing alignment. The original
   boot has a long forward toe and its source ankle/contact/cuff differ. Author a
   neutral silhouette with the supporting sole region beneath the torso/pelvis and
   plausible ankle/knee alignment; inspect actual pixels at both facing directions.
6. Initial rendering uses a whole sprite, while subsequent idle rendering uses the
   articulated pieces. The first and subsequent rest silhouettes must agree, or the
   transition can jump even if a mathematical blend has reached zero.

## Acceptance review

Inspect continuous playback first, then slow playback and individual frames. Show
side views first to isolate mechanics, then front/back. Review at least two cycles
and multiple start/stop phases; a single pleasant contact sheet cannot establish
fluidity. Watch planted painted soles, knee speed, cuff alignment, pelvis/feet at
rest, arm reversals, loop wrap and stopping without a foot teleport. Check a full
direction reversal separately. Numerical continuity/contact checks are useful
diagnostics; the owner still decides whether it looks human and preserves Maziss.

Deliver this as an image-guided candidate before studying the uploaded FBX files.
Keep supplied reference imagery outside public assets until reuse rights are known.
