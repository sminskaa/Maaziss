# Resume checkpoint: geometry-first Maziss rebuild

Paused 18 October 2026 at the owner's explicit request to preserve allowance.
Do not resume implementation until the owner asks. Existing research is saved;
no replacement model, new texture set or new animation has been built this turn.

## Owner's current decision

- Original cartoon drawings are accepted and must be preserved.
- The earlier complete 3D motion is broadly useful.
- The painted projection attempt is strongly rejected: repeated/smeared faces,
  mixed clothing and lost identity. Do not continue patching that method.
- Research first, then construct a model from the drawings' defining forms.
  Establish the likeness in geometry before painting it.
- Zero additional budget. Final game remains offline desktop Godot. HTML is review.

## Files and retained evidence

- `docs/CHARACTER_REBUILD_RESEARCH.md`: coordinator's workflow research, sources,
  access limits and chosen stages.
- `production/FREE_CHARACTER_TOOLS_RESEARCH.md`: independent official-source
  tool/license/CPU-GPU review. No package installs, weight downloads or paid use.
- `build/checks/character-rebuild/research/`: ignored raw source snapshots,
  readable extracts, access results and `free-tools-sources.json`.
- Original drawings: `art/walking/maziss-depth-atlas.png` and
  `art/walking/maziss-side-atlas.png`; approved scene
  `art/proposals/apartment-cartoon-v2.png`. All remain unchanged.
- Existing rig/body: `tools/character3d_body.py`; geometry/clearance refinements
  `tools/character3d_fit.py`; existing assembly/motion
  `tools/build_character_3d.py`. Existing private motion:
  `private/motion/fbx-motion.json`. Keep raw/derived motion private.
- Rejected painted model and old previews remain in
  `build/checks/painted-character/` and `visual-preview/`; preserve as comparison,
  do not infer approval from their 26 numerical checks.
- Owner-confirmed delivery: `visual-preview/maziss-review-small.html` (850KB),
  native video plus still fallback, no page scripts/WebGL. Builder:
  `tools/build_compact_character_review.py`. Do not overwrite this historical
  comparison when making a new candidate; add input/output options or new paths.

Blender4.3.2, FFmpeg, Chromium, Playwright, NumPy, SciPy and Pillow are available.
The research worker found five logical CPUs/~33GiB RAM and no accessible CUDA GPU.
No new environment configuration was required.

## Actual agent/plan state

- RESEARCH-002: coordinator research completed and saved, then paused.
- RESEARCH-003: `/root/free_character_tools` completed its report. No workers need
  to remain running.
- MODEL-003: recorded brief only; no sculpt worker started, no geometry written.
- QA-012: recorded brief only; no QA worker started or new-model tests run.

Follow `AGENTS.md`: bounded brief before delegation, at most two workers, genuine
native identifiers/state, nonoverlapping ownership. A role label is not an agent.

## Proposed implementation, not completed work

1. Actually inspect the original front/profile drawings and register face/body
   landmarks. Pixel and metre values below are initial estimates from visual
   inspection, not measured acceptance results. Verify them before adoption.
2. Use `tools/character3d_sculpt.py` for a new head/neck, eyes/lids, nose, mouth,
   brows and designed hair. Suggested interface `build_portrait(armature)` returns
   closed weighted objects with `part_group` tags. Own coherent surfaces; no atlas
   image textures or screenshot projection on this first shape pass.
3. Useful starting landmarks near the existing two-metre-scale rig: hair top~2.0,
   chin~1.56, eye line~1.775, mouth~1.62, eyes aroundx±.065–.070. Front source head
   center is roughlyx260px in the first depth-atlas frame, eyes around245/278px,
   eye line~67px, chin~112px. Reference poses/perspective disagree, so fit both
   front and profile rather than forcing a perfect scan reconstruction.
4. Construct a continuous skull/cheek/jaw/nose surface with designed profile and
   smooth facial transitions. Fit tired/worried oval eyes and brows, a restrained
   downturned mouth, thin neck, and the original swept untidy hair. Avoid the old
   random spike cloud, floating eyelids, disconnected chin blobs and giant eyeballs.
   Neutral-material likeness comes before paint. Head rigidly follows its bone
   for now; facial animation topology is a later explicit task.
5. Coordinator can create a separate rebuilt assembly/wardrobe module while the
   sculpt worker owns only its new module/report. Retain body proportions and
   stride where useful. Model jacket lapels, rolled cuffs, pockets/buttons, shirt
   collar/placket, trouser seams/knee patches, boot soles/laces and intact bag/strap
   as geometry/material regions rather than printing a whole sprite over them.
6. Existing `build_character_3d.py` has top-level assembly side effects. If reusing
   its bag/motion helpers, first make its assembly import-safe with `main()` plus
   a `__name__` guard. Do not execute the old painting exporter just to import a
   helper. Alternatively extract pure shared helpers explicitly.
7. If using `apply_art_geometry`, apply its useful body/cuff/continuity work before
   adding a new portrait. Its old head-union and eye-shrink transforms must not
   silently modify the new fitted face. Retain `adjust_arm_targets` clearance and
   the supplied cycle/timing, with fresh actual-pose checks after geometry changes.
8. Export geometry and intentional material colours only for the first review.
   Verify no character material contains `Image Texture` nodes and no browser
   shader loads the old sprite projections. Original drawings belong beside the
   model as reference, or as nonrendered image empties in the authoring file.
9. Compare actual neutral/front/profile/three-quarter renders against the original
   at matching scale. Fit the silhouette and landmarks before procedurally adding
   hand-painted-style materials. Do not use generated illustrations as pretend
   renders of the model. Later UV painting must be designed for this geometry.
10. Render a short real-model walk and turntable; deliver a compact review near or
    below1MB, with a small still fallback. The previous10–18MB HTMLs failed while
    older smaller ones worked. This is a confirmed workaround, not a known limit.
11. QA must inspect actual images for likeness, body/clothing continuity, camera
    overlap and bag contact. Distinguish visual findings from numerical passes.
    Save code/reports to the existing feature branch/draftPR4; no merge or release.

Potential free AI reconstruction experiment: TripoSR explicitly supports CPU and
MIT code/weights, but performance/likeness are untested. It is an optional rough
volume aid, not an accepted substitute for fitting Maziss. Check the saved official
source/license report before installing. Do not spend time on inaccessible GPU
stacks or gated services as a prerequisite for the next geometry study.

## Resume entry point

Read this file, `AGENTS.md`, `CHARACTER_REBUILD_RESEARCH.md` and the free-tool report;
inspect repository status and the retained originals. Continue with MODEL-003's
geometry-first shape study. Do not restart the research from scratch or present
the rejected projection as the latest acceptable model.

## Laptop GPU follow-up

The owner asked whether their Windows laptop GPU can help. This cloud session
cannot directly borrow local GPU hardware. A future Windows-local Blender or
selected reconstruction workflow can use it; the GPU model and dedicated VRAM
are not yet known. Geometry-first modeling does not require a GPU. Do not install
remote-access software, expose a GPU service or resume a long setup based solely
on that question. Ask for hardware details when assessing a local option.
