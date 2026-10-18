#!/usr/bin/env python3
"""Generate local Maziss dialogue with a prepared Chatterbox Nano model.

Run --help with any Python 3.10+ interpreter. Model dependencies are imported only
after command-line, file, and model-approval checks. No downloads run in this tool.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TTS_ROOT = PROJECT_ROOT / ".local" / "tts"
APPROVAL_FILE = TTS_ROOT / "model-approved.json"
MAX_TEXT_FILE_BYTES = 128 * 1024


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description=(
            "Generate English WAV dialogue locally using Chatterbox Nano and your "
            "own reference recording. A prepared, licence-verified model is required."
        ),
        epilog=(
            "No external service is used. --text-file contains one spoken line per "
            "line; multiple lines produce numbered WAV files. Outputs never replace "
            "existing files."
        ),
    )
    result.add_argument(
        "--reference", required=True, type=Path,
        help="Existing WAV or FLAC reference: over 5 and up to 30 seconds, ideally 6–15.",
    )
    source = result.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Text to speak, 1–300 characters per nonempty line.")
    source.add_argument(
        "--text-file", type=Path,
        help="UTF-8 file, one 1–300-character spoken line per nonempty line.",
    )
    result.add_argument(
        "--output", type=Path,
        help="WAV path; default: .local/tts/output/maziss-<UTC timestamp>.wav.",
    )
    result.add_argument(
        "--model-dir", type=Path,
        help="Local model directory; must match the verified model approval record.",
    )
    result.add_argument("--seed", type=int, default=0, help="Random seed (default: 0).")
    result.add_argument(
        "--threads", type=int, default=4,
        help="CPU threads, 1–32 (default: 4); GPU use is disabled.",
    )
    return result


def read_lines(args: argparse.Namespace) -> list[str]:
    if args.text_file is not None:
        source = args.text_file.expanduser().resolve()
        if not source.is_file():
            raise ValueError(f"Text file does not exist: {source}")
        if source.stat().st_size > MAX_TEXT_FILE_BYTES:
            raise ValueError("Text file is too large; provide a dialogue batch under 128 KiB.")
        raw = source.read_text(encoding="utf-8-sig")
    else:
        raw = args.text
    lines = []
    for number, line in enumerate(raw.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        if len(line) > 300:
            raise ValueError(f"Text line {number} has {len(line)} characters; maximum is 300.")
        if any(ord(character) < 32 for character in line):
            raise ValueError(f"Text line {number} contains control characters.")
        lines.append(line)
    if not lines:
        raise ValueError("Provide at least one nonempty spoken line of 1–300 characters.")
    return lines


def approved_model(requested_dir: Path | None) -> Path:
    if not APPROVAL_FILE.is_file():
        raise ValueError(
            "Run model preparation after downloads are allowed; weights/licence "
            "have not yet been verified. No speech has been generated."
        )
    if APPROVAL_FILE.stat().st_size > 64 * 1024:
        raise ValueError("Invalid model approval record: file is unexpectedly large.")
    approval = json.loads(APPROVAL_FILE.read_text(encoding="utf-8"))
    if not isinstance(approval, dict):
        raise ValueError("Invalid model approval record: expected an object.")
    if (
        approval.get("license_verified") is not True
        or not isinstance(approval.get("model_repo"), str)
        or not approval["model_repo"].strip()
        or not isinstance(approval.get("license"), str)
        or not approval["license"].strip()
        or not isinstance(approval.get("revision"), str)
        or not re.fullmatch(r"[a-fA-F0-9]{40}", approval["revision"])
        or not isinstance(approval.get("model_dir"), str)
        or not approval["model_dir"].strip()
    ):
        raise ValueError("Model approval record is incomplete; rerun model preparation.")
    recorded_dir = Path(approval["model_dir"]).expanduser().resolve()
    chosen_dir = requested_dir.expanduser().resolve() if requested_dir else recorded_dir
    if chosen_dir != recorded_dir:
        raise ValueError("--model-dir must match the licence-verified model directory.")
    if not chosen_dir.is_dir():
        raise ValueError(f"Prepared model directory is missing: {chosen_dir}")
    return chosen_dir


def output_paths(requested: Path | None, count: int) -> list[Path]:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    base = (requested or TTS_ROOT / "output" / f"maziss-{stamp}.wav").expanduser().resolve()
    if base.suffix.lower() != ".wav":
        raise ValueError("--output must end in .wav; generated files use WAV PCM 16-bit.")
    paths = [base] if count == 1 else [
        base.with_name(f"{base.stem}-{index:03d}.wav") for index in range(1, count + 1)
    ]
    for path in paths:
        if path.exists():
            raise ValueError(f"Output already exists; choose a different path: {path}")
    return paths


def configure_local_runtime() -> None:
    cache = TTS_ROOT / "cache"
    variables = {
        "HF_HUB_OFFLINE": "1",
        "TRANSFORMERS_OFFLINE": "1",
        "HF_DATASETS_OFFLINE": "1",
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "DO_NOT_TRACK": "1",
        "XDG_CACHE_HOME": str(cache),
        "HF_HOME": str(cache / "huggingface"),
        "HF_HUB_CACHE": str(cache / "huggingface" / "hub"),
        "TORCH_HOME": str(cache / "torch"),
    }
    for name, value in variables.items():
        os.environ[name] = value


def synthesize(args: argparse.Namespace, lines: list[str], model_dir: Path,
               paths: list[Path], reference: Path) -> None:
    configure_local_runtime()
    try:
        import numpy as np
        import soundfile as sf
        import torch
        from chatterbox.tts_turbo import ChatterboxTurboTTS
    except ImportError as error:
        raise ValueError(
            "Speech dependencies are not installed in this interpreter. Run "
            ".local/tts/venv/bin/python tools/synthesize_voice.py with the same arguments. "
            f"Import detail: {error}"
        ) from error

    metadata = sf.info(str(reference))
    if metadata.format not in {"WAV", "WAVEX", "FLAC"}:
        raise ValueError("Reference must contain WAV or FLAC audio, not a renamed file.")
    if metadata.channels not in (1, 2):
        raise ValueError("Reference must be mono or stereo; mono is preferred.")
    if not 5 < metadata.duration <= 30:
        raise ValueError(
            f"Reference is {metadata.duration:.2f} seconds; use an excerpt longer "
            "than 5 seconds and up to 30 seconds (ideally 6–15 seconds)."
        )
    if not 8_000 <= metadata.samplerate <= 192_000:
        raise ValueError("Reference sample rate must be between 8 kHz and 192 kHz.")
    reference_audio, _ = sf.read(str(reference), dtype="float32", always_2d=True)
    if not np.isfinite(reference_audio).all():
        raise ValueError("Reference contains invalid audio samples.")
    if float(np.max(np.abs(reference_audio))) == 0:
        raise ValueError("Reference is silent; choose a recorded speech excerpt.")
    if not 6 <= metadata.duration <= 15:
        print("Note: a clean 6–15 second speech excerpt is recommended.", file=sys.stderr)

    torch.set_num_threads(args.threads)
    torch.manual_seed(args.seed)
    print("Loading the local Chatterbox Nano model on CPU; no download will run.", flush=True)
    model = ChatterboxTurboTTS.from_local(
        ckpt_dir=str(model_dir), device="cpu", nano=True,
    )
    sample_rate = int(model.sr)
    if not 8_000 <= sample_rate <= 192_000:
        raise ValueError("Model returned an unsupported output sample rate.")
    for index, (line, destination) in enumerate(zip(lines, paths)):
        torch.manual_seed(args.seed + index)
        print(f"Generating line {index + 1}/{len(lines)} ({len(line)} characters)…", flush=True)
        with torch.inference_mode():
            waveform = model.generate(line, audio_prompt_path=str(reference))
        audio = waveform.detach().to(device="cpu", dtype=torch.float32).numpy()
        if audio.ndim == 2 and audio.shape[0] == 1:
            audio = audio[0]
        if audio.ndim != 1 or audio.size == 0 or not np.isfinite(audio).all():
            raise ValueError("Model produced empty, non-mono, or invalid audio; no WAV was saved.")
        peak = float(np.max(np.abs(audio)))
        if peak == 0:
            raise ValueError("Model produced silence; no WAV was saved.")
        if peak >= 1.0:
            audio = audio * (0.99 / peak)
            print("Reduced output amplitude to avoid clipping.", file=sys.stderr)
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation protects existing recordings even if another process
        # creates the requested output after our initial checks.
        with destination.open("xb") as target:
            sf.write(target, audio, sample_rate, format="WAV", subtype="PCM_16")
        duration = audio.size / sample_rate
        print(f"Saved {destination} ({duration:.2f} s, {sample_rate} Hz, mono PCM 16-bit).", flush=True)
    print("Listen before approving: generated delivery, wording, and accent can vary.")


def main(argv: list[str] | None = None) -> int:
    cli = parser()
    args = cli.parse_args(argv)
    try:
        if not 1 <= args.threads <= 32:
            raise ValueError("--threads must be between 1 and 32 (default: 4).")
        if not 0 <= args.seed <= 2**32 - 1:
            raise ValueError("--seed must be between 0 and 4294967295.")
        reference = args.reference.expanduser().resolve()
        if not reference.is_file():
            raise ValueError(f"Reference recording does not exist: {reference}")
        if reference.suffix.lower() not in {".wav", ".flac"}:
            raise ValueError("Use a WAV or FLAC reference; keep the original M4A unchanged.")
        lines = read_lines(args)
        paths = output_paths(args.output, len(lines))
        if reference in paths:
            raise ValueError("Output must not replace the reference recording.")
        model_dir = approved_model(args.model_dir)
        synthesize(args, lines, model_dir, paths, reference)
    except (ValueError, OSError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Stopped. Previously completed WAV files, if any, are retained.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
