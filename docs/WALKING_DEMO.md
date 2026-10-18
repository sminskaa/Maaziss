# Walking study — human reference (revision 5)

Open `visual-preview/maziss-walking-v5.html`, or the latest `maziss-walking.html`.
The owner sees self-contained HTML in the panel; native chat images still fail.
The review page is generated locally, not served by an external game service.

## What changed

Revision 4 was rejected: human knees/feet moved unnaturally, especially in depth.
Revision 5 uses a measured near-leg stride from the owner's side-view footage:
frames 36–78 at 30 fps, approximately 1.4 seconds. Twenty-four filtered phase samples plus
an identical closing sample are stored in `walking/reference-motion.json`. The other
leg is reconstructed with a half-cycle offset. Exact source/uncertainty and the
analysis method are in `production/MOTION_REFERENCE_ANALYSIS.md`.

The new `walking/reference-gait.js` evaluates the leg in its forward/vertical plane
before projecting into room depth. It retains a forward-bending human knee instead
of solving a screen-space knee out to the side. Grounded toe contacts can remain
planted while the heel rises. Contact extension is fitted to Maziss's proportions;
copying oblique tracking angles literally would introduce a crouch. Heel-rise foot
pitch is bounded to 35 degrees; that fit is not an exact ankle measurement.

In side views, an opaque point on the original painted forefoot sole is registered
to that planted toe. The boot and trouser cuff use the same transform, so fixing
model contacts also fixes the visible sole instead of letting it slide around the
ankle. Registration releases gradually after lift-off. Depth views still use their
original flat boot drawings and need further foot-roll refinement.

The first original source atlases, head, jacket, bag, trousers and boots are retained.
Original arm pixels are masked and moved at their shoulders with restrained opposing
swing, while the torso follows the pelvis. No source PNG is edited or replaced with a
new character. The game pace scales the recorded cycle for room travel (1.3× nominal
cadence at constant height); in-place study uses the reference 1.4-second cycle. Phase
follows distance during travel. Heading uses angle interpolation, including 180-degree
turns. Existing room geometry and obstacle routing are retained.

## Review controls

- Click room floor to walk and change destination.
- Use Left, Right, Toward camera or Away from camera for an in-place cycle study.
  This study intentionally has treadmill-style foot travel; judge stationary contacts
  in room movement, not from an in-place animation against an unmoving background.
- Pause freezes the pose; Next frame advances 1/30 second in study mode.
- Playback offers normal, half and quarter speed. Reset exits the study.
- Show footsteps marks the model's heel projections; the toe is the planted anchor
  during the loaded/heel-rise part of a moving step.

## Original design and limits

The approved room composition and original character PNGs remain unchanged. Depth
views use projected leg motion with original flat front/back boot drawings. Full 3D
boot roll, torso twist, lateral weight transfer, refined stopping/turn transitions,
foreground masking and a production sprite cleanup remain refinement work. This is
an improved motion-review candidate, not a claim of finished animation or owner
approval. Inspect normal-speed rendered motion; geometry checks alone cannot prove
naturalness.

Godot's playable apartment remains unchanged and still uses SVG placeholders. This
HTML study is separate; integrating accepted art/motion into the actual offline
Godot game is GitHub issue #3, after the owner's creative review of issue #2. Personal
recordings, face images and raw tracking are excluded from GitHub and previews.

## Reproduction

```sh
python3 tools/build_walking_demo.py
python3 tests/browser_reference_walk.py
python3 tools/capture_reference_review.py
```

The builder needs Python/Pillow. The browser tools need Playwright and Chromium
(`/usr/bin/chromium` in this workspace). The source analysis helper can regenerate
normalized data from the existing private cache using Python's standard library;
optional fresh tracking uses MediaPipe 0.10.21 / OpenCV 4.11.0.86. Neither model nor
private footage is needed to play the already-built HTML or final game.

The current build/source identity is recorded under `build/checks/reference-walk/`.
Independent QA is `production/QA_REFERENCE_WALK.md`. The review output contains actual
rendered phase captures under `visual-preview/maziss-walking-v5-poses.html`, not new
painted assets or personal video frames. Preview files are 0644 and directory 0755.

Final build `56d1b9cb1e56` passed 62 focused browser checks. The reviewer inspected
all four views and confirmed alternating contacts, coherent painted boot joins and
zero loaded forefoot drift in the measured straight traverse. Direct local-file
navigation is blocked by this workspace's managed Chromium policy; an embedded copy
did animate with browser networking disabled. Owner visual approval remains pending.

The final target remains a locally installed, offline desktop Godot game, with bundled
assets, text/audio and local saves, without required AI/API/login/server connections.
