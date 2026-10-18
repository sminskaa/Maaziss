# QA-007 — image-guided walking revision 6

**Recommendation: ready for another owner comparison in the HTML panel.** This
does not approve naturalness or production integration. The final frozen build
passed 48 scoped browser checks with no failed checks or JavaScript errors.

This is an image-only animation study; no FBX or owner-video motion was imported
by this QA assignment.

The owner rejected revision 5 for jerky movement, abrupt knee extension and resting
feet displaced from the torso. The relevant checks therefore cover complete
start/stop transitions and neutral alignment as well as the repeating cycle.

## Review method

`tests/browser_image_walk.py` exercises the actual embedded HTML renderer, captures
eight poses in each direction, checks neutral sole placement, and samples the
embedded gait class deterministically at 120 Hz through starting, walking,
settling and idle. A separate 240 Hz steady-cycle sample reports knee angular
speed and minimum bend. Root navigation, pause, playback timing and browser
network-disabled execution receive scoped regression checks.

The suite also interrupts a partially settled pose and switches fully active
room/study modes. It verifies that upper-body blend resumes from its current
weight instead of suddenly dropping toward zero. The coordinator identified and
corrected this additional arm/torso transition discontinuity during final review.

Technical bounds detect teleports and abrupt angular changes. They do not certify
natural human movement. Rendered side and depth-view poses require visual review;
creative acceptance remains with the owner.

## Findings and final visual assessment

The first candidate retained Maziss's original painted appearance. In the rendered
idle pose the boots were below the hips rather than extended ahead of the body.
The side-view key poses were more coherent than revision 5, while front/back views
still showed substantially less apparent knee and arm motion.

The initial candidate's late-swing knee speed reached approximately 567 degrees
per second. Despite continuous joint positions, this rapid extension could still
read as a snap. QA reported the finding to the coordinator before final review;
the coordinator revised swing-clearance timing, shoe-roll support and leg-reach
softness before the final frozen build. The final deterministic measurement is
374.39 degrees per second. This reduction is an engineering comparison, not a
human-motion quality score.

QA inspected eight actual rendered poses in each of the four directions, six
painted starting frames, six painted settling frames, initial and post-route idle,
and twelve separately captured poses from the actual `#detail` canvas. The side
sequence shows clearer alternating contact, passing and swing, with the source
boots attached to the trousers. No gross source-mask gap was visible in these
captures. Starting leaves the neutral pose progressively; settling returns both
feet underneath the pelvis without an immediate pose replacement. The original
body, head, bag and character proportions remain recognizable.

Front/back movement is still visibly stiffer than side movement: shallow knee
projection, flat original boot drawings and restrained upper-body movement limit
its weight shift and depth cues. Directional artwork changes and full torso twist
remain approximate. Those are material limits for the next owner comparison,
not reasons to call this finished animation.

## Final evidence

- Build: `cdeb0051479636cb524fbd3d70a8d314991295fa9328963d2d063f6dbf9d1bf3`.
- HTML SHA-256: `1ce88dd76c34a693e13b7bb1cb73dc17bb540d12677312878f2c212a9995cadb`.
- Browser: Chromium 154.0.8037.57.
- Result: 48 checks passed, 0 failed; 0 JavaScript runtime errors.
- Initial sole-base displacement from the pelvis: at most 5.32 scene pixels.
- Maximum cuff movement per deterministic 120 Hz transition step: 7.23 pixels.
- Maximum knee-angle change per deterministic 120 Hz transition step: 3.52 degrees.
- Maximum steady-cycle knee speed at 240 Hz: 374.39 degrees per second.
- Minimum steady-cycle knee bend: 18.92 degrees; no straight-leg IK singularity.
- Maximum painted flat-sole drift across 125 observed loaded-stance pairs:
  0.00245 scene pixels during aligned straight traversal.
- Initial, stand-after-study and arrived idle poses were checked; paused study and
  paused room movement freeze the complete pose.
- Interrupted settling resumed from blend 0.892626 to 0.892653; fully active
  room/study/room switching retained blend 1 throughout.
- Playback, five-cycle frame-step timing, furniture routing and wall rejection
  passed. The browser made only its HTML document request, and a separate embedded
  copy animated with browser networking disabled.
- Reviewed runtime source and HTML hashes remained unchanged throughout the run.

`tests/browser_image_walk.py` produces
`build/checks/image-walk/browser-results.json`, actual pose/transition PNGs and
`qa-contact-sheet.html`. Additional closeup captures used for visual review are
under `build/checks/image-walk/detail-review/`. These generated review artifacts
remain outside source control.

## Limits

- No claim of naturalness follows from joint joins, finite positions, or a passing
  numerical suite alone.
- The source drawings and runtime projection remain a 2D puppet approximation,
  especially in front/back views and direction changes.
- The Godot game and final animation integration are outside this HTML study.
- Direct local-file navigation is blocked by managed Chromium policy. The suite
  checks an embedded copy with browser networking disabled instead.
