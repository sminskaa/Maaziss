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

Owner clarification: furniture Maziss physically sits on must be an **actual
visible 3D model**, not a flat furniture sprite with Maziss posing in front of it.
The current sofa study has only hidden contact proxies and is not the completed
solution for that requirement. For stool/sofa, build seat, legs/base, back/arms
where applicable, thickness and hidden surfaces; use geometry for foreground
occlusion, contact and shadows. Decorative background can remain painted.
The proposed stool trial therefore requires a complete mesh, not a billboard.

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

## Follow-up: AI assistance and hosted services actually checked

Owner asks how models will be created and specifically requests online AI options.
Checked official current pages on 19 October 2026; snapshots/fetch results are in
`build/checks/room-interactions/research/services/`. Prices and quotas can change.

| Option | Observed access and limits | Project decision |
| --- | --- | --- |
| Blender, already installed | Direct CPU mesh construction with Python, rounded/beveled forms, UV painting and GLB export; no hosted account needed. | First stool attempt: construct an editable seat and complete legs/braces to match the source, inspect the shape, then paint. This is an available method, not a demonstrated matching stool yet. |
| [Meshy pricing](https://www.meshy.ai/pricing) | Page lists 100 monthly free credits, 10 Meshy 6 Lite model downloads/month and CC BY 4.0 commercial use with attribution. Its comparison marks free-plan API access unavailable. | Possible web-based candidate generator. A free website account is distinct from an accessible free API; do not claim automatic integration here. Any export/feature limit needs checking on the actual generation. |
| [Meshy terms](https://www.meshy.ai/terms-of-use) | Section 3.2 states free outputs belong to Meshy and are licensed to the customer under CC BY 4.0. Section 2.9 permits non-Enterprise input/output use for training unless otherwise agreed. Paid plans offer privacy options. | Owner's private art is not assumed confidential on a free plan. No account, upload, key, payment or generation submitted. Recheck terms and the owner's private-asset constraints before choosing this route. |
| [Tripo hosted pricing](https://www.tripo3d.ai/pricing) | Free plan lists 200 monthly credits, public models, non-commercial use and limited exports; paid tiers list private/commercial use. [Terms](https://www.tripo3d.ai/terms), section 5.2.1, also assign broad rights over free-user input/output. | Not selected for zero-budget game production assets under the observed free plan. Distinct from the MIT-licensed TripoSR code. No upload or inference performed. |
| [TripoSR local](https://github.com/VAST-AI-Research/TripoSR) | Existing MIT code/weights documentation; inspected official `run.py` explicitly selects CPU when CUDA is unavailable. Supports texture baking. Runtime and quality on this CPU are unmeasured. | Possible local AI-assisted volume proposal if manual stool modeling fails. No weight download or installation this pass. Absence of a CUDA GPU here is a practical limitation, not a claim that local CPU execution is impossible. |
| [TripoSR public demo](https://huggingface.co/spaces/stabilityai/TripoSR) | Hugging Face's Space metadata reported `RUNTIME_ERROR`; direct app configuration returned HTTP 503 during this check. | Currently unusable in this check; do not promise a functioning free online generator from its README alone. Recheck later if needed. |

[Meshy API documentation](https://docs.meshy.ai/en/api) describes REST tasks and
API-key management, but no key or account is configured in this workspace. A
guessed older endpoint and an initial Tripo terms URL returned 404; the official
linked API overview and `/terms` pages were then accessed. Documentation and site
claims are recorded as such; none of these services produced a tested mesh here.

### Actual model-to-contact pipeline

1. Use the stool's visible proportions/design as reference; build full geometry in
   Blender, or import an AI-generated base mesh if that route is later selected.
2. Repair shape, hidden surfaces, scale, pivots and UVs; add coherent cartoon wood,
   wear and lighting. AI geometry still needs these checks.
3. Render a turntable and the room camera view before animation. A suitable model
   must remain recognizable from sides and behind and have a solid seat surface.
4. Place it in the matched camera/room coordinates. Set the seat-top landmark,
   floor height, leg room and hand targets against the actual model. Author the
   approach, turn, weight shift, descent and settle; a collision shape alone does
   not automatically create believable sitting or cushion deformation.
5. Render model and Maziss together so furniture genuinely occludes body parts,
   with appropriate contact shadows. Add modest cushion compression only after
   rigid contact is convincing. The painted original stool/sofa must be removed
   from the clean background to avoid a double image.
6. Art and independent QA judge the same actual multi-angle views and complete
   motion for support, penetration, floating boots, style and intact background.
   Do not claim success based on a model file, collider or scripted pose alone.

No third-party service or AI assistant is silently available merely because it has
a website. This environment can use exposed tools and permitted HTTP APIs; account
or paid API access is not assumed. The offline game will contain exported assets,
never a dependency on any hosted generator. Character animation remains paused.
