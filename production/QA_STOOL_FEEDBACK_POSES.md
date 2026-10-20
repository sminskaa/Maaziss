# QA-FEEDBACK-POSE — isolated ordered turn and desktop reach

2026-10-20. **Current recommendation: HOLD full desk-clearance/contact claims.** Ordered foot/torso targets and fixed proportions pass. Current hand-associated surfaces clear the sampled finite slab, but actual forearm surfaces still cross it. Owner creative approval remains separate; the staging model, appearance, acting, full action and Godot integration are unapproved.

## Evidence and version

Read `AGENTS.md`, the current handoff, `docs/STOOL_DIRECTION_DECISIONS.md`, the new pose/renderer and shared pose/application helpers. QA inspected actual initial eight room-camera geometry images and nine alternate-camera opaque-desk diagnostic images. These earlier renders revealed a conspicuous backward arm flare and left-surface/desk merging. They have been superseded as pose candidates and are **not final visual evidence for the current numerical revision**. Updated room composites and diagnostic images are pending.

Latest numerical candidate: pose SHA-256 `66d3c9c7c4e7294ec66802676aa48fa145bf5e82efd02cd51bf495f2d8649b40`; bound `probe-scene.blend` SHA-256 `6a4ff16b54bed8c18fc7a3ab74d577dd0a820a7bab9438e20ee82f48729e3b72`. Preserved original scene SHA-256 `f239b41c1657d351534ee46e31f07b9eb890759697c6ce16e02ec8eb547fe12a`. All private evidence is under `build/checks/stool-feedback/qa/`.

Independent source-versus-bound-scene audit compared every mesh's exact rest coordinates/topology and all rig rest head/tail/matrices: identical, with no changed objects (`binding-preservation.json`). The isolated binding modifies weights; it does not change rest geometry or bone proportions. QA did not save over either source model/scene.

## Ordered seated turn and proportions

Independent Blender sampling at 40 Hz over 0–6 s (241 samples) applies the shared renderer function and measures targets plus actual evaluated pose-bone lengths. Evidence: `check_feedback.py`, `pose-numerics.json`.

- Right foot changes during 0–0.65 s, with left foot fixed. Right ankle moves +0.030 m and toe +0.062 m along screen-right/world +X, with an intermediate lift.
- Left foot changes during 0.80–1.45 s, after the right finishes. Left ankle moves +0.254 m along +X.
- Torso/root yaw and head change only during 1.65–2.40 s, after both feet finish: 135° to 90°. Head follows torso; independent head acting is not claimed.
- Maximum target bone-length drift is 0.000000383 m; evaluated pose-bone drift is 0.000000590 m, consistent with floating point tolerance. No stretching was detected.

The original actual pose images made the right boot movement followed by torso turn visible; left-foot movement was subtler because of overlap/perspective. Numeric sequencing passes. No boot/seat pressure or physical-dynamics pass follows from fixed bone lengths.

The jump after 3 s remains a separate-test cut, including feet/stool/root. The current reach test also proposes moving stool/body 0.18 m farther from the desk than the preceding fit and reducing lean from 15° to 5°. Those are explicit fitting hypotheses for review, not approved changes to the full occupied slide.

## Evaluated finite-slab surface audit

QA clips actual evaluated mesh triangles against the fitted finite tabletop polygon and interior `0.8705 < Z < 0.9295`, allowing 0.5 mm at each horizontal surface. A triangle is included if any vertex has >0.65 Hand or ForeArm influence, and a second count requires all three vertices to satisfy that threshold. The clipped surface area must exceed 1e-12 m². This catches crossings missed by checking vertex locations alone. Latest sampling: **200 Hz, 3.005–6.000 s, 600 samples**. Evidence: `check_hand_triangles.py`, `hand-triangle-probe.json`; final forearm debugging: `debug_forearm.py`, `forearm-final-debug.json`.

For this candidate, both hand-associated triangle regions have zero sampled slab intersections, including wrist-adjacent triangles. Final strongly hand-weighted vertices over the top bottom out at Z≈0.94210 m, approximately **12.1 mm above the desktop** for both hands. This is clearance of that region, not exact palm resting contact.

Forearms still fail: Left forearm-associated triangles cross in 280 samples, including the start and endpoint; Right crosses in 48 samples from 5.765–6.000 s. At the endpoint Left has 117 crossing triangles/32 strictly interior core forearm vertices and Right 74 triangles/27 core vertices. Entirely forearm-weighted triangles intersect, so this is not merely a generous hand-region classification.

Concrete examples: left source vertex 4272 is 100% LeftForeArm at rest `(0.311,0.092,1.046)`, evaluated near `(0.084,0.255,0.906)`; right-arm vertex 32 is 100% RightForeArm at rest `(-0.282,0.054,1.045)`, evaluated near `(0.131,-0.049,0.917)`. Both lie in the finite slab. A hand-only clean probe cannot establish clear arm placement. Raise/reposition actual evaluated forearm surfaces and rerun, while retaining plausible acting.

## Resolved diagnosis from earlier revisions

The original left hand had inherited Hand/Thigh mixed weights. A >0.65 hand-vertex probe missed penetrating lower hand skin connected to strongly hand-weighted vertices. For example source left vertices 4208/4209 had approximately 0.53/0.51 Hand weight and 0.47/0.49 Thigh weight. `left-patch-classification.json` records exact rest positions, influences and bone distances. They lie in the established free-arm region used by `prepare_stool_right_arm.py` to construct the independent mirrored right arm.

The coordinator created a separate study binding with shoulder taper; `left-arm-binding.json` records 385 rebound vertices. Original rest geometry is preserved. That fix removed the earlier mixed hand/thigh surface failure. A later 40 Hz probe found a brief lift crossing at 4.125–4.150 s missed by the 20 Hz vertex probe; subsequent path changes cleared sampled hands. These earlier issues are diagnostic history, not passes for current forearms or acting.

## Scope

QA changed only this report and private diagnostics under `build/checks/stool-feedback/qa/`; no source or model edits. No full render was initiated by QA. Discrete sampling cannot guarantee continuous clearance. The audit excludes the 0.5 mm surface tolerance and does not cover every upper-arm/body/prop collision. No full action, boot-floor, satchel-seat, desktop-item, playback or Godot validation is claimed. Final room-composite visual inspection remains pending.
