# QA-003 — Revised gait review

**Go for owner review of the revised walking study. Naturalness remains unapproved.**
The previous QA established routing and changing images; it did not establish a
convincing walking cycle. The owner's criticism exposed that gap. This review checks
the actual identities and contacts of both rendered legs, not frame-index changes.

## Final build and executed checks

Reviewed 17 October 2026 using Chromium 154.0.8037.57. Final HTML SHA-256:
`211288e0b1f652b3dae35c3b008ef0337d9b30ca9e90b43b76d8c5bd2dedc98a`.
It matches `build/checks/walking-revision/build-manifest.json` (build `b5b9e95d16ba`).

- `node tests/test_gait.cjs`: **15,487 assertions passed**, including 1,570 room-route
  poses, stance contacts, joint lengths, swing clearance and turns.
- `node tests/test_navigation.cjs`: **9,584 assertions passed**, 1,025 navigation nodes.
- `python3 tests/browser_walking.py`: **26 checks passed**, with **2,186 recorded legal
  root-position samples**. Real browser traversals retain the chest detour, rejected
  wall clicks, adjusted furniture targets, rapid redirection, scaled mouse mapping,
  pause/resume, bounded recovery after a blocked frame and self-contained delivery.
- Both planted and airborne boot ground projections passed the independent Python
  polygon/32 px clearance check across the browser's recorded poses. The rig image
  decoded with real transparency; no external asset requests or page errors occurred.

The dedicated continuous horizontal route yielded **268 rendered-pose records**:

| Requirement | Measured result |
| --- | --- |
| Both legs genuinely change lead | Each identified leg moved both ahead of and behind the body by more than 25 px. |
| Alternating foot contacts | Six new contacts: **left, right, left, right, left, right**. |
| Grounded stance foot | Maximum world-contact drift **0 px**, measured separately for each leg/contact ID. |
| Swing and joint motion | Maximum foot lift **17.02 px**; both knee positions changed relative to their hips. |
| Brisker horizontal movement | Observed peak **413.75 scene px/s**, above the former 260 px/s ceiling. |
| Upright torso | Pose lean remained below 2.3 degrees. This measures the rig, not every line in the painted body. |

The phase screenshots briefly use the real Pause control so screenshot latency cannot
crop a character that has already moved beyond its measured position. They preserve
actual rendered poses, rather than manufacturing ideal poses. Resume and blocked-frame
checks examine actual consecutive rendered positions; fixed displacement limits across
separate automation calls were replaced because call latency is not a frame duration.

## Actual visual review

Inspected final `idle.png`, `chest-detour.png`, `narrow-debug.png` and the seven-pose
`contact-sheet.png` using image viewing. The contact sheet shows distinct passing and
wide-stride leg configurations. Boots remain visible and the upper body stays upright;
the large arm swings from the rejected version are absent. No obvious opaque sprite
rectangle, detached boot or severe knee seam appeared in those sampled views.

The approach still looks like an articulated cutout: the upper body and arms are quite
rigid, and knee bend is visible in the initial side-on resting pose. That may need
further art refinement. Some narrow screenshots catch the short foot-lowering transition
after arrival; they do not depict a certified final idle stance. Mathematical zero
contact drift alone cannot prove that boot artwork, shading and perceived weight feel
natural. The owner must judge the actual moving HTML before approving this gait.

Horizontal pace is 350–440 scene px/s by depth. Vertical projected speed is deliberately
foreshortened to match the shorter projected stride; it should not be described as
350–440 px/s in every direction. This review measured horizontal pace and inspected
the implementation's depth scaling; it did not certify perceived cadence in all views.

An independent early room-route challenge found airborne projections entering the
clearance margin while remaining outside solid furniture. The gait worker corrected
that before final testing. The final browser clearance check above includes both feet
through turns. Foot-space clearance still does not supply foreground furniture layers
or full-body collision/occlusion.

## Scope and handoff

Changed only `tests/browser_walking.py` and this report. Generated results, actual gait
history, phase crops and rendered screenshots are in `build/checks/walking-revision/`.
Inspected project instructions, QA-003 brief, gait/navigation/runtime sources and tests,
final build manifest, browser results and rendered evidence.

No approval of final naturalness, real-device performance, accessibility, other browsers,
or integration into the Godot puzzle game is implied. HTML previews remain the owner's
working delivery route; these checks do not repair or certify inline chat images.
