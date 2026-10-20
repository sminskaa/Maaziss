# QA-018 stool approach/pull/sit

Independent actual-image review, 19 October 2026. Scope: private offline review
prototype, not a Godot integration or final art approval. QA owns this report and
`build/checks/stool-interaction/qa/` only.

## First corrected-image gate

Actual images opened at full room size:

- `build/checks/room-cutaway/room-reframed-source.png` (original painted stool).
- `build/checks/stool-interaction/room-clean.png` and `clean-crop.png`.
- Corrected actor-root composites `room-key-000.png`, `room-key-050.png`,
  `room-key-156.png` (0, 2.5, 7.8 seconds).

Earlier distorted first captures are superseded and provide no approval evidence.

The cleanplate has no visible old stool, open hole, duplicated leg, isolated old
shadow or obvious rug/floor/desk discontinuity. Rug weave/check pattern and fringe,
floor joints and desk edge remain plausible in the exposed crop. This is a visual
recommendation for this background candidate, not proof of full-motion layering.

At rest the replacement is a complete recognizable stool with round seat, legs
and circular footrest; its room scale and floor perspective are plausible. Its
regular shape, plain seat and smoother surfaces remain visibly preliminary beside
the painted furniture. Maziss retains recognizable proportions, continuous coat,
bag and boots, and appears floor-supported. The free Left hand reaches the near
seat edge at 2.5 seconds; surface overlap is plausible, but fine finger wrapping is
not resolved by this view. The source Right hand/bag fusion is a known limitation.

The first corrected final front-facing pose is a **readability blocker**: the
thigh bend and seat support are hidden, so the still looks close to standing.
This agrees with Art's independent finding. Coordinator is testing a 25-degree
seated heading with compensated root before the expensive full render. That
original frontal endpoint is provisional and must not be called approved.

Current recommendation: background reconstruction may proceed to the next scoped
review; inspect changed endpoint and exposed midpull patch, then the continuous
clip and actual compact HTML. Three key frames cannot establish motion quality,
held grasp, foot sliding, depth continuity, reset/replay or offline behavior.

## Outstanding evidence

Full motion and final compact review have not yet been supplied to QA. No
full-motion, action-control, retained-state or final interaction pass is claimed.
Owner creative acceptance and Art's final recommendation remain separate.

## Independent baked-scene audit

Read-only `build/checks/stool-interaction/qa/audit_scene.py` opened the corrected
25-degree baked scene and sampled all 157 frames at 20 fps. Result is in
`qa/scene-audit.json`; scene SHA-256
`39ef53244c8a92a3d22d0748de051a62d12c20044e7678d285fef80124f0e27e`,
pose source SHA-256
`8f56063153b9666d48ca0a673f1d3a216a92cad7e96cbcf881b7ef8b717f80ae`.
Maximum baked world bone endpoint error versus fresh authored targets was
0.0000040 m. Every evaluated body vertex was finite at every frame.

The actual body mesh reaches -0.020596 m below the floor at 5.2 seconds during
alignment (about 4 pixels at the nominal room scale). This is a concrete numerical
limitation requiring an actual 5.2-second room-view check. Start, reach and final
body minima are within 0.000001 m of floor; midpull minimum is +0.000944 m. These
checks do not prove surface grasp, butt/seat contact, clothing continuity or motion
quality, and should not be substituted for the pending visual gates.

Corrected raw `key-065.png` and 25-degree `key-156.png` were also opened. The
changed endpoint reads materially more like sitting: bent thighs, a seat beneath
the pelvis and a stool leg between the boots are visible. No new garment split
is apparent. Midpull shows the hand meeting the rim; the mitten-like source hand
does not show a detailed wrapped grip. Recommend proceeding to changed room
composites and continuous-motion review; this clears the earlier raw-silhouette
objection provisionally, not the full visual gate.

## Pre-final-render recheck

Opened corrected room composites `room-key-065.png` and `room-key-156.png`.
The vacated stool area remains intact, and the angled endpoint reads as supported
sitting with bent thighs and visible stool geometry. Recommend the motion gate.

Reran the same independent audit on the subsequent pure-Z foot-heading and
distance-based gait revision: frozen scene SHA-256
`793facec8862e2adf5f1bec5e6b1d02f99b1f77b6d8c4cbc455a53fa0d116348`,
pose SHA-256
`e6d5943d0513ac575db81b8f4c9a7a20ee6e68139dba8b8fc7975dfb9993a32c`.
157 samples remain finite; world joint maximum error remains 0.0000040 m.
The floor deficit persists: -0.0205804 m at 5.2 seconds, vertex 118 weighted
entirely to RightFoot. This clears neither the numerical floor issue nor final
motion. A likely cause to investigate is direction-only foot bone orientation
losing sole twist as the body turns against a planted boot. This is a diagnosis
proposal, not an established code defect. Current `qa/scene-audit.json` contains
this latest run, including the lowest vertex and weights at every sample.
