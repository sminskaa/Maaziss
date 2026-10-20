# ART-013 — final bounded stool interaction review

**Recommendation: proceed to owner review of this approach/pull/sit candidate.**
No new blocking visual defect was found in this focused pass. This is not final
painted-art approval, Godot integration approval, or approval of other room actions.
The owner retains creative approval; independent QA remains a separate gate.

## Exact output reviewed

- Frozen compact HTML: `visual-preview/maziss-stool-interaction.html`, 930920 bytes,
  SHA-256 `29e45f1274caf82099af98cd29aa6e91a865aa0cdd14e8bb5d4ad67dcb8e6f24`.
- Actual movie: `build/checks/stool-interaction/desk-stool-action.webm`, SHA-256
  `18de29f487c220f307a196deda8ee4ab704ee707068118d5bb62ad7c8dd7633c`.
- Actual composed frames 000, 050, 065, 080, 104, 116, 136 and 156: start,
  held rim, midpull, completed pull, corrected turn, standing alignment,
  descent and final seated pose. These are final output, not superseded staged keys.
- `clean-crop.png` beside `stool-background-crop.png`: the repaired vacated
  rug/floor/desk patch beside its original painted stool region.

Evidence is retained under `build/checks/stool-interaction/art-final/`:
`reviewed-files.json`, `composed-action-sheet.jpg`, `native-motion-sheet.jpg`,
20 `native-*.png` player captures, `native-playback.json` and the capture script.
Only this report and that evidence directory were authored for this assignment.

## Actual visual findings

**Approach and scale.** Maziss approaches the near side of the desk stool at a
consistent room scale. His head, body, clothes, bag and boots remain recognizable
and continuous across the turn. There is no bounding-box size pulse in the reviewed
sequence. Boots appear supported at normal room-view scale. This visual finding
does not replace QA's deformed-mesh floor/contact measurements.

**Rim and pull.** At 2.5 seconds and during the pull, the free Left hand meets the
near seat rim and travels with it. The seat, legs and footrest move together as one
complete stool. The bag-side arm stays quiet with the bag. Simplified hand geometry
limits finger-grip detail, but the intended hold and pull are readable. The low,
forward preparation is exaggerated and deliberate-looking; it remains a candidate
acting choice for the owner rather than finished subtle performance.

**Release, turn and sit.** The player samples from 4.39 through 5.81 seconds show
release, a compact repositioning step and upright alignment. The actual 5.2-second
frame no longer has the former extreme split stance. A temporary bent/lowered leg
is still visible during the step, without the former wide lunge. The 25-degree
endpoint exposes bent thighs and some stool leg/footrest silhouette; the descent
and held endpoint read as sitting with hips over the seat. The stool top is partly
hidden by body and bag, so motion carries more of the seated read than the final
small still alone. The reviewed samples show no obvious detached hip, floating
seat or abrupt silhouette discontinuity. This is a visual judgment at the retained
camera, not a numerical guarantee of all surface contacts.

**Background and camera overlap.** The exposed former stool region has continuous
rug/floor and desk surfaces, with no obvious old stool fragment, duplicate stool,
open hole or stranded old stool-shaped shadow. The rug repair is coherent at the
actual room-view scale. The desk remains intact as Maziss reaches and turns in
front of it; the inspected camera overlap does not visibly cut away his head,
hand, stool or boots. The light stool top remains visibly plainer than the room.

## Native motion/delivery check and limits

System Chromium played the compact HTML's embedded native video from 0.02 seconds
to its natural 8.85-second endpoint. Twenty actual player captures span that
playback, including the final hold. Native video dimensions were 1120×630;
`readyState` was 4 and no media error or page exception was recorded. The decoded
motion samples agree with the actual source composites and preserve the ordered
approach → rim grip → pull → release → turn → descent → seated hold action.

Playwright's bundled browser was absent and system Chromium blocked `file:`
navigation. The capture therefore loaded the **unchanged HTML bytes** into Chromium
with `page.setContent`, then used its actual embedded video and native decoder.
This proves that player path, not successful delivery through the owner's host
panel or direct-file opening on the owner's computer. No preview rewrite or
replacement movie was made. The review is sampled visual inspection of real
continuous playback, not examination of every intervening decoded frame.

No bounded visual blocker remains from this pass. Remaining nonblocking limits:
preliminary palette/textures, simplified mitten hands and face, plain stool finish,
quiet attached bag-side hand, and restrained seat visibility. Refined acting,
cloth deformation and painted material matching still need later art work and
owner feedback. No claim is made about reverse/reset actions, arbitrary walking,
runtime collisions, or the offline Godot implementation.
