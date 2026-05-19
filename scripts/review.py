#!/usr/bin/env python3
"""Prepare a generated clip for quality control — the first half of the
skill's self-improvement loop.

review.py does NOT judge the clip; it extracts the artifacts Claude needs to
watch it: a frame contact sheet, the individual sampled frames, the first and
last frame, and a probe of duration / audio / resolution. Claude then Reads
those images, scores the clip against the prompt, and records a lesson in
LESSONS.md (see SKILL.md, "Quality control & self-improvement").

Usage:
    python review.py CLIP.mp4 [--job JOB.json] [--frames N] [--out DIR]

Outputs into DIR/review/<clip-stem>/:
    contact_sheet.jpg   N frames tiled — Read this first
    frame_00.jpg ...    individual sampled frames (full detail)
    probe.json          duration, audio stream, resolution, fps
    qc_template.json    a QC rubric for Claude to fill in

Requires ffmpeg + ffprobe on PATH.
"""
from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
from pathlib import Path


def need(tool: str) -> None:
    if not shutil.which(tool):
        sys.exit(f"ERROR: '{tool}' not found on PATH — install ffmpeg")


def probe(clip: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_format", "-show_streams", str(clip)],
        capture_output=True, text=True)
    data = json.loads(out.stdout or "{}")
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    fps = 0.0
    if video.get("r_frame_rate", "0/1") != "0/0":
        num, _, den = video.get("r_frame_rate", "0/1").partition("/")
        fps = round(float(num) / float(den or 1), 2)
    return {
        "duration_s": round(float(data.get("format", {}).get("duration", 0)), 2),
        "resolution": f"{video.get('width', '?')}x{video.get('height', '?')}",
        "fps": fps,
        "has_audio": audio is not None,
        "audio_codec": (audio or {}).get("codec_name"),
        "size_bytes": clip.stat().st_size,
    }


def extract_frames(clip: Path, dst: Path, n: int, duration: float) -> list[Path]:
    frames = []
    duration = max(duration, 0.1)
    for k in range(n):
        t = duration * (k + 0.5) / n          # centre of each 1/n slice
        fp = dst / f"frame_{k:02d}.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.3f}",
             "-i", str(clip), "-frames:v", "1", "-q:v", "3", str(fp)],
            check=True)
        if fp.exists():
            frames.append(fp)
    return frames


def contact_sheet(frames: list[Path], dst: Path) -> Path | None:
    if not frames:
        return None
    cols = math.ceil(math.sqrt(len(frames)))
    rows = math.ceil(len(frames) / cols)
    sheet = dst / "contact_sheet.jpg"
    inputs = []
    for f in frames:
        inputs += ["-i", str(f)]
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", *inputs,
         "-filter_complex",
         f"tile={cols}x{rows}:padding=4:margin=4", "-frames:v", "1",
         "-q:v", "3", str(sheet)],
        check=True)
    return sheet if sheet.exists() else None


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    clip = None
    job_path = None
    n_frames = 9
    out_dir = Path("./seedance_out")
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--job":
            job_path = Path(args[i + 1]); i += 2
        elif a == "--frames":
            n_frames = int(args[i + 1]); i += 2
        elif a == "--out":
            out_dir = Path(args[i + 1]); i += 2
        elif not a.startswith("--"):
            clip = Path(a); i += 1
        else:
            print(f"unknown flag {a}"); return 1

    if not clip or not clip.is_file():
        print(f"ERROR: clip not found: {clip}"); return 1
    need("ffmpeg")
    need("ffprobe")

    dst = out_dir / "review" / clip.stem
    dst.mkdir(parents=True, exist_ok=True)

    info = probe(clip)
    (dst / "probe.json").write_text(json.dumps(info, indent=2))

    frames = extract_frames(clip, dst, n_frames, info["duration_s"])
    sheet = contact_sheet(frames, dst)

    prompt = None
    if job_path and job_path.is_file():
        obj = json.loads(job_path.read_text())
        jobs = obj if isinstance(obj, list) else [obj]
        match = next((j for j in jobs if j.get("id") == clip.stem), jobs[0])
        prompt = (match.get("input", match) or {}).get("prompt")

    qc = {
        "clip": str(clip),
        "clip_id": clip.stem,
        "prompt": prompt,
        "probe": info,
        "_instructions": (
            "Claude: Read contact_sheet.jpg and the frame_*.jpg files, then "
            "fill the fields below. Score 1-5 (5 = flawless). Do NOT "
            "regenerate unless the user asks — record the lesson and move on."),
        "scores": {
            "prompt_fidelity": None,
            "subject_consistency": None,
            "camera_and_motion": None,
            "audio_match": None,
            "overall": None,
        },
        "failure_modes_observed": [],
        "what_worked": None,
        "what_to_change": None,
        "lesson": None,
    }
    (dst / "qc_template.json").write_text(json.dumps(qc, indent=2))

    print(f"Review artifacts for '{clip.stem}':")
    print(f"  probe        : duration={info['duration_s']}s "
          f"{info['resolution']} {info['fps']}fps "
          f"audio={'yes' if info['has_audio'] else 'NO'}")
    if sheet:
        print(f"  contact sheet: {sheet}")
    print(f"  frames       : {len(frames)} in {dst}")
    print(f"  qc template  : {dst / 'qc_template.json'}")
    print()
    print("Next: Read the contact sheet + frames, fill qc_template.json, then")
    print("append a one-line lesson to the skill's LESSONS.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
