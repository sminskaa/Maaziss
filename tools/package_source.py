#!/usr/bin/env python3
"""Package version-controlled source; never scoop up unrelated untracked files."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = (".git/", ".godot/", ".local/", "build/", "voice-preview/",
            "visual-preview/", "attachments/", "recordings/", "private/", "docs/local/")


def main() -> None:
    names = subprocess.check_output(
        ["git", "ls-files", "--cached", "-z"], cwd=ROOT,
    ).decode().split("\0")
    target = ROOT / "build/maziss-opening-source.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    manifest = {}
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as out:
        for name in sorted(set(names)):
            if not name or name.startswith(EXCLUDED):
                continue
            if name == "docs/WALKING_FOOTAGE_INTAKE.md" or any(
                part == ".env" or part.startswith(".env.") and part != ".env.example"
                for part in Path(name).parts
            ):
                continue
            source = ROOT / name
            if source.is_symlink() or not source.resolve().is_relative_to(ROOT):
                raise ValueError(f"Refusing non-project file: {name}")
            if not source.is_file():
                raise FileNotFoundError(f"Tracked source is missing: {name}")
            data = source.read_bytes()
            manifest[name] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            out.writestr("Maziss/" + name, data)
        if "project.godot" not in manifest:
            raise ValueError("Stage the project source before packaging it")
        out.writestr("Maziss/SOURCE_MANIFEST.json", json.dumps(manifest, indent=2) + "\n")
    target.chmod(0o644)
    print(f"Created {target.relative_to(ROOT)} ({len(manifest)} source files, {target.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
