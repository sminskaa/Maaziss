# Asset record

The current room, character and application icon are original SVG illustrations
authored as source for this prototype. They contain no embedded fonts, external image
links or commercial-game assets. Their deliberately limited animation and flat-vector
finish are provisional. The owner has requested a more exaggerated painted-cartoon
direction; see [ART_DIRECTION.md](ART_DIRECTION.md).

| File | Origin | Status |
| --- | --- | --- |
| `assets/room.svg` | Original code-authored apartment illustration | Used in prototype |
| `assets/maziss.svg` | Original code-authored Maziss character | Used in prototype |
| `assets/icon.svg` | Original monogram application icon | Used in prototype |
| `assets/items/*.svg` | Original code-authored inventory illustrations | Used in persistent inventory |
| `art/proposals/apartment-cartoon-v1.png` | AI-generated original art proposal, revised using OpenAI image generation | For owner review; excluded from playable export |

The game uses Godot's built-in fonts. Godot and bundled third-party components retain
their own licences; engine notices are retained with the web build. The game itself
has not been assigned a public open-source licence merely because its engine is MIT.

No online voice clip, music track, paid asset or generated speech is included. Before
adding third-party audio, record the exact source, creator, licence/version, edit and
credit requirement. A free download alone does not establish editing/redistribution
permission or permission to clone a speaker.


The separate movement study uses `art/walking/apartment-background.png`,
`maziss-side-atlas.png`, and `maziss-depth-atlas.png`, edited/generated with OpenAI
image generation from the approved original v2 composition. Source PNGs are retained.
These are first-pass room/animation assets for the offline walking example, excluded
from Godot import by `art/.gdignore`. See WALKING_DEMO.md for provenance and limits.

Revision 2 walking uses `art/walking/maziss-rig-parts.png`, generated from the approved
reference as upright body and leg/boot components. Runtime texture sampling and
articulated bone rendering replace the rejected whole-figure pose loop. Earlier
atlases are retained as source history, not approved final animation.
