# Painted character study — independent QA

Assignment QA-011 covers the actual offline painted model, its authoring file and
the reported hand/bag and trouser defects. This is a bounded technical and visual
review. It does not approve a finished Maziss design or replace the owner's art
judgement.

## Frozen evidence

Final build **98259839b0e0**, checked on 18 October 2026: **26 focused checks passed,
zero failed**, in 136.37 seconds using Chromium 154.0.8037.57 and Blender 4.3.2.
The actual source and HTML hashes stayed fixed through the run. This result belongs
to the final candidate, not the earlier candidates interrupted for corrections.

The harness is `tests/browser_painted_character.py`. Captures, full geometry arrays,
authoring inspection and measurements remain in ignored
`build/checks/painted-character/qa/`. The run captured 32 actual rendered walking
frames at eight camera angles and four cycle phases. Both contact sheets were
visually inspected; representative front/profile frames were also inspected at
their original capture size.

The harness checks the unchanged original drawings, images actually embedded in
the browser and packed into the Blender file, all three UV registrations, closed
garment geometry, opaque depth-tested materials, fixed registration during
deformation, sampled actual skinning and offline controls. It independently
evaluates deformed Blender triangles against the bag/tools and trousers.

- All 106 exported meshes are closed after coincident-coordinate welding for
  topology counting. Pants, jacket, shirt and rounded head each have one connected
  surface. All paint coordinates are finite and skin weights are normalized.
- All three actual reference images are packed into the saved authoring file.
  Every painted mesh retains its three registered UV layers. The browser embeds
  the unchanged original front/back and side drawings, plus the separately
  prepared clean jacket reference.
- The actual browser material stays opaque and uses depth occlusion. Transparent
  source pixels do not remove pieces of geometry, and paint registration remains
  fixed to the surface during deformation.
- Independent evaluated-triangle queries found zero hand/forearm intersections
  with bag or tool meshes in neutral standing plus all 36 exported cycle samples.
- Skin/trouser intersections occur only at the deliberately closed lower trouser
  caps, with rest height at most 0.209892 m, enclosed by boot shafts. No exposed
  knee or trouser-wall skin breakthrough was found in those samples.
- Actual browser skinning remained finite over 24 cycle samples. The lowest
  sampled boot vertex was 0.003515 m above the floor. Offline loading, standing,
  frame stepping, surface controls and room setting passed without JavaScript
  errors or external network requests.

## Visual findings

The actual paintings are present on real complete geometry; the model can be
viewed from intermediate angles. The lower head placement improves the collar
join. Shortened tools and the independently fitted arm improve bag clearance.
The final upper-trouser painting no longer shows the earlier obvious duplicate
bag/hand fragments or abrupt projection-strip changes. The temporary horizontal
face-stripe regression is absent in this final candidate. No detached transparent
garment fragment was seen in the 32 captured final frames.

Remaining art defects are conspicuous: facial features still stretch or duplicate
around the cheeks/ears at oblique views; the eyes and face silhouette need an
actual likeness pass; shoulder/cuff tailoring remains angular; and trouser folds
can read as broad projected pigment bands. The bag and hands still need more
coherent painting from every angle. This is a surface-mapping study, not a finished
painted cartoon character.

The saved Blender file has actual packed paintings and UVs, but its basic material
nodes do not include the browser's extra facial feature cleanup. Exact appearance
parity between authoring and browser output is therefore not claimed.

## Scope of recommendation

Suitable to share as an **intermediate mapping and construction review**. It is
not ready to approve as the finished character or integrate as final game art.
Do not describe geometry or sampled collision passes as
proof of final cartoon style, natural movement at every speed, or collision freedom
for new animation. Original drawings supply a limited set of views rather than a
complete production texture atlas. The next useful step is a clean production UV
layout, facial landmark/silhouette fitting and complete texture painting; additional
owner walking references are not the missing ingredient for these remaining art
defects. More projection-mask patches should not replace that work.

No Windows player, Godot integration, cloth simulation, arbitrary animation,
navigation, packaging or player performance claim is covered by this assignment.
