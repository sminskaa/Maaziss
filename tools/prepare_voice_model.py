#!/usr/bin/env python3
"""Resolve, licence-check and download the publisher's Nano model at an exact revision.

This downloads model files only. It does not upload text or recordings or generate speech.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
TTS = ROOT / ".local/tts"
REPO = "ResembleAI/chatterbox-nano"
MODEL_REVISION = "71ccd1d0081b430592cea481f4307e764e07bc64"


def main() -> int:
    cache = TTS / "cache/huggingface"
    os.environ.update({
        "HF_HOME": str(cache),
        "HF_HUB_CACHE": str(cache / "hub"),
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "HF_HUB_ETAG_TIMEOUT": "15",
        "HF_HUB_DOWNLOAD_TIMEOUT": "60",
        "XDG_CACHE_HOME": str(TTS / "cache"),
        "DO_NOT_TRACK": "1",
    })
    # A direct metadata request gives a clear, bounded network diagnosis before a
    # download library starts retries. Existing authentication is reused if present.
    headers = {"User-Agent": "Maziss-voice-setup/1"}
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request(
        "https://huggingface.co/api/models/" + REPO + "/revision/" + MODEL_REVISION,
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            metadata = json.loads(response.read(2 * 1024 * 1024))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as error:
        detail = str(error)
        if token:
            detail = detail.replace(token, "[redacted]")
        print("Model metadata could not be reached: " + detail, file=sys.stderr)
        print("Review/save the prepared Hugging Face network additions in environment settings, "
              "then retry. An egress denial does not establish that an API token is needed.", file=sys.stderr)
        return 2
    revision = metadata.get("sha", "")
    card = metadata.get("cardData") or {}
    licence = card.get("license") if isinstance(card, dict) else None
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Publisher metadata did not provide an exact model revision.")
    if revision != MODEL_REVISION:
        raise ValueError("Publisher metadata did not match the pinned model revision.")
    if not isinstance(licence, str) or licence.lower() != "mit":
        raise ValueError(f"Model declares {licence!r}, not the expected MIT licence; investigate its actual terms before using it.")
    review = TTS / "model-review"
    review.mkdir(parents=True, exist_ok=True)
    (review / "publisher-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    from huggingface_hub import hf_hub_download, snapshot_download
    readme = Path(hf_hub_download(REPO, "README.md", revision=revision, token=token or None))
    (review / "README.md").write_bytes(readme.read_bytes())
    print(f"Publisher model: {REPO}\nRevision: {revision}\nDeclared model licence: {licence}", flush=True)
    destination = snapshot_download(
        repo_id=REPO, revision=revision, token=token or None,
        allow_patterns=["*.safetensors", "*.json", "*.txt", "*.pt", "*.model", "README.md", "LICENSE*"],
    )
    model_dir = Path(destination).resolve()
    for name in ("ve.safetensors", "t3_nano_v1.safetensors", "s3gen_meanflow.safetensors"):
        if not (model_dir / name).is_file():
            raise ValueError(f"Official snapshot is missing {name}; model was not marked prepared.")
    # This records the publisher's MIT model declaration and exact downloaded revision.
    # It is separate from the source-code licence and can be reviewed with its saved card.
    record = {"model_repo": REPO, "revision": revision, "license": "MIT",
              "license_verified": True, "model_dir": str(model_dir),
              "license_source": "Publisher model-card metadata; original README retained in model-review/"}
    marker = TTS / "model-approved.json"
    temp = marker.with_suffix(".pending.json")
    temp.write_text(json.dumps(record, indent=2) + "\n")
    temp.replace(marker)
    print("Model files prepared locally. Run a short synthesis and inspect its output before using it in the game.", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, RuntimeError) as error:
        print("Model preparation failed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
