# QA-FEEDBACK-POSE — isolated ordered turn and desktop reach

2026-10-20. **Current recommendation: HOLD full desk-clearance/contact claims.** Ordered foot/torso targets and fixed proportions pass. Current hand-associated surfaces clear the sampled finite slab, but actual forearm surfaces still cross it. Owner creative approval remains separate; the staging model, appearance, acting, full action and Godot integration are unapproved.

## Evidence and version

Read `AGENTS.md`, the current handoff, `docs/STOOL_DIRECTION_DECISIONS.md`, the new pose/renderer and shared pose/application helpers. QA inspected actual initial eight room-camera geometry images and nine alternate-camera opaque-desk diagnostic images. These earlier renders revealed a conspicuous backward arm flare and left-surface/desk merging. They have been superseded as pose candidates and are **not final visual evidence for the current numerical revision**. Final follow-up: inspected `build/checks/stool-feedback/review-contact-sheet.jpg`, containing the current nine paired room composites and opaque-desk diagnostic renders for pose `5c809b…`, presented by `visual-preview/maziss-stool-pose-test.html`. This satisfies the bounded actual-image check for the checkpoint, not full motion/contact approval.

Latest numerical candidate: pose SHA-256 `5c809b5247a61f1cac43230e6976d2c8ebda0569c76af6131b7de6676e29b64d`; bound `probe-scene.blend` SHA-256 `a297731d6df193f019887759702508adea646acde204d8c6e5154523b819e3f4`. Preserved original scene SHA-256 `f239b41c1657d351534ee46e31f07b9eb890759697c6ce16e02ec8eb547fe12a`. All private evidence is under `build/checks/stool-feedback/qa/`.

Independent source-versus-bound-scene audit compared every mesh's exact rest coordinates/topology and all rig rest head/tail/matrices: identical, with no changed objects (`binding-preservation.json`). The isolated binding modifies weights; it does not change rest geometry or bone proportions. QA did not save over either source model/scene.

## Ordered seated turn and proportions

Independent Blender sampling at 40 Hz over 0–6 s (241 samples) applies the shared renderer function and measures targets plus actual evaluated pose-bone lengths. Evidence: `check_feedback.py`, `pose-numerics.json`.

- Right foot changes during 0–0.65 s, with left foot fixed. Right ankle moves +0.030 m and toe +0.062 m along screen-right/world +X, with an intermediate lift.
- Left foot changes during 0.80–1.45 s, after the right finishes. Left ankle moves +0.254 m along +X.
- Torso/root yaw and head change only during 1.65–2.40 s, after both feet finish: 135° to 90°. Head follows torso; independent head acting is not claimed.
- Maximum target bone-length drift is 0.000000229 m; evaluated pose-bone drift is 0.000000590 m, consistent with floating point tolerance. No stretching was detected.

The original actual pose images made the right boot movement followed by torso turn visible; left-foot movement was subtler because of overlap/perspective. Numeric sequencing passes. No boot/seat pressure or physical-dynamics pass follows from fixed bone lengths.

The jump after 3 s remains a separate-test cut, including feet/stool/root. The current reach test also proposes moving stool/body 0.28 m farther from the desk than the preceding fit and reducing lean from 15° to 5°. Those are explicit fitting hypotheses for review, not approved changes to the full occupied slide.

## Evaluated finite-slab surface audit

QA clips actual evaluated mesh triangles against the fitted finite tabletop polygon and interior `0.8705 < Z < 0.9295`, allowing 0.5 mm at each horizontal surface. A triangle is included if any vertex has >0.65 Hand or ForeArm influence, and a second count requires all three vertices to satisfy that threshold. The clipped surface area must exceed 1e-12 m². This catches crossings missed by checking vertex locations alone. Latest sampling: **200 Hz, 3.005–6.000 s, 600 samples**. Evidence: `check_hand_triangles.py`, `hand-triangle-probe.json`; final forearm debugging: `debug_forearm.py`, `forearm-final-debug.json`.

For this candidate, both hand-associated triangle regions have zero sampled slab intersections, including wrist-adjacent triangles. Final strongly hand-weighted vertices over the top bottom out at Z≈0.934925 m, approximately **4.925 mm above the desktop** for both hands. This is clearance of that region, not exact palm resting contact.

Right forearm-associated surfaces are clear in all 600 samples. **Three Left forearm-adjacent skin triangles still intersect** late in placement: 47 consecutive samples from 5.770–6.000 s, at most three triangles per sample. No >0.65 forearm vertex and no triangle with all three vertices >0.65 forearm weight is inside, but these mixed-weight boundary surfaces are still part of the visible body. At 6 s, triangles `[4165,4144,4094]`, `[4094,4144,4143]`, `[4094,4102,4165]` on `Maziss supplied sculpt` cross the slab. Vertex 4094 evaluates to `(0.03288,0.19873,0.91805)` with approximately 0.535 Spine/0.431 LeftForeArm/0.034 LeftHand weighting; vertex 4102 is `(-0.05904,0.21934,0.89549)` with 0.704 Spine/0.296 LeftForeArm. These connect to strongly forearm-weighted vertices above the desktop. Evidence: `debug_final_boundary.py`, `final-boundary-debug.json`, plus these persisted diagnostic values. This supports a remaining left torso/sleeve-to-arm boundary deformation issue, not a core palm penetration.

**Checkpoint decision:** sampled hand clearance passes for the stated surface region; full visible arm/body clearance and final resting contact remain HOLD. Do not erase the failing boundary triangles by narrowing the weight filter. No additional fixes or expensive renders were requested by QA after the owner indicated approximately 10% allowance remained. The final candidate's proposed extra separation, lean, palm orientation and lap tuck have now been inspected in the paired contact sheet; they remain proposals rather than owner-approved fitting or acting.

## Resolved diagnosis from earlier revisions

The original left hand had inherited Hand/Thigh mixed weights. A >0.65 hand-vertex probe missed penetrating lower hand skin connected to strongly hand-weighted vertices. For example source left vertices 4208/4209 had approximately 0.53/0.51 Hand weight and 0.47/0.49 Thigh weight. `left-patch-classification.json` records exact rest positions, influences and bone distances. They lie in the established free-arm region used by `prepare_stool_right_arm.py` to construct the independent mirrored right arm.

The coordinator created a separate study binding with shoulder taper; `left-arm-binding.json` records 385 rebound vertices. Original rest geometry is preserved. That fix removed the earlier mixed hand/thigh surface failure. A later 40 Hz probe found a brief lift crossing at 4.125–4.150 s missed by the 20 Hz vertex probe; subsequent path changes cleared sampled hands and most forearm surfaces. The latest revision adds a lap tuck during the first test to address its earlier forearm encroachment; QA’s final 200 Hz surface probe covers the separate reach test only, so no full-first-test surface-clearance pass is claimed. These earlier issues are diagnostic history, not passes for current boundary skin or acting.

## Scope

QA changed only this report and private diagnostics under `build/checks/stool-feedback/qa/`; no source or model edits. No full render was initiated by QA. Discrete sampling cannot guarantee continuous clearance. The audit excludes the 0.5 mm surface tolerance and does not cover every upper-arm/body/prop collision. No full action, boot-floor, satchel-seat, desktop-item, playback or Godot validation is claimed. Final current-candidate room-composite and diagnostic visual inspection is complete for the nine supplied paired poses only. Continuous playback and unsampled surfaces remain outside this check.

## Final current-image check

The nine paired room/diagnostic images match the scoped numerical HOLD. A1→A2 shows the right boot changing while torso/head retain their heading; A2→A3 shows the other boot following; A4 then turns torso/head screen right. The room view makes the ordered foot changes more legible than the opaque desk angle, which hides much of the boots. **A may be shown separately for owner review of sequence**, without claiming final contact, acting or model approval.

B1/B2 show a separate seated setup rather than the intervening slide. B3 still flares the arms outward/backward; the visible hand reads broad and rigid. B4/B5 raise the elbows prominently and show thick curled/mitten-like hand shapes. This remains rough acting despite improved sampled clearance. The desk and props obscure part of the far arm/palm in the room view; the diagnostic angle helps expose the surface but cannot visually negate the three measured left sleeve/torso boundary crossings. Endpoint hands appear placed over the top, while the measured roughly 4.9 mm vertex gap and mixed sleeve triangles prevent an exact resting-contact pass.

**Final checkpoint recommendation unchanged: A sequence is reviewable; B and the full corrected action remain HOLD.** No new numerical runs, renders or source edits were made for this follow-up image check.
