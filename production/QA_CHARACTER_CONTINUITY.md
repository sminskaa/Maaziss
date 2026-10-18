# QA-004 — Character proportions and continuity

**Go for owner review of revision 3. Aesthetic approval remains with the owner.**
The revised renderer preserves the accepted leg mechanism while changing the painted
upper body, arm motion and trouser-to-boot registration. This is an HTML review study;
Godot remains the intended engine for the installed, offline desktop game.

## Executed validation

Tested 17 October 2026 with Chromium 154.0.8037.57:

- **33 browser checks passed**, with no page errors or external asset requests.
- **15,487 gait assertions and 9,584 navigation assertions passed** in actual Node runs.
- Browser root-position history contained **2,163 legal samples**. Both airborne and
  planted foot projections retained the room's 32 px clearance through the recorded
  traversal and turn sequence. Chest detour, invalid clicks, rapid redirection, scaled
  pointer input, pause/resume and bounded stall recovery still passed.

Actual render/gait history from the dedicated horizontal route contained 266 records:

| Acceptance point | Evidence |
| --- | --- |
| Restrained, moving arms | Opposing rotations, both signs observed; maximum absolute rotation **5.9994°**. |
| Modest painted torso motion | Absolute lean ranged **5.2001–6.7994°**, with a nonzero variation. The anatomical gait solver's separate angle remains bounded too. |
| Corrected proportions | Nominal head-to-pelvis / pelvis-to-floor division is **49.26% / 50.74%**, calculated from the renderer's declared dimensions. |
| Boot registration | Rendered shin endpoints and transformed boot-cuff points had **0 px** difference in sampled metrics. |
| Retained alternating gait | Six new stance contacts: **left, right, left, right, left, right**; each identified leg crosses ahead of and behind the body. |
| Retained foot planting and lift | Maximum same-contact world drift **0 px**; maximum swing lift **19.06 px**. |
| Retained pace | Peak horizontal speed **413.75 scene px/s**; projected depth travel is deliberately slower. |

Pause checks now include the painted torso and arm transforms, not only the root and
IK pose. Contact screenshots use the real pause control to avoid capture-latency crop
errors. The test permits at least five alternating contacts for this fixed-length
route because the corrected character scale increases stride length; this actual run
recorded six. No implementation or asset was changed by QA.

Tested HTML SHA-256:
`6a49d8d0d5a81da45b2fe91c3b35fb440208e8b830fd2cb5a867509fb02cb903`.
It matches `build/checks/walking-revision/build-manifest.json`, build `14378f795dba`.
Results, gait samples and screenshots are in `build/checks/walking-revision/`.

## Visual inspection and qualifications

Inspected the matching-camera earlier/rejected/corrected comparison, seven actual
rendered gait phases, and the narrow front-view/debug screenshot. The current version
has a shorter painted upper body relative to its legs than the rejected version.
Shoulder/hand positions vary slightly through the phases. Trouser legs visually reach
the boot shafts; no obvious detached boot, duplicate hand or gross shoulder hole was
visible in those sampled side phases. The front-view screenshot remains readable at
the tested narrow viewport, though it catches the short foot-settling transition.

There are limits to these conclusions:

- The 49/51 figure is nominal rig geometry, not a measurement of the painted silhouette
  after rotation or a proof that the original character likeness is restored. The
  earlier comparison faces forward while the corrected character is angled; head
  silhouette, clothing and posture remain visibly different.
- Zero cuff endpoint error is partly guaranteed by sharing one transformed cuff point
  between the two draw calls. It establishes mathematical registration, not perfect
  alignment of opaque pixels or every ankle at every possible angle. The sampled
  screenshots provide a separate visual check, not exhaustive certification.
- Rotating masked painted arms can still reveal small seam defects at uninspected
  phases or directions. A full turn/stop animation review is still warranted before
  approving the character for production.
- Contact math does not certify naturalness, weight, appeal, frame rate, accessibility,
  other browsers or desktop builds. Foreground occlusion and Godot interaction
  integration remain separate work. Working HTML delivery does not fix chat images.

**Changed:** `tests/browser_walking.py` and this report only.

**Inspected:** `AGENTS.md`, QA-004 brief, current walking runtime and rig metadata,
gait/navigation test outputs, final manifest and browser evidence, actual gait contact
sheet, narrow screenshot, and `visual-preview/maziss-character-comparison.html`
(captured as `character-comparison.png` in the evidence folder).

**Unresolved:** owner approval of appearance and motion, exhaustive seam/turn review,
production animation/occlusion, and native game integration/performance.
