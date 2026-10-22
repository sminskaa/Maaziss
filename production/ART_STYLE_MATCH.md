# Supplied-character room lighting study — ART-008

19 October 2026. Bounded look-development study, not finished character approval.

## Actual visual comparison

Opened the approved `art/proposals/apartment-cartoon-v2.png`, the original side
character atlas, the retained supplied-model front render, and the new actual
Blender renders. The original room and character paintings remain unchanged.

The approved painting has amber highlights, teal/green clothes, ochre fabric,
warm brown leather, purple shadows and fine dark drawn contours. The prior
Workbench character reads darker and more clay-like than that painting.

The new real render uses the supplied complete mesh and existing FBX-derived
motion, retaining its continuous vertex-colour palette. A diffuse toon material,
restrained procedural colour grain, thin brown Freestyle contours, amber room key
and weaker cool window fill make the face, green jacket and ochre shirt more
readable. No original portrait or complete sprite is pasted onto the model.

Inspected the final front, oblique and profile idle renders, plus actual profile
walking phases 0, 6, 12, 18 and 23 of the completed 24-frame capture. The warmer skin and leather, clear green jacket and fine
contours bring this candidate closer to the room. It is recognizable as the same
supplied sculpt at the checked headings and poses; no new detached clothing or
disappearing pieces were visible in this bounded sample.

The fixed scene camera and room lights remain still while a presentation parent
turns the whole character. This matters: orbiting the camera instead produced a
cool, grey profile that would not match the same on-screen room light. The final
captures replace that rejected orbit-camera test.

## Evidence and reproducibility

- Source: private `build/checks/supplied-character/maziss-supplied-rig.blend`.
- Tool: `tools/render_character_style.py`.
- Run: `blender -b --python tools/render_character_style.py`.
- Actual captures: private `build/checks/style-match/character/idle-{0,45,90}.png`
  and `walk-90-00.png` through `walk-90-23.png`; transparent PNG, 480 × 640.
- Manifest: private `build/checks/style-match/character/manifest.json`, including
  source hashes, fixed-camera heading convention and projected ground anchor.
- CPU Cycles, 128 samples, diffuse toon BSDF and Freestyle; the initial seven
  stills took about 39 seconds before capture was extended to a 24-frame cycle.
  The final three idle views plus all 24 walking frames took about 148 seconds.
  The available Blender build lacks OpenImageDenoise, so
  denoising is disabled. The 32-sample first test was too grainy and was replaced.
- Orthographic scale is 2.23; the retained model rest height is 2 world units.
  World floor anchor (0,0,0) projects to approximately (240,606.923) pixels in
  every heading. Geometry and motion are unchanged. Do not normalize each pose
  to its silhouette bounds when compositing: that would change body proportions
  and apparent scale during walking.

## Remaining art work

This shading pass does not solve facial likeness. The sculpt remains rounder and
younger than the tired adult drawing, hands remain mitten-like, and bag-side
motion still has the earlier topology limitation. Some shadow transitions are
smooth and the materials have much less authored wear, seams, stitches and
painterly detail than the room. Thin contours and procedural grain alone do not
equal the approved drawing style.

Next art work should refine the adult face and independent bag/hand topology,
then paint dedicated UV material detail on those coherent forms. This candidate
is suitable for a room-comparison review. It is not a production-ready character
or a decision to alter the approved room. Runtime Godot shading must be developed
and compared separately; this is a Blender look target, not an exported Godot
toon shader.

## Final room-composite review

After the allowance reset, opened the actual final room composites in
`build/checks/style-match/delivery/`: `original.png`, `baseline.png`, `styled.png`,
`side.png` and `scale.png`. Also opened composite video frames 0000, 0023, 0047
and 0071. This was a visual scene comparison, not an inference from render code
or numerical checks. No additional rendering or model changes were made.

The proposed treatment is worth showing the owner. At the same placement as the
original drawing, Maziss remains a plausible occupant of this room: his boots
meet the floor, his head and shoulders are believable against the door and
window, and the sofa seat and desk top read at useful body heights. The three
depth placements give a plausible smaller figure near the door and larger figure
in the foreground. The sampled constant-depth walking composites keep his size
stable as he passes the desk, door and sofa; no silhouette-based stretching or
independent limb resizing is visible in these samples. This remains an initial
perspective proposal, not confirmation of a reconstructed 3D room camera.

Compared with the previous shading, the warm face, ochre shirt, brown bag and
green jacket read more clearly against the amber room and turquoise window.
Thin contours also connect the sculpt to the drawn background. The source mesh
is still recognizable in front and side views, and the inspected walking frames
do not show new disappearing clothing or detached fragments.

The character nevertheless remains visibly simpler than the environment. His
jacket is relatively pale and flat compared with the deeper teal painted design;
skin is brighter and more uniformly orange; cloth and boots lack the room's
crisp dark creases, wear and varied painted shadows. The round youthful face and
bulky mitten hands still differ from the older, thinner, more angular original
Maziss. The small composited floor shadow supports placement but does not model
room-object shadows, reflected colour or real 3D contact. A modeled room and
shared game camera will be needed to evaluate those relationships properly.

Recommendation: present this compact review as a useful lighting, palette and
scale direction. Preserve the approved background. Next refine the character's
adult facial likeness and authored material detail, with a later shared-camera
room test. Do not describe this review as final cartoon-style parity, production
rig approval or newly improved animation mechanics; the underlying gait is
unchanged, and this Art check inspected selected video frames rather than
certifying continuous playback.
