# Complete character construction study

The owner requested a change from cutout deformation to complete independently
constructed anatomy, clothing and equipment, viewable from any angle. The repeated
2D patch attempts remain historical studies; their technical passes did not resolve
all visible discontinuities. The supplied walking references remain useful.

This increment builds actual 3D geometry and a shared skeleton in Blender 4.3.2.
It is a construction proof, with preliminary facial forms and plain materials.
It does not approve a new character design or replace the approved painted art.

## Construction

- Complete head and neck volumes, separate eye whites/irises/pupils/lids, mouth,
  nose, ears and hair. Facial pieces follow the Head bone; there is no facial acting.
- Separate complete upper arms, forearms, hands, thighs, shins and feet. Underlying
  body geometry remains present behind clothing. Hands are simplified palm/thumb
  forms, with detailed fingers still to be modeled.
- A continuous welded jacket with sleeves, a complete shirt, a belt/buckle and a
  continuous welded pair of trousers. Closed meshes provide the surfaces that
  painted cutouts did not contain.
- Complete left/right boots and soles, plus a separate bag, flap, fastening,
  tools and flat shoulder-strap loop. Bag elements share the Spine transform.
- Bone weights blend the jacket at shoulders/elbows and trousers at hips/knees.
  Covered anatomical roots use matching influence fields and fit inside garments.
- Existing private bilateral FBX walk retargeted to fixed construction-model bone
  lengths. It is a new retarget onto new geometry, not a claim that the previous
  painted character's appearance has already been reproduced in 3D.

Camera depth determines overlap continuously. There is no hand-authored painter
order that must switch between flat front/side/back cutouts. Clothing is normally
opaque, and hiding it in the inspection tool reveals the existing body underneath.
Complete geometry still requires good fit, weighting, joint overlap and art review;
it does not guarantee collision-free or natural movement.

## Art and delivery boundary

The approved room and original character PNGs remain unchanged. This simple model
establishes construction; the approved painted cartoon face, silhouette, tailoring,
lighting and surface detail remain the target for a later art pass. Do not silently
replace the painted Godot assets with this model.

Blender is an authoring tool, not a new player dependency. Godot stays the final
offline desktop engine. We can render fixed-view 2D sprites from a refined 3D model
or use a suitable stylized 3D presentation in Godot; this study does not decide that
production rendering choice. Required shipped assets must be local, with no runtime
AI, network, account or server requirement.

The live HTML study supports camera orbit, walking/idle, pause/frame stepping,
part visibility, underlying-body inspection and wireframe. A second HTML review
plays actual rendered frames without requiring WebGL. Neither is game integration.

## Tools and reproduction

```sh
blender -b --python tools/build_character_3d.py
python3 tools/build_character_3d_preview.py
python3 tools/capture_painted_character.py
python3 tests/browser_painted_character.py
```

The full builder requires retained ignored `private/motion/fbx-motion.json`; no raw
FBX is loaded by the geometry builder. Standalone rest-body generation/validation
is described in `production/MODEL_3D_BODY.md`. The complete Blender file, generated
geometry/pose JSON, manifests, captured frames and HTML stay in ignored build/preview
locations. The Blender file contains a private derived walking action. Do not publish
or package it while source-motion reuse rights are unresolved.

Three.js 0.160.1 is bundled under its MIT licence for the local WebGL reviewer. Its
official npm archive was checked against registry SHA-512 integrity before extraction.
The viewer embeds the library and model, rather than fetching a CDN at runtime.
Captures/tests use installed Playwright/Chromium. Native Windows and Godot execution
are separate checks. See `production/QA_CHARACTER_3D.md` for actual scoped results.


## Earlier construction evidence

Frozen build `62773eacf060` passed 32 focused independent checks. All 138 exported
mesh objects have closed welded triangle-edge topology; the main jacket, shirt and
trousers are each connected garments. Actual skinned vertices were checked over
24 phases, with 32 walking renders across eight camera angles and four underlying
body views. The saved animated Blender model also loads successfully with 14 bones.

The rendered fallback contains 224 walking frames. Coordinator checks exercised
24 angle/mode image combinations, pause/frame step/playback controls and offline
execution with no runtime errors or network requests. Model/output hashes and
preview permissions match. These checks establish the scoped construction workflow;
they do not establish artistic success or native Windows/player performance.

Visual review confirms improved long rear strap placement. Upper-shoulder tailoring,
small waist surface intersections, simple hands/face, fabric detail and secondary
movement remain open. Do not treat complete geometry as finished garment fit.

## First painted pass

The owner accepts the overall motion but reports hand/bag penetration, apparent
trouser gaps and an angular model that loses the cartoon style. The next candidate
rounds the silhouette and registers the original face, trousers, boots and bag
onto complete surfaces. A new clean jacket reference removes baked equipment.
Packed images and actual UV layers are retained in the ignored authoring `.blend`;
the live browser uses the same registered coordinates. Head surfaces sit closer
to the collar and tool silhouettes are shorter above the bag. Separate fixed-length
arm IK clears the bag; shared shin/trouser knee weights prevent skin breakthrough.

Current output is `build/checks/painted-character/`. The HTML reviews are
`visual-preview/maziss-painted-3d.html` (live model) and
`visual-preview/maziss-painted-rendered.html` (actual rendered frames, no WebGL).
The earlier plain-construction HTML is preserved for comparison. Generated model
and motion inputs remain private. Original PNGs and the Godot runtime are unchanged.

Face/projection seams, shoulder tailoring, hands and convincing original likeness
still require art refinement. This is a first painting-registration study; it
does not yet reproduce the drawing convincingly from every angle. See
`CHARACTER_PAINT_WORKFLOW.md`, `production/CHARACTER_FIT_REVIEW.md` and
`production/QA_PAINTED_CHARACTER.md` for method, resources and scoped evidence.

Frozen painted build `98259839b0e0` passed 26 focused independent checks. It has
106 complete objects and 145,468 vertices. The actual authoring file packs all
three reference images and retains all three UV registrations on painted meshes.
Evaluated hand/forearm triangles clear bag/tool triangles in idle plus all supplied
cycle samples; skin/pant intersections remain confined to closed caps inside boots.
The rendered HTML contains 192 actual walking frames across eight angles plus
standing views. These results support an intermediate art review, not approval
of the face, silhouette, painting or arbitrary future motion.
