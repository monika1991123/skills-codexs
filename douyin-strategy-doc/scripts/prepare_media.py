#!/usr/bin/env python3
"""Extract audio, sampled frames, contact sheet, and an optional transcript."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--frame-seconds", type=int, default=8)
    parser.add_argument("--whisper-model", default="tiny")
    parser.add_argument("--skip-transcript", action="store_true")
    args = parser.parse_args()

    video = args.video.expanduser().resolve()
    output = args.output_dir.expanduser().resolve()
    frames = output / "frames"
    output.mkdir(parents=True, exist_ok=True)
    frames.mkdir(exist_ok=True)
    if not video.is_file():
        parser.error(f"video not found: {video}")
    if args.frame_seconds < 1:
        parser.error("--frame-seconds must be positive")

    audio = output / "audio.wav"
    run("ffmpeg", "-y", "-v", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(audio))
    run(
        "ffmpeg", "-y", "-v", "error", "-i", str(video),
        "-vf", f"fps=1/{args.frame_seconds},scale=480:-1", str(frames / "%03d.jpg"),
    )
    run(
        "ffmpeg", "-y", "-v", "error", "-framerate", "1", "-i", str(frames / "%03d.jpg"),
        "-vf", "tile=5x6", "-frames:v", "1", str(output / "contact-sheet.jpg"),
    )

    whisper = shutil.which("whisper") or str(Path.home() / ".local/bin/whisper")
    if not args.skip_transcript and Path(whisper).exists():
        run(
            whisper, str(audio), "--model", args.whisper_model, "--language", "Chinese",
            "--task", "transcribe", "--output_dir", str(output), "--output_format", "all", "--fp16", "False",
        )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

