#!/usr/bin/env python3
"""Validate a Seedance 2.0 request body against the canonical Replicate schema.

The Seedance schema is the canonical interchange format for this skill — even
when a job is routed to Kling / Wan / Veo, the job is authored against this
schema and generate.py translates it. So validating here covers every model.

Usage:
    python validate.py request.json        # a body, or a {id,model,input} job,
    python validate.py jobs.json            # or an array of either
    cat body.json | python validate.py      # stdin also works

Exit code 1 if there are hard ERRORS, 0 otherwise (warnings never fail).
Also exposes `validate(body) -> (errors, warnings)` for import by generate.py.
"""
from __future__ import annotations

import json
import re
import sys

ALLOWED_KEYS = {
    "prompt", "image", "last_frame_image", "reference_images",
    "reference_videos", "reference_audios", "duration", "resolution",
    "aspect_ratio", "generate_audio", "seed",
}
RESOLUTIONS = {"480p", "720p", "1080p"}
ASPECT_RATIOS = {"16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "9:21", "adaptive"}
SAFE_DURATIONS = {4, 5, 6, 8, 10, 12, 15}
RISKY_DURATIONS = {7, 9, 11, 13, 14}
AUDIO_WORDS = re.compile(
    r"\b(audio|dialogue|ambient|ambience|sound|sfx|music|voice|score|"
    r"room tone|whispers?|says?|crackle|hum|sizzle|rain|wind)\b", re.I)


def _word_count(text: str) -> int:
    return len(re.findall(r"\S+", text or ""))


def _max_citation(prompt: str, kind: str) -> int:
    """Highest N cited as [Image N] / [Video N] / [Audio N] in the prompt."""
    nums = re.findall(rf"\[{kind}\s*(\d+)\]", prompt or "", re.I)
    return max((int(n) for n in nums), default=0)


def validate(body: dict) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a single Seedance request body."""
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(body, dict):
        return ["request body is not a JSON object"], []

    # --- unknown keys -----------------------------------------------------
    for key in body:
        if key not in ALLOWED_KEYS:
            errors.append(f"unknown field '{key}' (not in the Seedance schema)")

    prompt = body.get("prompt")
    if not prompt or not str(prompt).strip():
        errors.append("'prompt' is required and cannot be empty")
        prompt = prompt or ""

    image = body.get("image")
    last_frame = body.get("last_frame_image")
    ref_images = body.get("reference_images") or []
    ref_videos = body.get("reference_videos") or []
    ref_audios = body.get("reference_audios") or []

    # --- mutually exclusive modes ----------------------------------------
    if (image or last_frame) and ref_images:
        errors.append(
            "'image'/'last_frame_image' cannot be combined with "
            "'reference_images' — pick first-frame mode OR reference mode")
    if last_frame and not image:
        errors.append("'last_frame_image' requires 'image' to also be set")
    if ref_audios and not ref_images and not ref_videos:
        errors.append(
            "'reference_audios' requires at least one reference image "
            "or reference video")

    # --- array ceilings ---------------------------------------------------
    if len(ref_images) > 9:
        errors.append(f"reference_images has {len(ref_images)} entries (max 9)")
    if len(ref_videos) > 3:
        errors.append(f"reference_videos has {len(ref_videos)} entries (max 3)")
    if len(ref_audios) > 3:
        errors.append(f"reference_audios has {len(ref_audios)} entries (max 3)")

    # --- duration ---------------------------------------------------------
    duration = body.get("duration", 5)
    if duration is not None:
        if not isinstance(duration, int) or isinstance(duration, bool):
            errors.append(f"duration must be an integer, got {duration!r}")
        elif duration != -1 and not (4 <= duration <= 15):
            errors.append(
                f"duration {duration} is invalid — must be -1 or 4..15")
        elif duration in RISKY_DURATIONS:
            warnings.append(
                f"duration {duration}: the underlying API may silently reject "
                f"this; safe set is {{4,5,6,8,10,12,15}}")

    # --- enums ------------------------------------------------------------
    resolution = body.get("resolution", "720p")
    if resolution not in RESOLUTIONS:
        errors.append(f"resolution {resolution!r} not in {sorted(RESOLUTIONS)}")
    aspect = body.get("aspect_ratio", "16:9")
    if aspect not in ASPECT_RATIOS:
        errors.append(f"aspect_ratio {aspect!r} not in {sorted(ASPECT_RATIOS)}")

    if "seed" in body and body["seed"] is not None:
        if not isinstance(body["seed"], int) or isinstance(body["seed"], bool):
            errors.append(f"seed must be an integer, got {body['seed']!r}")

    gen_audio = body.get("generate_audio", True)
    if not isinstance(gen_audio, bool):
        errors.append(f"generate_audio must be true/false, got {gen_audio!r}")

    # --- citation coherence ----------------------------------------------
    for kind, arr, name in (
        ("Image", ref_images, "reference_images"),
        ("Video", ref_videos, "reference_videos"),
        ("Audio", ref_audios, "reference_audios"),
    ):
        cited = _max_citation(prompt, kind)
        if cited > len(arr):
            errors.append(
                f"prompt cites [{kind}{cited}] but {name} has only "
                f"{len(arr)} entr{'y' if len(arr) == 1 else 'ies'}")
        if arr and cited == 0:
            warnings.append(
                f"{name} has {len(arr)} entr{'y' if len(arr) == 1 else 'ies'} "
                f"but the prompt never cites [{kind}1] — uncited references "
                f"are treated as a vague moodboard, not a directed input")

    # --- audio direction --------------------------------------------------
    if gen_audio and prompt and not AUDIO_WORDS.search(prompt):
        warnings.append(
            "generate_audio is on but the prompt has no audio direction — "
            "describe foreground SFX + ambient bed + score policy, or the "
            "model invents a generic cinematic score")

    # --- lip-sync needs a spoken line ------------------------------------
    if gen_audio and ref_audios and '"' not in (prompt or ""):
        warnings.append(
            "reference_audios is set (lip-sync) but the prompt has no "
            'double-quoted line — include the spoken words so the model '
            "gets semantic content, not just timing")

    # --- word budget ------------------------------------------------------
    wc = _word_count(prompt)
    if wc and wc < 120:
        warnings.append(
            f"prompt is {wc} words — under ~120 tends to render generic; "
            f"fine for a single simple shot, thin for multi-shot work")
    elif wc > 280:
        warnings.append(
            f"prompt is {wc} words — over ~280, prompts develop internal "
            f"contradictions; cut before you add")

    return errors, warnings


def _bodies_from(obj) -> list[tuple[str, dict]]:
    """Normalise input into a list of (label, body) pairs."""
    if isinstance(obj, list):
        out = []
        for i, item in enumerate(obj):
            label, body = _bodies_from(item)[0]
            out.append((label or f"job[{i}]", body))
        return out
    if isinstance(obj, dict) and "input" in obj and isinstance(obj["input"], dict):
        return [(obj.get("id", "job"), obj["input"])]
    return [("body", obj)]


def main() -> int:
    raw = (open(sys.argv[1]).read() if len(sys.argv) > 1
           else sys.stdin.read())
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON — {exc}")
        return 1

    total_errors = 0
    for label, body in _bodies_from(obj):
        errors, warnings = validate(body)
        total_errors += len(errors)
        status = "FAIL" if errors else ("WARN" if warnings else "PASS")
        print(f"[{status}] {label}")
        for e in errors:
            print(f"  ERROR   {e}")
        for w in warnings:
            print(f"  warning {w}")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
