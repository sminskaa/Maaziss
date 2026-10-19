# ART-011 — geometry-only stool review

19 October 2026. One initial inspection pass of the actual supplied images, opened
with `view_image`, followed by the coordinator-requested focused connection check
of corrected room-angle and underside images. No Art renders, research, workers
or model edits.

**Recommendation: suitable to show the owner as a first complete-geometry study.**
Independent QA found an approximately 9.35 mm leg-to-seat gap in the first imported
GLB, which the initial art image pass did not resolve. I opened the corrected
room-angle and underside images: the visible leg tops now reach into the seat
underside without the earlier outlined top caps or a visible separation. The
silhouette and bracing remain coherent. This confirms the visible correction;
numeric attachment and export validation remain QA's scope.

The stool is recognizable and its broad construction reads from all three supplied
angles. This report is not final art approval or approval to replace the painted
room stool. Reference likeness still needs the proportion and edge-profile
decisions below.

## Evidence inspected

All paths are under `build/checks/stool-study/`:

| Image | Visible evidence |
| --- | --- |
| `stool-reference.png` | Unchanged painted reference crop: round wooden seat, splayed dark legs and low circular bracing beneath the desk. |
| `room-angle.png` | Broad seat top and front rim, four leg positions, near/far brace arcs and grounded feet. |
| `rear-angle.png` | Opposite leg arrangement, continuous seat rim and the brace passing behind/in front of the appropriate legs. |
| `underside.png` | Actual seat underside, four leg attachments and a continuous brace ring; hidden surfaces exist rather than ending at the reference silhouette. |

Initial-pass image SHA-256 identifiers, in the same order:

```text
cb7962db29ddc1865cc47eaee15f024d43bef63838c51045e8874159505dab62
1aa1130d309610624be25693025b9463727418f1d8c8abfdff6bd7a6f390a128
422ade3c741b2b2bde9e88304c9ebf7d6c8cbbe2e86f0f886cd9e0bb5ed7affe
a0f79de9590f9ebe415a7a4add45a62c61f165d1ecb8c1e4a2acbb074fec7d51
```

Final corrected images opened for the focused connection check:

```text
room-angle.png a32c617dbfe459f61edb0de372a583f7a6f23bdcbad51de770cadd39a5bdc69e
underside.png e00aa3fdc1d69bb0f75db4fb40e8cbda862a686f544af119672a3d18afe50d12
```

The coordinator also reports regenerated rear-angle hash
`728594670ef2c9b636301474ab85c7cba96ffa4dc3b6614f9bbba0d9ee18964d`;
that final rear image was not reopened in this two-view correction check.

## Shape findings

- **Seat:** The circular top and continuous thickness are convincing. The model's
  broad, rounded rim gives it a softer, almost padded edge. The reference reads
  more like a wooden slab with a firmer top edge and a deeper dark front band
  relative to its width. Prefer a tighter bevel and a flatter side wall if closer
  reference matching is requested; preserve the complete underside.
- **Height and spread:** In the nearest comparable view, the model looks taller
  and more evenly flared. Its exposed legs extend roughly one seat width below
  the rim; the painted stool is more compact. The outer feet also project a
  little farther beyond the seat sides. A modest reduction in exposed leg length
  and/or spread would bring its silhouette closer. These are image comparisons,
  not recovered dimensions: camera matching must precede exact measurements.
- **Leg character:** Four substantial, beveled legs read clearly, without obvious
  broken or floating sections in the checked views. Their straight, similarly
  sized beams and regular arrangement look more manufactured than the reference's
  subtly uneven, tapered painted legs. Small controlled variation in taper and
  silhouette could help; strong bending would change the design unnecessarily.
- **Bracing:** The circular low brace matches the important reference motif and
  remains legible in front, rear and underside views. Near/far arcs maintain
  coherent overlap. Its uniform section and smooth regular circle are cleaner
  than the reference's slightly uneven drawn brace. No obvious missing arc is
  visible. Some joints are occluded, so these images do not establish watertight
  topology or structural joinery.
- **Cartoon readability:** Round seat, outward legs and open central space give a
  clear stool silhouette. The chunky forms are a useful basis for the approved
  painted cartoon direction. Current regularity and the soft rim are the main
  geometry departures; finished paint, wear and contours remain separate work.

## Scope and next decision

Materials and lighting are preliminary and are not a failure of this geometry
study. The small painted crop cannot establish the exact concealed construction.
The private `maziss-stool.blend` and `maziss-stool.glb` were not modified; this is
an image-based art review, not an export/topology audit.

Present the corrected candidate and reference for the owner's shape decision. If they
want a closer match, prioritize the compact leg proportions and firmer wooden
seat edge before surface detail. No further modeling or rendering is requested
by this report. Room scale, clean background, replacement, shadows, movement,
character contact and sitting animation were not demonstrated or approved here.
