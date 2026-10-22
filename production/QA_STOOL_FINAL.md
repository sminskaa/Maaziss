# QA-019 — final desk-stool action review

Independent final QA, 20 October 2026. Recommendation: **show this bounded first interaction to the owner**, with the approach-foot limitation below disclosed. The corrected pull/turn/sit and compact offline controls pass this review. This is not finished character art, a general interaction controller, or main Godot integration. Owner creative approval remains pending.

## Actual output inspected

Opened actual composite frames 0, 50, 65, 80, 104, 116, 136 and 156, enlarged contact crops, the corrected `align-final.png`, original stool reference and repaired clean crop. Also ran the actual embedded native movie from Use → highlighted stool click to its end, sampling its advancing clock and opening eight screenshots captured during that playback. Evidence is in `build/checks/stool-interaction/qa-final/` (`actual-motion-contact-sheet.jpg`, `contact-detail.jpg`, `reference-and-corrected.jpg`, `browser-real-motion.jpg`). These are current full-action outputs, not the historical rejected alignment images.

- The stool is visible complete geometry, with seat, legs and ring; it moves from the desk toward Maziss. The pull reads as a reach to the rim, though the broad hand and partial body occlusion do not establish a detailed finger grasp.
- The corrected Right-leading turn keeps the transfer compact; the raised boot is visible instead of the former sole-roll floor failure. The later bend and held endpoint read as sitting, with a stool edge/support visible behind him. Clothing and bag remain coherent through the sampled sequence; no gross clothing explosion, detached limb or obvious seat/body crossing was found.
- Fixed actor proportions and camera maintain room scale through approach and descent. The character occupies the foreground side of the desk, and the visible stool/background ordering is coherent in this authored action.
- The vacated stool location exposes continuous rug/floor and the desk face. No duplicated painted stool, retained painted stool shadow, transparent hole or conspicuous local repair seam was found. The shadow travels with the rendered objects. The local repaired area is still an approximation of the original painting.
- The smoother, muted character/stool surfaces remain visibly less painted than the room. Face, mitten-like free hand, joined bag-side hand, fabric wear and prop paint are unfinished. Endpoint support is sufficient for this first study; exact soft-body contact or production rig quality is not certified.

## Independent scene and artifact evidence

Copied the existing read-only baked-scene audit into `qa-final/audit_scene.py`, changed only its report destination, and ran Blender 4.3.2 against the retained final scene. No scene/model/source edits or rerender were made.

157 evaluated samples are finite. Maximum baked world joint endpoint discrepancy is **0.0000029001 m**. At corrected pivot 5.2 s the lowest body vertex is **+0.0009431 m**; throughout 4.6–7.8 s the audit minimum is **−0.000001342 m**, consistent with numerical tolerance. The former approximately 2.06 cm pivot defect is resolved in this scene. Scene SHA-256: `add771a6e48647d307ef759e6070d15db524d26185949aebfc7950bdb8010072`. Pose SHA-256: `2de1ed08fea8a58d0d57b071d65352e8ddc6ce76d52d0f8c0145d09e46af3d81`.

**Known limitation:** the inherited walking approach still reaches **−0.01633 m at 1.05 s** on the RightFoot sole. The render manifest independently records the same excursion. It is outside the corrected non-walking pivot and small at this preview scale, but a claim of zero floor penetration across the entire action would be false. Fix before accepting production walking/contact quality; it does not prevent owner review of this first stool action.

All 157 PNG hashes match the current render manifest; its scene hash matches the audited scene. Reused frames retain explicit source renderer/pose and prefix-equivalence provenance where applicable. The retained proof states exact full-state equality at 460 samples, 0–4.59 s; its SHA-256 matches the manifest reuse references. This audit verified that retained proof/hash relationship, rather than claiming a new independent rerun of the historical pose comparison. Details: `artifact-audit.json`, `scene-audit.json`, `scene-audit.log`.

Final delivered HTML: `visual-preview/maziss-stool-interaction.html`, **930920 bytes**, SHA-256 **`29e45f1274caf82099af98cd29aa6e91a865aa0cdd14e8bb5d4ad67dcb8e6f24`**.

Movie SHA-256: `18de29f487c220f307a196deda8ee4ab704ee707068118d5bb62ad7c8dd7633c`; ffprobe confirms VP9, 1120×630, 20 fps, 8.850 s including held endpoint.

## Offline browser check

Playwright launched installed Chromium with an offline context and loaded the complete actual HTML with `set_content`; file-URL navigation was not needed. Eleven functional checks passed: initial decoded paused movie; Use selection/hotspot; real playback through all seven displayed phases; advancing movie clock; seated end at 8.85 s; reset to paused frame zero with controls cleared; repeat playback after reset; no horizontal overflow at 390 px; all embedded images decoded; no page/console errors; no HTTP/HTTPS requests. Desktop/native movie and mobile screenshots were opened and inspected. Reproducible probe and observed states: `qa-final/browser_audit.py`, `browser-results.json`, `browser.log`, `browser-mobile390.png`.

These checks establish local Chromium operation and embedded offline assets. They do not prove the host chat preview will open the file or certify every desktop/mobile browser. No public publication or engine integration was performed. Historical `QA_STOOL_INTERACTION.md` describes the earlier unresolved pivot and must not be treated as the current final verdict.
