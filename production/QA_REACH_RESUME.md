# QA-REACH-RESUME — bounded desktop reach

2026-10-21. **Current sampled arm-region clearance PASS; exact resting contact and finished visual anatomy remain HOLD.** Assignment is limited to the resumed isolated reach. The A foot-order poses are frozen; existing art, acting, full action and Godot integration remain unapproved.

## Historical boundary diagnosis

Read project instructions, current handoff, `docs/STOOL_DIRECTION_DECISIONS.md` and `production/QA_STOOL_FEEDBACK_POSES.md`. Historical evidence remains in `build/checks/stool-feedback-checkpoint-20261020/`; QA did not rewrite it. The old audit found three triangles crossing during 5.770–6.000 s, despite clear strongly hand-weighted regions. This is a real visible mixed-weight surface failure within that historical pose, not a reason to remove triangles from checks.

QA opened the preserved original `build/checks/stool-slide/stool-interaction.blend` and old bound checkpoint `probe-scene.blend` read-only. Exact rest coordinates, original/bound weights and one-ring neighbors are in `build/checks/stool-feedback/qa-resume/boundary-rest-diagnosis.json`; reproducible extractor: `diagnose_boundary.py` in that directory.

The three recorded triangles are `[4165,4144,4094]`, `[4094,4144,4143]`, `[4094,4102,4165]` on `Maziss supplied sculpt`. Their five vertices are:

| Vertex | Rest XYZ (m) | Bound Spine / LeftForeArm / LeftHand |
|---|---|---|
|4094|0.256118, −0.025826, 0.965079|0.534940 / 0.430866 / 0.034193|
|4102|0.251524, 0.004678, 1.002654|0.703723 / 0.296277 / 0|
|4143|0.259127, −0.046806, 0.958311|0.423454 / 0.503672 / 0.072874|
|4144|0.265910, −0.025526, 0.968644|0.201006 / 0.758509 / 0.040485|
|4165|0.265197, 0.003207, 0.969410|0.221474 / 0.742518 / 0.036008|

These vertices sit inside the study binding's lateral `smooth(.24,.28,x)` torso-to-arm transition, below the shoulder taper. Neighbor 4004 at X=0.2398 has 0.973 Spine weight; neighbor 4166 at X=0.2690 has 0.872 forearm weight. Thus connected triangles span a sharp change from torso-following to arm-following skin over roughly 3 cm. The historical deformation stretches these transition surfaces between the moving forearm and stationary torso. Core hand clearance cannot establish clearance of that skin.

**Minimal repair recommendation:** first reassess the same surfaces under the new fixed anatomical elbow pole. If they still cross, revise a smooth, anatomically defined sleeve/torso transition patch, including its one-ring neighbors, so the arm-side skin moves coherently and the torso-side attachment stays gradual. Move the blend toward the torso only as far as the connected sleeve region warrants; verify nearby torso deformation and preserve all triangles/rest geometry. A small local rest-shape or arm separation adjustment may be more honest if the shared sculpt has no separable sleeve region. Exact replacement weights are not established by this diagnosis. Do not reweight just the five indices to satisfy a slab test, delete faces, or narrow the collision filter.

## Frozen resumed candidate: independent numerical audit

Pose SHA-256 `bfc3114daf95ff99e1c371e4e7fe4b98dcca78ff35419f8e5275908cae5280dd`; bound probe SHA-256 `413ec64d47198287bd88a05a5f860b17a9fc455d59e42dd6427ed08b9d1fb8f1`. Frozen scene, pose and result copies are retained in `build/checks/stool-feedback/qa-resume/clearance-bfc3114d/`. Do not apply this pass to a later scene, modifier or pose revision without a new audit.

The coordinator widened the connected sleeve transition with a smooth local height field and replaced the time-varying elbow pole with a constant anatomical side pole. The hand path now gathers near the lap before lifting. QA did not implement these changes.

QA independently clipped evaluated triangles against the fitted finite tabletop polygon and inner slab `0.8705 ≤ Z ≤ 0.9295 m`, excluding 0.5 mm at the top/bottom. Clipped area must exceed `1e-12 m²`. The audit covers 600 samples at 200 Hz from 3.005–6.000 s; 3.000 s belongs to the separate A hold. It includes:

- Every triangle incident to a vertex with >0.65 Hand or ForeArm influence, comparable with the historical check.
- Every triangle incident to *any* Hand or ForeArm influence >1e-8, reported separately so the revised weight transition cannot escape the original threshold.
- All three historical boundary triangles regardless of current weights.

**Zero slab intersections** in every category at all 600 samples. The inclusive region contains 932 body triangles and 683 separate right-arm triangles. No strongly weighted hand/forearm vertex entered the slab either. Evidence: `qa-resume/check_hand_triangles.py`, `hand-triangle-probe.json`, `audit.log`. Pose/scene/helper hashes were unchanged before/after the run.

Endpoint strongly hand-weighted vertices over the desk bottom out at Z=0.93492478 m (left) and 0.93492484 m (right), approximately **4.925 mm above the desktop**. This is not exact palm resting contact. Sampling and weighted surface regions cannot prove continuous clearance or clearance of every upper-arm, torso, prop or furniture surface.

Independent A preservation check compares complete state dictionaries, including every target, root, stool and phase, against the checkpoint pose at 40 Hz over 0–3 s: **121/121 exact identity**. Across 241 samples over 0–6 s, all 14 target and evaluated rig-bone lengths stay within floating point tolerance; maximum target drift 0.000000229 m and evaluated drift 0.000000590 m. `pose-preservation.json` records each bone. Independent exact rest-coordinate/topology and rig-rest comparison with the preserved original scene is identical with no differing objects (`binding-preservation.json`). This establishes fixed proportions/rest geometry, not physical pressure/contact.

## Actual image inspection and recommendation

QA initially inspected the two-pose opaque-desk preview at 4.5/6.0 s (image hashes `9885e4ad…`, `c1175b6f…`); its retained privately composed sheet and image manifest remain historical preview evidence. Backward arm flare is reduced and elbows lie closer to the body. At the endpoint the near hand still reads as a curled lump, the far hand hooks down, and the far sleeve/torso forms a broad stretched panel with a dark underside wedge. Improved sampled slab clearance does not resolve these visible anatomy/acting defects. The table/props also obscure portions of the far hand.

QA also generated and inspected `qa-resume/current-paired-sheet.jpg`, using the two manifest-hash-verified current pose renders, preserved room-clean plate and exactly the existing compositor scaling/offset. `image-review-manifest.json` records the input image hashes. The room composites confirm the reduced backward flare and remaining curled/hooked hand silhouettes and stretched far sleeve; painted props obscure some contact edges. These are two actual paired poses, not a complete intermediate image sequence. Any later skin-modifier candidate requires its own numerical audit and actual-image check. **The frozen candidate passes the stated sampled clearance audit; exact palm resting contact, relaxed hand anatomy and finished sleeve deformation remain HOLD.** A target preservation passes, but no new A surface/contact approval is implied. No full continuous action or owner creative approval is claimed.

QA changes only this report and private diagnostics under `build/checks/stool-feedback/qa-resume/`; no model/source edits, full renders or Godot work.

## Final full image artifact check

QA then opened the final current `build/checks/stool-feedback/review-contact-sheet.jpg` containing all nine paired room/diagnostic poses and separately opened full-resolution `diagnostic-370.png` and `diagnostic-540.png`. The nine room-view inputs and nine diagnostic PNGs all match their manifest SHA-256 values. Pose source remains `bfc3114d…`; bound probe remains `413ec64d…`. The final image-binding evidence is `qa-resume/final-image-binding-check.json`; final sheet SHA-256 is `f2dfcdcb99c769f15012f22765c650969ddb3e64acdf3c86c2c281587c6b3354`. Final PNG hashes differ from the earlier two-pose preview, so the earlier image hashes must not identify this final render set.

A1–A4 still show the ordered boot changes and subsequent torso/head turn. B2 (3.7 s) gathers the hands near the lap rather than raising them behind the body; the near wrist/hand remains rigid and downward curled. B3 keeps the elbows closer to the body than the historical flare. B4 (5.4 s) visibly carries the hands above the desktop, but accentuates the far shoulder/sleeve's broad triangular stretched panel and hooked hand. B5 retains the same curled/hooked endpoint silhouettes. The room view makes the direction readable while obscuring some contact edges; the diagnostic view exposes these remaining deformations. No additional visually obvious desk crossing was identified in these images, which does not extend the numerical audit beyond its stated region and sampled times.

**Final recommendation unchanged:** scoped sampled clearance and A preservation pass; the corrected route can be shown as an unfinished direction checkpoint. Exact palm resting contact and convincing relaxed hands/sleeve anatomy remain HOLD. No numerical audit was repeated for this artifact-only check. No dual-quaternion or smoothing experiment was integrated into this assessed candidate.
