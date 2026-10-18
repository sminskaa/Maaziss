# QA-001 — Prototype readiness review

Reviewed 17 October 2026. This is an independent evidence review, not a new test run
or a security certification. No tests were rerun for this assignment.

**Recommendation: go for owner creative review; no-go for public release.** The
recorded checks support reviewing the existing apartment prototype. They do not
establish readiness of the approved painted artwork as playable assets, later scenes,
or an unrestricted public build. Public release also requires the owner's approval.

## What the evidence supports

| Area | Available evidence and limit |
| --- | --- |
| Existing apartment interactions | `build/checks/browser-results.json` records 19 checks with an empty error list, including visible floor movement, sofa/tool/window/leaflet progression, inventory preservation, unsupported-verb feedback and the Morgrave plan. This is recorded evidence, not my observation of a fresh run. |
| Save recovery | The browser record includes checkpoint restoration, page reload, a distinct previous backup and recovery from a corrupted primary save. It does not promise recovery of every unsaved or unsynchronised action. |
| State model | `.local/cache/checks/model.log` reports Godot 4.6.3 and **2,505 assertions, zero failures**, matching `docs/VALIDATION.md`. The log itself does not record a process exit code or tie the run to a source revision. |
| Browser scope | The result records Chromium `154.0.8037.57`, consistent with the validation document. No inspected result establishes Firefox, Safari, mobile or real-GPU behaviour. |
| Controls | The documented nine-verb interface has recorded checks for several relevant behaviours. All nine buttons being present does not mean all nine have useful apartment actions: there is no NPC conversation, Give transfer or required item-to-item combination in this room. |
| Approved visual direction | `docs/ART_DIRECTION.md` records the owner's approval of `art/proposals/apartment-cartoon-v2.png`, including Maziss and restrained frames. It explicitly identifies this as a composition, while the playable background and character remain placeholders. No inspected test establishes integration of that artwork. |

## Claims still outside this review

The validation document reports resource import, startup, export, archive verification,
repeatable setup, native save-store checks and screenshot inspection. Those claims are
not contradicted by the two inspected result files, but those files alone do not
independently demonstrate all of them. Neither includes a run timestamp or source
revision, so their relationship to the latest working tree remains unproven here.

Dialogue humour, clue fairness and accessibility require human playtesting. Walking
animation, automatic approaches to objects, later scenes and in-game voice/music are
unfinished. The accepted development-time voice sample is not in-game audio validation.
Security, licence provenance, private-file exclusion and performance need explicit
release checks; this review supplies no guarantee of a bug-free or unhackable game.
The owner's working HTML preview is the delivery route; internal rendering does not
prove inline chat images work for the owner.

## Acceptance checklist for integrating the approved art

- Preserve v2 unchanged as the approved reference. Make a separate background without
  a baked-in Maziss, plus a separately drawable character consistent with his approved
  appearance; agree any character-design changes with the owner.
- Preserve mostly straight door/window frames, palette, texture and lighting. Check
  character scale, feet placement, foreground occlusion and clear walkable space.
- Match visible interactive props to their hotspots and actual state: sofa, metal
  strip, window catch, open/closed window and collected/uncollected paper. Decorative
  generated details must not silently become clues or plot facts.
- Verify legibility of objects, inventory icons, verb selection and subtitles at the
  supported viewport sizes; confirm the room remains readable behind the interface.
- Rerun relevant state and browser checks after integration, add visual/state checks
  for the new assets, and record build/source identity with the results. Agree and
  measure a target-platform loading, frame-time and memory budget before release.
- Inspect the actual export for private recordings, caches and proposal/reference
  assets; obtain owner creative acceptance through the working HTML preview.

## Handoff

**Changed:** only `production/QA_READINESS_REVIEW.md`.

**Inspected:** `AGENTS.md`, `agents/ROLES.md`, QA-001 in
`production/agent-board.json`, `docs/VALIDATION.md`, `docs/ART_DIRECTION.md`,
`build/checks/browser-results.json` and `.local/cache/checks/model.log`.

**Unresolved:** no fresh execution, asset integration, source-to-result traceability,
target-platform/performance certification or public-release approval was established
by this assignment.
