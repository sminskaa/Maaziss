# QA-022 — resumed stool-slide final review

20 October 2026. **HOLD for final native movie/control review; corrected frozen-key geometry and image checks clear.** This report continues QA-021 in [QA_STOOL_SLIDE.md](QA_STOOL_SLIDE.md); previous key-scene findings do not establish a pass for the resumed candidate.

Scope: actual anatomical Right-hand pull from the stool’s left, short direct sit, occupied body/stool co-motion with Right seat grip, and both hands resting on the desk. No writing or main Godot integration is covered.

The saved candidate `8326324040b6b14f230e61d7528505b2d7690435d03af3144892d359d15a4837` still had Right boot/leg 3 crossings at 3.05–3.85 s, 434 intersecting triangle pairs and a ray-parity-confirmed inside vertex at 3.2 s. Its actual desk-proxy check cleared. Art also identified the pull-interval bag/seat contact to correct. Those are retained blockers until the corrected candidate is frozen and inspected.

Independent scripts have been prepared in private `build/checks/stool-slide/qa-resume/`, with outputs separate from the previous evidence and scene/source hash guards. No resumed audit has run while authoring is active. Required remaining gates are the explicit frozen-scene audit, actual current room and unobscured palm images, current full native movie, Use/reset/repeat and offline/mobile controls.

## First resumed frozen audit

Root explicitly froze scene `9e16256b39a083efbc88dc15be6a43b0b1775c27db2e970353d91b7a87423e68` and pose `5418f084dc7ae9891e9135f15e3931d20abb6641268410a0c5e4339ccfce0731`. Independent read-only checks evaluated all 177 authored samples. All actor meshes are finite; maximum baked world-joint error is 0.0000036731 m. Approach floor minimum remains −0.0103431 m. Seat marker and held Right-grip errors remain below 0.0000006671 m; nearest selected Right-hand vertex to grip reaches at most 0.0145033 m.

**Boot clearance remains HOLD:** the actual baked scene produces 709 intersecting boot/stool triangle pairs at 3.0–3.85 s, all Right boot versus leg 3. Orientation-independent closed-mesh ray parity confirms a Right boot vertex 0.0163402 m inside leg 3 at 3.05 s. This differs from Art’s in-memory proposal result; the frozen scene/source match and target errors are small, so no pass can be inferred from that proposal. Coordinator and Art notified immediately.

The independent evaluated bag selection (349 vertices identified from original local YZ coordinates) has no seat-inside vertex deeper than 0.5 mm in all 177 samples. This clears the measured bag/seat vertex concern for this candidate, subject to actual image review. Surface crossing checks remain sampled and do not certify continuous collision or exact mesh separation.

Evidence is retained separately in `build/checks/stool-slide/qa-resume/`: `scene-audit.json`, `contact-audit.json`, `boot-clearance.json`, `bag-seat-audit.json`, their scripts/logs and frozen source/scene snapshots. The current desk-hand endpoint still needs refreshed final acting/contact and actual movie review. Root notified audits complete and source may change.

The Art proposal discrepancy was traced to a stale rig-world inverse while the animated actor root changed, and omission of the renderer’s explicit planted-foot sole orientation. Equal bone head/tail coordinates did not establish equal skinned boot geometry. Art is correcting its search application to match the real renderer; no final render is authorized by this QA checkpoint. Failed audit outputs were archived with `-pre-resume-correction` suffixes.

## Corrected frozen scene — scoped key gate cleared

Current scene `e3df556e2207972d8f346d6b0ae8e59624b0995aae64611cbeec7e507bf46ba3`, pose `95f60d2ef89f423a123c696d809495e0ca6026c41e5cac500cac07708b82c2ec`. All five independent audits completed coherently on the root-frozen candidate. All 177 samples are finite, maximum baked world-joint error is 0.0000033570 m, and approach floor minimum remains −0.0103431 m.

The evaluated boot/stool check now finds **zero triangle crossings and zero inside vertices** across all 177 samples; smallest sampled vertex-to-surface gap is 0.0047497 m at 4.7 s, Right boot versus bracing ring. The whole-clip fitted desk-proxy check also finds zero crossings and zero inside vertices; minimum boot vertex gap is 0.0817403 m to the painted diagonal brace. The 349 selected bag vertices have no seat-inside vertex deeper than 0.5 mm. These resolve the measured pull clearance defects in this frozen candidate. Discrete surface/vertex checks do not establish continuous physics or exact global separation.

Seated landmark error is at most 0.0000000667 m; held Right-grip bone error at most 0.0000004579 m. Nearest selected Right-hand vertex reaches at most 0.0145036 m from the declared grip. This measures authored occupied co-motion/grip consistency; exact finger wrapping is still limited by mitten geometry.

Opened all eight actual current combined room keys at 2.8, 3.05, 3.2, 3.4, 4.25, 6.85, 8.1 and 8.8 s in `qa-resume/corrected-room-keys.jpg`, plus Art’s new unobscured `art-resume/corrected-final-palm-contact.png`. The pull is performed by the anatomical Right hand with Maziss left of the stool. Boot and stool remain visibly separate in the previously affected interval; the compact route leads directly to the seat, with coherent occupied slide and a complete stool. Bag, recognizable silhouette and repaired background stay coherent in these samples; no duplicate stool or exposed patch hole is evident. The final arm correction lowers the sideways elbow. Both rounded mitten hands read as supported at the desk in the alternate view; articulated flat fingers/palms are not present. Art’s current >65% Hand selection independently reports hand minima 0.931226 m Left and 0.933096 m Right over the 0.93 m tabletop, with no selected vertex below the plane.

This clears the corrected frozen-key gate for final native motion review. The full current movie, artifact binding and Use/reset/repeat/offline/mobile checks remain pending, so there is no final release recommendation yet.

## Final-bake geometry binding

The full-render bake is `f239b41c1657d351534ee46e31f07b9eb890759697c6ce16e02ec8eb547fe12a`; source remains `95f60d2…`. A read-only exact comparison of every evaluated actor, Right-arm, stool and desk world vertex (32-bit position) and polygon topology at all 177 frames matches the independently audited `e3df556…` key bake byte for byte. This binds the above clearance results to the full-render scene without repeating unchanged triangle checks. Evidence: `qa-resume/compare_geometry.py`, `geometry-binding.json` and `.log`. It does not replace the pending native-movie review.
