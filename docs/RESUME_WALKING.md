# Resume checkpoint — FBX walk and rendering corrections

## Immediate status

The owner requested a pause because allowance is nearly exhausted. Stop new motion
work until they return. Agents do not continue indefinitely or resume automatically.
Current branch is `feat/reference-human-walk`; draft PR #4 contains the earlier
image-guided revision 6. The Godot game remains unchanged with placeholder art.
The last completed HTML is `visual-preview/maziss-walking-v6.html`, build
`cdeb00514796`; its 48 technical checks did not establish visual acceptance.
No FBX-based revision 7 has been built or approved.

## Owner's latest feedback — must address

1. Side-view resting boots point up. Visually plant the soles.
2. The arm farther from the camera incorrectly appears in front. Respect depth
   ordering for every body part.
3. Front-view resting boots lean sideways. Keep neutral boots upright and grounded.
4. A detached ghost sliver appears ahead of Maziss. Clean source-part masks.
5. Trouser bottom pixels detach and travel with the boot. Keep trouser cuffs part
   of a continuous trouser leg and align the boot top underneath.

Preserve the original character design and approved room PNG. Slight exaggeration
is welcome if the result is smooth, coherent and recognizably human. HTML panel
works for the owner; chat embedded images do not.

## Inputs and retained work

- All 16 supplied FBX files were downloaded outside the public repository. The
  ignored `private/motion/fbx-intake.json` records names, paths, sizes and hashes.
- Original walking videos and three image sheets remain prior references. The
  image-only attempt is already complete; the owner now explicitly requests FBX.
- Blender 4.3.2 and its FBX importer were previously verified available.
- Task briefs MOTION-002, TECH-007 and QA-008 are in production/agent-board.json.
- `/root/fbx_motion_extract` was started for MOTION-002, then interrupted on the
  owner's pause request. At checkpoint inspection there was no completed extraction
  helper, motion JSON or report. Do not assume an animation has been selected or
  extracted; inspect any later worker checkpoint before doing more work.

## Next actions when owner resumes

1. Check branch/status and retained inputs; read AGENTS.md and ART_DIRECTION.md.
2. Resume bounded FBX extraction (MOTION-002). Inspect ordinary walks first:
   `10-WalkCycle_01_MIXAMO_769.fbx`, `02-walkforward.fbx`, then slow walk. Avoid
   running/injured/wind clips as the baseline. Actually import and inspect timing,
   skeleton/coordinates and a clean loop. Keep raw and derived animation private
   while provenance/reuse rights are unresolved; public helper/report can describe
   the method without embedding motion arrays or private absolute paths.
3. Implement revision 7 from real FBX joint trajectories, preserving original
   cartoon proportions. Treat neutral standing separately from walking foot pitch.
4. Fix rendering alongside motion: far arm before torso, near arm after; remove
   detached silhouette islands; keep pants/cuffs out of boot masks. Current source
   locations are originalLegs, originalBoot and originalUpper in walking/demo.js.
   The present Side boot polygon includes trouser/cuff pixels, and front boots are
   tilted by the cuff-to-sole affine transform. Inspect actual painted pixels.
5. Start independent QA-008 after an inspectable candidate exists. Require actual
   idle side/front/back and moving close-up review for all five screenshot defects;
   mathematical joint equality alone is insufficient. Retain routing/controls.
6. Deliver a new self-contained revision 7 HTML with 0644 files/0755 directory,
   save source to the feature branch/update draft PR, and leave merge/creative
   acceptance to the owner. Do not silently integrate into Godot.

No motion work or tests beyond checkpoint/input checks were completed after the
owner requested the pause.
