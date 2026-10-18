#!/usr/bin/env python3
"""Extract a normalized, cyclic motion study from private walking footage.

The default reads an existing MediaPipe landmark cache. Supply --video to record
its hash, or --track to create a new private cache with MediaPipe/OpenCV. No video,
landmark coordinates, faces or private absolute paths are written to the public
motion JSON. Optional analysis dependencies are isolated from the game runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from statistics import median


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def track(video: Path, cache: Path, end: int) -> None:
    import cv2
    import mediapipe as mp

    capture = cv2.VideoCapture(str(video))
    fps = capture.get(cv2.CAP_PROP_FPS)
    records = []
    with mp.solutions.pose.Pose(
        static_image_mode=False, model_complexity=1, smooth_landmarks=True,
        min_detection_confidence=0.5, min_tracking_confidence=0.5,
    ) as model:
        index = 0
        while index <= end:
            ok, image = capture.read()
            if not ok:
                break
            result = model.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if result.pose_landmarks:
                height, width = image.shape[:2]
                records.append({
                    "frame": index, "time": index / fps,
                    "image": [[p.x * width, p.y * height, p.visibility]
                              for p in result.pose_landmarks.landmark],
                    "world": [[p.x, p.y, p.z, p.visibility]
                              for p in result.pose_world_landmarks.landmark],
                })
            index += 1
    capture.release()
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(records), encoding="utf-8")
    cache.chmod(0o600)


def angle(a, b) -> float:
    """Image-left is forward; angle from downward vertical, in degrees."""
    return math.degrees(math.atan2(a[0] - b[0], b[1] - a[1]))


def distance(a, b) -> float:
    return math.hypot(b[0] - a[0], b[1] - a[1])


def wrapped_degrees(value) -> float:
    return (value + 180) % 360 - 180


def periodic_smooth(rows, key: str, phase: float, width: float = 0.035) -> float:
    weights = []
    for row in rows:
        gap = abs(row["phase"] - phase) % 1
        gap = min(gap, 1 - gap)
        if gap < width * 3:
            weights.append((math.exp(-0.5 * (gap / width) ** 2), row[key]))
    return sum(w * value for w, value in weights) / sum(w for w, _ in weights)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tracking", type=Path,
                        default=Path("build/checks/reference-motion/raw-side.json"))
    parser.add_argument("--video", type=Path)
    parser.add_argument("--track", action="store_true")
    parser.add_argument("--source-name", default="Video Projectbiks.mp4")
    parser.add_argument("--start", type=int, default=36)
    parser.add_argument("--end", type=int, default=78)
    parser.add_argument("--body-height", type=float, default=420)
    parser.add_argument("--samples", type=int, default=24)
    parser.add_argument("--output", type=Path, default=Path("walking/reference-motion.json"))
    args = parser.parse_args()
    if args.track:
        if not args.video:
            parser.error("--track requires --video")
        track(args.video, args.tracking, max(args.end, 120))
    records = json.loads(args.tracking.read_text(encoding="utf-8"))
    by_frame = {record["frame"]: record for record in records}
    cycle = args.end - args.start
    if cycle <= 0 or args.samples < 8:
        parser.error("end must exceed start; samples must be at least eight")
    missing = [frame for frame in range(args.start, args.end + 1) if frame not in by_frame]
    if missing:
        parser.error(f"tracking frames are missing: {missing}")
    duration = by_frame[args.end]["time"] - by_frame[args.start]["time"]
    height = args.body_height
    first, last = by_frame[args.start]["image"], by_frame[args.end]["image"]
    mean_hip_y = lambda points: (points[23][1] + points[24][1]) / 2
    rows, thighs, shins, visibilities = [], [], [], []
    for frame in range(args.start, args.end):
        points = by_frame[frame]["image"]
        hip, knee, ankle, heel, toe = [points[index] for index in (23, 25, 27, 29, 31)]
        phase = (frame - args.start) / cycle
        thigh, shin = angle(hip, knee), angle(knee, ankle)
        foot_pitch = math.degrees(math.atan2(heel[1] - toe[1], heel[0] - toe[0]))
        # Remove the slow vertical trend caused by the oblique camera/path.
        baseline = mean_hip_y(first) * (1 - phase) + mean_hip_y(last) * phase
        rows.append({
            "phase": phase, "thigh_deg": thigh, "shin_deg": shin,
            "foot_pitch_deg": foot_pitch,
            "ankle_forward": (hip[0] - ankle[0]) / height,
            "ankle_up": (hip[1] - ankle[1]) / height,
            "pelvis_up": (baseline - mean_hip_y(points)) / height,
        })
        thighs.append(distance(hip, knee) / height)
        shins.append(distance(knee, ankle) / height)
        visibilities.append(min(hip[2], knee[2], ankle[2]))

    samples = []
    for index in range(args.samples):
        phase = index / args.samples
        sample = {"phase": round(phase, 6)}
        for key in rows[0]:
            if key != "phase":
                sample[key] = round(periodic_smooth(rows, key, phase), 6)
        measured_flex = wrapped_degrees(sample["thigh_deg"] - sample["shin_deg"])
        sample["knee_flex_deg"] = round(max(3, measured_flex), 6)
        sample["shin_deg"] = round(sample["thigh_deg"] - sample["knee_flex_deg"], 6)
        # The toe landmark is noisy during blurred push-off. Retain the observed
        # pitch separately and provide a conservative range-limited fit explicitly.
        sample["fitted_foot_pitch_deg"] = round(max(-45, min(10, sample["foot_pitch_deg"])), 6)
        sample["contact"] = phase < 0.69
        samples.append(sample)
    samples.append({**samples[0], "phase": 1.0})

    result = {
        "version": 1,
        "purpose": "Measured side-view human pose relationships; retarget to original Maziss proportions.",
        "source": {
            "filename": args.source_name,
            "sha256": sha256(args.video) if args.video else None,
            "tracking_sha256": sha256(args.tracking),
            "frames": [args.start, args.end],
            "seconds": [by_frame[args.start]["time"], by_frame[args.end]["time"]],
            "fps": round(cycle / duration, 6),
            "private_footage_embedded": False,
        },
        "coordinates": {
            "angle": "degrees from downward vertical; positive points thigh/shin forward",
            "forward": "actor travel direction; image-left in selected pass",
            "up": "positive toward head; hip-relative ankle_up is normally negative",
            "length": "approximate standing crown-to-sole height; original character lengths take precedence",
            "foot_pitch": "positive toe-up from heel-to-toe vector; measured2D and uncertain at push-off",
        },
        "cycle_seconds": round(duration, 6),
        "cadence_steps_per_minute": round(120 / duration, 3),
        "estimated_stride_body_heights": round((first[23][0] - last[23][0]) / height, 6),
        "contact_window": [0, 0.69],
        "heel_rise_window": [0.48, 0.69],
        "swing_window": [0.69, 1],
        "phase_zero": "near/left heel contact; opposite leg sampled at phase+0.5",
        "near_leg": "left-labelled MediaPipe landmarks23/25/27/29/31",
        "far_leg": "reconstructed from near-leg curve with half-cycle offset; not independently measured",
        "normalization": {
            "standing_body_height_pixels": height,
            "standing_height_uncertainty": "approximately5percent; visually estimated crown/sole, elevated camera",
            "thigh_median": round(median(thighs), 6),
            "shin_median": round(median(shins), 6),
            "minimum_joint_visibility": round(min(visibilities), 6),
        },
        "processing": [
            "MediaPipe0.10.21 full pose landmark cache; no rerun of retained tracking needed",
            "Use clean near-leg cycle; far leg is occluded and not reliable enough for its own curve",
            "Circular Gaussian smoothing, sigma0.035cycle;24samples plus identical closing sample",
            "Small negative tracking knee-flex values are bounded at3degrees; source contact estimates are approximate",
            "Pelvis vertical camera trend removed linearly; foot pitch range-fit[-45,10]deg is explicitly approximate",
            "Do not project these image2D knee offsets directly into front/back views; use sagittal-plane geometry",
        ],
        "uncertainties": [
            "Single oblique2D video does not measure ground-plane3D positions or ankle rotation accurately",
            "Footwear blur/heel-toe landmarks make measured foot pitch particularly uncertain",
            "Video container30fps does not independently establish unaltered original playback speed",
            "Start/end contact frames and stance boundary are visually estimated within about2frames",
            "This is a motion reference, not proof that a retargeted painted animation is natural",
        ],
        "samples": samples,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output.chmod(0o644)
    print(json.dumps({
        "output": str(args.output), "samples": len(samples),
        "cycle_seconds": result["cycle_seconds"],
        "thigh_range": [min(s["thigh_deg"] for s in samples), max(s["thigh_deg"] for s in samples)],
        "knee_flex_range": [min(s["knee_flex_deg"] for s in samples), max(s["knee_flex_deg"] for s in samples)],
        "thigh_length": result["normalization"]["thigh_median"],
        "shin_length": result["normalization"]["shin_median"],
    }, indent=2))


if __name__ == "__main__":
    main()
