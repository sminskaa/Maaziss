# Complete 3D construction study: focused QA

This review covers a new construction prototype with separate, complete geometry
for anatomy, clothes and equipment on a shared skeleton. It does not approve a
replacement for the owner's painted character identity.

## Evidence and reproduction

The focused harness is `tests/browser_character3d.py`. It uses the existing
Playwright, Chromium, NumPy and Pillow installation. Build the private model and
self-contained preview using the documented project builders, then run:

```sh
python3 tests/browser_character3d.py
```

The supplied FBX-derived poses, model arrays, actual browser captures and detailed
results stay under ignored private/build directories. They are not redistributed
in this report. The harness verifies the model and runtime hashes before and after
its run.

The checks cover welded triangle-edge closure for every object, valid skin
weights and normals, fixed retargeted bone lengths, finite actual skinned vertex
positions across 24 poses, all requested inspectable part categories, offline
execution, owner-facing controls, and actual front/rear facial occlusion through
pixel comparisons. It also captures 32 dressed poses from eight camera angles
and four anatomy views for visual inspection.

## Result

Frozen build `62773eacf060d33f2e91f91dd099034c33a6860034bb3f69b8fc72d11631a1ca`
passed **32 focused checks, with no failures or automated warnings**, using
Chromium 154.0.8037.57 with software WebGL and browser networking disabled. The
run took 167.08 seconds; this is test duration, not a player performance result.
An earlier completed run survived the allowance interruption. The coordinator
then corrected the strap's fit against the jacket and shirt, requiring this
new focused run against the changed model and its frozen preview.

All 138 exported objects had closed welded triangle-edge topology. The shirt,
pants and jacket were each one connected surface. Skin weights and normals were
valid, actual skinned vertices stayed finite through 24 phases, and segment
length drift remained below 0.000000164 metres. Cycle endpoints matched. The
lowest sampled boot vertex was approximately 0.003515 metres above the world
origin, just above the preview floor at 0.002 metres.

The actual viewer retained every exported object and all requested part groups.
The complete bag assembly shared one rigid transform. Front-facing eyes and
mouth changed 1,798 and 141 rendered pixels respectively when hidden; from the
rear neither changed visible pixels. Cast shadows were temporarily disabled for
that comparison so a hidden eye's shadow on a shoulder could not be mistaken for
an incorrectly visible eye. Normal renders retained shadows.

The pause, frame-step, idle, body-only, dressed, wireframe, side-view and camera
drag controls worked. No JavaScript errors or network requests occurred, and
source/output hashes remained unchanged during the run.

## Visual review and recommendation

Inspected the actual 32-frame contact sheet spanning eight camera directions,
plus enlarged rear walking, both rear three-quarter walking views and side
anatomy captures.
The body, limbs, clothes and bag retain complete geometry as the camera changes;
the old painted cutout fragments are absent from this construction technique.
Foot and trouser volumes remain coherent in these sampled frames, and distant
limbs are hidden by nearer surfaces through normal camera depth.

**Go for owner review of the construction approach; no approval for final
character art or production integration.** The study is visibly simpler than the
approved painted Maziss: angular tailoring, simplified hands and facial forms,
basic hair and flat surfaces. The shoulders, neck and sleeve transitions remain
rough. The corrected long diagonal strap now remains visibly continuous across
the jacket's back in the sampled rear and rear three-quarter walking views,
instead of becoming buried as in the earlier model. Its upper shoulder/neck
connection still needs clearer tailoring. Small underlying surface breakthroughs
remain visible near the waist. Those remaining issues are garment placement or
intersection defects, not missing geometry; complete production garment fit is
not established. The bag and strap currently move rigidly with
the torso, without independent secondary motion. The shared rig also needs
further torso, shoulder and facial articulation for a finished performance.

## Limits

Closed geometry prevents missing sprite cutouts; it does not prove garments fit
without intersections or that skinned fabric preserves volume and tailoring.
Some anatomy, face shapes, surfaces and equipment remain deliberately simplified.
The test does not establish naturalness, finished art quality, native Windows or
Godot behavior, or desktop performance. The owner retains visual approval.
