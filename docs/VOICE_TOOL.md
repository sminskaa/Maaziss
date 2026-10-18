# Free local voice generation

This tool generates new English speech from written lines and a short reference
recording. You do not need to record every line. Your own recordings remain the
best way to choose Maziss's delivery; generated speech may change the accent,
pronunciation, emotion, or timing. It needs listening and approval before use.

The user has authorised use of their own uploaded Maziss recordings for this work.
No recording is sent to a voice service. This setup uses local CPU inference,
not a paid API. It does not clone other people's voices or automatically add
audio to the game.

## Current status

**Working and tested.** The isolated Python 3.11.17 environment, CPU Torch 2.6.0,
pinned Chatterbox source, official Nano model and synthesis command are installed.
The environment's updated network settings allowed the model download. The owner
selected unrestricted access; setup does not silently change that preference.
No paid API or new secret was needed.

The verified publisher snapshot is `ResembleAI/chatterbox-nano` revision
`71ccd1d0081b430592cea481f4307e764e07bc64`, which declares MIT in its model card.
The preparation helper pins that exact revision. Its original card and metadata are
retained in `.local/tts/model-review/`; this is separate from the source-code licence.

To reproduce package setup from `/workspace/Maaziss`:

```sh
python3 tools/setup_voice.py
```

To prepare or refresh the pinned model:

```sh
.local/tts/venv/bin/python tools/prepare_voice_model.py
```

The first command pins Chatterbox to commit
`5de7a54aa4e5e2baadb0182dde554908b48b85c2` and its Perth watermarker to
`ff1c8ac55a976971245cdd53c18d6131ca00d993`, preserving the watermarker.
It uses CPU wheels and leaves the game's Python/system environments unchanged.
The preparation command resolves an exact model revision, checks the publisher's
MIT model declaration, retains its card, and downloads the required model files.

Model preparation downloads the official weights, verifies their actual
repository revision and licence, and writes
`.local/tts/model-approved.json`. Do not create this record by hand to bypass
verification. The synthesis command refuses to run without it. Code and model
licences are separate: permission to use the Chatterbox source code does not
automatically establish permission to use a particular model or voice.

## Prepare a reference

Use a clear excerpt of your own speech with no music, competing voices, or
added effects. **Six to fifteen seconds** is recommended; the tool accepts
more than 5 and up to 30 seconds, matching the model's minimum. WAV or FLAC is
supported, preferably mono. A long file containing
all the test lines should first be copied to a short excerpt. Keep the M4A
originals unchanged. See [recording advice](VOICE_RECORDING.md).

## Generate one line

Once installation and model preparation succeed, run these commands from
`/workspace/Maaziss`. The `--reference` path below is an example: replace it with
the actual prepared excerpt.

```sh
.local/tts/venv/bin/python tools/synthesize_voice.py --help

.local/tts/venv/bin/python tools/synthesize_voice.py \
  --reference .local/tts/references/maziss.wav \
  --text "They saw me. All three of them." \
  --output .local/tts/output/maziss-test.wav
```

An actual 10.8-second reference excerpt from the user's first audition is already
prepared at `.local/tts/references/maziss.wav`. The uploaded original remains unchanged.

The model directory normally comes from the verified preparation record. You can
provide `--model-dir /absolute/path/to/model`, but it must match that record.
Use `--seed 1` to try a different rendition. Identical seeds do not guarantee
bit-for-bit results across different machines or library versions.

Synthesis uses the CPU and four threads by default. `--threads 2` reduces CPU
parallelism if other work needs resources. The first measured run took 33.39 seconds
including process/model loading and generated a 4.88-second clip. This is one cold
run, not a general speed guarantee. Generate files during development and play the
stored audio in-game; the game does not run the speech model.

## Generate a small batch

Make a UTF-8 text file with one spoken line per line. Blank lines are ignored.
Each nonempty line must contain 1–300 characters; split long dialogue at natural
sentence boundaries. For example, save these as `.local/tts/lines.txt`:

```text
They saw me. All three of them.
Something under the cushion. That explains my back.
A fine I can pay. Eventually.
```

```sh
.local/tts/venv/bin/python tools/synthesize_voice.py \
  --reference .local/tts/references/maziss.wav \
  --text-file .local/tts/lines.txt \
  --output .local/tts/output/maziss-batch.wav
```

For three lines, this creates `maziss-batch-001.wav`, `maziss-batch-002.wav`, and
`maziss-batch-003.wav`. Each line is generated independently. A one-line batch
uses the exact requested output filename. Existing files are never overwritten.
If you omit `--output`, a unique timestamped name is used under
`.local/tts/output/`.

Output is mono WAV, PCM 16-bit, at the model's native sample rate. The command
checks samples for invalid values and reduces amplitude only if it would clip.
It does not pitch-shift, denoise, trim, or deliberately remove the model's audio
watermark. Listen to the actual output before approving it; successful file
creation does not certify performance quality or watermark detectability after
format conversion.

## What stays local

During synthesis, Hugging Face and Transformers are set to offline mode, and the
model is loaded from its verified local directory. There are no model downloads
in this command. Runtime caches, references, weights, and generated clips belong
under the ignored `.local/tts/` directory and are not part of the public game source.
Offline library settings are not a security sandbox for arbitrary downloaded Python code.

The current assistant cannot directly listen to these files. You choose whether
a delivery sounds right; automated measurements can check technical properties.
For other characters, your own changed performances can provide separate
references, but synthesis may partly erase an exaggerated voice. Test one short
line before recording or generating a full script.

## Validation so far

- `uv pip check`: 109 compatible installed packages.
- CPU Torch import reports `2.6.0+cpu` and no CUDA device.
- Real `ChatterboxTurboTTS.from_local` and `from_pretrained` APIs expose `nano`.
- CLI help and invalid-argument checks pass without model imports.
- Official model download and publisher MIT declaration verified at the pinned revision.
- Actual synthesis command exited 0 and wrote `.local/tts/output/first-synthesis.wav`:
  mono, 24 kHz, PCM 16-bit, 4.88 seconds; samples finite and non-silent, peak 0.574.
- Input text: “Apparently I need a permit to leave. I wonder if the murderers bothered
  with theirs.” Reference: the user's first audition, excerpted to 10.8 seconds.
- Cold process elapsed time: 33.39 seconds on four CPU threads. Detailed measurements
  are in `.local/tts/output/first-synthesis.json`.
- No other person's recording was supplied as a voice reference. The base model is
  pretrained on other audio; it is not trained exclusively on the user's samples.
- Human review of identity, spoken wording and acting is pending. The current assistant
  cannot directly listen; waveform validation alone does not certify those qualities.
