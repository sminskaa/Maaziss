# MOTION-002 — supplied FBX walking reference

Reviewed 18 October 2026 with Blender 4.3.2. This is an extraction and motion-reference report, not creative acceptance of Maziss's final animation.

## Actual imports and selection

Three owner-supplied files were imported and their animated skeletons evaluated frame by frame. No assumption was made that a filename guarantees a looping animation.

| File | Imported action | Observed behavior | Decision |
| --- | --- | --- | --- |
| `02-walkforward.fbx` | Frames 1–506, 30 fps | Setup T-pose, stationary preparation, then repeated ordinary walking steps; translation is substantially in place | Selected frames 234–269 |
| `10-WalkCycle_01_MIXAMO_769.fbx` | Frames 1–404, 30 fps | Changing headings, starts/stops and stationary stretches across a long take | Less suitable for the first ordinary loop |
| `09-SlowWalkForward_MIXAMO_769.fbx` | Frames 1–721, 30 fps | Long stationary section, then very slow walking with little arm movement | Slower than desired ordinary movement |

The other supplied running, injured, happy, cool, pacing and wind clips were not imported in this bounded task. Blender reported missing UV data in two mesh entries of the selected file; skeleton joint evaluation still succeeded. No source mesh or material is required for retargeting.

Selected source SHA-256: `f8a6dbfbf207df3e3113ee6391c20aa4cbb1b4c7d5916e0a32771347e3ea9fa1`.

## Data and timing

The private extraction contains both legs, both arms, chest, neck and head. Each side is evaluated independently from its own bones; the second leg is not reconstructed by shifting the first leg's phase.

- Complete same-leg cycle: 35 frames at 30 fps, **1.166667 seconds**, approximately 103 steps per minute.
- Samples: 36, including a repeated closing endpoint.
- Canonical axes: `[forward, left, up]`; origin is the current hip midpoint. Per-frame hip width determines heading and removes changing world orientation.
- Positions are divided by a 1.648596 m setup-skeleton height estimate: head-joint height plus neck-to-head vertical distance, minus the lowest toe joint. This is a reference scale, not a claimed body-mesh measurement.
- Separate `pelvisUp` retains vertical bob that hip-relative coordinates would remove.
- `footPitchDeg` uses ankle-to-toe direction relative to the supplied setup frame's foot calibration. Positive means toe up. Full foot-bone axis vectors are retained as additional orientation evidence.
- Actual root displacement across the chosen cycle is only 0.002409 m. Stride **0.714301 body heights** is inferred from backward motion of a low, loaded foot. It is not a measured root-travel distance.

The setup frame is a T-pose, **not an authored idle animation**. It can calibrate feet, hip width and proportions; its horizontal arms must not be used for Maziss's idle. No supplied idle clip was identified or invented.

## Loop fitting and retargeting limits

This is recorded motion rather than a perfectly closed authored loop. Before fitting, joint endpoint RMS mismatch is 0.007933 body heights. A cubic position/centered-velocity correction closes the chosen endpoints and their derivatives without changing duration. Maximum individual joint-coordinate correction is 0.030315 body heights. Endpoint joint coordinates are identical after rounding.

This changes measured segment lengths slightly: selected thigh length spans vary up to 7.2% and shin spans up to 3.9%. **Retarget normalized segment directions onto fixed Maziss segment lengths.** Do not stretch original artwork according to those varying lengths. The renderer must independently preserve perspective, occlusion, pant continuity, boot seams and flat idle soles.

The measured pitch includes substantial toe-off, approximately −73° at its extreme, and up to +24° toe lift. Those are walking poses; an idle pose must return to neutral. Original source knee trajectories are continuous; later discontinuities can still arise from retargeting, clipping, orientation changes or start/stop blending.

## Verification and scope

- Imported three actual FBX actions and evaluated their bone positions across the take.
- Inspected a private animated side/front skeletal review and its rendered screenshot. Selected cycle shows alternating steps with one foot low while the other swings.
- Confirmed every extracted joint coordinate is finite and first/last fitted joint positions match exactly.
- Original source frame rate and cycle duration are retained; both source sides remain separate.
- Extraction helper contains no animation arrays or personal absolute paths. Raw FBX, derived joint curves, intake records and skeletal preview remain in ignored private/build directories.

Owner-supplied download/licence evidence has not yet been inspected. Keeping the source motions and derived arrays private avoids publishing them while that is resolved. This report does not establish redistribution rights. It also does not certify that the final painted character animation is natural; the integrated renderer needs visual review in all directions.

## Reproduction

From the repository root, with the supplied private intake available:

```sh
blender -b --python tools/extract_fbx_walk.py -- --intake private/motion/fbx-intake.json
```

The helper writes the ignored private motion JSON. It does not upload files or modify the original FBX.
