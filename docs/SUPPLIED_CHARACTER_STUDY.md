# Supplied Maziss mesh: coherent walking study

The owner resumed work on 19 October 2026 with `white_mesh.glb` and explicitly
requested aligned Art and QA review of actual renders. The accepted drawings and
room remain unchanged. The rejected full-character image projection is not used.

## Method and scope

The supplied sculpt already contains recognizable hair, nose, ears, lapels, cuffs,
strap, bag, trousers and boots. It is retained as the continuous body surface.
Blender normalizes it to two metres, reconstructs one malformed local hand patch,
fits a 14-bone skeleton and transfers the retained owner-provided FBX walk. Sixteen
modeled eye/lid/brow/mouth parts follow the same head bone. Continuous vertex colours
describe the outfit on this actual geometry; there are no character image textures,
repeated portraits or transparency tricks covering missing surfaces.

This is not independently modeled cloth or a production retopology pass. The
supplied bag-side hand and satchel share geometry, so that arm stays in its resting
pose relative to the body. The other arm and legs move from the reference walk.
This is a disclosed constraint for a coherent study, not an independently animated
hand/bag solution. Those surfaces must be separated before adding free arm swing.

Art and QA inspected actual Blender captures from multiple cameras and walking
phases. Early candidates exposed source cross-body triangles, bag/hand stretching,
fingertip and forearm weight discontinuities, and a parent-update ordering error
that broke floor clearance. Those findings drove actual source/rig corrections;
passing export checks alone was not treated as visual acceptance. See the reports
for the final scope and unresolved defects.

## Reproduce privately

Required existing tools: Blender 4.3.2, Python with NumPy/Playwright, Chromium,
FFmpeg, and the repository's pinned Godot 4.6.3. No GPU, paid service or runtime
network access is needed. The saved free-tool research informed this choice;
the supplied sculpt makes another speculative AI reconstruction unnecessary.

Place the supplied model in ignored `private/models/white_mesh.glb`. Its inspected
SHA256 is `209c92bbfa786d3e6e268cbb386627bbe756ee40691a4ff84b3b16bd4ca0066d`.
Retain the existing private `private/motion/fbx-motion.json`; neither file is
distributed in the public repository.

```sh
blender -b --python tools/build_supplied_character.py
blender -b --python tools/render_supplied_character.py
python3 tools/build_supplied_character_review.py
python3 tests/browser_supplied_character.py \
  --input build/checks/supplied-character/maziss-supplied-rig.glb \
  --output build/checks/supplied-character/final-export --require-rig \
  --html visual-preview/maziss-rebuilt-review.html
bash tools/godot.sh --headless --path build/checks/supplied-character/godot \
  --script /workspace/Maaziss/tests/check_supplied_character.gd -- \
  /workspace/Maaziss/build/checks/supplied-character/maziss-supplied-rig.glb \
  /workspace/Maaziss/build/checks/supplied-character/godot/result.json
```

Create the ignored `build/checks/supplied-character/godot` directory before the
last command. Godot's runtime glTF conversion extension creates actual renderable
mesh instances, not only importer nodes. Its check verifies imported vertex
colours, materials, skin/skeleton, animation timing and finite moving bone poses.

Private authoring/runtime assets: `build/checks/supplied-character/maziss-supplied-rig.blend`
and `.glb`. Actual 24-frame walks from four cardinal directions, four phases from
four oblique directions, and eight idle captures are in `renders/`.
`render-manifest.json` binds these captures to the model hash; delivery records its
own hash and media sizes. The compact review is
`visual-preview/maziss-rebuilt-review.html`, a self-contained native MP4/still/
turnaround page with no required page scripts or WebGL. The room traversal is
composited placement evidence, not integration into the playable Godot scene.

## Final observed evidence, 19 October

Final GLB SHA256:
`eb3c9fb665f186221378cbe25bcc5739cc14c1b86259e11bae8d28f0debd1b06`.
QA inspected 32 independently rendered walk views plus idle views and evaluated
50 intermediate animation samples. No disappearing garments, detached needles,
repeated face or large stretched satchel was observed in those final images.
The 13 scoped export/deformation checks passed; their coarse fourfold edge-stretch
detector is not a game-industry quality threshold or proof of finished skinning.

Godot's actual runtime importer created 17 mesh instances, one 14-bone skeleton
and 19 colour-bearing surfaces; four animation phases yielded finite bone poses
and a moving shin. The hash-bound engine report identifies the final input above.
The compact HTML is 948,310 bytes with a 960×600, 16.382-second video and eight-view
still grid. QA checked actual playback progression and decoded images offline,
with no external requests or script errors. These internal checks cannot establish
that the owner's host preview panel will display this new file.

## Art and release boundary

The target remains the original painted cartoon drawing. The current model needs
finer adult facial likeness, hair/hand cleanup, designed garment boundaries, inked
detail, wear and purpose-authored UV painting. A plain shaded 3D interpretation is
not the final painterly style. The source has no facial animation topology or
expression rig. A successful Godot import does not certify production readiness,
collision-free arbitrary animation or a finished game character.

Independent reports: `production/ART_SUPPLIED_CHARACTER.md` and
`production/QA_SUPPLIED_CHARACTER.md`. Owner creative approval remains open.
Work stays on the feature branch/draft PR4. No merge or public asset release.

Official workflow references retained in the prior research include Blender's
UV editing, texture-painting and armature documentation, Godot's glTF import
documentation and free reconstruction-tool licensing/hardware checks. The added
engine check uses `GLTFDocumentExtensionConvertImporterMesh` to exercise real
runtime meshes; Godot's importer consumes glTF `COLOR_0` for the continuous palette.
