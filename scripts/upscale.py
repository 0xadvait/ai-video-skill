#!/usr/bin/env python3
"""Finishing pass — upscale resolution and/or interpolate frame rate.

The end of the pipeline: take a generated or assembled clip to delivery
quality. Default path is local ffmpeg (lanczos upscale + motion-compensated
interpolation) — no API key, fully deterministic. An ML upscaler on Replicate
is available via --model for a quality jump.

Usage:
    python upscale.py CLIP.mp4 [--out out.mp4] [--resolution R] [--scale N]
                       [--fps N] [--model SLUG]

    --resolution  1080p | 1440p | 4k        target height (keeps aspect)
    --scale       2 | 1.5 ...               multiply current size instead
    --fps         60                        motion-interpolate to N fps
    --model       SLUG                      Replicate ML upscaler slug
                                            (e.g. lucataco/real-esrgan-video)

With no --resolution/--scale/--fps it does a clean 2x lanczos upscale.
Local path requires ffmpeg + ffprobe; --model requires REPLICATE_API_TOKEN.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HEIGHTS = {"720p": 720, "1080p": 1080, "1440p": 1440, "2160p": 2160, "4k": 2160}


def need(tool: str) -> None:
    if not shutil.which(tool):
        sys.exit(f"ERROR: '{tool}' not found on PATH — install ffmpeg")


def probe_size(clip: Path) -> tuple[int, int]:
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", str(clip)],
        capture_output=True, text=True)
    w, _, h = out.stdout.strip().partition(",")
    return int(w), int(h)


def run_ffmpeg(clip: Path, out: Path, tw: int, th: int, fps: int | None) -> None:
    vf = f"scale={tw}:{th}:flags=lanczos"
    if fps:
        vf += f",minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc:vsbmc=1"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip),
         "-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", "16",
         "-c:a", "copy", "-pix_fmt", "yuv420p", str(out)], check=True)


def run_replicate(clip: Path, out: Path, slug: str) -> None:
    import replicate
    with clip.open("rb") as f:
        url = replicate.files.create(file=f).urls["get"]
    result = replicate.run(slug, input={"video": url})
    data = result.read() if hasattr(result, "read") else None
    if data is None and isinstance(result, list) and result:
        data = result[0].read()
    if data is None:
        sys.exit(f"ERROR: {slug} returned no video")
    out.write_bytes(data)


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    clip = None
    out = None
    resolution = None
    scale = None
    fps = None
    model = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--out":
            out = Path(args[i + 1]); i += 2
        elif a == "--resolution":
            resolution = args[i + 1]; i += 2
        elif a == "--scale":
            scale = float(args[i + 1]); i += 2
        elif a == "--fps":
            fps = int(args[i + 1]); i += 2
        elif a == "--model":
            model = args[i + 1]; i += 2
        elif not a.startswith("--"):
            clip = Path(a); i += 1
        else:
            print(f"unknown flag {a}"); return 1

    if not clip or not clip.is_file():
        print(f"ERROR: clip not found: {clip}"); return 1
    out = out or clip.with_name(f"{clip.stem}_finished.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)

    if model:
        print(f"upscaling via Replicate {model}...")
        run_replicate(clip, out, model)
    else:
        need("ffmpeg")
        need("ffprobe")
        w, h = probe_size(clip)
        if resolution:
            th = HEIGHTS.get(resolution.lower())
            if not th:
                sys.exit(f"ERROR: --resolution must be one of {sorted(HEIGHTS)}")
            tw = round(w * th / h)
        elif scale:
            tw, th = round(w * scale), round(h * scale)
        else:
            tw, th = w * 2, h * 2          # default: 2x
        tw -= tw % 2
        th -= th % 2
        label = f"{w}x{h} -> {tw}x{th}" + (f", interpolate to {fps}fps" if fps else "")
        print(f"finishing locally: {label}...")
        run_ffmpeg(clip, out, tw, th, fps)

    print(f"\nwrote {out} ({out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
