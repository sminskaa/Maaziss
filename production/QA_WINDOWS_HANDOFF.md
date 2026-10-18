# QA-006 — Windows source handoff review

Status: source handoff recommended for owner Windows review; native Windows launch
remains unverified. Reviewed on 18 October 2026.

Scope: a source checkpoint for the owner to import into Godot on Windows. This is
not a finished game release or approval of Maziss's animation.

## Checks completed

- `project.godot` names the existing `scenes/main.tscn` entry scene, uses Godot 4.6
  features and the GL Compatibility renderer. The documented engine pin is 4.6.3.
- The entry scene attaches `scripts/main.gd`; its SVG room/character references and
  JSON dialogue use portable `res://` paths. No shell wrapper is required to import
  or run the project using the Windows Godot editor.
- Save storage uses Godot's local `user://` location. Source inspection found no
  HTTP client, HTTP request or process-execution calls in the game scripts.
- Current export configuration is Web only. Importing and pressing F5 in the Windows
  editor does not require a Windows export preset or export templates. A standalone
  Windows executable has not been prepared or validated in this handoff.
- The actual game currently loads vector placeholders. The richer painted artwork
  and rejected walking studies are separate development assets/prototypes.
- Owner footage lives outside this repository under `/workspace/attachments`.
  Model environments and generated analysis live in ignored `.local/` and `build/`.
- Reviewed `docs/WINDOWS_SETUP.md`, `docs/PROJECT_STATUS.md`, `docs/BACKLOG.md`, README
  and the GitHub issue templates. Import/F5 instructions, no-Python requirement,
  placeholder-art warning, separate rejected walking study and Windows-test limits
  accurately describe the existing project. The suggested sofa/window interaction
  sequence agrees with `scripts/game_state.gd`.

## Actual source archive audit

Inspected `build/maziss-opening-source.zip`: 9,505,699 bytes, 94 source files plus
`SOURCE_MANIFEST.json`. Audit candidate SHA-256:

`2b0a68695084b7a4504aa6c668cb86c3bfad7eae4d07154cdf5c763f3fe0b12d`

This identifies the audited candidate before this report's final update. Rebuilding
the archive to include the updated report or board necessarily changes that hash.

- All 95 paths are relative under `Maziss/`; no absolute paths, parent traversal or
  duplicate names were found. Every source entry matches its manifest byte count
  and SHA-256 hash.
- Required project, scene, scripts, dialogue, SVG assets and Windows/status/backlog
  documentation are present.
- No personal audio/video, model-weight formats, nested archives, Python bytecode,
  `.env` files, `.git`, `.godot`, `.local`, build output, preview directories,
  recordings, attachments or private directories were found in the actual ZIP.
- The private intake note containing personal-recording filenames and workspace
  paths is excluded. The Git index contains 94 explicitly curated files.
- The revised helper uses tracked paths only, hard exclusions, symlink rejection
  and missing-file failure. Untracked personal files are no longer swept into the
  source archive. This is a focused audit, not a guarantee against every possible
  sensitive string or malicious future change.

## Validation limits

- Native Windows execution is unavailable in this cloud machine. Linux headless
  import/model/startup checks cannot establish Windows graphics, input or audio
  compatibility. The owner must perform the first Windows editor launch.
- The coordinator reports the existing Linux `tools/check.sh` checks passed and is
  separately validating a fresh archive extraction. QA did not rerun broad model
  tests for documentation/packaging changes.
- No standalone Windows executable, Windows native run, finished graphics review or
  animation approval is implied by this handoff recommendation.

No blocking archive/privacy/instruction issue was found in the audited candidate.
Proceed with the source checkpoint and the owner's first Windows import/play check.
Keep the unapproved painted animation as a separate task.

No source files were changed by QA; this report is the only assigned output.
