#!/usr/bin/env python3
"""Prepare the pinned Linux cloud tools without changing system directories.

Official release SHA-512 values were retrieved from the release's SHA512-SUMS.txt.
Keep verification enabled. The archive is large because upstream bundles all export
platforms; only web templates are retained after the verified extraction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "4.6.3"
RELEASE = "https://github.com/godotengine/godot-builds/releases/download/4.6.3-stable/"
ARCHIVES = {
    "engine": (
        "Godot_v4.6.3-stable_linux.x86_64.zip",
        "a035258da32b77f966a5376f9fa29c30a6adde826a85ba918e1605bd1fc9823eba7d85f1dd5e748956bd2ba72827c0025ffa11bb82aec91128c407a2e723c99c",
    ),
    "templates": (
        "Godot_v4.6.3-stable_export_templates.tpz",
        "da606b61c10157844f8300172df374472665f95015495cb1a7cd132c40ede404faa96cc1016a4b9662db9909ddea69632c4948b2cd11163438dad4808881fb68",
    ),
}
TEMPLATE_NAMES = ("web_nothreads_debug.zip", "web_nothreads_release.zip")


def digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as src:
        for chunk in iter(lambda: src.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_verified(kind: str) -> Path:
    filename, expected = ARCHIVES[kind]
    target = ROOT / ".local/cache" / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and digest(target, "sha512") == expected:
        print(f"Reusing verified {filename}", flush=True)
        return target
    partial = target.with_suffix(target.suffix + ".part")
    print(f"Downloading official {filename} (TLS and SHA-512 verification enabled)", flush=True)
    try:
        with urllib.request.urlopen(RELEASE + filename, timeout=60) as response, partial.open("wb") as out:
            total = int(response.headers.get("Content-Length", 0))
            read = 0
            next_report = 100 * 1024 * 1024
            for chunk in iter(lambda: response.read(4 * 1024 * 1024), b""):
                out.write(chunk)
                read += len(chunk)
                if read >= next_report:
                    print(f"  {read // (1024 * 1024)} / {total // (1024 * 1024)} MiB", flush=True)
                    next_report += 100 * 1024 * 1024
        if digest(partial, "sha512") != expected:
            raise RuntimeError(f"SHA-512 verification failed for {filename}; artifact not used")
        partial.replace(target)
        return target
    except BaseException:
        partial.unlink(missing_ok=True)
        raise


def engine_version(binary: str) -> str:
    return subprocess.check_output([binary, "--version"], text=True, stderr=subprocess.DEVNULL).strip()


def ensure_engine(force_local: bool) -> None:
    local_binary = ROOT / ".local/bin/godot"
    candidate = str(local_binary) if local_binary.exists() else shutil.which("godot") or shutil.which("godot4")
    if not force_local and candidate and engine_version(candidate).startswith(VERSION + ".stable."):
        print(f"Using Godot {engine_version(candidate)}", flush=True)
        return
    if platform.system() != "Linux" or platform.machine() not in ("x86_64", "AMD64"):
        raise RuntimeError("Automatic runtime install supports Linux x86_64. Install Godot 4.6.3 on this platform.")
    archive = download_verified("engine")
    local_binary.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        with zf.open("Godot_v4.6.3-stable_linux.x86_64") as src, local_binary.open("wb") as out:
            shutil.copyfileobj(src, out)
    local_binary.chmod(0o755)
    if not engine_version(str(local_binary)).startswith(VERSION + ".stable."):
        raise RuntimeError("Installed runtime returned an unexpected version")
    archive.unlink()
    print("Installed verified local Godot runtime", flush=True)


def ensure_templates() -> None:
    target = ROOT / ".local/share/godot/export_templates" / (VERSION + ".stable")
    manifest = target / "verified.json"
    try:
        old = json.loads(manifest.read_text())
        if old.get("archive_sha512") == ARCHIVES["templates"][1] and all(
            (target / name).is_file() and digest(target / name, "sha256") == old.get(name)
            for name in TEMPLATE_NAMES
        ):
            print("Reusing verified matching web export templates", flush=True)
            return
    except (OSError, ValueError, TypeError):
        pass
    archive = download_verified("templates")
    target.mkdir(parents=True, exist_ok=True)
    hashes = {"archive_sha512": ARCHIVES["templates"][1]}
    with zipfile.ZipFile(archive) as zf:
        for name in TEMPLATE_NAMES:
            with zf.open("templates/" + name) as src, (target / name).open("wb") as out:
                shutil.copyfileobj(src, out)
            hashes[name] = digest(target / name, "sha256")
    manifest.write_text(json.dumps(hashes, indent=2) + "\n")
    archive.unlink()
    print("Installed matching web templates; discarded unused platform archive", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native-only", action="store_true", help="Do not download web export templates")
    parser.add_argument("--force-local-engine", action="store_true", help="Install and verify a private runtime even if one is present")
    args = parser.parse_args()
    for relative in (".local/share", ".local/cache", ".local/config"):
        (ROOT / relative).mkdir(parents=True, exist_ok=True)
    ensure_engine(args.force_local_engine)
    if not args.native_only:
        ensure_templates()
    print("Tool preparation complete. Run bash tools/check.sh once the project files are present.", flush=True)


if __name__ == "__main__":
    main()
