# First-room validation

Validated on 17 October 2026 in the cloud workspace. This is an internal prototype
ready for creative review, not a production release or a claim that every defect is
absent.

## Executed checks

| Check | Result |
| --- | --- |
| Godot runtime | 4.6.3 stable, official release; private runtime and web-template archives verified against upstream SHA-512 values |
| Repeatable setup | Re-running `python3 tools/setup.py` reuses the matching runtime and verified single-thread web templates |
| Resource import | Completed without script or resource errors |
| Native headless scene startup | Actual main scene boots without script/runtime errors |
| State-model suite | 2,505 assertions, zero failures; process exit status 0 |
| Web release export | Successful, single-threaded Compatibility renderer build |
| Chromium walkthrough | 19 end-to-end checks passed, zero JavaScript/Godot console errors |
| Real browser persistence | Visible Save/Load, intermediate checkpoint restoration, full-page reload and corrupted-primary fallback to an actual previous valid backup passed |
| Visual inspection | Reviewed actual opening, leaflet, completion and 960×720 resized-notebook screenshots; text is readable, panels scroll, room fits with letterboxing |

The browser run used Chromium 154.0.8037.57 with software WebGL (SwiftShader), a fresh
isolated profile and the actual exported canvas. It clicked real controls and read the
game's own persisted JSON from IndexedDB; there is no shipped test hook or mock state.
Corruption checks modify only that test profile. The backup is an earlier valid save,
not a guarantee of recovering the latest unsynchronised browser writes.

The state suite covers prerequisites, alternate order, wrong actions, item retention,
repeat interactions, continued progress after restoring intermediate checkpoints,
detached save data, unknown IDs, contradictory flags, excessive inventory payloads,
wrong types and unsupported schema versions. The disk-backed save store additionally
received isolated native write/load/corrupt-primary/backup-recovery smoke checks.

## Cartoon direction and verb-interface increment

The owner supplied additional visual references and specified nine verbs and mouse
shortcuts. The state suite and real browser walkthrough were updated to exercise
separate Pick up/Open/Use actions, closing/reopening without item loss, safe inventory
combination attempts, unsupported-verb feedback, and visible floor movement. Existing
save/reload and corrupt-primary recovery checks still pass. The assertion total changed
because the deterministic random sequence now samples all verbs; tests still exercise
160 action steps and validate every resulting state and save.

A new painted-cartoon apartment proposal is stored under `art/proposals/` for owner
review. It is not the shipped room background; the playable room still uses the SVG
placeholder. The proposal and private voice-preview pages are excluded from game
exports; private voice-preview pages are also excluded from source bundles.

## Reproduce

```sh
python3 tools/setup.py
bash tools/check.sh
bash tools/export_web.sh
python3 tools/serve.py --port 8060
```

In another terminal:

```sh
python3 tools/browser_smoke.py
```

The optional browser suite requires Playwright (tested with Python package 1.62.0) and
Chromium. Its current-run evidence is written to `build/checks/browser-results.json`
and screenshots in `build/checks/`. These generated files are ignored by Git.

## Unrun or unfinished

- No human playtest has certified that the dialogue is funny, the character feels right
  or the clue chain is enjoyable.
- The owner's voice auditions are stored separately; no music or speech is integrated
  into the playable build.
- No introductory film, character walking frame animation, streets or next encounter is built. Basic floor movement of the placeholder sprite is implemented.
- No Firefox, real Safari, Windows, macOS, mobile or real-GPU performance certification.
- No claim of a tested 60 fps or memory budget based on this software-rendered cloud run.
- Browser save export/import and cross-device sync are not implemented.
- No public deployment, store submission, signing certificate purchase or paid service.

## Subsequent voice-tool check

After the owner applied the environment network changes, Chatterbox Nano downloaded
successfully. The official pinned model declares MIT; a new sentence generated locally
from the owner's reference in 33.39 seconds including model loading. The resulting
4.88-second, 24 kHz mono PCM16 WAV is finite and non-silent. See
[VOICE_TOOL.md](VOICE_TOOL.md) for reproducible commands and the exact revision.

This validates the separate development-time speech tool. The playable game itself
still contains no voice clips. The owner accepted the sample voice but rejected its departure-permit joke because it
assumed the killers intended to leave. Later lines must respect character knowledge; no new first-room platform/performance
claims follow from this speech test.

QA result: **go for owner review of the first apartment prototype**. Public-release
readiness remains a separate decision after platform, accessibility, licence, quality
and performance gates are established and met.


## Windows source handoff checkpoint — 18 October 2026

Re-ran the existing Linux Godot import, 2,505 state assertions and native headless
scene startup successfully. Independently unpacked the curated source ZIP into a
fresh temporary folder and repeated import, all 2,505 assertions and scene startup;
no Godot errors were reported. Archive entries were checked against SHA-256/size
metadata and exclusions for personal recordings, models, caches and previews.

The independent source/package/instruction audit is
`production/QA_WINDOWS_HANDOFF.md`. The official release API confirms the documented
Godot4.6.3 standard Windows64 editor asset exists. These checks validate a source
handoff; native Windows rendering/input/save behavior still requires the owner's
PC test in GitHub issue1. No standalone Windows executable or release was created.
