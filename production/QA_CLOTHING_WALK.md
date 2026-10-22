# Clothing and equipment continuity review — QA-009

Recommendation: ready for the owner's private HTML visual review. Revision 8
addresses the specific renderer defects examined here; creative acceptance and
naturalness remain the owner's decisions. No Godot or public release is approved.

## Reviewed candidate and result

- Frozen build: `5c3d7d3fcda2ca32b1ff5778f6cb7a7cff4d580287c0fd3ffa636160b08721f7`.
- `python3 tests/browser_clothing_walk.py`: **44 passed, 0 failed**, 13.45 seconds.
- Chromium `154.0.8037.57`, Linux cloud workspace, browser networking disabled.
- Both the HTML digest and all declared runtime/private-input hashes matched
  before and after the run.
- **100 actual transparent production poses**: neutral plus 24 cycle samples in
  each of four views. **80 isolated production-item captures**, including 64
  independently rendered trouser legs before global fragment cleanup.

Generated pixels, coordinates and detailed results remain ignored under
`build/checks/clothing-walk/`. The public test/report contains no reference-image
pixels, FBX arrays, intake paths or personal recordings.

## Why the previous checks were insufficient

The owner's revision 7 feedback is valid. A connected character silhouette can
still contain a hole in its jacket, and a boot can have zero programmed rotation
while its original painted shape visibly leans to one side. The previous check
that the rendered trouser end equals the rendered boot top also missed that both
could have been moved away from the actual skeletal ankle.

Fifty-two actual transparent revision 7 poses were preserved privately before
runtime edits. Inspection found these causes:

- Whole arm masks were removed from the upper-body cutout. An arm rotating away
  exposed the missing shoulder, shirt or bag pixels. Removing disconnected
  components does not restore those missing surfaces.
- Both front/back boots reused one directional shoe drawing. The pair consequently
  shared a visible sideways bias, even when the transform reported zero roll.
- Depth-view trouser ends used a separately constructed boot-height point rather
  than the actual skeletal cuff. At 440-pixel character height, the displacement
  reached **13.74 pixels in front view** and **15.38 pixels in back view**. Side
  views had zero displacement. This introduced deformation beyond the real
  perspective shortening of a bent leg.
- One source trouser cutout supplied both legs. Its mapping and the original
  fixed boot silhouette remain limited 2D approximations of the FBX skeleton.

The coordinator changed the runtime construction. This worker owns only the
focused test, this report, and ignored QA evidence.

## Evidence for the corrections

`tests/browser_clothing_walk.py` captures actual production-rendered poses through
the loaded painter, rather than reconstructing an older painter without the new
assets. Per-item captures temporarily hide other layers, use the actual mesh
mapping, and restore the original cache immediately.

| Owner concern | Scoped result |
| --- | --- |
| Ghost fragments and holes | All 100 whole-character captures have no detached painted component above 16 pixels. The isolated torso, bag leather body and 64 trouser legs have no enclosed transparency hole above 3 pixels. Isolated items have no detached component above 16 pixels. The real shoulder interiors are backed by cloth when arms are hidden. |
| Both depth-view boots lean observer-left | Actual lower-shoe silhouette centroids now oppose sides: front approximately **+6.83 / -9.94 pixels**, back **-8.34 / +6.52 pixels** from their cuffs. The old pair biased left on both feet. This measures painted silhouettes, not only transform angles. |
| Trouser ends shorten/lengthen beyond real leg movement | Every sampled rendered trouser end now equals the actual skeletal cuff in all views. The previous additional 13–15-pixel depth-view relocation is gone. Actual local thigh/shin lengths remain fixed across 241 sampled phases; projected knee foreshortening is still allowed. |
| Clothes and bag lack continuity | Each isolated sampled trouser leg remains filled and connected through deformation. The complete satchel is rendered rigidly with the torso. The original torso-core detail overlay still contains some original satchel/tool texture under the replacement; it shares the same rigid transform and does not move separately. This is a repaired 2D rig, not a complete independent 3D clothing model. |

QA caught a provisional neck-to-shoulder coverage gap after the new clothing
backing was introduced. The final original torso-core/collar overlay closes that
gap while retaining the original neck, face and jacket details. Actual side,
front and back rendered poses were visually inspected after the correction.

Full-character enclosed transparency is deliberately not treated as a universal
failure: the space between two crossing legs can form a legitimate enclosed gap.
Likewise, a tool-eye opening at the top of the satchel is legitimate hardware
transparency. The bag-hole check covers the leather body below the tools, rather
than treating that opening as torn fabric.

## Controls and performance

The real directional study, pause, frame-step and Stand still controls passed in
all four views. No JavaScript errors or asset/network requests occurred. The FBX
loop geometry closes without a joint teleport. No full navigation regression run
was repeated because navigation code is unchanged.

Thirty warm production renderer calls at 440-pixel character height measured
median **6.10 ms**, p95 **10.80 ms**, maximum **12.10 ms** on this cloud host. These
are renderer-only measurements, not whole-frame FPS or Windows performance.

## Limits

The final review still requires the owner's judgement of the moving animation.
Fixed bone lengths do not establish natural fabric deformation, good weight
transfer, or an appealing walk. The body and satchel remain rigid painted layers;
the trousers are a 2D skin over FBX-derived joints. Front/back foot projection and
turning are simplified, and source pose textures still impose limits. This HTML
study does not validate Godot or native Windows playback. Direct `file://`
execution remains blocked by managed Chromium; self-contained HTML was executed
with browser networking disabled instead.
