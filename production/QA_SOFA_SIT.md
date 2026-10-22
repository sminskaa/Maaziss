# Sofa interaction study — QA-016

Status: suitable for owner review as a first offline sitting interaction study. The final video delivery and actual browser captures were inspected; final art approval remains with the owner.

The owner requests a first interactive example in the new 16:9 room: click floor
to walk, select **Use** and click the sofa to approach one fixed clear cushion,
sit, and later stand to walk again. The yellow and blue pillows stay untouched.
The target is an offline HTML review, not integration into the main Godot game.

## Acceptance and evidence

Actual images are required alongside interaction checks. Inspect the new room,
neutral authored descent, final toon render and browser composites. A numeric pose
or navigation pass does not establish natural movement, support, art likeness or
correct occlusion.

- Preserve original body proportions at a calibrated floor depth; never fit every
  frame to its changing bounding box. Standing, approaching and seated states must
  remain recognizable as the supplied Maziss sculpt.
- Place hips on the clear right cushion, boots at floor level and bent knees in
  front. Check clothing, hair, bag, cuffs and boots through several descent phases.
  No disappearing fragments or repeated face projection.
- Account for the near sofa arm and cushion/furniture foreground where needed.
  A proxy seat is an authoring guide, not proof of room physics or full 3D scenery.
- Use actual DOM clicks to choose Use and sofa, observe walking, settling and seated
  states, then a floor click to stand and walk. Clicked sofa locations share one
  fixed seat. Right-click examines rather than activating sitting.
- Walls, sofa, desk and other furniture do not become walkable floor. Resize the
  canvas and test pointer coordinate conversion. Check offline loading and browser
  errors and inspect actual screenshots at desktop and compact sizes.
- Keep the review self-contained around one MB, while acknowledging this is a
  practical delivery workaround rather than a guarantee of host-panel support.

## Inspected preliminary images

Opened `build/checks/room-cutaway/room-reframed-source.png` and actual neutral
Blender poses `build/checks/sofa-sit/art/pose-90-1.png` and `pose-45-0.7.png`.
The final profile has a recognizable clothed figure, near-horizontal thighs,
continuously joined trouser cuffs/boots, bent knees and a near-upright chest.
The free hand is slightly forward of the knee; the source sculpt remains mitten
like. These neutral poses alone do not establish final room scale, hip/cushion
contact, grounded feet, painted-room coherence or sofa-arm occlusion.

The integrated page was subsequently exercised and inspected as recorded below.

Opened the actual toon `sit-00.png`, `sit-01.png`, `sit-02.png`, and
`first-composite.png`. The composite places the recognizable seated figure on the
clear right cushion, leaving the yellow and blue pillows intact. The bag and
trouser silhouette are continuous in these inspected frames. The free hand is
held forward, rather than demonstrably resting on the thigh. A soft floor/contact
shadow would improve grounding. Final proportions require a standing comparison
at the same anchor; doorway comparison alone is misleading across different depths.

An independent 241-sample pose audit found fixed foot transforms and maximum
bone-length error below 0.000001 world units. Eleven evaluated Blender body meshes
retain 4906 vertices and 10000 faces with finite coordinates, and boot minimum height
stays at the floor within floating-point tolerance. Those checks support continuity
but do not prove natural movement or absence of all surface intersections.
Private evidence: `build/checks/sofa-sit/qa/pose-audit.json`.

QA identified a camera-update ordering bug in the test manifest: its initial floor
projection was reported at image centre before the camera matrix had updated.
The coordinator corrected the update before full rendering. The final integrated
placement still needs direct browser/image inspection.

## First integrated browser result (historical atlas delivery)

Ran `python3 tests/browser_sofa_sit.py` against the self-contained
`visual-preview/maziss-sofa-sit.html`, 988636 bytes, SHA-256
`67a6695484cd76274397fb44d332068e56bd8713b23c70daef1fe3ea5e97df19`.
All 30 scoped browser checks passed in Chromium with networking disabled.

Actual DOM clicks demonstrated the observed sequence walking → turning → sitting
→ seated, then standing → walking → idle at the clicked floor destination. Wall
and desk clicks did not move the figure. Right-click examined the sofa and kept
Use selected. A second sofa click over the pillow area kept the same clear-cushion
seat. Floor samples stayed within the calibrated furniture-buffered polygon. Reset
restored position and verb. The same source-space click reached the identical seat
at desktop, 960-pixel and 390-pixel viewport widths without horizontal overflow.
There were no JavaScript errors or external network requests.

Actual canvas captures were opened, including initial, descending, seated, seated
at 960/390 pixels and walking after standing. The seated pose is readable on the
clear right cushion; the pillows remain in place, boots lie below the cushion and
clothes/bag remain visually joined in the inspected frames. The pose uses the same
fixed camera scale rather than independently resizing standing and seated frames.
Scale changes with floor depth during travel. A short turn precedes descent rather
than immediately replacing the walking heading.

The source audit checked all 249 declared actual RGBA model renders (41 descent,
192 walking, 16 idle/turn), matching source/script hashes and all 41 finite full-mesh
contact samples. Final ground projection is approximately (144,317.757), replacing
the initial stale camera-matrix value. Inspected final images cover front, both
profiles, back, oblique turn and several sitting times. No disappearing clothing,
repeated portrait or detached fragments were evident in those samples.

Private evidence is under `build/checks/sofa-sit/qa/`: `results.json`,
`render-audit.json`, `pose-audit.json` and actual canvas PNGs.

## Final video delivery

The coordinator replaced the small animated WebP atlases with full 288×360
transparent VP9 clips from the same retained model renders, keeping high-resolution
idle poses. Walking now uses one broad subtle contact cue rather than disconnected
rest-foot shadow ovals. Geometry, floor navigation and authored poses did not change.

Ran the focused key workflow on the final 978857-byte page, SHA-256
`9b2230c333c0e68f1e104c9ab591f605410bc7ace023ed85d6c938a519956a21`:
`python3 tests/browser_sofa_sit.py --focused --output build/checks/sofa-sit/qa/final`.
All 23 focused interaction checks passed, preserving the earlier 30-check
cross-room/resize evidence under its historical file hash. The final render/source
hash audit also passed for all 249 images. Recorded decoded-media assertions confirm
real video time advances during walking and sitting, rather than merely advancing
the desired frame index. The seated clip ends paused at 2.05/2.05 seconds.

Opened final initial, intermediate descent, seated and walking-after-standing canvas
captures. Transparent video composites correctly over the room; there is no black
rectangle. Face/outfit edges are clearer than the previous small-atlas delivery.
The fixed clear cushion, pillow placement, seated silhouette, knee/cuff continuity
and boot/floor relation remain coherent in inspected captures. The detached walking
shadow ovals from the first delivery are removed. The figure still has softer and
less painted surface detail than the room; this is a first interaction study.

Final evidence: `build/checks/sofa-sit/qa/final/results.json`, `render-audit.json`,
`media-decode.json`, and actual canvas PNGs. The final rerun covers key interaction
and encoding changes; it does not claim a new broad test campaign or host-panel
success on the owner's computer.

## Scoped recommendation and limits

Suitable to show the owner as a first sitting interaction study. This is not final
art approval, a production-ready rig, a full collision/physics system or integration
into the main Godot game. The page uses fixed-camera real model renders, a fitted
seat/floor proxy, buffered 2D navigation and a painted near-arm occluder.

The final animated figure remains somewhat softer than the room at the largest
canvas size; face, fingers and painted wear remain unfinished. The supplied sculpt still
joins the bag-side hand and bag, so that arm stays quiet. Its free hand is held ahead
rather than demonstrably resting on the thigh. Walking shadows are now a broad composited contact cue, rather than physically
cast shadows. Owner feedback remains necessary for acting, scale and style.

Internal browser success establishes local offline operation only. It does not
prove that the host chat panel will display the page for the owner.
