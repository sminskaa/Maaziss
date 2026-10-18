# Painted character geometry and fitting review

Bounded assignment MODEL-002: preserve the supplied walking reference and original
paintings while improving the complete model's silhouette, skinning and equipment
clearance. This is a candidate for visual review, not approval of the final art.

## Changes

- Head, jaw, cheeks, chin and nose now form one smoothly united closed skin surface.
  Neck and ears remain complete separate parts. Original bone coordinates and eye
  centers are unchanged. Eye whites, irises, pupils, lids and brows are reduced
  together around those centers to avoid a protruding ball-eye construction.
- Hair tufts, torso/shirt and belt receive rounded interpolation. Two complete
  rolled sleeve cuffs were added. Tiny separate stubble specks were removed because
  the original portrait supplies its painted stubble.
- A second silhouette pass lowers and rounds the high jacket shoulder caps,
  shortens the tallest hair spikes with a smooth transition from the scalp,
  reduces protruding ears and broadens the throat toward the shoulders. Head,
  eye and skeletal landmark centers remain unchanged for painting registration.
- The anatomical shins now use the same knee skinning transition as the continuous
  trousers. The trouser waist becomes pelvis-bound below the belt, reducing the
  fold that let moving thighs tug through the rigid waist layers.
- The satchel-side arm uses a smooth outward wrist bias and a two-bone inverse
  kinematics solve. Both arm lengths are preserved. Hand and forearm surfaces move
  outside the actual bag/tool extent; their geometry is never hidden or clipped.
- Coincident curve cap seams are welded, and every complete part retains exactly
  one armature modifier. This also repairs curve conversion removing a preceding
  object's skin modifier.

## Evidence

Blender 4.3.2 evaluated the complete geometry in idle and all 36 supplied-cycle
samples. Triangle intersection queries found zero intersections between the
satchel-side hand/forearm and any bag or tool mesh. Maximum arm bone-length error
was below 0.000001 m. The source stride and timing are unchanged.

Separate evaluated-surface queries found no thigh/trouser intersections in those
37 poses. Shin intersections occur only at the deliberately closed trouser-bottom
cap (rest-space height at most 0.210 m, enclosed by a boot shaft reaching 0.280 m).
No knee or exposed trouser-wall intersection was detected in those samples.

All constructed objects passed closed-manifold, single-component and normalized
skinning checks after the fitting hook: 145,468 vertices after the silhouette pass.
These checks establish geometry and sampled clearance, not artistic quality or
collision freedom for arbitrary future animations.

The local check script, evaluated outputs and detailed arrays are in ignored
`build/checks/painted-character/`; original paintings remain unchanged. Projected
painting registration and final rendered preview are owned and reviewed separately
by the coordinator. Complete new viewing angles still require visual judgement:
the original paintings supply a limited set of views, not a full production UV
texture atlas or physically simulated garment system.
