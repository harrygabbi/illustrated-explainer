#!/usr/bin/env python3
"""Render timed still images with optional audio and selectable captions."""

import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory


def ffmpeg(*args, cwd=None):
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y", *args],
        check=True,
        cwd=cwd,
    )


def require_file(base, value):
    path = (base / value).resolve()
    if not path.is_file():
        raise ValueError(f"File does not exist: {path}")
    return path


def read_manifest(path):
    config = json.loads(path.read_text())
    width, height = config["width"], config["height"]
    fps = config.get("fps", 24)
    if any(type(n) is not int or n < 2 or n % 2 for n in (width, height)):
        raise ValueError("Width and height must be positive even integers")
    if type(fps) is not int or not 1 <= fps <= 120:
        raise ValueError("FPS must be an integer from 1 to 120")

    shots = []
    elapsed = Decimal(0)
    previous_frame = 0
    for shot in config["shots"]:
        duration = Decimal(str(shot["duration"]))
        if not duration.is_finite() or duration <= 0:
            raise ValueError("Shot durations must be finite positive numbers")
        elapsed += duration
        boundary = round(elapsed * fps)
        frames = boundary - previous_frame
        if frames < 1:
            raise ValueError("Each shot must occupy at least one frame")
        shots.append((require_file(path.parent, shot["image"]), frames))
        previous_frame = boundary
    if not shots:
        raise ValueError("The manifest must contain at least one shot")

    audio = require_file(path.parent, config["audio"]) if config.get("audio") else None
    captions = require_file(path.parent, config["captions"]) if config.get("captions") else None
    return width, height, fps, shots, audio, captions


def render(manifest, output):
    width, height, fps, shots, audio, captions = read_manifest(manifest)
    video_filter = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1"
    )
    total_frames = sum(frames for _, frames in shots)
    with TemporaryDirectory(prefix=".illustrated-cut-", dir=output.parent) as scratch:
        folder = Path(scratch)
        concat = ["ffconcat version 1.0"]
        for index, (image, frames) in enumerate(shots):
            clip = f"shot-{index:05}.mp4"
            ffmpeg(
                "-loop", "1", "-framerate", str(fps), "-i", str(image),
                "-an", "-vf", video_filter, "-frames:v", str(frames),
                "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",
                "-crf", "18", "-pix_fmt", "yuv420p", "-video_track_timescale", str(fps * 1000),
                clip, cwd=folder,
            )
            concat.extend((f"file '{clip}'", f"duration {frames / fps:.9f}"))

        (folder / "shots.ffconcat").write_text("\n".join(concat) + "\n")
        inputs = ["-f", "concat", "-safe", "1", "-i", "shots.ffconcat"]
        streams = ["-map", "0:v:0", "-c:v", "copy"]
        if audio:
            inputs += ["-i", str(audio)]
            streams += [
                "-map", "1:a:0", "-af", "apad", "-ar", "48000",
                "-c:a", "aac", "-b:a", "192k",
            ]
        if captions:
            inputs += ["-i", str(captions)]
            index = 2 if audio else 1
            streams += ["-map", f"{index}:s:0", "-c:s", "mov_text", "-disposition:s:0", "0"]

        ffmpeg(
            *inputs, *streams, "-t", f"{total_frames / fps:.9f}",
            "-movflags", "+faststart", "finished.mp4", cwd=folder,
        )
        (folder / "finished.mp4").replace(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.suffix.lower() != ".mp4":
        parser.error("The output must have an .mp4 extension")
    try:
        render(args.manifest.resolve(), args.output.resolve())
    except (ValueError, TypeError, KeyError, OSError, InvalidOperation, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Render failed: {exc}\n")
    print(args.output.resolve())


if __name__ == "__main__":
    main()
