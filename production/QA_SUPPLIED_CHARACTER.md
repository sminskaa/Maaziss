# QA-013: supplied-character reconstruction study

19 October 2026. Independent QA coordinated with the art director.
Final private candidate GLB SHA-256:
`eb3c9fb665f186221378cbe25bcc5739cc14c1b86259e11bae8d28f0debd1b06`.

**Recommendation: suitable for owner review as a reconstruction study. It is not a
finished character, final art approval or a production-ready rig certification.**

## Actual visual inspection

QA opened the supplied mesh's front, oblique, profile and back intake renders, the
original character atlas and close-up facial studies. For the final candidate, QA
independently rendered and inspected 32 actual walking views: eight azimuths at
four different cycle phases. Idle front, oblique, profile and back were also checked.
The private contact sheets `qa/candidate/inspection-phase-0.png` through `-3.png`
contain these actual model renders, not generated replacement illustrations.

The result reads as one coherent stylized human under all inspected angles. Hair,
jacket, shirt, trousers, oversized boots and satchel remain recognizable. The face
has genuine modeled features and appears once, with profile depth; the rejected
repeated portrait projection is absent. In these samples QA observed no disappearing
clothing, floating fragments, cross-body needles or large stretched bag shelf.
Clothing and equipment retained their visible continuity during the sampled poses.

This does **not** establish finished likeness. Facial proportions and expression,
hair silhouette, mitten-like hands, garment detail and painted wear remain simpler
than the original illustration. The model still needs an art pass to fit the approved
painted cartoon identity. A technically valid exchange asset does not prove that it
meets that aesthetic goal.

The bag-side right arm deliberately stays quiet relative to the body; the opposite
arm swings. A local surface-path audit found a six-vertex connection between the
hand and bag seed regions below z=1.10 m, excluding the normal upper-arm/shoulder
route. This supports a local joined region; seed labels alone cannot uniquely
identify every intervening contact. Keeping the bag-side hand quiet prevents tearing
with the current rig. Independent free arm swing, expressive fingers and separate
equipment require further region separation, retopology and weight painting. The
quiet arm must not be presented as a complete solution for arbitrary actions.

## Engineering evidence

`tests/browser_supplied_character.py` directly parsed the final exported GLB and
independently evaluated 50 samples of its actual baked Blender animation, including
intermediate times. All 13 scoped engineering checks passed:

- Finite positions/attributes, nondegenerate triangles and unit exported normals.
- Actual skin attributes with normalized weights, at most four influences and valid
  joint indices; materials and finite, increasing animation sampler times.
- Finite evaluated motion, measured floor clearance and correct shared Head binding
  for all added facial features. Both eye-white meshes preserve their two materials.
- No edge exceeded the study's fourfold stretch detector. Maximum measured ratio
  was 3.9923; this is a coarse defect threshold, **not** an industry quality standard.

Minimum evaluated vertex height across those 50 samples was +0.00270 m. The private
GLB has a 14-joint skin and a 1.16667-second animation. These checks are useful game
exchange prerequisites; animation blending, alternate actions, production topology,
hand/bag separation and final game behavior remain outside their acceptance scope.

The original private input was preserved. Its 4,905-vertex, 10,000-triangle surface
was edge-closed with consistent winding, but a vertex-link audit found one pinched
vertex connecting two distant hand regions. Five triangles incorrectly extended
from one hand toward a tiny patch on the opposite hand. The candidate duplicates
that vertex and restores the local patch near its neighboring vertices; it retains
all original triangles. Earlier notes inferred the opposite patch was a leg from its
height; actual fingertip inspection corrected that anatomical label.

The first rigged attempts failed actual visual QA: bag weights produced a shelf,
fingertip/forearm classification produced needle-like triangles, and setting child
world poses before the parent caused floor penetration. Those findings were reported
to the coordinator and corrected before this final candidate. Passing finite-value
or glTF checks alone did not reveal or excuse these defects.

## Reproduction and private evidence

Run from the checkout:

```sh
python3 tests/browser_supplied_character.py \
  --input build/checks/supplied-character/maziss-supplied-rig.glb \
  --blend build/checks/supplied-character/maziss-supplied-rig.blend \
  --output build/checks/supplied-character/qa/candidate \
  --require-rig
```

Full input diagnostics, candidate metrics, actual renders and captures remain in
ignored `build/checks/supplied-character/qa/`. Raw models and personal media must not
be published with the source or review. The main Godot character has not been
replaced by this study. Owner review remains separate from final release approval.

## Compact delivery

The final `visual-preview/maziss-rebuilt-review.html` is 948,310 bytes. QA opened
its actual browser screenshot and verified the original/model comparison, native
player, eight-angle grid and explicit quiet-arm/unfinished-art limitations. With
browser networking disabled, all embedded images decoded, the 960×600 native video
loaded and advanced during playback, and no JavaScript errors or external requests
occurred. Its duration is 16.382 seconds. No live WebGL or application JavaScript is
required. HTML SHA-256:
`787d9bcbeba5879cf7ba8e690f57221ebf2460d651cd773d4e8f25bbf613b70b`.

Internal browser rendering cannot by itself establish that the host chat panel works.
The owner previously confirmed that the smaller native-video HTML format displays.

The coordinator also ran an actual Godot 4.6.3 import/animation check. QA inspected
its final hash-bound `build/checks/supplied-character/godot/result.json`: the input
SHA matches the reviewed final GLB, with 17 mesh instances, 14 bones and 19 vertex-
color surfaces, finite bone transforms at four animation phases and a moving shin.
This verifies scoped exchange/import behavior, not installation in the playable
Godot room, final art quality, alternate actions or arbitrary animation transitions.
