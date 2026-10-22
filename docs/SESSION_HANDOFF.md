# Current session handoff

## Current scope and owner direction

Work only on the first room and Maziss. Original room/character drawings and story
remain targets; Discworld II is closest presentation reference. All old resources
are preserved. Existing character3D appearance and full animation are unapproved.
The owner should direct through simple HTML tools, not Blender or reference-video
recording. Final game is offline desktop Godot; HTML studies are separate reviews.
See docs/VISUAL_WORKFLOW_PROPOSAL.md and docs/STOOL_DIRECTION_DECISIONS.md.

## Latest result: resumed pose proof, 21 October

Compact current review: visual-preview/maziss-stool-pose-review-v2.html
(889,796 bytes). Original drawing included separately as appearance target.
Owner can save one pose-feedback JSON for both isolated tests. This is sparse
actual posed renders, NOT continuous animation, full stool action or Godot work.

A: right foot → left foot → torso/head turn. Exact old targets preserved across
121 samples0–3s. B: revised lap gather/lift in front of chest, constant anatomical
elbow pole, wider feathered cuff binding. Initial backward flare reduced.
Candidate B sits more upright, body/stool setback40cm vs old source, as an explicit
fitting proposal; no owner agreement on changed spacing assumed. Hands target
x=.30m. Surface check clears hands AND sleeve patch, including inclusive regions.

Independent QA: 600 samples3.005–6.000s at200Hz; >.65 Hand/ForeArm incident,
inclusive any>1e-8 Hand/ForeArm and all3historically failing triangles: ZERO
sampled desk-slab intersections. All14bone lengths/rest geometry unchanged.
Scope is fitted slab/surface samples, not continuous physics/all body/prop checks.
Both Art and QA opened actual current room/diagnostic images. All18PNG hashes
match manifest. Browser checks:19imagesload, feedback save/reload/export, mobile
width, noJSerrors. Host chat delivery still requires owner to open the link.

Remaining explicit HOLD: curled mitten/hooked hands, far triangular sleeve panel
and exact relaxed palm rest (~4.925mm gap). No production art/contact approval.
Do not ask owner to rediscover these known model defects or polish a full sequence.
Next after direction review: local proper sleeve/hand deformation/shape work, then
actual pose+sampled surface verification before expanding animation. Preserve A.
A volume-preserving skin/corrective-smoothing experiment did NOT solve the sleeve
and was NOT integrated; saved under build/checks/stool-feedback/deformation-experiment.

## Reproduction and evidence

Source: tools/stool_feedback_pose.py, tools/render_stool_feedback_test.py,
tools/build_stool_feedback_review.py. Blender4.3.2; OIDN unsupported, disabled.
Run renderer -- --probe-only for bound probe; normal for9room+9diagnostic keys;
-- --preview renders only2poses and must not be packaged as complete review.
Builder verifies complete9+9manifest, pose hash and every rendered image hash.

Current pose SHA bfc3114daf95ff99e1c371e4e7fe4b98dcca78ff35419f8e5275908cae5280dd.
Audited probe SHA413ec64d47198287bd88a05a5f860b17a9fc455d59e42dd6427ed08b9d1fb8f1.
Reports: production/QA_REACH_RESUME.md and production/ART_REACH_RESUME.md.
Actual renders/scene/manifest/contactsheet: build/checks/stool-feedback/.
Audited source preserved in qa-resume/clearance-bfc3114d/.
Prior failed checkpoint archived build/checks/stool-feedback-checkpoint-20261020/;
original prepared/source models remain build/checks/stool-slide/ (unchanged).
Full previous handoff retained docs/archive/SESSION_HANDOFF_20261020.md.
Private assets excluded from Git: a source commit is not a complete asset backup.

## Directing workflow already tested by owner

visual-preview/maziss-director.html places start/destination/path/facing and notes;
static painted marker is only direction aid. Owner uploaded one full action file,
retained private/directions/seat-at-desk-original.json. Storyboard at
visual-preview/maziss-stool-storyboard.html. Owner feedback retained privately:
private/directions/stool-storyboard-feedback-original.json. Beats1/2/3/5 intention
agreed;4requires rightfoot thenleft thenbody;6no hand throughdesk. This pose proof
addresses only4/6. Clicking reachable floor must eventually pathfind/walk normally;
the owner will not author every possible click. Current game still placeholders.
