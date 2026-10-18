# Walking task checkpoint

The owner rejected revision 5 despite its technical passes: jerky movement, abrupt
knee extension and feet misaligned at rest. Three illustrated sheets and 16 FBX
files were then supplied. The owner explicitly requests an image-only attempt
first, with FBX comparison afterward. Slight cartoon exaggeration is acceptable if
fluid, coherent and recognizably human.

## Current candidate

- `walking/image-motion.json`: qualitative reference provenance and authored poses,
  timing and painted-boot calibration. No video or FBX data used.
- `walking/image-gait.js`: continuous foot trajectories, shared boot-cuff IK,
  neutral alignment, early swing fold, gradual extension and start/stop recovery.
- `walking/demo.js`: original texture rendering, live close-up and Stand still.
- `visual-preview/maziss-walking-v6.html`: self-contained review; ignored by Git.
- `production/IMAGE_WALK_BRIEF.md` and `production/QA_IMAGE_WALK.md`: independent
  reference interpretation and actual rendered validation, with limits.
- `docs/WALKING_DEMO.md`: reproduction and scope.

The original character PNGs and approved room are unchanged. Previous v1–v5 outputs
remain local history. The FBX downloads and private intake manifest remain outside
public source; they have not been imported for the image-only candidate. The
private manifest is `private/motion/fbx-intake.json`. Do not publish raw inputs or
silently use them in the image-only comparison.

Next: owner reviews revision 6 motion. Then evaluate a normal walking FBX for a
separate comparison if needed; do not mix the two sources and claim an image-only
result. Main Godot still uses placeholder art. Windows project opening is confirmed;
broader offline/save/input checks remain issue #1. No creative acceptance or merge
is implied by numerical QA or by opening the existing Godot project.
