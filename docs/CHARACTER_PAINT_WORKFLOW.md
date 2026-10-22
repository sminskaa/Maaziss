# From the drawings to an animated cartoon character

**Historical rejected attempt.** The owner rejected this projection candidate on
18 October2026 as distorted and unrecognizable. It is not the recommended next
method. Read `CHARACTER_REBUILD_RESEARCH.md` and `RESUME_CHARACTER_REBUILD.md` for
the geometry-first replacement plan and exact allowance-pause checkpoint.

The current approach builds complete body and garment surfaces, binds them to a
shared skeleton and attaches paintings to their rest surfaces. Camera depth
determines overlap. Separating complete items avoids the old sprite-mask holes;
it does not automatically produce the original drawing's likeness.

This pass rounds the underlying forms, unites facial forms, shrinks protruding
eye features and adds rolled cuffs. The hand beside the satchel uses fixed-length
arm IK around the real bag envelope. Anatomical shins now share the trousers'
knee weights, preventing the two surfaces from bending differently. The FBX gait
remains the movement reference. See `production/CHARACTER_FIT_REVIEW.md`.

Actual original portrait, trouser, boot and bag drawings supply surface colour.
A newly prepared front/side/back clothing painting removes baked equipment so
the actual separate strap and bag remain single objects. Source transparency
falls back to opaque pigment; it never cuts away clothes. Fixed coordinates
prevent the textures from being repainted according to a walking limb's angle.

This is a first registered painting pass, not a finished production character.
A proper next art step is a dedicated clean turnaround, explicit UV islands and
seam painting, plus more deliberate facial sculpting and hand/garment tailoring.
The current multi-view projections demonstrate the direction and expose the
remaining fit issues. The original paintings remain the target and are preserved.
No final game engine or offline delivery decision has changed.

The browser review also uses a soft pixel mask on the main skin surface where
the original painting contains eyes and ears: those features have their own
modeled parts, and painting them again behind those parts creates doubled contours.
This is a presentation cleanup, not a discontinuous UV jump or a transparent mesh
hole. The authoring file retains the packed source paintings and complete UV maps;
its basic material nodes do not yet reproduce that browser-only cleanup exactly.
Both trouser legs reuse the unobscured original cloth panel because a hanging hand
and bag cover the corresponding other panel in the source drawing.

## Free resources actually consulted

Consulted 18 October 2026. The Blender manual HTML site returned HTTP403 in this
environment; its official source repository was accessible and read instead.
These are software instructions, not evidence of model training or a watched class.

- [Subdivision Surface](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html):
  Catmull-Clark changes the silhouette; smooth normals alone do not.
  [Official source read](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/modeling/modifiers/generate/subdivision_surface.rst).
- [UV unwrapping](https://docs.blender.org/manual/en/latest/modeling/meshes/uv/unwrapping/introduction.html):
  registration links image coordinates to mesh surfaces.
  [Official source read](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/modeling/meshes/uv/unwrapping/introduction.rst).
- [Texture painting](https://docs.blender.org/manual/en/latest/sculpt_paint/texture_paint/introduction.html):
  paint or project references onto UV-mapped geometry and refine seams in 3D.
  [Official source read](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/sculpt_paint/texture_paint/introduction.rst).
- [Inverse Kinematics](https://docs.blender.org/manual/en/latest/animation/constraints/tracking/ik_solver.html):
  position an end effector through a connected chain and control stretching.
  [Official source read](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/animation/constraints/tracking/ik_solver.rst).

Blender is free and already installed here. No new purchased assets, subscriptions
or paid voice service were required. The supplied raw references, derived motion
and generated model/HTML review outputs remain private local build artifacts.
