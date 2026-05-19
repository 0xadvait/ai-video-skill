#!/usr/bin/env python3
"""Stitch generated clips into a finished video — the edit step.

Takes an edit list (JSON), trims and normalizes each clip to a common format,
then joins them with hard cuts or crossfades. Optionally lays a single audio
track over the whole cut (narration / music bed).

Usage:
    python assemble.py edit.json

edit.json:
    {
      "output": "final.mp4",
      "resolution": "1080p",            // 480p|720p|1080p, default 1080p
      "fps": 24,                          // default 24
      "audio": "narration.mp3",          // optional — replaces all clip audio
      "clips": [
        {"path": "a.mp4", "trim_start": 0, "trim_end": 5},
        {"path": "b.mp4", "transition": "crossfade", "transition_dur": 0.5},
        {"path": "c.mp4", "transition": "cut"}
      ]
    }

`transition` on a clip is how it joins the PREVIOUS clip (default "cut").
Requires ffmpeg + ffprobe on PATH.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RES = {"480p": (854, 480), "720p": (1280, 720), "1080p": (1920, 1080)}


def need(tool: str) -> None:
    if not shutil.which(tool):
        sys.exit(f"ERROR: '{tool}' not found on PATH — install ffmpeg")


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 0.0


def normalize(clip: dict, idx: int, tmp: Path, w: int, h: int,
              fps: int) -> Path:
    """Trim + re-encode a clip to a uniform format so joins are clean."""
    src = Path(clip["path"])
    if not src.is_file():
        sys.exit(f"ERROR: clip not found: {src}")
    dst = tmp / f"norm_{idx:03d}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    if clip.get("trim_start"):
        cmd += ["-ss", str(clip["trim_start"])]
    if clip.get("trim_end") is not None:
        start = clip.get("trim_start", 0)
        cmd += ["-to", str(clip["trim_end"] - start if False else clip["trim_end"])]
    cmd += ["-i", str(src),
            "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
                   f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,fps={fps},setsar=1",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2",
            "-pix_fmt", "yuv420p", str(dst)]
    subprocess.run(cmd, check=True)
    return dst


def concat_cuts(clips: list[Path], out: Path, tmp: Path) -> None:
    listing = tmp / "concat.txt"
    listing.write_text("".join(f"file '{c}'\n" for c in clips))
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(listing), "-c", "copy", str(out)], check=True)


def xfade_chain(clips: list[Path], trans: list[tuple[str, float]],
                out: Path) -> None:
    """Join clips with per-boundary crossfade or cut via xfade/acrossfade."""
    inputs = []
    for c in clips:
        inputs += ["-i", str(c)]
    durs = [duration(c) for c in clips]
    v, a = "[0:v]", "[0:a]"
    offset = durs[0]
    parts = []
    for i in range(1, len(clips)):
        kind, dur = trans[i]
        dur = 0.001 if kind == "cut" else max(dur, 0.05)
        offset -= dur
        vo, ao = f"[v{i}]", f"[a{i}]"
        parts.append(
            f"{v}[{i}:v]xfade=transition=fade:duration={dur}:"
            f"offset={offset:.3f}{vo}")
        parts.append(f"{a}[{i}:a]acrossfade=d={dur}{ao}")
        v, a = vo, ao
        offset += durs[i]
    filtergraph = ";".join(parts)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", *inputs,
         "-filter_complex", filtergraph, "-map", v, "-map", a,
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-c:a", "aac", "-pix_fmt", "yuv420p", str(out)], check=True)


def lay_audio(video: Path, audio: Path, out: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video),
         "-i", str(audio), "-map", "0:v", "-map", "1:a", "-shortest",
         "-c:v", "copy", "-c:a", "aac", str(out)], check=True)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    need("ffmpeg")
    need("ffprobe")
    spec = json.loads(Path(sys.argv[1]).read_text())
    clips = spec.get("clips") or []
    if not clips:
        sys.exit("ERROR: edit list has no clips")
    out = Path(spec.get("output", "final.mp4"))
    w, h = RES.get(spec.get("resolution", "1080p"), RES["1080p"])
    fps = int(spec.get("fps", 24))

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        print(f"normalizing {len(clips)} clip(s) to {w}x{h}@{fps}...")
        normed = [normalize(c, i, tmp, w, h, fps)
                  for i, c in enumerate(clips)]
        trans = [(c.get("transition", "cut"), float(c.get("transition_dur", 0.5)))
                 for c in clips]

        joined = tmp / "joined.mp4"
        if any(t[0] == "crossfade" for t in trans[1:]):
            print("joining with crossfades...")
            xfade_chain(normed, trans, joined)
        else:
            print("joining with hard cuts...")
            concat_cuts(normed, joined, tmp)

        out.parent.mkdir(parents=True, exist_ok=True)
        if spec.get("audio"):
            audio = Path(spec["audio"])
            if not audio.is_file():
                sys.exit(f"ERROR: audio not found: {audio}")
            print(f"laying audio track {audio.name}...")
            lay_audio(joined, audio, out)
        else:
            shutil.copy(joined, out)

    total = duration(out)
    print(f"\nassembled {out} — {total:.1f}s, {out.stat().st_size // 1024} KB")
    print("Next: upscale.py for a finishing pass, or review.py to QC.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
