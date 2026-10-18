# Current project status

This is the first source checkpoint of an unfinished game, not a finished release.
The final product is intended to be an offline desktop Godot game.

| Area | Current state |
| --- | --- |
| Runnable Godot game | One apartment; verbs, inventory, notebook reasoning, local save/load and simple click movement |
| In-game graphics | Original SVG placeholders; not the approved painted cartoon presentation |
| Approved visual direction | `art/proposals/apartment-cartoon-v2.png`; retained unchanged |
| Painted walking experiment | Separate HTML/Canvas study in `walking/`; previous revisions rejected by owner |
| Reference-based walk | Revision 7 uses actual FBX joint trajectories with revised boots, limb layering and continuous trousers; separate HTML candidate awaits owner review |
| Voice | Development-only synthesis tool and accepted sample voice; personal recordings/models/audio excluded; no in-game speech |
| World/story | Owner-established facts in STORY_BIBLE.md; opening puzzle in OPENING.md |
| Later scenes/cutscene | Not implemented |
| Windows | Owner confirms project opens in Windows Godot; broader save/offline/input walkthrough remains pending |
| Agents | Bounded task workers, not permanently running directors; snapshot in production/index.html |

Start with [Windows setup](WINDOWS_SETUP.md), [the backlog](BACKLOG.md), and
[the agent workflow](AGENT_WORKFLOW.md). Source is visible directly on GitHub.

The game's own code and original assets have not been given an open-source licence
merely by publishing this repository. Godot/third-party engine notices remain under
`docs/engine-notices/`. No commercial-game screenshots or assets are shipped.

Personal voice/video recordings, model weights, generated private previews, raw motion
tracking, caches and local intake paths are not part of this source checkpoint. Future
tasks requiring those inputs need the existing local files or an owner-provided copy.
