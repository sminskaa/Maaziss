# Closed body and clothing construction study

MODEL-001 — native worker `/root/model_body_rig`, 18 October 2026.

The owner's latest request changes construction strategy: visible body parts,
clothes and equipment should exist as complete objects under every camera angle.
`tools/character3d_body.py` implements actual closed three-dimensional anatomy and
clothing. It does not sample, cut, mask or warp the approved character pictures.
The original approved painted art remains the target for later art refinement;
this geometric study is not a replacement style proposal or finished production art.

## Interface and construction

`build_body()` returns `{armature: BlenderObject, objects: [BlenderObject, ...]}`.
Coordinates: X anatomical left, Y rear, Z up; character faces negative Y. All mesh
vertices are in rest/world coordinates and object transforms are identity. The
module exports `JOINTS` and the coordinator-agreed bone names. Head, eyes, mouth,
hair, neck and satchel are coordinator-owned additions.

The study provides 22 separate closed skinned meshes:

- Body core and independent upper arms, forearms, hands, thighs, shins and feet.
- One continuous welded pair of trousers, including the waist, crotch and both legs.
- One continuous thick open-front jacket, including the torso and both short sleeves.
- Complete shirt, belt and buckle.
- Separate complete left/right leather boots and soles.

The jacket uses a closed thick C-section shell so the shirt is visible through the
front opening; it has real inner and outer surfaces. Voxel unions weld the sleeves
into that shell and both trouser legs into the waist. Skinning blends the jacket
through the shoulders/elbows and trousers through the hip/knee regions. Underlying
closed anatomical surfaces overlap at joints. Trouser cuffs overlap boot shafts.
A standalone rest-pose render was inspected and used to correct coat/shirt clearance
and sleeve coverage at the shoulders. Objects are marked `category='anatomy'` or `'clothing'` for inspection toggles.

## Actual validation

Blender 4.3.2 built the module successfully. The final body module generates
**27,118 vertices across 22 meshes**. The generated local report is
`build/checks/character3d/body-validation.json` (ignored build output).

For every mesh the validation measured:

- Exactly one connected component and zero non-manifold edges.
- Every vertex has a normalized nonzero bone-weight sum within 0.001 of 1.
- Exactly one armature modifier, linked to the returned skeleton.

These are topology and binding checks, not evidence that every animated pose is
artistically correct. The coordinator must inspect animation and angle-dependent
occlusion in the integrated preview. Closed geometry eliminates source-mask holes;
it does not automatically eliminate interpenetration or every skinning artifact.

Reproduce locally in Blender:

```sh
blender -b --python-expr "import sys,json; sys.path.insert(0,'tools'); from character3d_body import build_body,validate_body; print(json.dumps(validate_body(build_body()),indent=2))"
```

## Limits

This is a modest-polygon cartoon construction mesh with plain named materials,
not sculpted or hand-painted game art. Hands are simple palms with thumbs; individual
fingers and garment seams/buttons/creases remain later work. Anatomy segments are
separate closed meshes with overlapping joints rather than one unified skin mesh.
The boots currently follow foot bones rigidly. The belt has an interior cap hidden
inside the waist. There is no cloth simulation, collision solver, production facial
rig or claim of release readiness. A later artist pass should refine silhouette,
proportions, fabric detail, skin tones and material texture while retaining the
closed construction and coherent occlusion of this study.

## Focused skin/garment overlap correction

An actual FBX phase near one quarter-cycle was rendered with the integrated target
bone transforms and linear skinning. A small pale patch at the waist was isolated
by temporarily hiding individual objects in diagnostic renders: hiding BodyCore
left the patch, while hiding Thigh removed it. The covered upper-thigh cap extended
slightly beyond the remeshed trouser waist. Its radius was reduced from 0.075 to
0.063 units, and the thigh's weights now use the same hip/knee influence function
as the enclosing trousers. Upper arms likewise use the jacket's influence function
at the shoulder/elbow instead of a rigid single-bone assignment.

The corrected phase render, with **all anatomy visible in the scene graph**, no
longer shows that waist skin patch. No production visibility workaround was used;
bone coordinates, outer garments and overall dressed silhouette are unchanged.
Actual local render: `build/checks/character3d/body-hip-correction-phase025.png`.
This focused inspection does not replace the coordinator's complete camera/phase
review of the assembled head, body and bag.
