# ART-001 — Approved visual baseline review

Role: Art director. Scope: review and next-increment brief only.

## Owner-approved direction

Use `art/proposals/apartment-cartoon-v2.png` as the preserved visual starting point.
The owner approved its painted cartoon look, rich colour, texture and lighting, with
Maziss visible and the door/window straighter than the earlier version.

The image shows the traits to carry forward: expressive ink contours, warm amber
interior light against turquoise city light, worn red upholstery, handmade timber,
repair clutter, and dark foreground shapes framing the room. The mostly straight
door and window frames can retain modest drawing irregularity. Do not restore the
extreme curved frames or replace this direction with the earlier flat-vector look.

Maziss's visible pose establishes a useful scale and silhouette in the room. It does
not settle every character detail: the story bible still leaves his age and detailed
appearance open. The city skyline, incidental skull and individual gadgets are
visual suggestions, not new plot facts or established technology capabilities.

## What still needs production work

This is one composed image. Maziss, furniture, shadows and the window are painted
together. It is not yet a clean background plus independently movable character,
foreground layers, inventory icons, or open/closed window states. A character cut
from the image would leave missing room detail behind him, and one pose does not
provide walking or interaction animation. The composition's presence does not mean
it has replaced the playable room's placeholder assets.

The metal strip, window catch and loose leaflet must become easy to identify at
the actual game display size. Decorative detail alone does not prove this. The
lower floor also needs a layout check with the nine-verb panel and inventory shown.

## Proposed next increment — one production-ready room layout proof

These are Art Director suggestions, not newly approved canon or completed work:

1. Preserve v2 unchanged. Make a separate clean background with the room behind
   Maziss reconstructed, keeping the accepted framing, palette and furniture.
2. Prepare one transparent full-body Maziss idle sprite at the approved scene scale.
   Add a small front/side/back reference sheet to resolve clothing and proportions
   consistently before attempting a walking cycle. Keep design questions explicit.
3. Separate only what this opening needs: a foreground mask for overlap, the window
   in closed/open states, the catch, the loose leaflet, and the sofa search area.
   Supply a readable metal-strip icon and leaflet icon. Avoid splitting every prop.
4. Assemble a static room mock-up with the character and existing verb/inventory
   panel. Mark the intended floor path and interactive areas in a separate review
   overlay. This is a layout proof, not a promise of finished navigation or animation.
5. Deliver a self-contained HTML review containing the complete scene and close-ups
   of the interactive objects. The owner can view HTML previews; inline chat image
   delivery remains unreliable. Do not treat an internal render as delivery proof.

This increment excludes other rooms, a full walk cycle, new story facts, dialogue,
voice work and game-code replacement. A subsequent increment can integrate approved
layers and produce animation once character proportions and room readability hold up.

## Acceptance criteria for that increment

- Original v2 stays unchanged; the proposed scene retains its colour, lighting,
  expressive outlines and restrained door/window geometry.
- The clean background has no baked-in Maziss or visible removal holes. His separate
  sprite has clean transparency and convincing floor contact at the shown scale.
- Closed/open window states align with the same frame. Catch and leaflet states
  support the established sequence without implying extra items or story events.
- Sofa, desk notice, catch, leaflet and strip are distinguishable in a preview at
  gameplay size, with the verb panel and inventory visible. Owner feedback settles
  subjective clarity; a beautiful full-size image alone is insufficient evidence.
- The layer list states each asset's purpose, dimensions, alignment and overlap;
  proposed walkable space does not visibly cross furniture.
- The character reference sheet stays consistent with the visible baseline and
  explicitly flags unresolved design choices for owner review.
- The HTML package includes the images, uses readable files/traversable folders,
  and the owner confirms it opens. No dependence on a working chat image preview.

## Evidence and limits

Reviewed `AGENTS.md`, `agents/ROLES.md`, `docs/ART_DIRECTION.md`,
`docs/STORY_BIBLE.md`, and the ART-001 brief in `production/agent-board.json`.
Inspected the actual v2 image with the image viewer. Changed only this review file;
no artwork, game assets, game code or task-board status changed. No gameplay tests
were run, and this review does not verify animation, asset separation, playability
or delivery through the owner's interface.
