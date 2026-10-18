# Walking checkpoint — FBX revision 7

The owner requested resumption after the allowance pause. Revision 7 now uses an
actual imported FBX ordinary walk and preserves the first original character art.
Branch: `feat/reference-human-walk`; draft PR #4. Do not merge without the owner.
The main Godot game still has placeholder graphics; this is a separate HTML study.
Final build `9d7c3a14af4f` passed 54 focused browser/pixel checks. This establishes
the scoped rendering/control checks, not owner acceptance of human naturalness.

## Review artifacts and implementation

- `visual-preview/maziss-walking-v7.html`: interactive room, four study directions,
  live close-up, idle, slow playback and frame stepping.
- `visual-preview/maziss-walking-v7-poses.html`: actual phase captures.
- `production/FBX_MOTION_REVIEW.md`: imports, selected cycle and extraction caveats.
- `production/QA_FBX_WALK.md`: final checks and candid visual limits.
- `walking/fbx-gait.js`: actual bilateral joint interpolation and fixed-length retarget.
- `walking/character-renderer.js`: runtime masks, continuous pants, depth layers,
  flat idle boots and disconnected-fragment cleanup.
- `docs/WALKING_DEMO.md`: controls and reproduction requirements.

Selected source: `02-walkforward.fbx`, frames 234–269 at 30 fps (1.166667 seconds).
Both legs/arms were extracted independently. Idle is authored separately from the
source T-pose and walking foot pitch. Three ordinary walks were inspected, not all16.

## Retained boundaries

Original approved room and character PNGs are unchanged. All16 supplied FBX files
remain outside the repository, listed by the ignored private intake. Extracted curves,
local previews and source skeletal review are private; no redistribution licence is
established. Public helpers/reports do not include source animation arrays. Rebuilds
need retained private inputs, not merely a fresh public checkout.

HTML panel delivery works for the owner; chat embedded images do not. Deliver readable
0644 HTML files in the 0755 preview folder. Do not claim repository edits repair the
chat renderer. No paid services, new dependencies, required runtime AI or server.

## Remaining work after owner feedback

Judge actual moving playback, not only geometric test passes. Front/back foot roll,
view switches while turning and world-space foot planting remain approximate. Further
motion corrections should be driven by observed defects in this candidate. Only after
creative acceptance should we integrate the art/movement into Godot. Owner approval
and merge remain separate from scoped QA results; do not claim a finished release.
