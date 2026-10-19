# QA-017 — geometry-only stool study

19 October 2026. Independent QA; one focused model/review-page pass. Scope is the separate stool candidate, not room integration or character animation.

## Recommendation

**Proceed to owner review of the corrected geometry-only candidate.** Reinspected all three corrected actual renders and independently reimported the final GLB. Solid seat, four legs and continuous hoop remain recognizable; no visible open attachment gap remains in the corrected underside view.

The initial independent import found a 9.35 mm seat/leg separation (seat underside Z 0.508000016 m; leg tops Z 0.498654544 m). This was blocking. The coordinator corrected the construction and regenerated the views. Final leg tops reach Z 0.524660885 m, overlapping the seat's vertical bounds by 16.66 mm; feet are at floor Z within 0.00000005 m. Bounds alone do not certify joinery, but together with actual underside reinspection they resolve this observed gap for the scoped study. Historical evidence remains in `qa/import-before-fix.json`.

## Actual visual inspection

Viewed `build/checks/stool-study/stool-reference.png`, `room-angle.png`, `rear-angle.png`, and `underside.png` directly with the image tool, then inspected desktop and mobile browser screenshots. The rounded solid seat, four splayed legs and closed circular hoop make this recognizable as the source stool. Rear and underside views expose complete hidden surfaces; no missing seat cap or broken hoop is apparent. The dark underside makes small attachment gaps difficult to judge by eye, so the independent import measurement is a meaningful additional check.

The model seat rim reads thicker and more regular than the painted source, and the legs/hoop are cleaner and more symmetrical. These are proportion/style limits to retain for owner review, not a finished painted-art claim. Base colours are preliminary as permitted by the brief. Exact dimensions and camera calibration are estimates.

## Browser and model evidence

- Offline Playwright/Chromium 154: all five embedded images decode, including the three actual model views, source crop and expandable room image. Zero external HTTP(S) requests and zero page errors.
- Inspected layouts at 1280×1000 and 390×844: readable source/model comparison; three desktop columns stack vertically on mobile; no horizontal overflow.
- Clicked the final actual GLB download and checked downloaded bytes against the model file and `model-manifest.json`; all three SHA256 hashes match: `5e4754e37cbf1e4764f32c80b50e9a6e6bf365865766f4ead7d351d59c1e713c`. Final HTML is 552,020 bytes, SHA256 `9c1bac72668f5ca9d2b9239726a68b852cce512b7f2062e4f723012e35acc960`.
- Independent Blender 4.3.2 final GLB import: six mesh objects, each with UVs, finite coordinates and no zero-area polygons. The focused attachment recheck passes as described above. The separate Blender file exists (SHA256 `ab326fcdacb76c3907d1199525bdbdcc6ec26b1d538d2d0392072cee060abb3b`); QA did not independently reopen it.
- This managed browser rejects direct `file://` navigation (`ERR_BLOCKED_BY_ADMINISTRATOR`). Browser checks therefore loaded the exact saved HTML bytes through Playwright `setContent` with the context offline. This verifies self-contained content and download behavior, not the owner's host preview delivery or an installed desktop/browser platform.

Evidence and repeatable probes: `build/checks/stool-study/qa/check-review.cjs`, `check-import.py`, `browser-results.json`, `import-before-fix.json`, `import-results.json`, `desktop.png`, `mobile.png` and `import.log`. Evidence is private generated output. The pre-fix import report's `pass` field covers its original basic mesh assertions, not seat contact.

## Limits

No room replacement, reconstructed background, movement, seat/body contact, character animation, Godot import/runtime or production release is tested or approved. No fresh art/render generation was performed by QA. Art's separate actual-image recommendation and the owner's creative acceptance remain separate gates. Only this note and QA probes/evidence were written.
