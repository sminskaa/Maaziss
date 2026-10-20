# ART-FEEDBACK-POSE — actual-image review

Status: HOLD — revision checkpoint; no final aesthetic or clearance pass.
20 October 2026.
Reviewer scope: two isolated posed studies of the owner's corrected beat 4 and
beat 6. This is not approval of the existing character art, full stool action,
timing, contacts or Godot integration. The owner retains creative approval.

## Evidence inspected — earlier candidate, now superseded

Actual `build/checks/stool-feedback/pose-*.png` captures at 0, .65, 1.45, 2.4,
3.05, 3.7, 4.0, 4.5, 5.4 and 6 seconds; actual alternate-camera
`diagnostic-*.png` captures at the same times except 4.0. ART made private
contact sheets and foot crops under `build/checks/stool-feedback/art/`.
The diagnostic camera shows the real character/stool and fitted opaque neutral
desk geometry; the plain desk material is evidence for depth, not replacement
room art. Frozen pose source SHA-256 from manifest:
`fa7e88c873d41654d1398318b71f5882a4e10e0242b6d31e83705c1b3cf23b67`.
Original target compared directly: `art/proposals/apartment-cartoon-v2.png` and
`art/walking/maziss-side-atlas.png`.

## Observations of the earlier candidate

- Beat 4: the boot nearest the camera (anatomical right in this staging) moves
  visibly toward screen right from 000 to 065. The farther left boot becomes
  separately visible by 145. The upper body retains its earlier diagonal/back
  facing through those foot samples and turns to the right-facing profile by
  240. These sampled changes communicate the requested right, left, then
  torso/head order more clearly than a simultaneous swivel. Sparse stills do
  not alone certify all intervening motion or the floor contacts.
- Beat 6: 370 keeps the hands behind/outside the front desk edge; 450 visibly
  lifts both arms clear; 540 carries the hands forward above the surface; 600
  lowers them to the desk. I see no desk crossing in those inspected pictures.
  This is sampled visual evidence; dense evaluated-surface inspection belongs
  to the separate QA report.
- The hand route has a substantial acting defect at 450: the elbows flare
  backward/out to the sides and the palms turn up, with one hand beside the
  back of the head. It reads as an exaggerated backward arm flourish rather
  than a comfortable lift and reach. Safe clearance does not establish a
  plausible pose, and I do not recommend this as finished reach choreography.
- At 600 the near hand is a thick rounded mitten/fist rather than a readable
  relaxed palm with fingers resting on the desk. The far hand is substantially
  hidden by the fitted desktop prop in this camera, so the picture cannot
  establish its detailed resting contact. The desk-height and upper-body
  relationship read as a cramped forward lean.
- The bag and its upper opening change into a conspicuous angular, stretched
  silhouette during the arm lift (especially 450). Broad cuff/hand shapes and
  shoulder folds also look coarse. These need artistic attention independently
  of desk collision results.

## Original-drawing mismatch

The staging character retains the teal jacket, ochre shirt, brown satchel and
boots, but does not reproduce the original's adult angular face, expressive
brows/eyes, nose/jaw profile, purposeful hair locks or drawn hand anatomy.
The simple smooth jacket lacks the original's tailoring, pockets, wear and
painted texture; boots lack drawn laces and material detail. The current hair
is noisy/spiky, hands are bulky and the lighting/render texture is soft/grainy
beside the room's deliberate painted contours. Those remain appearance work,
not an incidental limitation resolved by this pose test.

## Revision checkpoint and recommendation

The coordinator revised the hand route and isolated the inherited hand/thigh skin
weight defect after this image review. QA reported wrist/forearm intersections in
intermediate revisions. The pictures/hash documented above therefore do **not**
represent the current reach source and cannot establish its clearance or acting.
The current revision had not been rendered for ART inspection at this checkpoint;
the attempted full render encountered unavailable OpenImageDenoiser support and
was being retried without it. No room composite has yet been inspected by ART.

HOLD the revised hand reach: no final aesthetic or clearance pass. Preserve the
useful ordered-foot direction evidence, but do not treat that as approval of
interpolation, character appearance or the complete action. A subsequent review
must inspect the new actual reach images and room composites with their frozen
source hash, alongside QA's evaluated-surface evidence, before changing this
recommendation. No further polish or full sequence is authorized by this report.

Files changed by ART: this report only; private image contact sheets/crops under
`build/checks/stool-feedback/art/`. No code, model, room artwork or original drawing
was changed by ART.
