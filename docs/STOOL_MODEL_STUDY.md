# First complete stool model

The owner authorized one geometry-only modeling/review iteration with limited
remaining allowance. Character animation remains paused. This study builds a
complete separate 3D prop; it does not replace furniture in the painted room.

## Files and construction

- Source: `tools/build_stool_study.py`; packaging: `tools/build_stool_review.py`.
- Private editable scene: `build/checks/stool-study/maziss-stool.blend`.
- Private model: `build/checks/stool-study/maziss-stool.glb`.
- Compact review: `visual-preview/maziss-stool-study.html`, including a GLB download.
- Private manifests: `model-manifest.json` and `delivery-manifest.json` in the study
  folder bind geometry, sources, renders and delivery hashes.

The actual room crop is source rectangle (1368,592)–(1513,767), unpainted and
unchanged. It shows a rounded wooden seat, splayed legs and circular bracing. The
new model uses six named solid mesh parts: a closed rounded-profile seat, four
tapered beveled legs and a closed rectangular-section footrest ring. Each has
object-local UV coordinates prepared for later painting. Source mesh checks find
no non-manifold edges in those six parts. Dimensions are estimates; seat top is
0.568 authoring metres, not a measurement supplied by the owner.

The model is saved before rendering. Three actual CPU Cycles renders use the same
geometry and scale: a local reference-view estimate at 23° elevation, a rear view,
and a low underside view. The latter omits the studio floor so construction is
visible. The review offers these images beside the unchanged reference crop.

## Scope and limits

This is a shape candidate. Base colour, roughness and fine contours make the form
readable; painted wood grain, chips, scratches and local room lighting are not yet
finished. The camera estimate has not been solved against room geometry. A neutral
studio ground/shadow is not a reconstructed room floor. No clean background,
painted-stool removal, prop movement, Maziss sitting or Godot scene integration is
claimed. Those later stages must respect the owner's intact-background requirement.

The existing room, character model, walking curves and sofa preview are preserved.
No external model generator, account, payment or private-art upload was used: the
editable geometry was constructed directly in Blender. The generated Blender,
GLB, images and HTML remain private/ignored; only source and findings are versioned.

## Validation and restart

Art and independent QA inspect the same actual reference and three model renders,
with findings in `production/ART_STOOL_MODEL.md` and
`production/QA_STOOL_MODEL.md`. Their recommendation is scoped to this geometry
study; it cannot approve the later clean-background or sitting interaction.

Reproduce in the same workspace with retained private room source:

```sh
blender -b --python tools/build_stool_study.py
python3 tools/build_stool_review.py
```

The installed Blender CPU build lacks OpenImageDenoise support; the renderer uses
48 samples with denoising disabled. Review generation needs Pillow. Browser/GLB
checks and actual image paths are recorded in the QA report, rather than inferred
from source code. Read `SESSION_HANDOFF.md` for the pending animation pause and
later seating, blur, material and room-action requests.
