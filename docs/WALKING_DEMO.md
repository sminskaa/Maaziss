# Walking study — original character, corrected legs (revision 4)

Open `visual-preview/maziss-walking-v4.html`, also available as
`visual-preview/maziss-walking.html`. Use the HTML panel; embedded chat images still
fail for the owner. Click floor to walk, Pause to inspect, Reset to restore the first
pose. The walkable-area and foot-contact overlays remain available.

## Owner's current instruction

Revision 1's leg animation was rejected for sliding and keeping one foot ahead.
Revision 2's alternating physical steps were accepted, but its replacement character
proportions, rigid upper body and boot joins were rejected. Revision 3's further
proportion/posture/arm tuning was also rejected. The owner requested the FIRST actual
character with ONLY the leg movement correction. Do not keep tuning the replacement
rig. Earlier HTML versions remain preserved for reference, not approved replacements.

## What revision 4 does

Uses `art/walking/maziss-side-atlas.png` and `maziss-depth-atlas.png` from the first
proposal. `walking/original-sprites.json` retains its exact frame rectangles and foot
anchors. The head, jacket, bag and arms use the original painted frames at their
original scale; no new body texture, upper-body rescaling, shoulder rig or added lean.
The initial character is the complete original front-facing frame. During walking,
runtime source masks hide the old lower legs and sample the original trousers and
boots along the accepted leg solver. Original upper-body frame acting remains.

The accepted `walking/gait.js` solver is unchanged: named legs alternate swing and
planted contacts; phase follows distance and stance contacts hold still. Clothing
ends at each original boot's transformed cuff. Faster existing travel pace and the
same obstacle-aware routing remain. Foreground occlusion, polished transition acting
and native Godot integration are still outside this movement study. Source PNGs and
the approved `art/proposals/apartment-cartoon-v2.png` remain untouched.

## Verification

```sh
python3 tools/build_walking_demo.py
python3 tests/browser_original_walking.py
```

The focused Chromium harness checks original frame metadata, painted upper-body pixel
agreement against the original frame (allowing sparse one-level channel rounding),
alternating contacts, planted-foot drift, boot joins, routing, pauses and delivery
without external requests. It captures actual side/front/back movement under
`build/checks/walking-original-legs/`. The manifest records source/output hashes.
These checks do not establish the owner's aesthetic approval or guarantee every
possible mask seam is invisible. Previous revision 3 QA remains historical in
`production/QA_CHARACTER_CONTINUITY.md`; it is not evidence of v4 appearance approval.

## Offline target

This self-contained HTML is a development review prototype. Godot remains the engine
for the final locally installed desktop game. Required art, dialogue and generated
voice files ship with it; local saves, no required login, runtime AI/API or server.
Exact desktop OS targets remain to be agreed.

Final revision 4: 21 focused browser checks passed. Recorded contacts alternate left/right with zero measured stance-ground drift; source hashes confirm the accepted gait/navigation code is unchanged. Owner appearance/motion approval remains pending.
