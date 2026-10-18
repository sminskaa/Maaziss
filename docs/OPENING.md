# Opening: Maziss's apartment

Status: first-room design and **proposed English script**, not a replacement for the user's story. Confirmed background is recorded in [STORY_BIBLE.md](STORY_BIBLE.md). The opening film and the following locations are future work.

## Purpose and boundaries

Give the player a small, fair interaction sequence while establishing that Maziss is frightened, broke, untidy, and practically capable. The immediate discovery is a possible way to leave the city: a job-fair leaflet mentioning Morgrave, paid work outside the city, and included transport. He compares this opportunity with his existing travel restriction, then decides to investigate. The room ends with that provisional plan.

Aim for about five minutes on a first visit, including looking around and reading. Do not stretch the sequence with timed actions or a standalone arrangement puzzle. The staged actions are finding scrap, freeing the window catch, opening the window, collecting and reading the leaflet, reading the desk notice, and thinking through the two documents in the journal. Each interaction changes the visible state or supplies information. There is no NPC meeting, street exploration, gate crossing, or implemented murder/intro scene in this increment.

The player should be able to explore in any order, repeat observations, inspect the tool, and recover an explicit hint. No action destroys an essential object. The ending is a lead, not a secured job, actual escape, or administrative exemption. Maziss's priority is self-preservation: a bribe, bypass, deception or legitimate opportunity may be useful later. The player is considering an obstacle, not pledging to obey it or seek permission.

## Canon and proposed staging

**Confirmed:** Maziss wakes in his apartment the morning after witnessing the murder. He realizes that he must flee. The sofa/backache points toward hidden scrap metal; that metal helps open a jammed window; opening the window frees a paper advertising the job-fair opportunity. Morgrave's identity and exact location are not established.

**Proposed physical staging:**

- Maziss slept on a worn sofa. A short, rigid strip of scrap steel is trapped under the cushion, producing the uncomfortable lump. Its exposed edge gives the player something to notice.
- The small window has a catch stuck beneath hardened paint. The strip slips beneath the catch and breaks the paint holding it. This **frees the catch but leaves the window shut**. With the strip put away, an explicit **Open window** action opens it by hand.
- A folded printed leaflet is caught in the inner frame, with a paper corner visible from the room. Opening the window releases it onto the **inside** sill. The next **Pick up leaflet** action collects it. Reading it is a separate inventory inspection. The paper never falls somewhere unreachable.
- The leaflet's arrival and who put it there remain unconfirmed. Treat it as an ordinary piece of advertising; the prototype should not announce a secret sender or manufacture a mystery around it.

These are implementation proposals. Keep the obstruction, tool and visible action mechanically consistent. The painted catch is the only obstruction; do not add a hidden latch or another required item. The travel notice is on the desk and can be read by looking at the desk. Picking up the notice also places the notice in the inventory; collecting it is optional for forming the plan.

## Play flow and script references

References below are editorial IDs; runtime state names and journal choice IDs are identified separately. All lines are drafts for human review, not a claim that these exact words are all present in the build. Maziss speaks to himself sparingly; not every interaction needs a joke.

| Reference | Trigger / state | Proposed text or action |
| --- | --- | --- |
| `opening.start` | First entry | “Three of them. They saw me watching. I need to get out of the city before somebody decides I'm evidence.” |
| `opening.goal` | Initial objective | **Find a way to leave the city.** |
| `sofa.inspect.before` | Examine sofa before taking scrap | “Something hard under the cushion. That explains my back.” Visually indicate the raised cushion/metal edge. |
| `sofa.scrap.discover` | Pick up loose metal / search cushion | Reveal and collect the short metal strip in this action. “Scrap. I really must stop sorting it in my sleep.” Add **Metal strip** to inventory once. |
| `sofa.inspect.after` | Examine after taking scrap | “One improvement to the flat. Nobody tell the landlord.” |
| `strip.inspect` | Inventory examination | “Rigid enough to scrape with. Thin enough to get into a narrow gap.” |
| `window.inspect.before` | Examine closed window | “The catch's painted stuck. And there's paper caught in the frame.” Clearly show both details. |
| `window.open.without.strip` | Try to open by hand before freeing catch | “Jammed. I need something thin under that paint.” |
| `strip.use.window` | Use strip on closed window | Free painted catch; leave window shut. Keep strip in inventory. “The catch moves. Now I can open it.” |
| `window.open` | Put strip away; Open window | Open window by hand. Leaflet drops onto inside sill. “Advertising. There's no keeping it out.” |
| `window.inspect.after` | Examine open window | “Air. At least they haven't found a way to charge me for that.” |
| `leaflet.collect` | Pick up leaflet on inside sill | Collect **Morgrave leaflet** from sill; it is now inspectable in the bag. “Morgrave. Better read the rest.” |
| `leaflet.read` | Inspect leaflet in bag | Present the full, legible leaflet copy below. Keep it available for rereading. |
| `leaflet.reaction` | After reading | “Outside the city. Transport included. I can pretend to be employable for that long.” |
| `desk.notice.read` | Inspect or Use desk, at any point | Read the pending scrap-case travel restriction. “Still pending. Of course. A person can die waiting for a form; the form itself enjoys excellent health.” |
| `journal.compare` | Both documents read; choose `compare_documents` | “Paid work outside the city, with a ride included. The notice says I'm not allowed to leave. Those are the facts.” |
| `journal.restriction` | Then choose `check_restriction` | “The leaflet doesn't cancel the ban. I need to know how they move people, and who's likely to check.” |
| `journal.plan` | Then choose `investigate_morgrave` | “Morgrave first. Find out about the work and the transport. Then work out which guard, rule or fence is between me and leaving.” |
| `opening.complete` | Provisional plan formed | Record the plan to investigate the Morgrave lead. Remain in the apartment, with documents and journal still accessible. No gate encounter or escape occurs. |

Proposed leaflet copy, with no invented address or identity for Morgrave:

> **MORGRAVE — JOB FAIR**  
> **PAID WORK OUTSIDE THE CITY**  
> **TRANSPORT INCLUDED**

The leaflet must state all three useful facts directly: job fair, paid work outside the city, transport included. A joke, distressed font, tiny print or automatic dismissal must not obscure them. The restriction is a practical complication; the advertisement neither lifts it nor establishes whether Maziss could bypass it. Later story work will establish where he pursues the lead and which methods are possible.

Optional observations to test tone without adding required puzzles:

- Empty bottle: “Empty. I checked last night. Thoroughly.” This establishes mild drinking without requiring an intoxication mechanic.
- Repair bench: “Other people's broken things. Mine are apparently a lifestyle.” Useful evidence of his work; avoid introducing another collectible here.
- Door, before the lead: “I need somewhere to go. Wandering past the guards looking guilty is something I've already mastered.” This is hesitation, not a newly invented physical lock or proof the guards are seeking him for murder.
- Door, after forming the plan: “Morgrave, then. I'll find out what it takes.” The room remains explorable; the prototype ends without inventing the next encounter or committing him to requesting official permission.

## Hints and fairness

Clues exist in the observations **before** a hint is requested. An optional hint control can progressively offer:

1. “That lump in the sofa might be worth investigating.”
2. “The window catch is painted stuck. Something thin and rigid could free it.”
3. “Pick up the metal beneath the sofa cushion. Use the strip with the window, then Open the window. Pick up the leaflet; Look at it in the bag.”

Advance hints with the state: once the strip is collected, skip the sofa. Once the catch is free, say to open the window by hand. Once open, point to collecting the paper. Once collected, point to inspecting it in the bag. Once read, point to the desk notice if needed, then to the journal's document comparison, consideration of the restriction, and decision to investigate. Repeating Pick up after collecting the leaflet never grants another copy. After collection, Close and Open can shut and reopen the window without losing items.

The uncomfortable sofa, strip shape, painted catch and trapped paper should be readable at ordinary play size. Mouse-over labels support discovery. Do not rely on spotting an unlabelled single pixel or a sound cue alone. Expose an inventory description and make the leaflet readable separately from the background art. The UI must make putting away a selected item clear; otherwise the player may unknowingly repeat the strip action instead of opening the window.

## State and validation contract

The implemented state distinguishes `strip_found`, `window_unjammed`, `window_open`, `leaflet_collected`, `leaflet_read`, `restriction_read`, `plan_started`, `route_questioned`, and `plan_formed`. Observation flags and optional notice collection support these. The journal steps are `compare_documents`, `check_restriction`, then `investigate_morgrave`. Neither reading the leaflet alone nor simply collecting both papers completes the room. Save state and reconstruct matching room, inventory, documents, journal and choices when loading.

Acceptance checks for this room:

- From a fresh start, the player can reach the leaflet and form the provisional plan through the described interactions; each physical cause is visible.
- Inspecting the window first, inspecting the sofa first, or requesting hints does not block progress.
- The strip is granted once. Repeated interactions create no duplicate item or leaflet.
- The strip frees the catch without opening the window. A subsequent Use opens it; another Use collects the leaflet. Each completed action stays completed.
- The leaflet is reachable inside the room, readable, dismissible and rereadable. It contains all three confirmed opportunity details.
- The desk is readable before or after the leaflet. Reading the desk notice is sufficient; collecting it is optional. The journal advances only after both documents are read and through all three reasoning steps.
- The final plan considers the ban without declaring that Maziss must obey it, get permission, or confine himself to a lawful route. It does not pretend included transport automatically cancels the ban.
- Saving and reloading before collecting the strip, after freeing the catch, after opening the window, after collecting/reading the leaflet, and through the journal choices restores the matching room, inventory and objective.
- Full text is available without audio or fast reactions. Repeated observation and unfamiliar item combinations do not punish the player.
- Nothing claims that Morgrave is another city, explains the murder, makes Smot corrupt, or establishes that the murderers are actively pursuing Maziss. Any recollection refers to **three** men across the street near bridge stairs; it does not move the murder into an alley.
- This draft's lines remain candidates: playtesting should check natural delivery, brevity, fear beneath the jokes, and whether the opening feels like Maziss rather than an uninterrupted stream of generic quips.


## Updated interaction contract

The nine-verb interface and art direction are specified in [ART_DIRECTION.md](ART_DIRECTION.md). Pick up is separate from Use and Open. There are distinct loose-strip and loose-leaflet hotspots, persistent inventory icons, right-click examination, safe inventory combination attempts, and basic floor movement. No NPC conversation or successful inventory-to-inventory combination is invented for this room.
