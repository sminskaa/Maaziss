# ART-004 — Character proportion and articulation review

Reviewed: original `maziss-side-atlas.png`, `maziss-depth-atlas.png`, articulated
`maziss-rig-parts.png`, v2 idle/contact-sheet browser captures, `rig.json`,
`demo.js` and `gait.js`. This is a visual/source review; no art, code or tests changed.
The owner accepts the new alternating leg mechanics. Preserve them.

## What changed visibly

The v2 figure has an enlarged upper half, narrow lower limbs and small boots. Its
hands hang in one baked pose. The neutral upper-body source has also removed the
earlier slouch. These are rendering/calibration defects, not reasons to replace the
approved identity or regenerate the whole character.

Approximate measurements below use crown-to-sole height, excluding shadows. Source
landmarks are estimates from actual images; bent poses and perspective affect them.

| Feature | Earlier artwork | V2 rendering/source cause | Useful starting target |
|---|---|---|---|
| Crown to belt | Side roughly 45–48%; front roughly 49–50% | `.66 * .84 = .5544H` above pelvis versus `.45H` pelvis-to-ground: about 55% upper half | About 48–50% crown-to-belt and 50–52% belt-to-sole |
| Side boot length | Roughly 20–23% figure height | `.105 * 249/170 = .154H`: about 15% | Roughly 19–21%, compare at same actual figure height |
| Trouser width | Upper thigh roughly 10–12%, lower calf 8–10% | Side thigh renders about 9% H before opaque silhouette narrowing | Recover a little thigh fullness, avoid stretching a narrow texture into long sticks |
| Side boot height | Roughly 14–17%, depending on lifted/tilted pose | 10.5% nominal H | About 13–15%, with a visible trouser cuff overlapping its top |

Do not simply lengthen the legs without reducing the oversize upper-body ratio.
Rebalance both halves, then compare characters at matching crown-to-sole height.
Front/back body ratios should stay close to the side figure; retain depth foreshortening.

## Attachment causes and repairs

1. **Boots use the wrong joint.** Shin IK currently ends at ground minus `.018H`,
   almost the sole. The drawn boot extends `.105H` above ground. Its actual cuff is
   toward the heel side of the crop, whereas the renderer centres the complete
   heel-to-toe crop on the leg. Therefore the trouser endpoint dives into the boot's
   lower middle and misses the cuff axis. Register an explicit source cuff/ankle
   pivot (side approximately x=0.23–0.28, y=0.08–0.20 of the cropped boot, to refine
   against the actual opaque opening) and a separate sole/contact pivot. Rotate both
   together. The rendered shin endpoint should land inside that boot opening with
   a small overlap, not at the centre of its sole. Keep world contacts planted.
2. **Arms cannot swing independently.** Hands, sleeves and torso are baked into each
   `body*` part. Rotating that whole image will only rock the person like a plank.
   Separate/mask source arms at shoulder pivots, retain their painted textures and
   overlap sleeve/torso seams. Hide the original static arms in the torso pass.
   Opposing shoulder swings of roughly ±5–8 degrees are a starting point, with a
   quieter far arm and relaxed slight elbow bend. A tiny hand wiggle alone will not
   restore arm acting. No broad windmilling or detached shoulder gaps.
3. **Upper body has nearly no acting.** Current moving torso angle is a constant
   `direction.x * .025` (about 1.4 degrees), with zero lean at rest. Add a modest
   persistent side-view forward slouch, initially around 5–8 degrees, then a much
   smaller cyclic rocking contribution (roughly ±1 degree). Keep belt overlap and
   shoulder/head relationships intact. The original source's bent silhouette means
   these are calibration suggestions, not universal anatomical measurements.
4. **Vertical motion should be visible but restrained.** Keep accepted contact-driven
   leg phases; allow a few pixels of pelvis/body rise/fall at the review scale, and
   slight shoulder counter-rotation. Do not compensate for frozen arms by greatly
   increasing whole-body bounce.

## Review required after implementation

Compare original, rejected v2 and corrected figure at equal height, on the same
background and without debug overlays. Inspect both contact extremes and passing
poses in left/right and depth movement. Check boot cuffs on the airborne as well as
planted foot; inspect shoulder seams when the near arm moves away. Existing contact
and navigation checks remain valuable, but do not certify proportions or naturalness.
The owner must judge the revised overall appearance and motion.

## Coordinator revision 3 — visual follow-up

Inspected actual browser captures `/tmp/maziss-idle.png` and
`/tmp/maziss-moving.png`, plus the revised rendering source. At their displayed
full-scene scale, the corrected character has a visibly more balanced upper/lower
split and fuller lower limbs. The boots have recovered substantial size and meet
the trouser cuffs in both supplied poses; there is no obvious sole-centred attachment
error remaining in these frames. The modest forward bend reads clearly without the
earlier exaggerated hunch. No gross shoulder gap or duplicated static hand is apparent
in either capture. The arms remain near the body rather than adopting a broad swing.

Calibration now gives `(.52 * .84 + .45) * 1.12 = .9932` nominal visible height;
crown-to-belt is roughly 49.3% of that height. Side boot length is about 20.5% of the
previous nominal visible scale, consistent with the starting target. Shin rendering
now terminates at the source-registered cuff, separate from the unchanged anatomical
ankle/contact model. These source calculations corroborate the visible correction;
they do not establish animation quality by themselves.

No blocking art defect found in these two side-view captures. This limited review
does not examine every swing phase, left-facing mirror or depth-view shoulder seam,
and still frames cannot establish whether motion feels natural. Retain browser/contact
QA and present the revised HTML to the owner for the final appearance/motion judgement.
