# Owner's room and character work list

Recorded 19 October 2026. These are future requirements, not completed features.
The owner prefers small iterations, one visible change at a time. Character
animation remains paused until allowance resets or the owner explicitly resumes
it. Research/planning is authorized now. No new worker was started for this record.

## Responsibilities

| Role | Responsibility |
| --- | --- |
| Coordinator | Keep this list, choose one bounded experiment, save checkpoints and deliver compact HTML. |
| Art director | Match the original cartoon design, paint clean backgrounds, approve object shapes/textures, lighting, silhouettes and depth order from actual images. |
| CTO / implementation | Model props, match camera/scale, implement animation/contact, object state, inventory and offline Godot integration. |
| QA | Independently inspect actual before/during/after images and playback with Art; check continuity, interactions, persistence and reversibility. Code checks alone cannot pass a visual change. |
| Research | Check practical free tools, documented capabilities, licenses and hardware needs; distinguish reading documentation from successfully using a tool. |
| Story director | Resolve event order and object purpose where needed without inventing canon, particularly the window paper and unspecified desk equipment. |

These are role assignments, not claims that agents are currently running. Art and
QA must jointly recommend each visual change; the owner gives creative acceptance.

## Character and motion

| ID | Owner requirement | Lead and review |
| --- | --- | --- |
| CHAR-01 | Character remains blurry. Diagnose source render resolution, delivery encoding and display scaling separately. | Implementation + Art, QA |
| CHAR-02 | Sitting makes him blurrier; his left side mixes with the environment. Check actual alpha edges, occlusion masks and compression at multiple descent phases. | Art + implementation, QA |
| CHAR-03 | Increase walking speed moderately, keeping stride playback matched so feet do not slide. | Implementation, Art + QA |
| CHAR-04 | Add blinking, directed gaze and mouth movement; later facial expressions must retain Maziss's identity. | Art + rigging, QA |
| CHAR-05 | Colours are too pale for the room. Match saturation, warmth, shadows and the established cartoon palette. | Art, QA |
| CHAR-06 | Restore clothing and boot texture/detail, including seams, folds, wear and scuffs. Flat colour alone is insufficient. Preserve coherent geometry and avoid the rejected full-character picture projection. | Art + implementation, QA |
| CHAR-07 | Sit deeper in the sofa, between the yellow and white pillows; keep the pillows unchanged. Earlier requested correction remains pending. | Art + implementation, QA |

## Room interactions

| ID | Required visible action and resulting state | Primary dependencies |
| --- | --- | --- |
| ROOM-01 | Pick up objects such as a book under the window: show the reach/grasp, remove the room copy and leave a complete plausible surface behind. | Separate prop, clean background, hand contact and inventory state |
| ROOM-02 | Open the window. | Hinges, frame/foreground depth, newly revealed surfaces and catch state |
| ROOM-03 | Open the door. | Hinged door, handle/contact, doorway image or geometry behind it |
| ROOM-04 | Close the door. | Same persistent door and reversible pose/state |
| ROOM-05 | Move the stool out from under the desk and sit on it. | Separate stool, clean background, desk occlusion, collision/seat alignment |
| ROOM-06 | While on the stool, pick up the existing desk pen and write on the existing paper. | Stable seated pose, separate pen/paper, timed grasp, desk/hand contact, marks on paper |
| ROOM-07 | Use the equipment already on the desk. | Identify equipment and intended behavior before scripting effects |
| ROOM-08 | Pick up something on the floor beside and underneath the sofa. | Low reach/bend, sofa occlusion, clean floor, persistent object removal |
| ROOM-09 | Pull the strings left of the door to switch off the light. Provide a coherent dark room state. | Moving cord, reachable hand target, warm-light removal while preserving other light sources |
| ROOM-10 | Have a window paper detach and fall to the floor; pick up the fallen item. Owner also mentioned picking something up from the floor. | Separate paper, airborne/landed/collected states and clean window/floor; exact event linkage needs Story check |
| ROOM-11 | Search behind the sofa pillow and retrieve hidden metal scrap. | Movable pillow, intact sofa behind it, hidden/revealed/collected scrap states |
| ROOM-12 | Lean over the open window. | Open-state prerequisite, sill/body contact, camera depth and safe coherent pose |
| ROOM-13 | Pick up the key already hanging to the right of the door. | Separate key, clean wall/hook behind it, grasp and inventory |
| ROOM-14 | Slightly move the carpet in front of the door. | Separate rug, reconstructed floor and changing contact/shadow |
| ROOM-15 | Pick up a new object revealed under the carpet. | Rug position, hidden/revealed/collected object and clean floor |

The list is a capability backlog, not an approved puzzle sequence. Existing canon
links opening the window to the falling job-fair paper; do not silently change its
trigger while implementing ROOM-10. New object identities and desk functions are
not decided by this list.

## Shared acceptance rule

Art and QA inspect the **same actual output**, at normal game size and enlarged
detail, before/during/after the change. A moved or removed object must leave no
hole, duplicate, old shadow, painted remnant, alpha fringe or implausible patch.
Newly revealed surfaces, perspective, lighting and foreground overlap must remain
coherent. Test the full motion, reset/reverse where applicable and retained object
state. Record image paths, defects and both scoped verdicts; a numeric/code pass
cannot replace these visual checks. Owner approval remains separate.

## First room-asset trial

Start with the **stool only**, as proposed by the owner: isolate its visible design,
reconstruct the background it covers, build a small complete model, composite it
at its original location, then move it a short distance near the desk. Show before,
replacement-at-rest and moved views plus motion in compact HTML. Do not add Maziss
sitting/writing or rebuild other props in this first trial. Art + QA must accept
the background continuity and replacement before proceeding to more interactions.

Owner clarification: the stool and sofa Maziss sits on need visible **3D geometry**,
not a flat furniture sprite beneath a posed character. Hidden contact proxies alone
do not meet the finished interaction requirement. Check actual seat/body contact,
complete furniture shape and real foreground occlusion before adding acting.

Research and the step-by-step trial brief: `ROOM_INTERACTION_RESEARCH.md`.
Current pause and private asset continuity: `SESSION_HANDOFF.md`.

Geometry-only substep completed separately: `STOOL_MODEL_STUDY.md` and
`visual-preview/maziss-stool-study.html`. Art and QA recommend owner review of that
candidate. A subsequent first ROOM-05 action candidate now repairs the background,
replaces the stool with actual geometry, and shows Maziss approaching, pulling and
sitting: `STOOL_INTERACTION_STUDY.md` / `visual-preview/maziss-stool-interaction.html`.
Final Art and QA recommend owner review; approach boot-floor overlap and acting/
paint polish remain. This is one authored offline review action, not main-Godot
integration, stool return, writing or approval of the rest of the room backlog.

A separate owner-directed ROOM-05 revision passes around the stool and ends
facing the writing desk: `STOOL_DESK_FACING_STUDY.md`. It does not complete the
pen/paper writing or other desk-equipment interactions.
