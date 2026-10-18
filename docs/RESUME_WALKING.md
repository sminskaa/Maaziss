# Resume Maziss human walking correction

Owner asked to pause because allowance was nearly exhausted. This checkpoint records
actual retained work; a new animation has not been implemented or reviewed.

## Preserved

- Main project: /workspace/Maaziss. Original approved art and walking v1–v4 HTML remain.
  V4 is rejected by owner; no natural walking cycle is approved.
- Three owner reference videos remain under /workspace/attachments. Exact paths and
  metadata are in the local, unversioned docs/WALKING_FOOTAGE_INTAKE.md. Side reference: Video Projectbiks.mp4.
- Local analysis environment: .local/motion/venv, MediaPipe0.10.21/OpenCV4.11.0.86.
  MediaPipe's bundled full pose model was available. No paid service/API used.
- Actual raw side tracking is retained at build/checks/reference-motion/raw-side.json.
- The previous native worker /root/human_motion_analysis is no longer active.
  Its final normalized reference-motion.json and report were not saved before pause.

## Preliminary findings reported by the worker

Treat these as preliminary until the raw tracking and frames are reviewed again:
central side stride frames60–100 (2.000–3.333s at30fps), approximately1.33s per stride;
right heel contact near frame60, left heel contact aroundframes78–80, right toe-off
aroundframe84. Exported playback speed was not independently verified. Toe landmarks
are noisy on motion blur; hip/knee/ankle observations are more useful. Earlier worker
reported peak swing knee flexion around65–70degrees nearframes68–69; verify before use.

## Next work

1. Inspect retained tracking and exact reference frames; finish normalized pose samples
   with measured timing, visibility and honest uncertainty. Save reproducible analysis
   helper and production/MOTION_REFERENCE_ANALYSIS.md; do not invent missing values.
2. Retarget observed pose relationships to FIRST Maziss artwork/proportions. Replace
   rejected screen-space knee solving: solve/project human leg motion in its sagittal
   plane so front/back knees do not bend sideways. Do not copy actor image coordinates
   directly because footage uses an elevated, oblique camera.
3. Review an actual side-view cycle before expanding directions. Preserve original
   face/body/boots. Avoid renewed redesign and excessive cutout distortion.
4. Inspect rendered movement, stance, low swing-foot clearance, weight transfer, arm
   coordination, depth views and stop/turn transitions. Numeric tests alone cannot
   establish naturalness. Independent QA remains unstarted.
5. Deliver self-contained HTML in visual-preview with0644 permissions and0755 folder.
   Embedded chat images fail for owner; HTML panel works. Do not expose personal videos
   in previews or shipped game. Final game remains offline desktop Godot.

Task briefs: MOTION-001, TECH-005 and QA-005 in production/agent-board.json. No commits
or GitHub push were made. No new environment configuration draft was saved for motion
analysis; reproducible setup still needs to be documented if this tool is retained.
