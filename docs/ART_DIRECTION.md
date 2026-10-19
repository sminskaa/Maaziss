# Visual and interaction direction

Owner references: Day of the Tentacle (original and redrawn examples), Space Quest VI,
Sam & Max, and Discworld / Discworld II. These establish visual goals, not a source
of game assets or a requirement to reproduce their characters, logos or rooms.

## Approved starting point

On 17 October 2026, the owner approved `art/proposals/apartment-cartoon-v2.png` as the
starting point for the game's visual style. Preserve the original image unchanged.
Use its painted cartoon texture, ink outlines, palette, warm/cool lighting, room
furnishings and more restrained door/window geometry as the baseline for future work.
Maziss is visible in this approved scene composition. Further character turnaround,
animation, asset separation and gameplay readability work must stay consistent with
this baseline; approval is not a claim that production assets are already complete.
Record proposed departures for owner review instead of silently replacing the style.

## Visual goals

- Painted cartoon backgrounds with visible drawing, expressive architecture,
  exaggerated silhouettes and perspective; avoid restrained flat-vector geometry.
  Owner feedback: retain the painted style, colours, lighting, furniture and texture,
  but make door and window frames mostly straight and plausibly constructed. Slight
  handmade irregularity is welcome; extreme bowed or banana-shaped frames are not.
- Rich colour and purposeful light: warm lived-in interiors, cool city daylight,
  coloured shadows, strong foreground framing and depth.
- Environmental details tell the story of an inhabitant and support readable objects.
  Maziss is poor, practical and untidy; his workspace contains signs of actual repairs.
- Original fantasy city with limited remnants of ancient electronics. A broken device
  is not an excuse to give the story unrestricted technological solutions.
- Maziss must be visible in scene-composition reviews so his scale and relationship
  to the room can be judged. A character-free background alone is insufficient.
  Expressive character proportions and acting will need a separate design pass.
  The current playable character sprite remains a placeholder.
- The references include both pixel-era and higher-resolution art. Pixelation is not
  mandated; first settle the drawing, shapes and colour design.

`art/proposals/apartment-cartoon-v1.png` is an AI-generated art proposal, revised from
an initial generation using OpenAI image generation on 17 October 2026. It is not yet
approved or installed as the playable background. Some props and perspective remain
provisional; avoid treating the distant city silhouette, incidental skull, or mechanical
clutter as new narrative canon. The image has no character or UI and does not yet
provide separate layers or animated window states. The art folder is excluded from
Godot import/export. User reference screenshots are not shipped as game assets.

## Revised scene composition

`art/proposals/apartment-cartoon-v2.png` retains the approved colour, texture, lighting
and furnishing direction, straightens the door and window frames, and adds a full-body
design for Maziss. It was edited from v1 using OpenAI image generation. The original
v1 is retained. The owner has approved v2 as the visual starting point; finer character
production details remain open, and incidental props do not establish new plot facts. This is a scene composition,
not a ready-made background/sprite package: it must be separated into production assets
before replacing the playable SVG room and character. The scene is available through
`visual-preview/maziss-art-revision-2.html` and the stable preview index.

## Controls

The bottom panel exposes Give, Pick up, Use, Look at, Talk to, Pull, Push, Close and
Open. A selected verb applies on left-click. Clicking empty walkable floor moves
Maziss instead. Right-click examines a room object or inventory item while preserving
the selected verb. The action line describes the intended verb and target.

Inventory objects have persistent graphical icons and readable labels. Select Use or
Give, then an item, then its target. Selecting another inventory icon with Use attempts
a combination. Invalid attempts never destroy items. Look at or right-click reads an
item; a bag panel provides an alternative with labelled controls.

The apartment deliberately has no NPC, so Talk to and Give cannot start a conversation
or transfer an item yet. No useful item-to-item combination is required here. Push and
Pull have distinct safe responses but no staged mechanism in this first room. These
verbs must receive scene-specific behaviours when such targets are introduced.

The strip frees the catch with Use. Open releases the leaflet; Pick up collects it.
Close can shut the window after collection; Open can reopen it without duplicating
items. The loose leaflet must be taken before closing so it cannot be trapped or lost.

Movement is currently a smooth translation of the placeholder sprite within a clear
floor corridor. It is not a completed walking cycle, full navigation mesh, automatic
walk-to-object interaction, or a multi-room movement system. Its position is temporary
presentation state, not stored in the puzzle save.


## Separate walking study

The approved composition now also has separate working room/character assets under
`art/walking/`, used in `visual-preview/maziss-walking.html`. That study demonstrates
obstacle-aware animated movement, while the main Godot game still uses its earlier
placeholder assets. See WALKING_DEMO.md and the independent QA_WALKING_REVIEW.md for
what was checked and what still needs owner motion feedback and game integration.


## Owner motion correction

The owner rejected the first walking cycle: travel was too slow, the same foot stayed
ahead, feet slid rather than alternating, arm movement was excessive, and the torso
leaned too far forward. Treat that gait as rejected, not approved animation. Revised
walking must show alternating planted feet and swing, quiet arms, a mostly upright
posture with only slight forward lean, and a faster comfortable pace. Changing frame
numbers or passing path tests does not demonstrate a correct human walk.


## Proportion and motion correction after articulated review

The owner accepts the alternating leg movement, but rejects the v2 cutout proportions,
rigid arms/torso, fully straight posture and boot-to-leg discontinuity. Preserve the
new leg mechanics while using v1 overall character proportions as reference. Restore
a slight forward bend (less than v1, more than v2), modest opposing arm swing and
small torso motion. Boots must join the trouser legs at their actual ankle/cuff
location. Do not interpret requests for less motion or bend as requests for none.


## Owner rollback: first character, legs only

After reviewing revision 3, the owner rejected further proportion/upper-body tuning.
Use the actual revision 1 character drawings as the baseline and apply only the
accepted alternating leg mechanism. Preserve the original head, torso, arms, posture,
proportions and boot artwork. Do not continue refining the replacement rig. Revision 4
is this constrained rollback, with the original atlases sampled at runtime.


## Walking reference correction (18 October 2026)

Owner rejected revision 4: unnatural human leg motion, including sideways knee bends
and distorted crossed legs in depth views. No walking revision is approved. Retain
the first character appearance, but stop presenting contact/navigation test passes as
proof of natural gait. Use inspected human motion and animator-authored pose guidance;
see WALKING_REFERENCES.md for sources, access limits and the next side-view study.

## Measured walking study (revision 5)

The retained owner footage now supplies a measured side-view stride and contact
timing. The original character atlas remains the drawing source. Motion is solved
in a forward/vertical plane before depth projection; actual painted side-view soles
are registered to their contacts. The HTML adds four study views, slow playback and
frame stepping. This is a new candidate for owner review, not approved animation.
See WALKING_DEMO.md and production/QA_REFERENCE_WALK.md for evidence and remaining
limits. The playable Godot room has not adopted this study yet.

## Owner rejection of revision 5

The owner finds revision 5 less bad but still far from natural human walking:
movement lacks fluidity, feet are misaligned with the torso at rest, knees straighten
abruptly, and motion is jerky. Treat this version as rejected despite its technical
test passes. Preserve the original character design. The owner is seeking further
references and asked whether animated FBX files can be inspected. Evaluate continuous
skeletal animation and neutral standing alignment before another motion proposal;
do not present numerical contact checks as proof of visual success.

## Image-guided attempt and permitted exaggeration

The owner supplied three pose sheets and 16 FBX references, requesting an image-only
attempt before the FBX comparison. Slight exaggeration is welcome if motion remains
smooth, coherent and recognizably human. Revision 6 retains the original textures
and uses authored smooth transitions, shared painted cuff geometry and a calibrated
neutral stance. No FBX/video data is used. It remains a candidate until owner review.

## Revision 6 feedback and requested FBX attempt

The owner finds motion slightly better but reports these unresolved visible defects:

- Side-view idle boots point upward; standing soles must be visually planted.
- The far arm appears in front of the body; every body part must respect camera perspective.
- Front-view resting boots lean sideways; neutral feet must remain upright and grounded.
- Detached ghost fragments appear ahead of the character; remove source-mask remnants.
- Trouser bottoms detach and follow boots. Trouser cuffs belong to continuous trousers,
  with the boot top aligned underneath; boot masks must not carry pieces of trousers.

The owner authorized using the supplied FBX files for the next attempt. Modest
cartoon exaggeration remains acceptable when motion is smooth and coherent. Work
was paused at the owner's request before the FBX extraction/render revision was
completed, to preserve remaining allowance. No revision 7 has been delivered.


## FBX candidate — revision 7

Work resumed at the owner's request. Three supplied FBX walks were actually imported;
`02-walkforward.fbx` supplies independent left/right joint trajectories for this
candidate. The original PNGs and character proportions are retained. Runtime masks,
continuous trouser skinning, camera-depth arm order, neutral planted boots and small
orphan-fragment cleanup address the five reported rendering defects. The 3D reference
is retargeted into 2D original drawings, so turning, depth views and planted-foot
travel remain limited. See WALKING_DEMO.md and production/QA_FBX_WALK.md. Revision 7
is a new review candidate, not owner-approved animation or Godot integration.


## Clothing continuity correction — revision 8

The owner finds the FBX walk much better and wants this motion retained. Remaining
feedback concerns holes/stray garment fragments, disconnected clothes/bag, both
front-view boots leaning observer-left, and front/back trouser shortening beyond
natural movement. Each garment and item must remain a continuous object.

The renderer now uses complete painted jacket backing underneath original torso
and neck detail, plus an intact separate satchel; arms never uncover subtractive
holes in those items. Head/face and original atlases remain unchanged. New repair
art is documented in art/walking/CLOTHING_REPAIR.md. Each front/back leg uses its
actual corresponding trouser and boot drawing. Cloth endpoints are the actual
skeletal cuffs, removing the previous extra screen-space cuff displacement.
The supplied FBX motion and timing are unchanged. This remains 2D layered animation,
not a set of 3D garment models or cloth simulation; natural foreshortening and
simplified turns still require visual judgement. See production/QA_CLOTHING_WALK.md.


## Complete-geometry study requested by owner

The owner still observes disappearing pieces after revision 8 and requests complete
anatomy (head/neck, eyes, mouth, arms, hands, legs, feet) and separate continuous
clothes/equipment, understood from every angle. Stop treating more sprite-mask
patches as the long-term solution. A complete 3D rig is now being evaluated as an
authoring/construction approach; camera depth handles overlap. The first procedural
model has deliberately preliminary face/surface detail and is not approval to replace
the painted cartoon identity. Preserve all approved art and the separate 2D studies.
See CHARACTER_3D_STUDY.md for construction, tooling, private-input and game boundaries.

## Painted complete-geometry candidate

The owner finds the overall movement acceptable but rejects angular construction
shapes, hand/bag penetration and remaining trouser defects. The complete model must
fit the original cartoon face, clothing and environment. A first surface-painting
study now rounds the forms, repairs sampled arm clearance and trouser knee weights,
and registers the original paintings onto complete surfaces. A clean jacket
reference supplies cloth without a second baked bag/strap. This first mapping
attempt still has visible face/projection and tailoring differences; it is not a
replacement visual approval. Keep the original drawings as the target. See
CHARACTER_PAINT_WORKFLOW.md for the actual approach and consulted free resources.

## Owner rejection of whole-sprite projection

The owner strongly rejects the painted3D candidate: the portrait repeats and
smears across the sides, clothing mixes together and Maziss is unrecognizable.
Original drawings remain accepted; the earlier3D movement remains useful. Do not
continue wrapping/blending full dressed sprites over a generic model. Research
reference-based modeling, then fit actual facial forms, hair, silhouette and outfit
geometry to the original design. Evaluate neutral-material front/profile/oblique
views before UV painting. Research has been saved, but the owner requested an
allowance pause before a replacement model was built. See
CHARACTER_REBUILD_RESEARCH.md and RESUME_CHARACTER_REBUILD.md.

## Supplied-mesh reconstruction study, 19 October

The owner resumed with a recognizable complete `white_mesh.glb`. The new private
study retains that sculpt, repairs malformed cross-hand geometry, fits the FBX
walk and adds modeled facial features plus continuous outfit colours. Actual
eight-angle/multiple-phase reviews by Art and QA find a coherent stylized human
without the earlier repeated portraits, disappearing pieces or stretched bag shelf
in the checked poses. This is a reconstruction study, not a finished art approval.

The bag-side arm stays quiet because a local joined hand/bag region does not yet
support independent motion with the current rig. Separate topology/weight painting,
adult facial likeness, hair/hands, inked detail and painterly clothing remain work.
Original drawings are unchanged and remain the artistic target. See
SUPPLIED_CHARACTER_STUDY.md and the scoped Art/QA reports. The compact review is
`visual-preview/maziss-rebuilt-review.html`; the playable Godot room is unchanged.

## Lighting and room-scale comparison

The owner prefers the supplied-sculpt method. A separate actual Blender look test
uses diffuse toon shading, warm interior key light, cool window fill and thin brown
contours, with fixed camera/lights as the character changes heading. Art and QA
reviewed actual room comparisons, scale placements and sampled walking images;
the palette/contours improve coherence, while adult face likeness, hands, wear,
deep teal jacket detail and real room shadows remain incomplete. This is a visual
target, not an implemented Godot toon material or replacement art approval.

The owner also supplied a dimensional cutaway room image and explicitly selected a
16:9 rectangular view, removing the lower pointed floor. A separate image-assisted
reframing proposal preserves recognizable furnishings and warm/cool painted style.
It has not replaced the earlier approved room and does not supply actual room
geometry. The floor/camera and character scale need calibration to the new image
before movement is integrated. See STYLE_MATCH_STUDY.md and the room review reports.
