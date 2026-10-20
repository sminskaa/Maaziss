# Right-hand stool pull and occupied slide

Owner direction replaces the rejected circling/shuffle candidate: Maziss takes the
stool with his anatomical right hand from its left side, makes a short direct
move to sit facing the desk, grips the seat with his right hand again, slides
himself and the stool toward the desk together, then rests both hands on the top.
Writing is a separate future action. Earlier previews and original art/models
remain preserved.

## Construction

- `tools/prepare_stool_right_arm.py` creates a private derived rig. A closed arm
  reconstructed from the supplied free-arm shape moves independently of the bag.
  The retained bag is gently shifted outward with a continuous transition. The
  source face/hair coordinates remain unchanged; original supplied GLB/rig stay intact.
- `tools/stool_slide_pose.py` authors8.8seconds at20fps with one compact boarding
  transfer rather than a walk around the stool. The right-hand seat contacts,
  seat/body relationship during the slide and final desk support are explicit.
- `tools/stool_desk_geometry.py` fits solid support/depth meshes to the painted
  desktop, cabinet, actual diagonal brace and nearby objects. Their camera
  holdouts retain the room's painted appearance while providing correct overlap.
  These are fitted contact volumes, not finished textured movable desk assets.
- `tools/render_stool_interaction.py` applies the same world transforms and boot
  orientation in rendering and geometry probes through `apply_sample`. The source
  and dependencies remain frozen during a render. `--resume` verifies retained
  inputs and individual PNG hashes before reusing interrupted full-render frames.

The scene, sources, images and progress manifests are saved privately under
`build/checks/stool-slide/`. The independent arm candidate SHA-256 is
`0b4f0fd6c7f180c3c71bab70dae384cac5341d5c6ccc23b615896631907352b2`;
the frozen pose SHA-256 is
`95f60d2ef89f423a123c696d809495e0ca6026c41e5cac500cac07708b82c2ec`.
All original models/painting remain untouched.

## Compact review

`visual-preview/maziss-stool-slide.html` is945456bytes, SHA-256
`8ebd75f67a8c947177db035e2607a5b9a5052f8993987c3465eece1a60de9928`.
Select **Use**, then the highlighted stool. Native video controls also work.
The9.85second clip includes177actualframes and a one-second held endpoint.
An optional alternate-camera image exposes both hands over the support surface;
it is a diagnostic view, not a replacement room/art style.

## Current review gate

Art and QA inspected the actual corrected room keys and a separate unobscured
view of the hands over the desktop. The lowered elbows improve the working pose;
coarse rounded hand shapes are supported, not fully articulated flat palms.
Independent QA checks all177baked samples: no detected boot/stool or boot/desk
surface crossings, no tested bag vertices more than0.5mm inside the seat, and
held contact/finite geometry checks pass. Skin lies1.23mm/3.10mm above the desktop.
The initial approach has a measured10.34mm boot-floor overlap; that inherited
walking-quality limitation remains disclosed. This is sampled evidence, not
runtime collision/cloth certification.

Full native motion and offline controls now pass: Art inspected36advancing
playback captures and QA inspected14native movie views. All177frame hashes and
source/scene binding checks pass;11offline Chromium checks plus touch start/reset
pass. Both reviewers recommend owner review, not finished-art approval. See `production/ART_STOOL_SLIDE_FINAL.md` and
`production/QA_STOOL_SLIDE_FINAL.md` for current exact evidence and scope. Historical
failed probes remain recorded separately; an earlier in-memory test's stale rig
inverse/missing boot roll was fixed rather than treated as a visual pass.

## Resume/reproduce in the retained private workspace

```sh
blender -b --python tools/render_stool_interaction.py -- --pose-module stool_slide_pose --source-blend build/checks/stool-slide/character-right-arm.blend --output build/checks/stool-slide --resume
python3 tools/build_stool_interaction_review.py --output build/checks/stool-slide --html visual-preview/maziss-stool-slide.html --contact-view build/checks/stool-slide/art-resume/corrected-final-palm-contact.png
```

The retained generated clean-background patch must already exist in that folder.
No runtime service is used. If an old full render has different source/configuration,
`--resume` refuses before overwriting the saved scene. Archive that candidate into
a separate private folder before starting a different full render. Add `--keys`
without `--resume` for a small image gate; do not overwrite a full final scene
while another agent audits it. Current approach remains a compact authored review
for an offline Godot game, not main-game integration or arbitrary navigation.
