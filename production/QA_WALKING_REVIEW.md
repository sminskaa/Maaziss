# QA-002 — Walking example review

**Go for owner review of this standalone walking study. Not a public-release or
finished-animation approval.** Tested on 17 October 2026 using actual headless
Chromium 154.0.8037.57 and the self-contained `visual-preview/maziss-walking.html`.
The earlier Godot puzzle prototype has not been replaced or retested by this work.

## Executed evidence

- `node tests/test_navigation.cjs`: **9,584 assertions passed**, covering 1,025
  clear navigation nodes, broad endpoint pairs, segment clearance and redirection.
- `python3 tests/browser_walking.py`: **18 browser checks passed**, no page errors.
  Ten completed traversal legs included the non-straight route from `(1030,563)` to
  `(1460,598)` around the chest. Additional furniture, redirection and pause tests ran.
- The browser harness independently applies Python polygon and edge-distance checks
  to the recorded feet, rather than merely asking the implementation whether it is
  correct. The final run retained **1,772 legal position samples**, plus 239 observed
  animation/movement states. Observed traversal positions did not show a large jump.
- High-wall clicks stayed rejected; a chest click adjusted to legal nearby floor.
  Rapid destination changes preserved legal feet, and a mid-walk redirect started
  at the actual position. Pause froze movement; resuming and a 700 ms blocked browser
  frame did not cause a catch-up teleport within the harness's stated bounds.
- A real mouse click on a 650 px-wide viewport mapped correctly to room coordinates.
  Multiple directional frames appeared during movement and the idle frame remained
  stable after stopping.
- Both character atlases decoded with substantial real alpha transparency, and all
  artwork was embedded. The page issued only its initial document request, with no
  asset or external requests afterward. This was an internal HTTP test; it does not
  certify every browser's local-file or workspace preview handling.

Results: `build/checks/walking/browser-results.json`. Its HTML SHA-256
`69949ac6e94b5800c234b3b55f95f5e3eece3bba63f982457fcabc2be524656a`
matches `build/checks/walking/build-manifest.json`. The first harness run encountered
a CSP restriction on a string polling predicate; using a function predicate fixed
the harness without weakening the page policy or changing the demo implementation.

## Visual inspection and limits

I inspected the actual `idle.png`, `chest-detour.png`, `narrow-debug.png` and
`narrow.png` screenshots in the evidence folder. Maziss is clearly visible, without
an opaque rectangular sprite background or a duplicate character baked into the
room. Character scale reads plausibly against the door. The room, controls and
instructions remain visible in the narrow layout. The debug overlay shows furniture
exclusions in the relevant painted areas; no obvious foot-through-furniture mismatch
was visible in these sampled views.

During review the coordinator identified that the original 18 px clearance allowed
a narrow gap between the bench and chest that was implausible for the depicted body.
Clearance increased to 32 px, and the final node and browser suites above were rerun
on the rebuilt file; the detour now starts on the doorway side. This correction
illustrates why geometry tests alone cannot establish visual plausibility.

This is **foot-space collision avoidance**, with a 32 px clearance. It is not a full
body collision model. The flat background cannot place foreground furniture in front
of parts of Maziss; painted-object overlap needs depth/occlusion layers for production.
The authored floor is a conservative subset of the visible floor, so clicks may adjust
even where an owner might expect to stand. Owner feedback should refine that mapping.

The evidence demonstrates animated movement, speed changes and obstacle routing;
it does not establish that the animation feels natural. Generated pose consistency,
turning, foot sliding and body sway still need the owner's moving-image judgement.
Static screenshot inspection cannot certify these. No claim of a tested frame rate,
memory budget, real-GPU performance or long background-tab suspension behaviour is
made. Firefox, Safari, mobile touch, keyboard-only interaction, screen-reader usability
and full game integration were outside this run.

## Next acceptance gates

1. Owner tries the working HTML and judges gait, speed, scale and desired floor access.
2. Refine any visible pose changes/foot sliding and add appropriate furniture occlusion.
3. Integrate movement with game hotspots, interaction stopping distances and puzzle state,
   then rerun the game checks; a standalone navigation result is not integration evidence.
4. Establish actual target-browser performance and accessibility expectations before
   any public release decision.

**Changed files:** `tests/browser_walking.py` and this report only. Generated browser
results and screenshots are under ignored `build/checks/walking/`.

**Inspected:** project instructions and QA-002 brief; `walking/room.json`,
`navigation.js`, `demo.js`, `index.template.html`; navigation tests; final HTML,
sprite metadata, build manifest, browser result and four rendered screenshots.

**Unresolved:** owner motion judgement, production animation/occlusion, platform scope,
performance and game integration. No game code, assets, task board or other documents
were changed by QA.
