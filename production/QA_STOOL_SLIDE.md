# QA-021 — right-hand pull, short sit and occupied stool slide

Checkpoint, 20 October 2026. **HOLD: first combined keys reveal boot/stool crossings and contact defects; corrected final motion is pending. No release recommendation.** The owner rejected the preceding circling-step candidate. Its prior technical QA does not establish creative acceptance. This assignment covers the replacement: anatomical Right hand pulls while Maziss is left of the stool, a compact sit, Right hand grips the seat during occupied slide toward the desk, and both hands finish on the desk. Writing and Godot integration remain outside scope.

## Required actual-output gates

- Inspect the changed character's real Right arm, continuous satchel and shoulder/hand transitions. Arm independence must be visible in actual moving geometry; changing bone targets alone cannot repair fused hand/bag topology.
- Open combined room renders at Right-hand pull, compact boarding, seated slide start/mid/end and two-hand desktop endpoint. Check actual anatomical hand identity, seat contact, occupied co-motion, boots/stool/desk clearance, hands on the writing desk, recognizable character and clean repaired background.
- Play the final native movie via Use, inspect captured advancing output, then verify endpoint, reset, repeat and offline/mobile operation. No code-only visual pass.

## Planned independent scene checks

Use the frozen final scene/source hashes. Compare baked world bones to fresh targets and inspect finite evaluated geometry/floor minima at every authored frame. Track the seated pelvis/support landmark relative to the stool center throughout occupied translation, and the actual Right grip landmark relative to the seat rim while grip is held. Contact invariants apply during declared contact intervals, not intentional reach/release.

For the endpoint, measure both evaluated hand/palm surfaces against the desk support plane and projected writing-surface polygon. Screen y combines world Y-depth and Z-height with the fixed 23-degree camera: a bone endpoint placed on an arbitrary plane can still appear floating or embedded in the painting. Verify actual palm shape/orientation and depth against the actual composited paper/near edge. The painted desk is not automatically complete collision geometry.

Reuse the prior evaluated boot/stool surface audit with the new rig and motion, avoiding assumptions that old Foot weighting/topology are unchanged. Allow intended pelvis/seat contact. Surface sampling does not certify continuous physical collision or cloth simulation. Any inherited approach-floor overlap must be measured/disclosed rather than assumed fixed.

## Current evidence and blockers

Character-only diagnostics and first combined action keys/bake have been reviewed as recorded below. Corrected final scene, continuous native movie and offline controls remain pending.

## Character-only checkpoint

Opened all six actual Art diagnostics (`art/arm-{rest,reach}-{0,65,135}.png`) together as `qa/actual-right-arm-diagnostics.jpg`. The anatomical Right arm visibly moves independently while the satchel remains a continuous recognizable bag. No gross shoulder gap, detached hand or leftover duplicate hand is evident in these views. The reconstructed arm remains broad and mitten-like, with preliminary cuff/shoulder seams. This clears local readiness for combined action keys only; it does not establish stool grasp, seated motion or desktop contact. Art reports closed topology and isolated motion, but QA has not independently reproduced that topology/displacement check yet.

## Provisional frozen-key scene/contact audit

Current key bake SHA-256 `f52e1159e2b314240215939b8ead7d5d14043f21d83f3bc8d696e7bce41ab46e`, pose `bec53198d6dc755334f541d45c42bf86d47eefb69486f969088bfce998be9135`: 177 evaluated samples finite, maximum baked world bone discrepancy 0.0000033831 m. The separate Right arm is included in the finite-mesh audit. The first key bake body minimum is −0.00968294 m at 1.4 s, weighted to LeftFoot during the changed approach. It is a current measured limitation rather than an assumed unchanged original-prefix result. Visual severity remains to be assessed in final motion.

Independent contact probe: seated authored seat-marker error at most 0.0000000619 m; held Right-grip bone-tip error at most 0.0000005413 m; closest evaluated Right-hand vertex stays within 0.0145033 m of the declared grip landmark. These establish the baked contact invariants, not finger wrapping or exact soft seat contact.

**Endpoint concern sent to coordinator before full render:** both evaluated hand selections (>80% Hand weighting, 107 Left/119 Right vertices) reach z=0.904096 m against desk height 0.93 m, approximately 2.59 cm below the support surface. Correct bone-tip placement at z=.956 m does not resolve actual palm skin fit. Their lowest vertices project inside the writing-desk region, near (1476,556) and (1517,589). Actual endpoint images must determine visibility/severity; raise or reorient the contact if needed rather than relying on holdout to hide it. No final desktop-contact pass is made. Evidence: `qa/contact-audit.json`/`.log`.

## New boot/stool clearance blocker

The independent actual-geometry audit of the same first key bake detects boot/stool surface crossings, including approach Right boot versus leg 4 from 1.2 s and both boots versus the bracing ring during/after the occupied slide. Across all 177 samples there are 33,423 intersecting triangle edge pairs; that count is mesh-tessellation dependent and is not a count of distinct visible defects. The per-frame/object evidence is retained in `qa/boot-clearance.json`.

Opened actual `room-key-148.png`, `room-key-176.png` and raw `key-176.png`: the seated boots look cramped and intertwined with stool geometry, consistent with the independent crossings. Keeping both boots fixed while moving the stool toward the desk brings the legs/ring into them. Sent coordinator a blocker before full render: change planted foot positions/step support or slide path/distance, then rerun geometry and actual combined visual checks. Raising final hands alone does not resolve this separate defect.

Coordinator is already raising final hand endpoints and rebaking for the earlier desk-skin issue. The first key audit does not certify any subsequent scene; each new final candidate must be bound to current hashes and rechecked.

## Revised candidate checkpoint

Revised key bake `e37b80b727f50e896b9b21993217849fcf443eb6430e8d8d965407b18190d68a`, pose `b6da525a972a6edadc16180a8f4665c27b04864d31f700a5f6bb454ca9da5ab5`: 177 evaluated samples finite; maximum baked bone error 0.0000040076 m; floor minimum −0.0050429 m. Authored seat-marker and held Right-grip invariants remain within numerical tolerance.

**Improved but still HOLD:** occupied-slide and final boot/stool crossings are resolved in this sampled candidate. However, 3,231 triangle edge pairs remain during approach 1.3–1.5 s and pull/boarding 2.65–4.15 s. A nearest-surface-normal check finds a Right boot vertex approximately 0.01916 m inside leg 3 at 4.1 s, so the remaining result is not just tangency. The root was notified before final render. Correct the earlier foot/path contacts and rerun the full interval.

Raised endpoint hands no longer put the >80% Hand-weighted selections below the desktop: selected minimum z is 0.947096 m Left and 0.933096 m Right. Left high-weight finger selection is about 1.71 cm above the plane; lower-weight wrist contact and visible palm pose still require the unobscured actual final view. This selection alone neither proves whole-hand clearance nor establishes a visibly resting palm. No final desktop-contact pass or full-motion pass is claimed.

## Audit synchronization checkpoint

A later provisional audit caught another active bake transition while the coordinator revised the foot arc/IK. Its scene/source snapshots differ and it is not final evidence; no contact or clearance verdict is based on that mixed run. Retained `*-first-key.json` and `*-revised-key.json` preserve the earlier coherent candidates. Wait for the coordinator's explicit frozen-key completion before the next audit. Final motion and offline controls remain pending.

## Latest frozen key review

Scene `03c70d1e39cf07b6a2c432aabe8838c0e85ca72ee5b5a52bc83a9aa14214ef28`, pose `bac5d4ba04791d8b7912fa047e20814b38a7ffa919f810582ae56679be877761`: opened seven actual room keys at 1.4, 2.8, 4.1, 4.4, 6.3, 8.1 and 8.8 s, combined in `qa/frozen-keys-room-sheet.jpg`. This restaging makes the boarding visibly shorter and more direct; recognizable body, bag and complete stool stay coherent in these samples. The clean room patch remains intact. The end faces the real writing desk, though the body/desk hide much of the palms. At 8.1 s the Left arm visibly raises sideways before reaching the desk; continuous movie/unobscured hand view is still required to judge that transfer.

The independent frozen-scene audit has 177 finite samples, maximum world-joint discrepancy 0.0000034518 m and body minimum −0.0095900 m. Seat-marker and held Right-grip bone invariants pass numerical tolerance. Actual grasp wrapping/skin fit remains an image/surface gate rather than a bone-target pass.

**Remaining clearance HOLD:** 2,891 boot/stool crossing triangle pairs remain at 1.1–1.2 s and 3.05–4.05 s, all involving Right boot versus leg 3, leg 4 or the bracing ring. Later slide/end surfaces clear this sampled check. The same frozen-bake boot check against the fitted desk finds 2,733 edge-crossing pairs with `Desk / far leg`, across 1.3–5.5 s; none against the cabinet/tabletop. The far-leg proxy's fit to the painting should be verified before changing motion solely to avoid it.

Earlier nearest-normal “inside” distances depend on mesh winding and must not be treated as certified penetration depth. Surface-edge intersections establish the crossing finding independently. The auditor is being strengthened with orientation-independent ray parity for actual closed-surface inside distances. No final pass is made.

The orientation-independent closed-mesh ray-parity rerun confirms the latest frozen candidate has a Right boot vertex 0.0177123 m inside stool leg 3 at 3.25 s and a Left boot vertex 0.0422587 m inside the fitted desk far leg at 5.1 s. These supersede the winding-dependent distance interpretation for this candidate. The triangle-crossing counts and final scene hash remain unchanged. Coordinator notified audit complete; source may now change for correction.

## Corrected desk-fit / nearly clear candidate

Scene `8326324040b6b14f230e61d7528505b2d7690435d03af3144892d359d15a4837`, pose `f5587773c688b89ba87930abae01e012501d2483d6d817fb9e27fcee68670799`: all 177 samples finite, max baked joint error 0.0000035899 m. Current approach floor minimum is −0.0103431 m at 1.1 s, LeftFoot. Contact invariants remain within numerical tolerance.

The formerly invented far leg is replaced by the fitted actual painted diagonal brace. Whole-clip boot/desk-proxy check now detects **zero** crossing pairs, with nearest sampled boot vertex 0.0817403 m from the brace. This resolves the earlier proxy crossing finding for this fitted geometry.

Opened eight current actual room keys (1.15, 2.8, 3.25, 4.1, 5.1, 6.3, 8.1, 8.8 s), saved as `qa/final-keys-room-sheet.jpg`. The short direct boarding and supported seated endpoint read coherently; the Left arm now reaches forward at 8.1 s rather than lifting sideways. Clean background, character/bag continuity and complete stool remain intact in these samples. Unobscured final palms and actual full movie remain pending.

**Still HOLD:** Right boot/leg 3 crossings remain from 3.05 through 3.85 s, 434 triangle edge pairs total. Ray parity confirms a boot vertex 0.0151973 m inside leg 3 at 3.2 s. Approach and all samples from 4.0 s onward now clear the boot/stool test. Root notified to correct this last pull-foot interval before full-motion gate. Exact evidence archived in `qa/*-832632.json`.
