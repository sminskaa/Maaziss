#!/usr/bin/env python3
"""Install the pinned, free CPU speech tools in the ignored .local/tts directory."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TTS = ROOT / ".local/tts"
SOURCE = TTS / "chatterbox"
COMMIT = "5de7a54aa4e5e2baadb0182dde554908b48b85c2"


def run(command: list[str], environment: dict[str, str], capture: bool = False) -> str:
    result = subprocess.run(command, cwd=ROOT, env=environment, check=True,
                            text=True, stdout=subprocess.PIPE if capture else None)
    return result.stdout.strip() if capture else ""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-model", action="store_true",
                        help="Also verify/download the official Nano model; needs allowed model hosts.")
    args = parser.parse_args()
    uv = shutil.which("uv")
    if not uv:
        raise SystemExit("The cloud base must provide uv; no system Python packages will be modified.")
    TTS.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ)
    environment.update({
        "UV_CACHE_DIR": str(TTS / "uv-cache"),
        "UV_PYTHON_INSTALL_DIR": str(TTS / "python"),
        "XDG_CACHE_HOME": str(TTS / "cache"),
        "HF_HOME": str(TTS / "cache/huggingface"),
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "DO_NOT_TRACK": "1",
    })
    interpreter = TTS / "venv/bin/python"
    if not interpreter.exists():
        run([uv, "venv", "--python", "3.11.17", str(TTS / "venv")], environment)
    actual = run([str(interpreter), "-c", "import platform; print(platform.python_version())"], environment, True)
    if actual != "3.11.17":
        raise SystemExit(f"Expected isolated Python 3.11.17, found {actual}; existing environment retained.")
    if not SOURCE.exists():
        run(["git", "clone", "--no-checkout", "https://github.com/resemble-ai/chatterbox.git", str(SOURCE)], environment)
        run(["git", "-C", str(SOURCE), "checkout", "--detach", COMMIT], environment)
    current = run(["git", "-C", str(SOURCE), "rev-parse", "HEAD"], environment, True)
    if current != COMMIT:
        raise SystemExit("Speech source differs from the tested commit; not resetting an existing checkout.")
    run([uv, "pip", "install", "--python", str(interpreter), "--torch-backend", "cpu",
         "--constraints", str(ROOT / "tools/voice-constraints.txt"),
         "torch==2.6.0", "torchaudio==2.6.0"], environment)
    run([uv, "pip", "install", "--python", str(interpreter), "--torch-backend", "cpu",
         "--constraints", str(ROOT / "tools/voice-constraints.txt"),
         "--overrides", str(ROOT / "tools/voice-overrides.txt"), "-e", str(SOURCE)], environment)
    run([uv, "pip", "check", "--python", str(interpreter)], environment)
    # Import the real implementation: successful pip installation alone is insufficient.
    environment.update({"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"})
    run([str(interpreter), "-c",
         "import inspect, torch; from chatterbox.tts_turbo import ChatterboxTurboTTS; "
         "assert 'nano' in inspect.signature(ChatterboxTurboTTS.from_local).parameters; "
         "assert torch.__version__ == '2.6.0+cpu'; print('CPU Nano implementation imports successfully')"], environment)
    run([str(interpreter), str(ROOT / "tools/synthesize_voice.py"), "--help"], environment)
    print("Speech dependencies prepared. Model weights/licence and synthesis require separate validation.", flush=True)
    if args.prepare_model:
        environment.pop("HF_HUB_OFFLINE", None)
        environment.pop("TRANSFORMERS_OFFLINE", None)
        run([str(interpreter), str(ROOT / "tools/prepare_voice_model.py")], environment)


if __name__ == "__main__":
    main()
