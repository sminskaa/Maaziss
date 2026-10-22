# Human walking reference analysis

Completed scope: inspect the owner's retained side-view footage and turn the
existing landmark tracking into a reproducible, normalized motion reference.
This task does not change the renderer or approve a painted walking animation.

## Source and selected passage

- Source: `Video Projectbiks.mp4`, the owner's side-view recording.
- SHA-256: `9214df22c5db2c8ba1965f60c63e9683ed91bf52d4393059c8b6996abdefeff3`.
- Retained landmark-cache SHA-256:
  `defe0ceda44fb8bc773f183185c6fbf651ca615495e404ba282d45ee63afd6e9`.
- Selected near-leg cycle: frames 36–78, or 1.200–2.600 seconds at 30 fps.
  Contact boundaries are visually estimated within about two frames.
- Frame montages and individual images at frames 60 and 68 were inspected.
  All original and extracted personal images remain in ignored local locations.
  Neither the motion JSON nor this report embeds footage or absolute private paths.

The earlier checkpoint suggested frames 60–100. That passage follows the farther
leg, whose thigh/knee is more frequently occluded. The nearer leg, labelled left
by MediaPipe, is more useful. The output uses its cycle and reconstructs the other
leg with a half-cycle phase offset. It does not claim to have independently
captured both legs or their small asymmetries.

## Observed motion

The selected stride lasts approximately 1.40 seconds, about 85.7 steps/minute.
Container frame rate does not independently verify whether an earlier export
altered original speed. This timing is an observed reference, not an instruction
to make the game character travel slowly. Translation speed and stride need to
remain consistent when retargeted.

The near foot remains on the floor for roughly 69% of the cycle. Its heel rises
before the toes leave the floor; swing follows, then the leg extends for contact.
The forward thigh angle is about 30 degrees at contact and reaches approximately
12 degrees behind vertical before swing. Smoothed swing knee flexion reaches
approximately 59 degrees; the raw peak is approximately 64 degrees. The knee folds
behind the moving thigh, not sideways out of the leg's sagittal plane.

The swing ankle rises roughly 20–25 image pixels relative to its preceding stance
height, around 5% of the estimated standing height. Heel rise is much larger
because the foot rotates; the toes remain much nearer the floor. A boot that is
held flat while being lifted by the heel's full height would exaggerate this walk.
There is little arm flourish. The visible human is walking normally, rather than
performing a high-knee march or kicking each foot straight out.

## Data and interpretation

`walking/reference-motion.json` contains 24 circularly filtered phase samples and
an identical closing sample. It records thigh/shin angles, knee flexion,
hip-relative ankle forward/up coordinates, detrended pelvis vertical movement,
and observed heel-to-toe pitch. Angles use downward vertical as zero, with forward
positive. Lengths use an approximate 420-pixel crown-to-sole height. Near-leg
thigh/shin median lengths are about 0.219/0.214 of that scale; uncertainty is
approximately 5% because the camera is elevated and the actor changes position.
Maziss must retain his original artwork proportions instead of adopting these
actor measurements.

The circular Gaussian filter uses a sigma of 0.035 cycle, approximately 1.5 source
frames. It removes tracking jitter and joins the cycle without a discontinuity.
The source trajectory's slow vertical camera trend is removed from pelvis bob.
The measured foot pitch is preserved, alongside a separate conservative fit
bounded to -45 to +10 degrees. That bound is an editorial approximation: toe/heel
landmarks are particularly unreliable during motion blur. The helper does not
pretend that its inferred ankle rotation is a precise measurement.

**Do not copy the image-plane knee bend literally into a sagittal rig.** Even the
visible leg shows approximately 13–32 degrees of apparent stance flexion. The
elevated, oblique camera and landmark bias contribute to that value. MediaPipe's
estimated world landmarks are also inaccurate for this stance and were not used
as authoritative 3D motion capture. A literal copy can make Maziss crouch. Keep
the observed order of events, swing fold/extension and relative timing, while
fitting contact extension and restrained weight-bearing knee bend in the rig.
Any such fit must be identified as retargeting, rather than a measured fact.

For front/back movement, solve the leg in its sagittal plane and then project it
into the view. Mapping image-X knee deviations directly into those views is the
source of the previous sideways-knee defect. The side clip does not determine
exact 3D hip rotations, foot yaw or lateral weight shift, so those should remain
small and be judged against the owner's other recordings and rendered results.

## Reproduction and checks

The analysis helper reads the retained private cache with the Python standard
library. No paid service, runtime model or network call is needed:

```sh
python3 tools/analyze_walk_references.py \
  --tracking build/checks/reference-motion/raw-side.json \
  --video /path/to/private/Video\ Projectbiks.mp4
```

If a fresh cache is necessary, `--track` uses the isolated motion environment's
MediaPipe 0.10.21 and OpenCV 4.11.0.86. It processes the private video into an
ignored cache with permissions 0600. The game never requires those tools or the
owner's footage. The default output includes only normalized motion, source
filename/hash and the documented limitations.

The output was regenerated from the retained cache, checked for finite values,
25 samples, strictly ordered phases, identical start/end pose, positive knee
flexion and absence of private absolute paths. The full-cycle knee maximum is
59.34 degrees after filtering; thigh range is -12.52 to 32.87 degrees. Visual
naturalness still requires inspecting the actual retargeted animation and owner
approval. Passing these data checks cannot establish it.
