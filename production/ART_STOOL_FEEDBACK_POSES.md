# ART-FEEDBACK-POSE — actual-image review

**Result: A is useful for limited owner direction review; B remains HOLD.**
20 October 2026. No final aesthetic, complete-clearance, contact or motion approval.
The owner retains creative authority. Existing character art remains unfinished
and unapproved; this is two isolated posed studies, not the full stool action or
Godot integration.

## Current evidence inspected

ART opened the actual final `build/checks/stool-feedback/review-contact-sheet.jpg`:
all nine paired room composites and opaque-desk diagnostic captures, A1–A4 and
B1–B5. ART also opened current full-resolution `diagnostic-450.png`,
`diagnostic-600.png` and `room-600.jpg`. Current source SHA-256 from manifest:
`5c809b5247a61f1cac43230e6976d2c8ebda0569c76af6131b7de6676e29b64d`.
The neutral diagnostic desk is real fitted geometry for depth inspection, not
replacement painted room art. The current room composites show the same poses
against the actual painted room.

An earlier candidate was separately inspected at all rendered key samples and
compared directly with `art/proposals/apartment-cartoon-v2.png` and
`art/walking/maziss-side-atlas.png`. Earlier private ART contact sheets/crops in
`build/checks/stool-feedback/art/` are **superseded**; they retain the earlier
`fa7e88…` candidate and must not be mistaken for current evidence.

## A — ordered feet, then torso/head

A1–A2 visibly moves the near/anatomical-right boot toward screen right while the
upper body remains diagonal/back-facing. A2–A3 then brings the far/left boot into
its separate position while the upper body retains that facing. A3–A4 turns the
torso and head to the right-facing profile. This makes the requested right,
left, then torso/head order readable in the room as well as the diagnostic view.
The seated body remains associated with the same visible stool.

Recommend these four poses for **limited direction review**. Sparse stills do not
establish the quality of every in-between, precise foot grounding or comfortable
seated mechanics. They do not approve the model or complete action.

## B — hand approach remains blocked

- B1–B2 separates the below-edge withdrawal from the lift. B3 then lifts outside
  the edge, B4 brings the hands forward above the tabletop and B5 lowers them.
  The broad intended route is more explicit than the previous candidate.
- **B3 still has an unnatural backward/outward flare.** At full-resolution 450,
  the visible forearm turns back beside the bag and the oversized upturned palm
  faces outward. The pose reads as a sideways/rearward gesture rather than a
  relaxed lift toward work. The earlier hand-near-head extreme is reduced, but
  this is not finished reach choreography.
- **B4–B5 keep the elbows conspicuously high and out.** The arms arch over the
  desk and the thick hands remain curved/mitten-like; they do not read as relaxed
  palms and fingers resting on the surface. The current alternate camera exposes
  both hands better than the earlier candidate, which is useful evidence.
- The tabletop hides enough boundary surface that room images alone cannot
  establish absence of intersection. QA's current evaluated-triangle review
  reports three remaining left torso/sleeve-to-arm boundary triangles entering
  the slab late in placement. ART does not override that failure because the
  small overlap is difficult to see in the room composition.
- QA also reports core hand clearance at the endpoint of approximately 4.925 mm
  above the tabletop. Clearance is not resting contact. The rendered thick,
  curved hand silhouettes do not supply convincing palm contact either.
- The bag remains a coarse, angular hanging shape with stretched-looking folds
  during the arm poses. This is an appearance/deformation concern separate from
  the desk-intersection test.

Next bounded correction: repair the left sleeve/torso boundary deformation,
then lower and guide the elbows forward with a readable palm-down hand shape
and a real relaxed tabletop endpoint. Recheck the whole resulting route against
actual evaluated surfaces and actual room images. Do not hide the failing skin
triangles with narrower weight filters. This is a correction brief, not approval
of a particular new lift pose; no further iteration was performed by ART.

## Original-drawing mismatch and room fit

The room preserves the painted setting, but the current smooth, pale, softly
shaded character remains visibly separate from its deliberate warm/cool colours,
ink contours and textured surfaces. Teal jacket, ochre shirt, brown satchel and
boots communicate the costume; they do not reproduce the original's adult angular
face, expressive brows/eyes, nose/jaw profile, purposeful hair locks or drawn hand
anatomy. The jacket lacks the original's tailoring, pockets, wear and texture;
boots lack laces and material detail. No likeness or finished-room-coherence pass
is claimed. These are substantive appearance tasks, not solved by pose ordering.

## Scope and changes

Recommend A only for owner feedback on the corrected ordering. Hold B for both
remaining deformation/contact defects and unnatural arm acting. Do not present
this as a finished full action, motion-timing pass or production-art approval.
The transition between A and B is a separate test cut to the desk position; an
occupied slide was not authored or reviewed here.

ART changed this report only and created earlier private image sheets/crops.
No code, model, original artwork, full sequence or Godot content was changed.
Companion evidence: `production/QA_STOOL_FEEDBACK_POSES.md`.
