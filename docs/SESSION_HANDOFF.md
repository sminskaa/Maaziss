# Current session handoff

## Status and permission

Owner clarifies this is private, non-commercial experimentation, with no
distribution planned. Free non-commercial services are eligible for trials;
check their specific terms. Do not reject them for hypothetical commercial use.
No paid service is authorized; prior private-asset handling still applies.

Animation is **paused**. The owner wants to use the remaining allowance to improve
efficiency/continuity and research later art/room interactions. Resume character
animation only when they say allowance has reset or
explicitly authorize it. Do not restart rendering merely because a new chat opens.

## Working result and next task

The owner says the interactive sofa study is on the right track. In the compact
offline HTML, floor clicks walk, Use on sofa approaches/turns/sits, and another
floor click stands/walks. Actual Art/QA review passed for this first candidate.
The next authorized animation changes, once unpaused, are deeper seating between
the yellow and white pillows and moderately faster walking with matched gait.
The full new owner list (blur/alpha, palette, clothing detail, facial acting and
15 room interactions) is saved in `ROOM_INTERACTION_BACKLOG.md`, with role owners.
Actual-source research and a proposed one-stool trial are in
`ROOM_INTERACTION_RESEARCH.md`. The owner then authorized one geometry-only stool
trial. A complete model and three actual views are now saved; final Art/QA checks
are being closed out. Art and QA must inspect the same actual changed imagery and
jointly recommend proceeding; intact backgrounds after object movement are a gate.
Latest clarification: sitting furniture must be actual visible 3D geometry, not
flat sprites or hidden proxies alone. The research notes now include checked
Meshy/Tripo free-plan limits, TripoSR CPU support and its currently failing demo.
No service was given private art and no model generation was performed.

## New stool checkpoint

- Read `docs/STOOL_MODEL_STUDY.md`, `production/ART_STOOL_MODEL.md` and
  `production/QA_STOOL_MODEL.md` for the geometry-only result and final review state.
- Sources: `tools/build_stool_study.py`, `tools/build_stool_review.py`.
- Private assets: `build/checks/stool-study/maziss-stool.blend`, `maziss-stool.glb`,
  `model-manifest.json` and the three PNG views.
- Preview: `visual-preview/maziss-stool-study.html`, 552020 bytes,
  SHA-256 `9c1bac72668f5ca9d2b9239726a68b852cce512b7f2062e4f723012e35acc960`.
- GLB SHA-256 `5e4754e37cbf1e4764f32c80b50e9a6e6bf365865766f4ead7d351d59c1e713c`.
- Six solid mesh parts: seat, four legs and footrest ring; preliminary base colours
  and UVs. A QA-found leg/seat gap was corrected, with the same three views rebuilt.
- Do not redo research/modeling from scratch. Next shape/paint choices need owner
  feedback. Clean background, room replacement, movement and Maziss sitting on the
  stool are not yet implemented. Character animation is still paused.

- Repo: `/workspace/Maaziss`; branch: `feat/reference-human-walk`.
- Draft PR: https://github.com/sminskaa/Maaziss/pull/4; no merge approval.
- Preview: `visual-preview/maziss-sofa-sit.html` (private/ignored).
- Detailed task/assets/source map: `docs/RESUME_SOFA_INTERACTION.md`.
- Preserve supplied geometry, original artwork and working preview. Final target:
  offline desktop Godot; HTML is a review prototype. Inline chat images fail.

## Efficient restart

1. Read this file and applicable project instructions. Check branch/worktree status
   and required private assets before claiming the previous state is available.
2. Read only task-relevant source/report sections. Do not reprocess the entire chat,
   old experiments, generated board, base64 HTML, recordings or every reference.
3. Work on one bounded visible change. Reuse valid renders/evidence; verify changed
   behavior and actual images. Keep required Art/QA review, with focused briefs and
   selected files rather than full-history agent handoffs where tools permit.
4. At a checkpoint, save source and a brief handoff: current result, pending request,
   relevant paths, remaining issues and authorization state. Update this file in
   place; do not grow it into a transcript.

The same workspace or private asset backup is needed after a restart: Git alone
does not retain the supplied models, derived motion and generated previews.
Context shortening does not replenish usage allowance or guarantee a saving of a
specific amount. Automatic compaction may already shorten a long visible chat.
