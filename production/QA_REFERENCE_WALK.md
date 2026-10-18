# QA-005 — human-reference walking revision 5

**Recommendation: ready for owner review in the HTML panel.** Production integration and creative approval remain pending.

The final frozen build passed **62 focused browser checks**, with no failed checks or JavaScript errors. This covers the separate HTML study; the main Godot game was unchanged.

## What was reviewed

- Actual Chromium-rendered animation in left, right, toward-camera and away-camera views, with eight paused phase captures per view.
- The first character artwork, original proportions/posture and restrained synchronized arm movement.
- Measured reference data: owner recording `Video Projectbiks.mp4`, frames 36–78, a 1.4-second cycle, 24 sampled poses and the closing pose. Private recording frames are excluded from review artifacts.
- Loaded forefoot placement, articulated trouser/boot joins, forward-plane knee movement, pause/idle behavior, slow playback and source-frame stepping.
- Real room traversals, wall rejection, furniture detours, a scaled-canvas mouse click and operation with browser networking disabled.

## Findings addressed during review

1. Exact-opposite heading interpolation initially prevented a Right-to-Left reversal. Angle interpolation and the final Left-view check confirm the correction.
2. A planted logical toe initially allowed the painted boot to slide because its source transform pivoted around an approximate ankle. The final renderer registers an actual opaque forefoot sole point, source pixel `[380,417]`, to the planted contact and computes the trouser cuff from the same transform. Heel/forefoot alignment uses the original drawing's geometry; release after lift-off is blended.
3. An exact-equality idle test detected floating-point trig roundoff around 1e-13 scene pixels. The final test checks numerical fields with a strict 1e-9 tolerance and retains exact identities, booleans and structure. No visible residual idle movement was found.

## Final evidence

- Build identity: `56d1b9cb1e5660fb5468f395eb6919d9ae7942527ffaec2bcd609f6b7bb3a154`.
- Reviewed HTML SHA-256: `6aeb751402d2122e0d365886c2d845c4fc365dd566c7873f9642690db6e6a60a`.
- Browser: Chromium 154.0.8037.57.
- Checks: 62 passed, 0 failed.
- Recorded root substeps: 2398; each respects independently checked room geometry and clearance.
- Straight-traverse rendered gait samples: 212.
- Loaded contact sequence after heading alignment: left, right, left, right, left, right.
- Maximum logical loaded toe drift: 0 scene pixels.
- Maximum painted loaded forefoot drift: 0 scene pixels.
- Maximum painted-contact registration error: 0 scene pixels.
- Maximum settled idle numerical delta: 0.
- All four views close the measured cycle after exactly 42 source-frame button steps.
- All reviewed source hashes and the HTML output hash remained unchanged throughout the run.

`tests/browser_reference_walk.py` produces `build/checks/reference-walk/browser-results.json`, actual phase screenshots, `contact-sheet.html` and straight-traverse pose evidence. Source identity is recorded in `build/checks/reference-walk/build-manifest.json`.

## Visual assessment and remaining limits

The side-view sequence now has a recognizable contact, passing and swing progression, with heel rise and alternating leg roles. The original character remains recognizable. The previous sideways knee kicks and gross trouser/boot separation were absent in the reviewed phases. After the forefoot correction, side-view loaded contact follows the visible sole point rather than an abstract ankle alone.

Front/back motion uses a shallow projection and flat original boot drawings. Its shoe rotation, depth cues, torso twist and weight shift remain simpler than a fully drawn directional animation. The motion source is one visible near-leg cycle from an oblique 2D recording; the far leg uses a half-cycle offset, and foot pitch/ground position are fitted estimates. These approximations remain open to the owner's visual judgment.

These checks establish continuity, animation controls and room routing. They do not assign a score for human naturalness or confer the owner's creative approval. Full-body occlusion and final Godot integration are outside this study.

The internally served HTML made only its document request, and an embedded copy animated with browser networking disabled. Direct `file://` navigation was blocked by managed Chromium with `ERR_BLOCKED_BY_ADMINISTRATOR`; direct local-file opening therefore remains unverified in this browser environment. No platform policy was changed.
