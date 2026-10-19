# Painted room interactions: research and first stool trial

Research performed 19 October 2026. Documentation was fetched and read directly
from official project sources. This is a researched plan, not a completed stool
extraction, working new model, tested external generator or passed visual gate.
Private source snapshots and fetch status are in
`build/checks/room-interactions/research/sources.json` (ignored by Git).

## Recommended construction

Use a fixed-camera scene with the painted room, separately movable props and
selected geometry for contact/depth. A full new 3D room is not necessary to test
one stool. Some props can remain layered 2D images; turning doors, a pulled-out
stool and handheld items benefit from actual complete geometry. Choose per action.

For each movable object, author two assets: a complete background showing what
was covered, and a separate prop. The clean background must remove the old object
**and its baked shadow**. Removing pixels or placing a model over the existing
painted stool is insufficient. The original image cannot supply hidden floor,
desk, backsides or underside surfaces; those must be reconstructed and reviewed.

Preserve the original and make a local edited candidate. A masked image-editing
tool can propose missing background; Krita clone/heal painting is another route.
Check floorboard perspective, grain, seams, desk legs and lighting, not just whether
the hole is filled. Keep the rest of the scene stable; broad scene regeneration
can introduce unrelated visual changes. Future image editing should use the
available image-editing tool when applicable, with the source image provided.

Match a fixed camera and prop scale to the room before texturing. The painted
room is stylized and need not obey a single perfect perspective camera everywhere;
check local seat, floor and desk landmarks rather than assume an exact recovered
camera. Model the stool seat, all legs/braces and hidden surfaces. Smooth edges
and deliberate irregularity should preserve its cartoon design.

Paint a designed UV layout with wood grain, edge wear and colour appropriate to
the room. Selected source detail can guide local projection, but projection from
one view cannot texture unseen faces. Do not repeat the rejected whole-character
projection approach. Once registered, freeze/bake object-local texture coordinates:
a moving object must carry its paint instead of sliding through a live projector.

Separate contact shadows and occluders from the static background. Desk edges and
legs may need foreground layers or simple depth geometry so the stool can pass
behind them. Use depth testing where appropriate; disabling it everywhere would
make overlap depend on drawing order. Do not darken an already painted shadow
again without comparing the result. Move collision/hotspot geometry with the prop.

## First bounded trial, then a gate

1. Preserve current working room/character review. Work in a separate private
   stool study; do not overwrite the baseline.
2. Save a reference crop/mask and identify the stool's silhouette, contact points,
   colour, desk foreground and old shadow. Confirm what the source actually shows.
3. Produce a stool-free local background candidate. Show this alone for inspection
   so an overlaid stool cannot hide mistakes. No transparent or empty patch.
4. Build a simple complete stool in Blender using measured primitive/mesh forms;
   compare neutral front/side/oblique views and the original camera view. This is
   feasible to attempt with Blender/Python on CPU; visual fidelity is unproven until
   the actual trial. No external generative service is required for simple geometry.
5. Paint and composite at its original pose. Compare original/replacement at the
   same scale, camera and room lighting. Fix shape/material mismatch before motion.
6. Move it a short distance near the desk (including the slightly-behind-desk
   position the owner suggested), with shadow and depth order following. Do not
   introduce character sitting or writing in this trial.
7. Deliver compact HTML with original, clean background, replacement-at-rest and
   moved views plus actual motion. Check the entire movement and return/reset.
8. Art and independent QA review the same retained images/clip. Both must recommend
   proceeding; unresolved holes, duplicates, seams or perspective errors fail the
   trial. Record evidence and limitations before applying the method to another prop.

## Later interaction state

Keep objects and scene state separate: `book_on_shelf / held / inventory`,
`paper_attached / falling / landed / collected`, `door_closed / opening / open`.
These are proposed implementation states, not new story facts. At the grasp frame,
transfer one object to a hand attachment; at collection, update inventory and room
visibility together. Avoid two copies or deletion before the hand reaches it.
Interrupted actions, reset and save/load must not duplicate or resurrect items.

Use layered props over a shared clean background instead of generating a complete
room image for every combination of removed objects. For an opening door/window,
also build what becomes visible through and behind it. Cloth rug and falling paper
may use a simple deformable mesh rather than rigid transformations alone.

Switching off a lamp needs a coherent painted-light change. Changing a Godot light
cannot remove warm highlights baked into a flat background. Plan a reviewed dark
background/light layer plus matching character/prop light, preserving any remaining
window/city glow. A uniform black overlay alone is not a lighting solution.

Facial work can use eyelid/mouth shape keys and eye/gaze transforms, after checking
the supplied face topology. Clothing/boots need deliberately painted texture maps;
render sharpening cannot invent lost seams, folds or scuffs. Diagnose blur with
actual source PNG versus decoded video versus displayed canvas at the same size;
check alpha fringes and sofa occlusion separately before selecting a fix.

## Sources actually consulted and what they establish

- [Blender camera manual](https://docs.blender.org/manual/en/latest/render/cameras.html):
  perspective gives depth-dependent scale; orthographic keeps parallel lines and
  apparent size. Useful for choosing and fitting a presentation camera.
- [Blender UV Project](https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/uv_project.html):
  camera projection follows perspective/orthographic settings; low-poly perspective
  projections and vertices behind the camera have documented limitations. This is
  a local texture tool, not automatic reconstruction of hidden surfaces.
- [Krita Clone Brush Engine](https://docs.krita.org/en/reference_manual/brushes/brush_engines/clone_engine.html):
  clone source paint onto another area, with a healing mode. Its documented
  perspective-correction feature is currently disabled; do not promise that feature.
- [Godot SpriteBase3D](https://docs.godotengine.org/en/stable/classes/class_spritebase3d.html):
  alpha blending can have sorting problems; alpha discard has harder edges; opaque
  prepass supports smoother overlap. Settings need actual frame inspection rather
  than a universal transparency toggle. Sprite3D supports textured layers in 3D.
- [Godot BaseMaterial3D](https://docs.godotengine.org/en/stable/classes/class_basematerial3d.html):
  filtering/mipmaps affect sharpness and distant grain; alpha depth prepass differs
  from simple blending. These are diagnostic options, not proof of a blur fix.
- [Godot animation tracks](https://docs.godotengine.org/en/stable/tutorials/animation/animation_track_types.html):
  transform, blend-shape and method tracks support object motion, facial morphs and
  timed state changes. Method-track events do not run in editor preview; test in
  actual runtime, particularly item collection.
- [Godot BoneAttachment3D](https://docs.godotengine.org/en/stable/classes/class_boneattachment3d.html):
  attachment nodes follow selected skeleton bones, suitable for held pen/book/key
  placement. Hand contact and offsets still require authored motion and review.
- [Godot 3D import formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html):
  glTF 2.0 is recommended and GLB can contain meshes/textures; OBJ lacks important
  animation/scene data. Check exports in the installed Godot version.
- [Blender shape keys](https://docs.blender.org/manual/en/latest/animation/shape_keys/introduction.html):
  relative shape keys are designed for blended expressions and facial animation.
- [TripoSR official repository](https://github.com/VAST-AI-Research/TripoSR)
  and [license](https://github.com/VAST-AI-Research/TripoSR/blob/main/LICENSE):
  the project states MIT for code, pretrained models and its demo; the default
  single-image setup reports about 6 GB VRAM. Texture baking is supported. It can
  provide a candidate, not verified likeness, topology, hidden surfaces or room
  integration. No installation, inference, asset upload or demo availability was
  tested here. Free hosted capacity is not guaranteed by an open-source license.

The source snapshots use official Blender manual RST, Godot documentation source
and the TripoSR README/license; links above are their readable counterparts.
Two guessed Blender glTF paths and an initial Krita source path returned 404;
Godot's importer documentation and Krita's actual manual page supplied the relevant
information. Documentation from development branches must be checked against the
installed Blender/Godot versions before relying on a specific option.

## Tool decision and checkpoint

Use existing Blender and Godot first: zero new paid services, accounts or API keys.
Krita is a free painting option, not assumed installed. The available image tool
can propose edited backgrounds within the existing session allowance; it does not
produce a production-ready mesh. External reconstruction remains optional if the
simple model fails; check license, hardware, current access and handling of owner
assets before use. No site or AI was given private models in this research pass.

Research and the full owner backlog are saved. No stool was extracted, modeled,
rendered or visually approved during this documentation pass. Resume from
`SESSION_HANDOFF.md`, then implement only the bounded trial when appropriate.
