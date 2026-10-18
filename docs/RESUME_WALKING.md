# Walking task checkpoint

The allowance pause was resumed. The owner confirmed that the existing project opens
in Windows Godot. The three private recordings and raw side tracking were retained.
A new reference-driven revision 5 HTML study now exists on the feature branch and
awaits owner review before integration; it is not merged into the playable Godot room.

## Current files

- `walking/reference-motion.json`: 25 closed samples of the selected visible leg,
  frames 36–78 / 1.2–2.6 seconds of the side video. Opposite leg reconstructed by phase.
- `tools/analyze_walk_references.py` and `production/MOTION_REFERENCE_ANALYSIS.md`:
  measured reference extraction, camera/occlusion limits and reproducible method.
- `walking/reference-gait.js` and `walking/demo.js`: sagittal motion projection,
  original atlas rendering, foot contact and review controls.
- `visual-preview/maziss-walking-v5.html`: self-contained motion review; ignored by Git.
- `production/QA_REFERENCE_WALK.md`: independent scope/evidence/limitations.
- `docs/WALKING_DEMO.md`: reproduction and current animation limits.

The first Maziss design and approved room PNG are preserved. Previous v1–v4 HTML
versions remain local history and are not approved animation. Personal videos and raw
tracking stay outside GitHub; local exact paths remain in the ignored intake note.
Future fresh tracing requires those private inputs; replay of the generated study
uses only original art and normalized motion data.

Next: owner reviews the actual v5 motion and records feedback on issue #2. Further
cleanup or native Godot integration follows that decision; avoid silently merging
unapproved art/movement into the game. Windows source launch is confirmed, but
remaining issue #1 save/offline checks are not inferred from that confirmation.
