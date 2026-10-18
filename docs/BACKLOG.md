# Visible project backlog

The owner sets priorities and approves creative results. These are development tasks,
not background jobs: listing a task does not start an agent. GitHub Issues carries the
live discussion; this file is the initial planning snapshot.

| Priority | Task | Owner / review | Acceptance |
| --- | --- | --- | --- |
| P1 | First Windows local run | Owner, assisted by coordinator | Import project.godot, F5, verify controls and save/reload; play after disconnecting internet |
| P1 | Correct human walking from owner footage | Motion/implementation worker, independent QA, owner visual approval | Real reference poses/timing; natural side walk first; preserve original Maziss; inspect front/back and starts/stops; no sideways knees or detached boots |
| P2 | Integrate approved painted art and accepted motion into Godot | Art/implementation worker plus QA | Correct scale/occlusion/hotspots, existing room still solvable, no regressions in interaction/save state |
| P2 | Refine opening English dialogue and voice integration | Story, then implementation/QA | Character knowledge respected, owner approves humour/delivery, subtitles/volume controls, bundled offline audio |
| Later | Street, first NPC conversation and next escape-plan step | Story design before implementation | Owner-established story direction; meaningful next playable increment |
| Later | Standalone Windows executable | Implementation plus Windows QA | Run without Godot editor, offline assets/local saves, tested Windows package |

## GitHub tasks

- [#1 — Verify first Windows Godot run and offline save/load](https://github.com/sminskaa/Maaziss/issues/1)
- [#2 — Correct Maziss’s walk using recorded human movement](https://github.com/sminskaa/Maaziss/issues/2)
- [#3 — Integrate approved painted apartment and accepted movement into Godot](https://github.com/sminskaa/Maaziss/issues/3)

## Working rule for each increment

1. Coordinator shows the task, named worker(s), allowed files, acceptance criteria and
   intended checks before substantial work. Default at most two worker agents at once.
2. Use a feature branch. Keep the change small enough to review and roll back.
3. Implementation delivers files and an actual playable/visual result; QA reviews it
   separately when useful. Report uncertainty and untested platforms explicitly.
4. Open a pull request with the concrete before/after behavior, checks and limits.
5. The owner reviews creative results and controls merge/public release decisions.

The initial source checkpoint establishes a baseline on `main`. Future changes do
not silently become accepted artwork or finished features because a test passed.
