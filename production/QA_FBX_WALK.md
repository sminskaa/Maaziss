# FBX walking review — QA-008

Recommendation: ready for the owner's private HTML visual review. The candidate
is not creatively approved or integrated into Godot. Technical checks cannot
establish that a walk looks naturally human.

## Reviewed candidate

- Revision 7 build: `9d7c3a14af4fac87a11f8f6789b10cc3083ea0546fd56da4d26d415436bf0407`.
- `python3 tests/browser_fbx_walk.py`: **54 passed, 0 failed**, 30.1 seconds.
- Chromium `154.0.8037.57`, Linux cloud workspace, browser networking disabled.
- Build/source/private-input hashes matched before and after the run.
- Actual transparent browser captures: four neutral directional poses and twelve
  samples of the walking cycle in each direction, plus live-control close-ups.

The test and this report embed no source FBX motion arrays, owner footage, or
reference-image pixels. Generated captures and detailed metrics remain ignored
under `build/checks/fbx-walk/qa/`.

## Owner's five defects

| Reported problem | Independent evidence in revision 7 |
| --- | --- |
| Side idle boots point upward | Both side views have flat sole registration. Actual opaque pixels across the central outsole vary by four pixels vertically, following the curved source outsole rather than an upward tilt. Visually inspected at full size. |
| Far arm incorrectly appears in front | Painter sequence is far arm, legs, body, near arm in all sampled views. Four-direction transparent poses were visually inspected for depth overlap. |
| Front idle feet lean sideways | Directional boot artwork remains upright; both neutral front/back views were visually inspected. |
| Detached ghost fragment | **All 52 transparent poses contain one connected painted component at alpha >64**, with no detached secondary component. The earlier hand/bag sliver is absent from the final grey contact sheet. |
| Trouser cuff separates and travels with boot | Each cloth leg is rendered as one continuous strip; boot cutouts contain leather rather than the grey trouser fold. Actual poses show the cloth following the shin to the boot top. Both boot-top and shin-end registrations coincide. |

QA caught residual ghost islands and trouser mesh transparency seams in
provisional candidates. The final integer-aligned transparent compositing step
removes islands without a second sampling split. Overlapping subpixel triangle
clips close the repeated visible mesh cracks. Grey-background inspection is
necessary because room textures conceal these artifacts.

## Other checks

The actual FBX-driven cycle closes with zero joint-coordinate seam error and
preserves fixed retargeted thigh/shin lengths (floating-point variation below
`6e-14` pixels). Sampled cycle and start/stop coordinates remain finite. The
runtime visits starting, walking, settling and idle states.

Real browser controls were exercised: directional study, pause, frame stepping
with FBX timing, Stand still, reset, and room pause. Navigation reaches resolved
destinations, detours around furniture, keeps recorded root substeps on the
buffered floor, and rejects an unreachable wall click. No JavaScript errors or
asset/network requests occurred.

Thirty warm renderer calls at 440-pixel character height measured median 6.05 ms,
p95 6.60 ms and maximum 8.20 ms in build `afb7480d05f2`. The final change only
aligns the intermediate framebuffer origin to whole pixels; that microbenchmark
was not repeated. These are renderer-only timings on this cloud host, not a
whole-frame FPS claim or a Windows performance result.

## Remaining limits

Naturalness, character appeal and the amount of cartoon exaggeration still need
owner judgement in the moving HTML preview. Bone continuity and flat neutral
boots do not prove natural weight transfer or eliminate every instance of foot
sliding. Direction changes still switch between directional painted artwork;
front/back foot roll and upper-body depth rotation are simplified. A complete
turning animation has not been drawn.

Direct `file://` opening is blocked by managed Chromium policy. The complete HTML
was loaded and exercised with browser networking disabled instead. Godot
integration, native Windows playback, production licensing clearance for the
supplied animation and owner creative acceptance are separate follow-up work.
