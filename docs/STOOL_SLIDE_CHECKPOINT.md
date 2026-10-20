# Right-hand stool pull, occupied slide and desktop contact

Owner direction,20October2026: replace the rejected circling/small-step route.
Maziss approaches the stool's left side, pulls it with his anatomical right hand,
makes only a compact repositioning to sit facing the desk, grips the seat top with
his right hand, slides himself and the stool a short distance toward the desk as
one occupied unit, and ends with both hands supported on the desktop. Writing is
not requested in this increment. Preserve all original source artwork/models and
earlier reviews; those remain historical candidates, not approval of circling.

## Durable work in progress

- Art ART-015 `/root/right_arm_art`: `tools/prepare_stool_right_arm.py` and
  private `build/checks/stool-slide/character-right-arm.blend`. Anatomical right
  arm must be independent of the fused source satchel. Mirrored supplied free-arm
  geometry is locally capped and fitted; separate continuous bag remains attached
  to torso. Actual rest/reach images must show no holes, duplicate arm or bag tear.
- Coordinator: `tools/stool_slide_pose.py`, fitted desk/contact/occlusion geometry,
  renderer integration and compact review. Pose/contact definitions and source
  checkpoints saved before full rendering.
- QA QA-021 `/root/stool_desk_qa`: `production/QA_STOOL_SLIDE.md`, private
  `build/checks/stool-slide/qa/`. Actual images/motion mandatory. Audit Right bone
  and skin, seat/body co-motion, right seat grip during slide, both final hands on
  desk surface within clear area, feet/furniture clearance and coherent room.

## Required stages and checkpoint gates

1. Save/visually inspect independent right arm and stationary continuous satchel.
2. Save full authored action and fitted desktop/item support geometry; render only
   grasp, compact boarding, seated grip, slide and final contact keys first.
3. Art and QA inspect those actual room images. Correct contact/overlap before
   spending allowance on full motion. Do not mark unfinished motion as passed.
4. Save actual full scene/frames incrementally; package compact HTML with Use-stool
   and native playback controls. Inspect continuous motion and offline controls.
5. Commit source/reports/resume note; private assets/previews remain ignored.

If interrupted, read this note plus SESSION_HANDOFF and the latest private manifest.
Do not recreate original models or redo completed research. Resume from the last
saved stage and keep remaining checks explicit. Zero additional budget; final
player target remains offline Godot.

## Saved implementation checkpoint

Independent right arm and bag candidate is saved (SHA-256
`0b4f0fd6c7f180c3c71bab70dae384cac5341d5c6ccc23b615896631907352b2`).
`tools/prepare_stool_right_arm.py` rebuilds it from the preserved original rig.
Both resulting meshes are closed manifold; original face/hair remain unchanged.
The bag is shifted smoothly outward up to10cm to clear the stool.

`tools/stool_slide_pose.py` now contains the complete8.8second authored draft;
`tools/stool_desk_geometry.py` adds fitted solid desktop/cabinet/item contact and
camera-occlusion meshes. Original painted desk appearance is retained, not replaced
by untextured boxes. These are fitted support volumes, not finished textured props.
Renderer accepts `--source-blend`; saved scene includes the new independent arm.
The compact packer accepts phase labels and action descriptions from the manifest.

Early actual key checks caught skin-through-desktop, seat-grip/bag penetration,
and boots crossing stool legs/ring. Revisions fit the actual hand surfaces, offset
the bag, and stage a closer rear-left pull with one short boarding transfer.
Current whole881sample pose check preserves bone lengths within0.5micrometres.
That numeric result does not establish skin clearance or natural acting.
Actual corrected scene/key review and full motion are still pending at this
checkpoint. Old superseded audit evidence is retained privately; do not infer a
pass from model closure or bone targets alone.

Reproduce draft keys (preserved private assets required):

```sh
blender -b --python tools/render_stool_interaction.py -- --pose-module stool_slide_pose --source-blend build/checks/stool-slide/character-right-arm.blend --output build/checks/stool-slide --keys
python3 tools/build_stool_interaction_review.py --output build/checks/stool-slide --keys
```

Wait for source and scene freeze before auditing; never compare an older bake
with a newer pose module. Main deliverable will be
`visual-preview/maziss-stool-slide.html` only after full-motion/contact review.
