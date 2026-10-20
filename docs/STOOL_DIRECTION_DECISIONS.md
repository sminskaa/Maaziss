# Stool scene: owner storyboard feedback

Source: `private/directions/stool-storyboard-feedback-original.json`, exported
2026-10-20T18:53:03.670Z. Preserve the exact source; its comments are owner
instructions for this action, not approval of the existing rig or animation.
Original spatial direction: `private/directions/seat-at-desk-original.json`.

## Agreed intentions

1. Turn toward the desk at the starting position, then approach the stool's left
   side, within reach of the anatomical right hand.
2. Grasp the stool top with the anatomical right hand at the marked position.
3. Pull the stool back to the third mark with the hand following the seat.
5. Once seated and facing screen right, grip with the right hand and slide Maziss
   and the stool together toward the desk; desk occludes the right foot.

## Owner corrections to apply

4. Sit while facing upper right. Then, while seated, move the RIGHT foot toward
   screen right under the desk FIRST; move the LEFT foot SECOND; turn the TORSO
   and HEAD toward the desk/screen right AFTER the two foot movements. Do not
   implement simultaneous foot/torso swivel or a torso-only turn with fixed feet.
6. Move the hands to the desktop without either hand passing through the desk at
   any point. Endpoint correctness alone is insufficient; inspect the whole reach,
   including any lift, travel above the edge and placement on top. A plausible
   raised path is an implementation hypothesis, not a separately approved pose.

## Next bounded proof

Use the corrected intentions to prepare a small posed visual study of beat 4's
ordered foot/torso change and beat 6's hand approach. Show clear sequential poses
and enough intermediate samples to detect crossings before making another full
stool action. Inspect actual rendered geometry/contact and visible results.
Any existing 3D model used remains an explicitly unfinished staging model;
appearance, full animation, timing and physical contacts are NOT owner-approved.
No need for more owner videos or one file per beat. Do not ask the owner to
reapprove unchanged beats 1/2/3/5. Exact camera/depth mapping from their 2D marks
still requires fitting and visual verification, not literal 3D coordinate use.
