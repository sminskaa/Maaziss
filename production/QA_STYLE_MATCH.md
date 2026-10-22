# QA-014: character/environment lighting and style study

19 October 2026. Final actual render, scene-scale and compact delivery review.

**Recommendation: suitable for owner review as a lighting and perspective study.
It improves colour coherence, but is not finished likeness, final art approval,
a reconstructed three-dimensional room or a production-ready character.**

## Agreed visual criteria

QA opened the actual approved room composition, its character-free background and
the retained model's front render. The approved image remains the target: amber
interior light, turquoise window light, purple/brown shadows, ink-like contours,
painted wear and a clearly recognizable dark-haired, teal-jacketed Maziss. The
baseline model is coherent but reads as dark, desaturated clay beside that room;
its facial likeness, hands and garment detail remain simplified.

Art and QA are evaluating actual rendered pixels, not treating shader code, mesh
validation or successful file export as evidence of a matching artistic style.
The character, costume and bag must remain recognizable from front, oblique and
profile views, with no new disappearing pieces in sampled walking poses. Light
direction must stay consistent in room space as the camera changes. Character
shadows must relate to the room's warm/cool palette rather than glossy plastic.

Any room adjustment must remain subtle: retain the furniture/layout, straight
door/window construction, painted lines, colour relationships and depth. A change
that loses those qualities should be rejected in favour of the existing background.
A generated appearance study is not a reconstructed three-dimensional room.

## Delivery scope and checks

The existing model and motion, original room and character atlases are hash-bound
in `tests/browser_style_match.py`. Its offline Chromium check exercises actual
embedded images and any native videos at desktop/mobile widths, records captures,
rejects external requests and required application JavaScript, and enforces the
compact one-MB review budget. These checks do not prove that the host chat renderer
works. Owner review remains the artistic approval step.

The quiet bag-side arm, unfinished facial likeness and source geometry limitations
are not solved by a lighting pass; production cleanup and Godot scene integration
remain separate.

## Actual character-render findings

QA opened actual Blender images under `build/checks/style-match/character/`:
front, oblique and profile idle, then an actual contact sheet of every one of the
24 final profile walking frames. These are the 128-sample fixed-camera captures,
not the initial grainy test. The manifest explicitly records a stationary room camera and
lights with the complete character presentation rotated about world Z; the warm
key and cool edge therefore remain coherent with the same room while Maziss turns.

The new palette and contour are a useful improvement over the clay-like baseline:
skin, ochre shirt and brown bag receive warm light, the jacket remains muted teal,
and cooler edge/shadow colours relate to the turquoise window. In the inspected
images, the character reads coherently in profile and oblique view; the face is
not repeated on the side. QA observed no newly disappearing garment pieces, holes
or floating fragments in the inspected idle views and final 24-frame side cycle.

This is still visibly a simpler model beside the approved painting. The face is
rounder/younger, the hands are mitten-like, garment shading is soft, and drawn seams,
wear and facial detail are much sparser. A lighting pass has not reconstructed that
missing sculpt or painted detail. The sampled poses are sequentially coherent;
this study does not establish improved fluidity, perfect foot contacts or readiness
for arbitrary character actions. The retained model/motion hashes establish
preservation of the prior study, not a corrected gait or new animation system.

## Actual scene comparison and scale

QA opened the final desktop/mobile screenshots, expanded all comparison sections,
and inspected the native room-walk video at 0.00, 0.58, 1.16, 2.33 and 3.25 seconds.
The original approved drawing, prior shading and new shading use the same room,
making the warmer character and clearer outline improvement directly visible.
The character remains much simpler than the background: jacket planes are pale
and broad, skin is fairly uniformly orange, and the original adult face and dense
painted wear are not yet reproduced. The approved background itself is unchanged.

The three actual back/middle/foreground placements show a plausible progression
against the same door, sofa and desk. At the back, Maziss fits below the doorway;
the foreground version is larger in the way expected from the floor perspective.
The room-walk captures keep approximately the same head/boot scale as he crosses
at one depth; there is no visible frame-bounds-driven resizing. His contact area
stays on the same floor band in these captures. No new disappearing pieces were
observed in those native-video samples.

The accompanying calibration is a **2.5D perspective proposal**, using the approved
character's roughly 596-pixel height and foot anchor (1125,698), a proposed horizon
at y=130, and one scale rule. Its three proposed heights are about 451, 588 and 682
pixels at floor y=560, 690 and 780. This is not recovery of a unique camera from
the painting and is not metric validation of a modeled room. The soft ellipse under
the feet is a composited contact cue, not a physically cast room shadow. Furniture
occlusion, navigation, real shadow receivers and a shared room camera remain future
integration work. The HTML labels these limits rather than presenting the clip as
an interactive playable movement system.

## Final compact delivery

`visual-preview/maziss-style-match.html` is 633,890 bytes, SHA-256
`9bc868ad25cd531f15a60466209159f4d0689f41b148334ec9b942d0c2afc9bc`.
QA reused the completed hash-matching browser check after the interruption rather
than rerunning broad tests. Offline Chromium decoded all five embedded images and
the 960×406 native video; the 3.5-second video advanced during playback at both
1280×1000 and 390×844. No scripts, external requests, page errors or horizontal
overflow occurred. QA opened both actual screenshots and the expanded comparison.
The native video repeats the retained 24-frame cycle three times; this is review
footage, not a new animation or game controller.

The final render manifest is hash-bound to the retained source Blender file, and
all 27 actual PNGs decode at 480×640 with nonempty alpha. Source GLB, motion data,
approved room and character atlases retain their original recorded hashes. Private
results, comparison captures, five native-video moments and the 24-frame contact
sheet are under `build/checks/style-match/qa/final-match/`. Internal browser success
still cannot guarantee delivery through the host panel. Owner approval remains
the next artistic decision.

## Clean room reference delivery

QA exercised and opened the actual browser capture of
`visual-preview/maziss-room-reference.html` (642,530 bytes). At desktop 1280×1000
and mobile 390×844 with networking disabled, its embedded native image decoded;
there were no external requests, page errors, scripts or horizontal page overflow.
The displayed room retains the approved furnishings, line work, perspective and
warm/cool palette without Maziss. Its text correctly calls this an export of the
existing artwork, not a redesigned or modeled three-dimensional room. This page
alone cannot establish character scale or character/environment style coherence.

The source GLB, motion data, approved room composition, clean room PNG and both
character atlases match their retained hashes. Private browser screenshots and
machine results are under `build/checks/style-match/qa/room-reference/`.
