# Apartment puzzle tests

The suite uses Godot's own `SceneTree` runner; no external test plugin or service is required.
From the repository directory, run the import and tests together:

```sh
bash tools/check.sh
```

To run the state checks separately after import:

```sh
bash tools/godot.sh --headless --path . --script res://tests/test_opening.gd
```

The wrapper selects the installed Godot runtime and places writable configuration, cache
and user data in the project's ignored `.local/` directory, including in a sandbox with a
read-only home directory. With a normal writable desktop setup, the equivalent direct
command is `godot --headless --path . --script res://tests/test_opening.gd`.

The runner prints assertion and failure counts, prints a description for each failed assertion,
and exits with status `1` on failure (`0` on success). It does not change saved player progress.

Checks cover the complete apartment walkthrough, evidence and notebook prerequisites,
alternative document order, wrong actions that remain recoverable, repeated interactions,
save/reload at intermediate checkpoints, detached save data, strict rejection of malformed or
contradictory payloads without mutating current progress, and reproducible action sequences.
Save checks include unexpected fields, invalid item IDs and paths, duplicates, excessive
inventory data, wrong types and unsupported schema versions.

These are state-model checks. Run an exported build and play the scene to assess visible
hotspots, input, resizing, subtitle readability, music/voice balance, rendering, humour and
whether the next objective is understandable. Headless success does not establish those qualities
or prove that all security bugs are absent.
