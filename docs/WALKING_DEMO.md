# Walking study — image-guided revision 6

Open `visual-preview/maziss-walking-v6.html`, or the latest `maziss-walking.html`.
HTML works in the owner's panel; embedded chat pictures still do not. This is a
separate art/motion study, not the playable Godot apartment.

## Owner direction and reference boundary

The owner rejected revision 5: jerky motion, sudden knee extension and boots ahead
of the body at rest. Modest cartoon exaggeration is welcome if movement remains
smooth, coherent and recognizably human. Preserve the first Maziss design.

This candidate uses only the three supplied image sheets as qualitative pose
references. The running boy sheet helps identify exaggeration to avoid; the two
adult side-view sheets inform stance, passing and recovery. They do not specify
frame durations or reliable ground heights. Timing and curves are authored, not
measured or traced motion. The 16 FBX files are saved privately for a subsequent
comparison and have not been imported. Previous video tracking is not used by this
cycle. No supplied reference images, recordings or FBX files are embedded or committed.
See `production/IMAGE_WALK_BRIEF.md` for the independent image review.

## Motion construction

`walking/image-motion.json` records provenance, pose intentions, authored cadence,
60% stance and original painted-boot geometry. `walking/image-gait.js` uses smooth
foot trajectories with matched position/velocity at contact and loop boundaries.
A foot rolls from heel contact through flat support to toe-off. During swing its
support height is interpolated separately from rotation: forcing an airborne shoe
against an imaginary floor caused an abrupt knee tug as it rotated through flat.
The leg folds early in swing and has a longer interval to extend before landing.

Knees are solved against the painted boot cuff actually drawn, before rendering.
Soft reach limits avoid the straight-leg singularity and abrupt pelvis clamps.
Neutral sole positions are centered around the pelvis using opaque source heel and
forefoot pixels. Starting and returning to rest use smooth transitions and foot
recovery; the initial pose uses the same articulated renderer as later idle poses.

Original head, clothing, bag, trousers and boot textures remain unchanged. Modest
opposing arm swing, pelvis motion and torso rocking provide secondary movement.
The same forward/vertical leg model is projected into front/back views, where
original directional boot drawings remain a limited approximation. Movement phase
follows room travel; the in-place study uses an authored 1.08-second full cycle.

## Review controls

- Click floor to walk; a later click changes the route. Existing obstacle routing
  and root clearance are retained.
- Left, Right, Toward camera and Away from camera show an in-place cycle. Feet
  intentionally travel against the stationary floor in this treadmill-style view.
- The live close-up shows the actual same character render at a larger scale.
- Stand still exits the study/route and lets the recovery finish. Use this to
  examine resting foot alignment. Reset restores the initial resting pose.
- Pause freezes motion. Next frame advances 1/30 second of the study. Half/quarter
  playback helps inspect knees, shoe roll and the loop boundary.
- Show footsteps and Show walkable area are optional developer review overlays.

## Validation and limits

Final frozen build `cdeb00514796` passed 48 focused checks with no failures or browser
errors. Independent evidence and candid visual findings are in
`production/QA_IMAGE_WALK.md`.
Tests check onset/settling, pose continuity, painted contact, original source use,
routing, controls and offline execution. They do not certify naturalness. The owner
still decides whether the actual moving character is convincing.

Front/back foot perspective, directional drawing changes during turns, foreground
occlusion, clothing deformation and full production animation remain limited. This
single-layer room checks the navigation root, not full-body 3D collision. No native
Windows run of the HTML is inferred from Linux Chromium checks. The separate Godot
room still uses its earlier placeholder graphics; integrating accepted art/motion
is issue #3, after creative review of issue #2.

## Reproduction

```sh
python3 tools/build_walking_demo.py
python3 tests/browser_image_walk.py
python3 tools/capture_image_walk.py
```

The builder uses Python/Pillow. Browser tools use Playwright/Chromium in this
workspace. The output embeds its art/code and needs no runtime network or AI.
`build/checks/image-walk/build-manifest.json` records source/output identity.
`visual-preview/maziss-walking-v6-poses.html` contains actual rendered phase captures.
Previews are local, ignored by Git, readable with mode 0644, in a 0755 directory.
Previous v1–v5 HTML and the video-analysis helper/data remain historical references;
they are not approved and are not inputs to this new animation engine.

The final target remains an installed, offline desktop Godot game with bundled
art, text/audio and local saves. This review does not change that target.
