# Resume the sofa interaction

Owner feedback on 19 October 2026: the current interaction is on the right track.
Before further animation work, the owner asked about reducing context usage and
continuing after a reset. This handoff records the next changes; they are not yet
implemented. Preserve the working preview while making the next version.

## Next requested changes

1. Seat Maziss deeper in the sofa, in the area **between the yellow and white
   pillows**. This supersedes the previous clear-right-cushion placement. Inspect
   the actual room before choosing the new contact point; keep pillows unchanged
   and check the character/furniture depth order, hip support and boot contact.
2. Make him move a little faster. Increase walking speed moderately and keep gait
   playback matched to distance to avoid sliding. No exact speed was specified.

## Working checkpoint

- Repository `/workspace/Maaziss`, branch `feat/reference-human-walk`.
- Implementation commit `7a59c60`; draft PR #4:
  https://github.com/sminskaa/Maaziss/pull/4. Do not merge without owner approval.
- Current private preview: `visual-preview/maziss-sofa-sit.html`, 978857 bytes,
  SHA-256 `9b2230c333c0e68f1e104c9ab591f605410bc7ace023ed85d6c938a519956a21`.
- Floor click walks; Use plus sofa approaches, turns and sits; floor click while
  seated stands and walks. This HTML review is separate from the main Godot game.
- Read `AGENTS.md`, `docs/ART_DIRECTION.md`, `docs/SOFA_INTERACTION_STUDY.md`,
  `production/ART_SOFA_SIT.md` and `production/QA_SOFA_SIT.md` before changing it.
- Source: `tools/character_sitting_pose.py`, `tools/render_sofa_sit.py`,
  `tools/sofa_interaction.js`, `tools/build_sofa_sit_review.py`.
- QA: `tests/browser_sofa_sit.py`; 30 checks passed on the original delivery,
  then 23 focused checks and decoded-media checks on the final delivery. Art and
  QA opened actual output images. New placement needs new visible inspection.

## Private files and continuity

The supplied sculpt, rig, FBX-derived curves, renders and generated HTML are
intentionally ignored by Git. A new chat needs the **same workspace** or a private
copy of these assets; cloning the public repository alone will not restore them.
Required retained paths include `private/models/white_mesh.glb`,
`build/checks/supplied-character/`, `build/checks/room-cutaway/` and
`build/checks/sofa-sit/`. Do not publish them to solve session continuity.

Keep complete supplied geometry and fixed body proportions. Avoid the rejected
whole-sprite projection method. The bag-side hand is joined to its bag and cannot
yet act independently. Face, hands and painted surface detail remain unfinished.
Original art is preserved. Final target is an offline desktop Godot game, with no
additional budget. Inline chat images fail for the owner: deliver compact HTML.

Context compaction is distinct from usage allowance. A shorter handoff can reduce
repeated history, but it does not replenish an exhausted allowance.
