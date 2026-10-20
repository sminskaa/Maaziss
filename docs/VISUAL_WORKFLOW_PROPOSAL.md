# Proposed visual workflow reset — awaiting owner agreement

Follow-up: the owner asked how to direct interactively. The bounded first board is
implemented at `visual-preview/maziss-director.html`; see `SESSION_HANDOFF.md`.
This does not approve a new rendering architecture or the current character art.

The owner reports that the results do not meet the intended visual direction.
This document proposes a method; it does not approve an architecture, authorize
an editor implementation, or change stable agent instructions. No game, artwork,
rig or existing interaction was changed during this audit.

Source brief retained privately: `private/briefs/CODEX_GAME_DIRECTOR_BRIEF.md`.
Existing implementation checkpoint: `33260fc`, branch `feat/reference-human-walk`.
All original art, models, motion references, recordings, research and studies stay
preserved. Generated/private assets remain outside Git; preservation in the current
workspace is distinct from a complete backup in a fresh clone.

## Owner constraints that supersede the previous next task

- Work exclusively on the first room and Maziss until the whole scene meets the
  owner's expectations for appearance, walking, interactions and speaking.
- The existing original room and character drawings define the intended appearance.
  Preserve their masters and the original story. Discworld II is the closest
  presentation reference. No new area, character or story redesign.
- Restart derived production assets if evidence warrants it; retain prior resources.
- The owner directs visually using natural language and simple review controls.
  Codex operates the technical tools; no Blender/Godot operation is required of them.
- No additional budget. Final player runtime remains offline desktop Godot.
- Compact HTML reviews work for the owner; embedded chat images do not.
- Obtain agreement on the bounded first proof before implementation. Update stable
  AGENTS/role instructions only after the proposed workflow is approved.
- Latest owner clarification: neither the current animation nor the current 3D
  character meets expectations. The model is usable as a starting resource but
  still needs substantial work. A drastic pipeline change is acceptable. The
  owner has limited ability to supply motion videos; progress must not depend on
  further recordings, and previous video-driven attempts are not accepted results.
- Latest owner clarification: an interactive visual communication tool is required;
  text alone has been insufficient. Include a small directing/annotation tool in
  the first phase alongside appearance tests; do not postpone it until animation
  is settled. It must let the owner point to corrections rather than draw assets
  or record reference performances.

## Read-only audit: confirmed facts

1. `project.godot` starts `scenes/main.tscn`. `scripts/main.gd` constructs the
   original game using `assets/room.svg` and `assets/maziss.svg` TextureRects.
   Its floor-click action tweens a static picture. Recent stool reviews are
   separately authored Blender renders embedded in HTML, not those actions running
   interactively in the Godot scene.
2. The latest supplied-character derivative is a real skinned 3D surface with a
   14-bone skeleton: Spine, Head, and upper arm/forearm/hand/thigh/shin/foot per side.
   Arms, legs, torso and head can be posed. The derived right arm is independent
   of the satchel; the original supplied rig remains unchanged.
3. A direct read-only Blender inspection found no shape keys and no image-texture
   nodes in that derivative. There are no finger, jaw or facial bones. Its broad
   surface colours and toon lighting do not reproduce the original drawing's
   detailed ink, clothing texture, face or expressions. Speaking/blinking are not
   production-ready capabilities of this rig.
4. The room remains a painting. Stool geometry and fitted desk/item contact volumes
   support the recent study. This is not a completely modeled room or a finished
   library of independently movable textured objects.
5. The latest independent audits/reviews were scoped recommendations for owner
   review, not owner creative acceptance. Technical contact and playback passes do
   not demonstrate that the character looks or acts as the owner intends.

The original approved composition and the latest exposed-hand model render were
actually opened during this audit. The visual difference is substantial; further
contact fixes alone cannot recover the original painted character design.

Unproven: which affordable visible-character pipeline can preserve that identity
across new poses; whether existing references cover the necessary directions; and
which precise positions/timing the owner intends for each action. These require
small visual tests, not assumptions based on compile/test results.

## Rendering choices to test, not silently adopt

| Approach | Strength | Main constraint in this project |
|---|---|---|
| Directional painted 2D sprites | Closest control over the original painted appearance | Consistent new views/poses/frames must be produced; a single image is insufficient |
| 2D skeletal parts | Reusable small gestures and easy handles | Missing hidden views and deformation can produce the puppet/tearing problems already observed |
| Painted room plus stylized 3D actor, optionally rendered to sprites | Reuses motion/geometry and supports many poses | Existing sculpt/materials visibly diverge; a filter or pasted portrait will not repair identity |

Provisional recommendation: retain a painted 2.5D room. Keep the current 3D work
as a motion/depth reference while comparing a sprite finish and a stylized 3D
finish on one matching pose and one tiny movement. Decide the visible-character
method from those results. Do not rebuild the room to suit the current model.
Missing perspectives and room states can be separately approved derived assets;
masters remain intact. No promise of automatic all-angle character generation.

## Ways of directing

1. Annotated stills/storyboards: cheapest and fastest first communication test;
   exact contacts and silhouette can be agreed before animation.
2. Small browser directing board: real reference assets, draggable foot anchors,
   facing arrows, path/stop markers, a few named beats and save/open. Recommended
   next step if the stills establish the intended direction.
3. Full limb/timeline editor: defer until rig/appearance and simple controls prove
   adequate. It would otherwise become another major project and cannot invent
   missing art or facial controls.

The browser board manipulates documented scene data. Godot consumes the same data,
or a deterministic conversion with explicit units, facing and event semantics.
Every accepted feature must be shown running in Godot. Browser playback alone is
not evidence of engine integration. Initial browser arrows/cutouts are blocking
references, clearly labelled; sliding an unchanged drawing is not a walk cycle.

## Proposed small-step sequence

1. **Pin references.** Show the exact already-supplied room and Maziss originals
   at game size with file labels; confirm the reference pair and a short checklist
   of likeness, proportions, clothing detail, line, colour, scale and lighting.
2. **Minimal interactive direction tool, alongside appearance feasibility.** Use
   the originals on a lightweight HTML board with draggable start/end foot anchors,
   path points and facing arrows. Allow image annotations and pause/scrub on a
   supplied short review clip, attaching notes to a frame/time. Save/reopen/export
   direction data that Codex can read. First prove position, facing and one marked
   visual correction; add clip annotation when the first clip exists. Clearly
   distinguish instructions from actual animated output. No full pose editor yet.
3. **Appearance feasibility.** Compare one matching pose using a painted
   sprite approach and a properly shaped/styled 3D approach. Judge silhouette,
   face, clothing and painted detail against the original at game size. Improve
   one chosen direction before making a longer sequence. Existing 3D work is a
   labelled staging aid until its finish is accepted. If neither affordable route
   matches, report the limitation before expanding it.
4. **Short motion proof.** With the chosen appearance, show a few seconds of
   walking and stopping, including idle and one direction change. Source reference
   research, suitable existing FBX clips and motion analysis are Codex's work;
   further owner videos are optional. Reference quality and retarget quality are
   separate: check planted feet, stride/speed agreement, joint continuity, weight
   transfer and garment continuity on the actual rendered character. Approve look
   and movement separately. Do not infer acceptance from previous improvement.
5. **Same action in Godot.** Load the same positions/facing/timing into the real
   game, show its captured output and compare endpoints, scale, depth and stopping.
   A data round-trip must preserve approved choices. Codex runs these tools.
6. **One contact action.** Right hand reaches the existing desktop and returns to
   idle. Approve arrival, turn, reach, contact and return as individual beats.
   Then test one existing item pickup, such as the pen, including clean background,
   attachment, release/inventory and save/reload. Do not bundle a long stool action.
7. **Complete this room.** Extend approved pieces to the already-requested room
   interactions and a short speaking/facial-animation test based on existing story.
   No new areas/characters until the owner accepts the complete first scene.
8. **Extract reusable templates.** Only owner-approved clips/data/target rules enter
   the library, with baseline previews and parameters such as hand, target and timing.

Each iteration: intent → proposed images/beats → owner correction → approved scope
→ implementation → actual Godot capture + Art/QA → owner acceptance. Rejected
output stays explicitly rejected. Correcting one beat preserves the others.
Statuses stay separate: proposed / implemented / tested / owner-approved.

## Cost and governance

Use the coordinator plus bounded implementation/review help when useful, normally
at most two workers. More agents are not the proposed cure. Art compares against
original references; QA checks actual engine behaviour and visual continuity.
Neither substitutes for the owner's creative decision. Keep one short handoff
with approved references, current beat, exact preview/data, unresolved issue and
next task. Preserve completed source/resources and avoid rereading the whole chat.

Next approval requested: agree this staged method and the small directing/appearance proof
before implementing a new pipeline, creating the board or modifying the game. The attached brief's sections
1,12 and14 explicitly request proposal/approval before implementation or stable
workflow-rule changes. No replacement AGENTS instructions have been installed.
