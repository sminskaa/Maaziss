# Story bible

Status: compact record of user-established facts, followed by open questions. Detailed wording, extra locations and dialogue in prototype documents are proposals until accepted. The protagonist's name is **Maziss**; the repository is currently named `Maaziss`.

## World and intended experience

- Original heroic-fantasy world on a planet colonized by humans hundreds of thousands of years ago.
- Contact with the rest of humanity has been lost because the galactic portal no longer works.
- Much advanced technology is unusable. Some surviving technology is treated as magic. Most people nevertheless know that humans arrived aboard spacecraft and once possessed advanced technology.
- Societies vary: monarchies, dictatorships, guild cities, republics, anarchist societies and others. The current city's specific constitution and name are not yet established here.
- The protagonist comes from a corrupt, crowded city with some of the social energy of Ankh-Morpork. The setting, names, characters, images and dialogue are our own; references are creative influences, not shared canon.
- Intended presentation: painted cartoon point-and-click inspired by late-1990s/early-2000s adventures, with exaggerated architecture and characters, rich colour, graphical inventory, dialogue choices, and nine explicit verbs: Give, Pick up, Use, Look at, Talk to, Pull, Push, Close and Open. Few standalone arrangement puzzles. See ART_DIRECTION.md.
- Intended audience: adults around 30–50 in Europe. English is the current game language.
- Tone: dark humour, provocative dialogue, absurdity and Kafka-like institutional logic. French news/history and European/US politics and economics are research material for original satire. Comedy must coexist with coherent motivations, danger and a comprehensible story.
- Production has no additional budget. Paid tools, bought assets, subscriptions and chargeable services are not assumed.
- Confirmed delivery target: a locally installed desktop game, fully playable without internet. Godot is the main engine; HTML is for interim review. Required art, dialogue and generated speech must ship with the game; saves are local and no runtime AI/server/login dependency is required. Desktop operating-system targets remain open.

## Maziss

- An outcast living in the city; broke and careless, with mild drinking rather than an established severe addiction.
- Works at unlicensed odd jobs involving maintenance, electronics and scrap. He has useful practical knowledge; he is not merely incompetent comic relief.
- Knows many people through these jobs but has no close friends. Do not invent a trusted friend or confidant to supply the next story step.
- His city departure is restricted while an administrative decision about his illegal scrap activity is pending.
- He previously attempted to bribe officer **Smot**. Smot is upright and did not accept. The attempted bribe is not established as part of the scrap case. The existence of corrupt police elsewhere does not make Smot secretly corrupt.
- Self-preservation drives his attempted escape. He is willing to consider bribes and bypasses; he has not committed himself to following a lawful route or obtaining permission.

## Geography

- The river flows from east to west, with islands in it.
- The wealthy woman's home is in the west; the expensive bar is in the south; Maziss's apartment is in the northeast.
- Multiple bridges matter to his return route. On a detour he approaches a different bridge and sees the murder across the street near its stairs. Do not replace this geography with an alley encounter.

## Confirmed recent chronology

1. A moving job for a wealthy woman in the western part of the city brings Maziss a tip.
2. He goes to an expensive bar in the south and is expelled.
3. Returning toward his apartment in the northeast, he makes a detour toward a different bridge. Daylight is fading, but it is **not yet dark**.
4. Across the street, near the bridge stairs, he sees **three men stabbing a fourth man**. They see Maziss.
5. The three men leave almost at a run through a side street, in the opposite direction. They do **not** chase him.
6. Drunk and tired, Maziss returns home and sleeps.
7. In the morning he realizes that he must leave the city before something bad happens to him.

A visiting delegation from a foreign river city has increased the presence of guards. Its origin, political purpose, itinerary and connection, if any, to the murder are not established.

These events are intended for a later introductory film. The first playable increment begins in the apartment; it does not implement the film or introduce new witnesses to these events.

## Apartment opening

- A sofa and backache provide a clue to hidden scrap metal.
- A metal strip helps Maziss free/open a jammed window.
- Opening the window frees a paper announcing a Morgrave job-fair lead: paid work outside the city, with transport included.
- **Morgrave is a name attached to this lead. Its identity and location are unresolved.** Do not convert it into a second city, a named employer, a noble, or an established destination without further story direction.
- The prototype stages catch release, opening, paper collection and inventory reading as separate actions. The desk notice supplies the travel restriction; the journal compares the documents, considers the obstacle and records the decision to investigate Morgrave. These are implementation choices around the established opening.
- The first room ends with a provisional plan. Included transport is an advertised opportunity, not a guaranteed way through the restriction. A gate scene, route out, permission request or actual escape is not established by this room.

Physical staging, proposed English lines, editorial references and room acceptance checks are in [OPENING.md](OPENING.md).

## Guardrails for later writing

- Maziss's fear is reasonable from his perspective. It does not establish that the murderers have identified his address, work for the authorities, or intend to hunt him.
- The victim's identity, the killers' identities, their motives, and any larger conspiracy are unknown.
- Do not merge the administrative scrap case, foreign delegation and murder into a confirmed conspiracy merely because they occur near one another.
- Do not convert the travel restriction into an instruction that Maziss must act lawfully. He needs to understand the obstacle and survive; later opportunities can involve persuasion, bribery, evasion or other practical choices consistent with the user's direction.
- Preserve Smot's integrity and allow individuals to differ from their institution. A corrupt setting does not require identical cynical motives for everyone.
- Ancient technology has not been given unlimited capabilities. Record a specific object's capabilities and limitations before using it to solve a plot or puzzle problem.
- Distinguish designer truth, public belief and each character's knowledge. Characters cannot react to information they have not learned. In particular, Maziss has no evidence that the killers intend to leave the city; do not write a departure-permit joke based on that assumption.
- Political and historical research records source facts separately from fictional exaggeration. Original characters need personal wants, fears and contradictions beyond representing an opinion.

## Questions deliberately left open

City and district names; Maziss's age, appearance and longer personal history; Smot's wider role; murder identities and motive; the delegation's details; Morgrave's identity/location; the route to the job fair; the nature of the offered work; and the eventual escape route.

These questions do not prevent implementing the apartment. Keep them open rather than silently filling them with new canon.
