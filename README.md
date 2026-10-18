# Maziss — The Morning After

An original, zero-budget point-and-click adventure in development. The repository is
named **Maaziss**; the protagonist is **Maziss**.

**Windows: [download, import and run the project](docs/WINDOWS_SETUP.md).** The
source is in this repository; use **Code → Download ZIP** to get a local copy.
No Python or AI tool is required to play through the Godot editor.

This is an unfinished source checkpoint. The playable Godot room still uses SVG
placeholder art. The approved painted artwork and separate HTML walking experiment
are not integrated; the owner rejected the previous walking animation and the
video-based correction is paused. See [current status](docs/PROJECT_STATUS.md),
[planned work](docs/BACKLOG.md), and [how agents are assigned](docs/AGENT_WORKFLOW.md).

Feature requests and bugs belong in [GitHub Issues](https://github.com/sminskaa/Maaziss/issues).
Future features use branches and reviewable pull requests. This source checkpoint
does not publish a standalone Windows executable or a finished game release.

This first playable increment starts in his shabby apartment on the morning after
he witnesses a murder. Search the room, use the bag/inventory, free the window, read
the leaflet and travel restriction, and choose how to investigate the Morgrave lead.
The prototype ends when he has a provisional plan. The introductory film, streets,
other characters and later escape sequence have not been built.

## Play with the free Godot editor

1. Install the standard **Godot 4.6.3** editor from its official release.
2. In Godot's Project Manager, choose **Import** and select this folder's `project.godot`.
3. Open the project and press **F5** (Run Project).

No API key, account, purchased asset, or network connection during play is required.
This is a prototype with original vector placeholder art; frame animation, music and voices
are not yet included. Basic click-to-walk movement is implemented. The visual target is illustrated late-1990s/early-2000s adventures.

## Controls

- Choose **Give, Pick up, Use, Look at, Talk to, Pull, Push, Close, or Open**, then left-click a target.
- Right-click room objects or inventory icons to examine them. Click empty floor to walk.
- The graphical inventory stays below the room. Select **Use** or **Give**, click an item icon, then its target. Use one icon with another to try a combination.
- The first room has no NPCs or useful item-to-item combination; unsupported actions give feedback and preserve your items.
- Use the strip to free the catch, **Open** the window, then **Pick up** the leaflet.
- Open **Notebook** to review what Maziss knows and choose his next thought.
- **H** reveals hotspots; **I** opens inventory; **J** opens the notebook;
  **Esc** closes a panel; **F1** shows help.
- Buttons also support **Tab**, **Shift+Tab**, **Enter** and **Space**.
- **Save** and **Load** use one local slot and a previous-save backup. Resetting the
  room does not delete the saved slot. Browser saves can disappear if site storage
  is cleared; this prototype does not yet have save export or cross-device sync.

## Cloud/Linux development

From this repository:

```sh
python3 tools/setup.py
bash tools/check.sh
bash tools/godot.sh --editor --path .
```

Setup uses Godot **4.6.3**, verifies official SHA-512 checksums when downloading a
runtime or templates, and writes only inside ignored `.local/`. It reuses matching
verified files on subsequent runs. Upstream bundles every platform's export template
in a roughly 1.2 GiB archive; setup retains only the required single-threaded web
templates after verification. Use `--native-only` to skip web templates when unneeded.

The wrapper gives Godot writable XDG data, cache and configuration directories without
modifying the machine's system installation. Local native saves are therefore under
the repository's ignored `.local/share/godot/app_userdata/` in this workflow.

## Build and check the browser version

```sh
bash tools/export_web.sh
python3 tools/serve.py --port 8060
```

The exporter creates `build/web/` and `build/maziss-opening-web.zip`. A web export must
be served over HTTP for local testing or HTTPS for distribution; double-clicking its
HTML file is insufficient. The supplied server binds only to the local machine.
The ZIP can be uploaded to a compatible static game host after a separate publication
decision. This repository does not automatically deploy or publish anything.

The browser target requires WebAssembly and WebGL 2. The current preset is single
threaded and does not need cross-origin-isolation headers. Broader browser/device
support must be tested before it is promised.

## Tests and specifications

`bash tools/check.sh` imports resources, runs the standalone Godot state-model suite,
and boots the actual scene headlessly. Godot errors fail the wrapper even if the engine
returns a zero process status. No third-party test plugin is needed.

- [Story bible](docs/STORY_BIBLE.md): established canon, chronology and open questions.
- [Opening-room design](docs/OPENING.md): interaction flow, draft script and fairness.
- [Test notes](tests/README.md): model coverage and limitations.
- [Asset notes](docs/ASSETS.md): origin and licensing status.
- [Voice recording guide](docs/VOICE_RECORDING.md): a short Maziss audition script and
  free recording workflow.
- [Free voice-generation tool](docs/VOICE_TOOL.md): isolated CPU setup, synthesis
  commands, and the remaining model-download network requirement.
- [Validation report](docs/VALIDATION.md): what has actually been run.

The model checks cannot certify visual quality, humour or real graphics performance.
The browser walkthrough additionally exercises actual input and persisted save data.
No paid tools, downloaded voices or live AI calls are part of the game.

For the optional browser walkthrough, start the web server, then run
`python3 tools/browser_smoke.py` in another terminal. It needs the free Playwright Python
package (tested here with 1.62.0) and Chromium. The test uses a fresh browser profile and
reads only its own game's saved JSON in IndexedDB; no test API is shipped in the game.


## Click-to-walk art example

Generated HTML previews are local review artifacts and are not committed or packaged.
To rebuild the separate movement study on a development machine with Python and
Pillow, run `python3 tools/build_walking_demo.py`, then open
`visual-preview/maziss-walking.html`. Its rejected animation remains a development
reference, not an approved replacement for the Godot game. See
[WALKING_DEMO.md](docs/WALKING_DEMO.md) for controls, scope and limitations.
