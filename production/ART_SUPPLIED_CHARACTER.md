# Supplied character: art direction and visual review

Assignment ART-007, 19 October 2026. Status: original references and five actual supplied-mesh views inspected; targeted facial work pending. The owner controls likeness approval.

## Accepted target

I inspected the original `art/walking/maziss-depth-atlas.png` and `maziss-side-atlas.png` with the image viewer. These drawings remain the target. The failed painted-model preview is rejected, including the repeated/smeared face. This assignment must not rescue it with more whole-sprite projection.

Maziss's identifying shapes are a large head with messy, asymmetric brown hair; large tired eyes under worried brows; a long projecting nose and tapered jaw/chin; narrow shoulders; a modest forward stoop; slim, slightly loose work trousers and oversized rounded work boots. His face reads as an exhausted adult, not a smiling child or a realistic generic adult. The reference head including hair occupies roughly 23–25% of overall standing height; this is a design guide from a painted pose, not an exact orthographic measurement.

The outfit has its own readable construction: faded teal jacket with lapels and rolled sleeves, mustard shirt, dark brown continuous trousers, work boots, belt, diagonal leather strap and a separate tool satchel at his anatomical right hip. The satchel does not replace a missing section of jacket or trousers. The back view must show the same items, with the strap crossing the back toward that hip.

## Shared art and QA gates

Art and QA must look at actual rendered geometry rather than infer quality from code or passing structural tests.

1. **Recognizable form before paint.** Front, profile and three-quarter neutral renders should have a coherent skull, projecting nose, eye sockets/lids, jaw, hair silhouette and neck. No face billboard, repeating portrait, intersecting head fragments or faceless generic mannequin. A profile must retain the same character, not expose a second frontal face.
2. **Cartoon proportions.** Retain large expressive head, slim torso and legs, gently rounded hands/boots, modest stoop and asymmetry in hair. Smooth contours must not erase the purposeful nose, chin, hair clumps or clothing folds. A smooth sphere is not automatically a good sculpt.
3. **Outfit continuity.** Each visible garment/item remains coherent through motion. Pants do not lose triangles, change limb length independently of the pose, or leave isolated cuffs. Boots overlap cuffs plausibly. Jacket, shirt and bag retain thickness/coverage where limbs reveal them.
4. **Actual camera depth.** Far arm, hand, strap and bag occlude according to geometry and camera position. The hand must remain outside the bag. No floating material fragments or invisible skin pieces are acceptable.
5. **Animation deformation.** Review idle, left/right contact, passing and maximum knee/elbow bend from front, back, both profiles and oblique views. Preserve the useful FBX stride; do not hide problems in a flattering static angle. Check elbows, knees, armpits, crotch, ankle/cuff joins and bag clearance.
6. **Game-art readiness is separate.** A recognizable static mesh is a useful starting asset, not a completed game character. Rig/weights, topology around moving joints, stable normals/materials, coherent UV islands, animation clips, Godot import and in-room scale/lighting must be demonstrated before production-readiness claims.
7. **Paint follows approved shape.** Only after the neutral model reads correctly should deliberate skin/hair/garment regions receive their own materials or UV painting. The face occurs once in its facial region. No complete sprite wrapping or front/back/side portrait blending.
8. **Honest delivery.** Screenshots/video must come from the actual model at declared angles and frames. A newly generated 2D illustration is not evidence of the animated model's quality. Use compact HTML with still/video fallbacks, as established by the owner.

## Review evidence

The first automated intake render failed because the empty Blender scene had no world; this was reported and corrected. I then inspected actual `input-0.png`, `input-45.png`, `input-90.png`, `input-180.png` and `input-270.png`, plus a face closeup rendered from `input-normalized.blend`. These files stay in ignored `build/checks/supplied-character/`.

The supplied mesh is a substantially stronger starting volume than the rejected procedural model: the large messy hair, adult narrow head and projecting nose, jacket lapels/rolled cuffs, separate-looking strap/satchel silhouette and broad boots already identify the intended design. Keep this supplied geometry rather than replacing it with the old generic head/body. Static front, profile and oblique forms are coherent and have no repeated portrait.

The largest likeness block is the blank/sunken eye and mouth region. It needs true three-dimensional eye whites, iris/pupil, restrained lids, worried brows and a small downturned mouth registered to its existing skull. Hair clumps have noisy triangular ridges, hands read as mittens, jacket hems are irregular and boot soles flare/lump. Those are cleanup issues, not reasons to wrap a complete character image over the body. A tiny color or sculpt edit should not be called final hand/facial topology.

Measured against the normalized 2 m model: the head center is approximately X=+0.014 m; chin Z≈1.59 m; nose Z≈1.72 m and front Y≈−0.21 m; eye centers can start around X=0.014±0.065 m, Z≈1.77 m, surface Y≈−0.14 m. These are fitting landmarks, not face replacement instructions. Eyeballs should sit largely inside the skull, with lids following their rim; brows should lift toward the nose to retain his worried expression.

The input qualifies as a rough recognizable static sculpt, not a rigged game-ready character. All motion/deformation/clearance judgements remain pending actual sampled animation renders. Art and QA agree on that boundary.


## Targeted facial geometry study

`tools/character3d_sculpt.py` adds 16 actual geometry objects to the unchanged supplied skull: one eye-white/iris/pupil/catchlight/lid/brow set per side, plus a small closed frown and lower lip. The supplied skull, nose, jaw, ear and hair mesh are not replaced. Eyes sit mostly within the measured sockets, conform to their local curvature and have shallow relief; no image, alpha decal or face billboard is used. The optional shared Head binding is rigid and normalized. Future facial expression controls and facial topology remain separate work.

I rendered and inspected actual front, 35-degree, profile and back closeups from the test scene. The first eye placement protruded and looked like goggles; I rejected it and reduced the depth, conformed the whites to the actual orbit surface and narrowed the lid shapes. The current study reads as a worried cartoon human at these angles and does not repeat the face around the head. It still lacks the painted drawing's weathering, eyelid nuance, subtle cheek/stubble character and final hair refinement. The source's roughness and coarse material boundaries are visible. This is a targeted geometry fitting pass, not a finished likeness claim or owner approval.

Scratch evidence: `build/checks/supplied-character/art/face-{0,35,90,180}.png` and `face-study.blend`; temporary skin/hair partitioning in that test scene is for fitting inspection only. The final integrated body material assignment and motion tests belong to the coordinator and QA.


## Integrated candidate and second eye refinement

I inspected actual integrated `renders/idle-0.png`, `idle-45.png` and `idle-90.png`. The supplied sculpt and new features form a recognizable continuous cartoon character; this is a material/rig study, not the accepted painted finish. The first integrated pass had a stretched bag and source cross-body triangles identified independently by QA; the coordinator is correcting them and they are not art-approved.

Visible material cleanup needs were reported to the coordinator: isolated mustard triangles at the collar/skin boundary, jagged strap-to-shirt boundaries, leather region spill onto upper trousers, zigzag ankle cuff regions, and glossy dark lighting on hair/shirt/boots. Region labels assigned to arbitrary triangles cannot be represented as finished UV/material tailoring. Softer/flatter lighting and a correctly painted material pass remain needed to fit the approved environment.

QA also found the eyes too circular and goggle-like. I changed the actual eye surface so its upper area forms a skin-colored upper lid, narrowed the exposed white to a tired almond shape, reduced iris/pupil size and removed the continuous lower wire-like rim. I rendered and inspected the updated front, 35-degree and profile closeups. Each eye object now has two material slots with deliberate polygon material indices; any export must preserve both. The 16-object interface and source skull remain unchanged. It now reads as more tired and less startled, but subtle adult eyelids, facial weathering/stubble and final likeness remain unfinished.


## Matte integrated render review, manifest 10:04 UTC

I inspected final-generated idle angles 0°, 45°, 90°, 180° and 270°, plus actual walk frames 0°/06, 90°/06, 180°/12 and 315°/18. Continuous vertex colors and matte lighting improve the coarse material boundaries and reduce plastic highlights. Idle reads as one coherent stylized clothed human from these angles, with a single true face and a consistent hair/outfit silhouette.

This particular render set still shows a rearward triangular bag extension in walk-90-06 and thin spikes around the hand/crotch/bag in walk-90-06 and walk-315-18. I reported these exact files to both the coordinator and QA. Walking continuity is therefore **not art-approved on this evidence**; fresh corrected render review is required. Even after repair, the current flat 3D interpretation lacks the approved drawing's inked outlines, material wear, delicate face detail and painterly lighting, so it must be presented as a coherent model/rig study rather than the finished art style.


## Corrected actual-motion reinspection

After the coordinator repaired hand/bag weighting and pose order, I opened fresh `renders/walk-0-06.png`, `walk-90-06.png` and `walk-90-18.png`, then independent QA captures `qa/candidate/walk-90-1.png`, `walk-270-1.png`, `walk-180-3.png` and `walk-45-2.png` (candidate hash prefix `2492dbd8`). The previously reported needle-like triangles and rear bag shelf are absent in these inspected views. Trousers and boot/cuff joins remain visible and coherent; the face remains a single face from front/profile/oblique, with the same source-derived hair and outfit silhouette. QA identified one remaining inner-forearm weight-transition outlier for the coordinator to soften before the final capture.

Scoped art recommendation: suitable to show the owner as a **recognizable supplied-mesh rig study once the final weighting fix is revalidated**, rather than as finished character art. The bag-side arm is deliberately kept in a resting pose because the source mesh joins hand and satchel; disclose that acting constraint. This is a coherent temporary solution, not proper separated hand/bag production topology. The other arm and legs use retained FBX motion.

Remaining style work is substantial: adult facial nuance and tired eyelids, hand/finger form, hair ridge cleanup, precise garment/strap boundaries, original painted wear/ink/material texture and room-matched lighting. A real game-export smoke check or passing geometry statistics cannot approve those artistic details. Owner likeness approval remains pending.
