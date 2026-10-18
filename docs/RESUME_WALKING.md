# Walking checkpoint — clothing continuity revision 8

The owner finds the actual FBX-driven revision 7 much better. Preserve its gait,
timing and original character proportions. Remaining requested changes concern
clothing/bag holes and stray pieces, both depth boots leaning left, and trousers
apparently stretching/shortening independently of the walk.

Branch: `feat/reference-human-walk`; draft PR #4. Do not merge without the owner.
Godot still uses placeholder graphics; this work remains a separate HTML study.
Frozen build `5c3d7d3fcda2`: 44 focused checks passed, 100 whole poses and 80 isolated
item captures. See the final QA report for thresholds and construction limits.

## Current construction

- `walking/fbx-gait.js` and private FBX curves are unchanged from revision 7.
- `walking/character-renderer.js` uses complete painted jacket backing under
  original collar/torso detail and a separate intact bag. No subtractive arm/hand
  holes are left in either item. Original head/face, arms and original PNGs retained.
- New repair atlas and provenance: `art/walking/maziss-clothing-repair.png` and
  `art/walking/CLOTHING_REPAIR.md`. This is 2D layered rendering, not 3D garment models.
- Front/back use distinct left/right trouser and boot drawings. Cloth ends on
  actual animated cuffs; shoe projection no longer repositions the trousers.
- `visual-preview/maziss-walking-v8.html`: interactive review with close-up,
  directions, idle, slow playback and stepping.
- `visual-preview/maziss-walking-v8-poses.html`: phase captures plus actual layers.
- `production/QA_CLOTHING_WALK.md`: final focused evidence and limits.
- `build/checks/clothing-walk/build-manifest.json`: local source/output identity.

## Retained boundaries and follow-up

All 16 source FBX and private extracted arrays stay excluded from Git, as do generated
review HTML and captured pixels. Selected motion remains `02-walkforward.fbx`,
frames 234–269 at 30 fps. Raw redistribution rights are unresolved; public helpers
and reports contain no trajectories or private intake paths. Rebuilding needs the
existing ignored motion inputs.

The HTML panel works for the owner; chat images do not. Keep previews readable 0644
inside a 0755 folder. No claim is made to repair the host chat renderer. Natural
foreshortening, simplified front/back foot roll, turning and world-space foot
planting remain limited. Judge moving playback, not only test counts. Owner
acceptance comes before Godot art integration and before merging the draft PR.
