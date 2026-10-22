# Walking checkpoint — complete 3D construction study

The owner still saw disappearing clothing/equipment after revision 8 and requested
complete anatomy and clothing understood from every angle. Work now evaluates a
complete 3D rig, not more sprite-mask patches. The approved painted art and prior
HTML studies remain intact; the preliminary model does not replace the visual target.

Branch `feat/reference-human-walk`, draft PR #4; owner controls merge and art approval.
Main Godot game is unchanged. Read docs/CHARACTER_3D_STUDY.md for scope/reproduction.
Final frozen build 62773eacf060 passed 32 focused independent checks (no failures);
rendered HTML passed 24 angle/mode cases offline. Full scope/limits are in final QA report.

## Sources and review files

- tools/character3d_body.py: worker-owned closed anatomy and complete garments.
- tools/build_character_3d.py: complete head/eyes/mouth/hair/bag, source-FBX retarget,
  authoring model and geometry export. Bag strap fitted to actual outer clothing.
- character3d/: local offline viewer and pinned MIT-licensed Three.js.
- tools/build_character_3d_preview.py and tools/capture_character_3d.py: live HTML
  and a rendered 2D fallback requiring no WebGL.
- visual-preview/maziss-3d-study.html: orbit, part visibility, walking/idle, stepping.
- visual-preview/maziss-3d-rendered.html: eight views, 224 walking frames, idle/body.
- production/MODEL_3D_BODY.md and production/QA_CHARACTER_3D.md: actual evidence/limits.
- build/checks/character3d/: ignored complete .blend with private derived walk,
  geometry/pose data, manifests, captures and results. Never stage these files.

## Current boundaries

138 mesh objects, 37,876 vertices; face, hands, tailoring, texture and secondary
motion are preliminary. Connected closed geometry does not guarantee no intersections.
Skin/clothing fit and animated weight transfer still need visual judgement. The
bag currently shares the torso transform; no cloth simulation or facial acting.
Keep prototype and finished-character acceptance distinct.

All 16 raw FBX and extracted motion remain private. Source is still selected
02-walkforward.fbx frames 234–269 at 30 fps, retargeted to the new model. Generated
model/data/HTML stay ignored because they include derived private motion. Public
helpers/reports/vendor licence contain no FBX trajectories or private intake paths.
HTML panel delivery works for owner; chat images do not. Keep files 0644/folder 0755.

Before resuming further work, inspect actual final QA result/manifest and owner
feedback. No need to rebuild unchanged geometry or rerun passing checks merely
because a turn was interrupted. Godot integration follows creative acceptance.
