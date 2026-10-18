# Reassessing the character method

Research date: 18 October 2026. Status: research saved; implementation paused at
the owner's request before a replacement model was started.

The owner rejects the painted 3D candidate as unrecognizable. His face repeats
across the sides and his clothes are mixed up. The original drawings remain the
accepted design; the earlier complete 3D attempt supplies useful movement, not an
accepted likeness. The coordinator acknowledges that the projection approach
failed. Its numerical checks do not change that visual judgement.

## What went wrong

The previous pass sampled front/back/side sprite images over a generic model
whose face, silhouette and clothes had not first been fitted to the drawings.
Those images contain posed limbs, overlapping equipment and already-rendered
features. Blending them across unrelated surfaces repeated faces and transferred
hands or bags into clothes. Local masks could hide individual symptoms but could
not create the missing character design in geometry.

Controlled projection painting is a legitimate later texturing tool. The rejected
whole-sprite projection onto a mismatched character is not an appropriate modeling
method. A recognizable model must be constructed first.

## Sources actually read

The official Blender manual source repository is accessible here even where its
rendered manual pages or individual Studio lessons are not. Source snapshots are
retained in ignored `build/checks/character-rebuild/research/`.

- [Blender: reference image empties](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/modeling/empties.rst).
  The image object can display character sheets in orthographic views while the
  actual model is built separately. References need not become surface textures.
- [Blender: Mirror modifier](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/modeling/modifiers/generate/mirror.rst).
  Symmetry and merged center vertices support coherent initial forms; deliberate
  expression and design asymmetry can follow.
- [Blender: remeshing and retopology](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/modeling/meshes/retopology.rst).
  Voxel remeshing is useful for shaping/sculpt cleanup. The manual expressly warns
  that automatic voxel/quad remeshing does not create final animation topology:
  deformation loops must follow the character's forms and joints.
- [Blender: UV seams](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/modeling/meshes/uv/unwrapping/seams.rst).
  Separate meaningful regions, unwrap, check stretch, adjust seams and manually
  refine. The actual head and garments require designed UV regions; a whole
  character picture is not automatically that layout.
- [Topology Guides](https://topologyguides.com/).
  The accessible homepage includes the full text of “Modeling with Animation in
  Mind” and anatomy examples. Edge loops should align with movement, and problem
  poles should move away from highly deforming areas. The dedicated article URL
  returned 403, so only the accessible homepage text is claimed read.
- [Blender Studio: Stylized Character Workflow](https://studio.blender.org/training/stylized-character-workflow/).
  The public course overview describes design, head/body sculpting, outfit
  construction, expression tests, clean retopology, UVs, shading and presentation.
  Its listed clay/wire turnarounds are useful stage examples. The full course costs
  a subscription; only the public overview was read. No paid lesson/video was
  accessed or claimed watched. Several linked lesson/turnaround pages returned403.
- [Blender: Workbench](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/workbench/index.rst)
  is explicitly intended for fast modeling/animation review rather than final
  production rendering. It can support an honest neutral-shape review.
- [Blender: Toon BSDF](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/shader_nodes/shader/toon.rst)
  is marked Cycles-only. Choose renderer-compatible stylized materials rather than
  assuming every shader works in every rendering engine.

Internet search requests were also attempted. Google returned a redirect page and
Bing RSS returned mostly generic Blender results. These are not claimed as useful
specialist research. The directly accessed authoritative/community sources above
provide the substantive workflow evidence. Failed URLs and raw results remain in
the local research folder. No claim is made to have read every internet resource.

## Free tools considered

The independent [tool/license report](../production/FREE_CHARACTER_TOOLS_RESEARCH.md)
records actual official-source reads for Blender, MPFB/MakeHuman, TripoSR,
Stable Fast3D, TRELLIS, Hunyuan3D2, Instant Meshes, QuadriFlow and Krita.

Blender is already usable on this CPU workspace. MPFB may help anatomical topology
but does not reproduce a cartoon identity automatically. TripoSR has MIT-licensed
weights and a CPU fallback; its runtime/likeness here are untested. Stable Fast3D
has gated model access. TRELLIS needs an unavailable NVIDIA GPU. The specifically
reviewed Hunyuan3D2.0 license excludes the EU, UK and South Korea. Remeshers clean
existing geometry; they do not supply character design. No weights were downloaded,
packages installed, hosted models invoked or paid resources used in this research.

## Chosen next method

1. Register original front/profile landmarks and compare proportions. Resolve
   inconsistent poses/perspective in the drawings rather than treating them as
   exact orthographic scans.
2. Reconstruct skull, cheek/jaw shape, nose, eye placement, worried brows, mouth,
   hair silhouette and neck as real geometry. Review front, side and three-quarter
   views with neutral materials before spending effort on texture detail.
3. Fit the complete outfit: jacket shoulders/lapels/cuffs, mustard shirt, continuous
   trousers, boots, belt, separate strap and satchel. Keep each item coherent.
4. Reuse the useful FBX stride and timing, with the existing bag clearance work.
   Verify silhouette and deformation together; do not change the original drawings.
5. Only after the shapes read as Maziss, create proper UV/material regions and
   paint their colour, ink, cloth wear and scuffs. No repeated portrait projection.
6. Render actual geometry for a compact HTML comparison. Likeness remains an art
   judgement; geometry checks alone cannot approve it.

See `RESUME_CHARACTER_REBUILD.md` for the exact paused state and implementation
handoff. No replacement sculpt or animation is claimed by this research document.
