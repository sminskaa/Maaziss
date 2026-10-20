# QA-020 — rear boarding and desk-facing stool revision

Independent QA, 20 October 2026. Scope: the separate compact offline review; original accepted stool action remains preserved. **Recommend showing this bounded revision to the owner.** Actual image, native movie, baked-scene and offline-control gates pass with the inherited limitations below disclosed. No Godot integration or writing is claimed.

## Actual image gate

Opened the actual raw endpoint `key-230.png`, composed room keys 113, 127, 141, 155, 169, 183, 210 and 230, their room contact sheet, and the full room endpoint. Evidence: `build/checks/stool-desk-facing/qa/key-room-contact-sheet.jpg`.

The new route visibly takes Maziss around the back of the stool before turning toward the actual far-right writing desk and paper. The endpoint reads as sitting, with the stool rim beneath his pelvis and complete legs/ring visible. Back, coat, satchel and boots stay recognizable in these samples, with no detached body part or gross garment split. No obvious boot/stool crossing appears in these sampled keys. The clean floor/rug/desk area remains coherent, without a duplicate painted stool, old isolated shadow or visible hole. The actual native movie was subsequently played from Use to its end, with 97 advancing clock observations and 12 captured movie images opened as `qa/actual-native-motion-sheet.jpg`. The rear route, final turn and seated hold remain coherent in this output; no gross boot/stool crossing, body split, duplicate prop, exposed old shadow or repaired-floor hole was observed. The paired route steps look deliberate and slightly mechanical, and the circling takes longer than a polished performance; this is an authored study rather than finished natural acting.

The desk-facing endpoint provides a plausible starting direction for future writing; this does not certify hand-to-paper reach, writing posture or actual desk collision geometry. The room is a painted plate with rendered character/stool, not a complete collision-modeled room. Smooth surfaces, mitten-like hand, joined bag-side hand, stiff acting and character palette remain inherited first-pass limitations.

## Independent baked-scene audit

Ran read-only `qa/audit_scene.py` on frozen scene SHA-256 `c7d018036b92ede5d4cf396348ba7e3d7f0da9b6700a5acec34b720dd4ce1192`, pose SHA-256 `e925600b2691e9ec342e151f0e3b7e05bf938e9ca27470a08d10dd4e22044436`. All 231 evaluated mesh samples are finite, with maximum world bone endpoint error **0.0000028993 m** versus fresh authored targets. Independently compared all complete authored states at 460 samples from 0 through 4.59 seconds: exact equality to the original action. The new phase floor minimum is approximately **−0.0000012844 m at 6.3 s**, consistent with numerical tolerance.

The inherited approach still reaches **−0.01633044 m at 1.05 s**, the disclosed original boot-floor overlap. This revision does not fix it; do not claim zero penetration throughout. Bone targets and floor bounds do not establish exact skin/seat contact or continuous visual quality.

An initial provisional audit read an older bake during a source/bake transition and reported a 9.7 cm mismatch. That result is superseded: the hash-coherent frozen-scene rerun above resolves it and is the retained current evidence. No final defect is inferred from that transient mismatch.

## Evaluated boots versus actual stool surfaces

Read-only `qa/boot_clearance.py` independently evaluated 139 samples, 4.6–11.5 s, against each actual seat, leg and ring mesh. It selected 293 Left and 302 Right boot vertices with over 95% Foot weighting and corresponding fully selected triangles. No triangle edge crossings were detected; the smallest boot-vertex-to-stool-surface gap was **0.0278568 m at 4.75 s**, Left boot versus leg 1. This substantiates sampled boot clearance beyond ankle-marker distances.

These are discrete 20 fps checks on selected boot polygons. Vertex-to-surface distance is not exact global mesh separation, the edge test excludes coplanar overlap, and no continuous collision/physics or garment-to-seat guarantee is claimed. Intended pelvis/seat contact was assessed visually, not rejected as collision. Evidence: `qa/boot-clearance.json` and `.log`, bound to the same final scene hash.

## Final artifact and offline movie gate

`qa/artifact_audit.py` verifies all **231** final rendered PNG hashes, final scene/source hash consistency, and all **92** rendered prefix hashes before 4.6 s matching the original action. This complements the independent complete-state prefix comparison above. The previous stool review remains separate and preserved.

Final HTML: `visual-preview/maziss-stool-desk-facing.html`, **918447 bytes**, SHA-256 `8212067b1806a5b9b158079195118dfe85737ae30f941dae21b170702384ce0f`. Native movie duration is **12.55 s**, including the held endpoint. Evidence: `qa/artifact-audit.json`.

Actual Chromium playback in an offline context passed all **11** checks: initial decoded paused movie, Use hotspot, advancing playback through all eight displayed phases, desk-facing seated endpoint, reset to paused frame zero with selection/hotspot cleared, repeat action after reset, 390 px layout without horizontal overflow, decoded embedded images, no JavaScript/console errors and no HTTP/HTTPS requests. Opened the actual movie contact sheet and mobile screenshot. Probe and observed states: `qa/browser_audit.py`, `browser-results.json`, `browser.log`, `browser-mobile390.png`.

This verifies local offline Chromium behavior, not the host chat renderer or every browser. Final game work remains offline desktop Godot; this revision implements neither writing nor main-game integration. Owner creative acceptance remains final.
