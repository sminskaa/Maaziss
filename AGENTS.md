# Maziss project instructions

Use the existing `/workspace/Maaziss` checkout. Preserve user work; do not create a
worktree without a specific need or request. Read `docs/STORY_BIBLE.md` and
`docs/ART_DIRECTION.md` before changing narrative or visual content.

## Owner decisions

- English game, zero additional budget. No paid service or new subscription.
- Final target: a desktop game installed and running locally on the player's computer,
  fully playable offline. Godot remains the main game engine. HTML pages are review
  prototypes, not a decision to ship a browser-only or server-dependent game. Bundle
  required art, dialogue and generated audio; use local saves. No required runtime
  AI/API calls, login, asset download or online DRM. Online development is distinct
  from offline player runtime. Exact desktop operating systems remain to be agreed.
- Approved visual starting point: `art/proposals/apartment-cartoon-v2.png`.
  Preserve it. Door/window frames should be mostly straight, with modest hand-drawn
  irregularity. Use the approved painted cartoon palette, texture and lighting.
- Characters know only what they have learned. Maziss does not know whether the
  murderers intend to leave the city. His aim is to escape them and investigators.
- Use only the owner's recordings as voice references. Do not publish private audio,
  voice caches, model files or secrets as part of a review or source bundle.
- Self-contained HTML previews work for the owner. Inline chat images do not.
  Deliver visuals and interactive work through HTML links; do not keep retrying inline
  pictures or claim repository changes repair the host chat renderer.
  Use readable preview files (0644) and traversable preview folders (0755), and never
  claim chat delivery works solely because an internal browser renders it.
- On 18 October the owner confirmed older 2–2.5 MB HTML reviews still worked,
  while the new 10–18 MB reviews opened as source or failed in the web preview.
  The 850 KB `visual-preview/maziss-review-small.html` successfully displayed in
  the owner's panel. Prefer a compact review around or below 1 MB with native
  video controls, an embedded still fallback and no required JavaScript/WebGL.
  This is a tested workaround, not an established platform size limit or a repair
  of the chat renderer. Keep larger live models optional. Use
  `python3 tools/build_compact_character_review.py` after rendering the painted
  model; it re-encodes actual retained frames without changing art or motion.
- The owner rejected the latest whole-sprite projection as distorted and
  unrecognizable. Preserve the original drawings and useful existing3D motion;
  reconstruct the recognizable shapes before UV painting. Do not keep patching
  repeated portrait projections. Research and the explicit allowance-pause state
  are saved in `docs/RESUME_CHARACTER_REBUILD.md`; no replacement model was built
  before that pause.
- On 19 October the owner supplied `white_mesh.glb`. Its recognizable sculpt now
  supports a separate rig study; see `docs/SUPPLIED_CHARACTER_STUDY.md`. Preserve
  the original file privately. The bag-side hand shares the bag's surface and is
  held quiet for this study; independent movement needs separate topology. Do not
  describe the shaded model as finished painted art or a production-ready rig.
- The owner prefers the supplied-mesh/complete-geometry method over the earlier
  sprite projection. Next work should match Maziss to the room's painted colours,
  lighting and contours. Room changes should be small and separately reviewed.
  A clean room reference was supplied for possible owner-provided 3D modeling.
  Keep movement scale tied to the floor/camera perspective and fixed body
  proportions; never normalize every animation frame to its bounding box.
- The owner supplied a dimensional cutaway room image and clarified a16:9 game
  viewport. A separate image-assisted reframe removes the white surround and
  pointed lower floor; `visual-preview/maziss-room-16x9.html` includes a JPG
  download. This is a proposal, not a replacement approval or a room mesh.
  Recalibrate floor, camera, furniture obstacles and character size for this view;
  do not copy the prior room's screen coordinates unchanged.
- The owner requested an interactive first sofa action: click floor to walk,
  select Use and click the sofa to sit on one fixed clear right cushion, away
  from the pillows. Clicking floor afterward stands and walks. A separate fitted
  seat/floor proxy and actual rendered model poses support the compact offline
  `visual-preview/maziss-sofa-sit.html` study. Preserve the room and pillows;
  see `docs/SOFA_INTERACTION_STUDY.md` and actual Art/QA evidence. This is not
  yet an interaction installed in the main Godot game.

## Agent operation

GitHub is the versioned source/review location. Follow docs/BACKLOG.md and
docs/AGENT_WORKFLOW.md: show a bounded assignment before substantial work, default
to at most two worker agents, use a feature branch and reviewable pull request for
future increments. The owner controls creative approval and merge/public-release
decisions. The initial checkpoint saves the existing project on main; it does not
approve the rejected walking animation. Keep personal footage/intake notes,
generated private previews, models and caches excluded from commits and packages.

Role instructions are in `agents/ROLES.md`. Role descriptions alone do not create
running agents. The coordinating assistant starts only workers needed for a bounded
assignment, using native agent tools when available. The owner has requested visible
multi-agent learning; use small demonstrations, not all roles for every task. Workers
consume model allowance. They do not continue running indefinitely between turns.

Before delegation record a task ID, role, objective, allowed files, deliverable and
acceptance criteria in `production/agent-board.json`. Update actual agent identifiers
and observed states after tool results; do not invent running agents or progress.
Avoid overlapping file ownership. Workers must report what they changed, what they
checked, uncertainties and blockers. The coordinator integrates and reviews results.

The owner directs strategy. The coordinating assistant currently combines CEO and
human-liaison duties. CTO, Art, Story, QA and Research workers are started as needed.
QA provides a scoped release recommendation with evidence, never a guarantee that a
game is bug-free or unhackable. Owner approval is final for public releases.

The HTML activity board is a generated snapshot, not live monitoring. Its timestamp
and activity log must make that clear. `python3 tools/build_agent_board.py` rebuilds
it from the registry; it cannot independently query native agent runtime status.
Do not create pretend director activity, unearned test passes or fabricated research.

## Session continuity and allowance

Start from `docs/SESSION_HANDOFF.md`, then read only relevant sources and required
project guidance. Keep that handoff short and current at checkpoints; detailed
evidence belongs in linked reports. Prefer bounded tasks, concise updates, targeted
searches and compact tool output. Give workers focused briefs and relevant file
paths instead of the entire chat when possible. Preserve the owner's actual-image
Art/QA review requirements. Do not read embedded-media HTML or the full generated
activity board into context to discover project state.

Animation work is paused by the owner's latest instruction until they say the
allowance has reset or explicitly tell us to resume it. Workflow/continuity work
may continue. See the current handoff for the pending seating/speed changes.
