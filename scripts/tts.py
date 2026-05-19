#!/usr/bin/env python3
"""Synthesize speech with ElevenLabs — the voice half of "a video of me".

Generates an MP3 from text using a cloned voice, ready to hand to a
talking-avatar / lip-sync model as reference audio. Defaults to Advait's
cloned voice from profile/profile.json.

Usage:
    python tts.py "the line to speak" [--out speech.mp3] [--voice VOICE_ID]
    python tts.py --file script.txt --out narration.mp3

Env: ELEVENLABS_API_KEY (also accepts ELEVEN_API_KEY).
Output is MP3 44.1kHz — the format talking-avatar models expect.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
PROFILE = SKILL_ROOT / "profile" / "profile.json"
MODEL_ID = "eleven_multilingual_v2"


def default_voice_id() -> str | None:
    try:
        return json.loads(PROFILE.read_text())["voice"]["elevenlabs_voice_id"]
    except Exception:  # noqa: BLE001
        return None


def synthesize(text: str, out: Path, voice_id: str) -> None:
    key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_API_KEY")
    if not key:
        sys.exit("ERROR: ELEVENLABS_API_KEY is not set")
    url = (f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
           f"?output_format=mp3_44100_128")
    payload = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.85},
    }).encode()
    req = urllib.request.Request(
        url, data=payload, method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json",
                 "Accept": "audio/mpeg"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            out.write_bytes(r.read())
    except urllib.error.HTTPError as e:  # noqa
        sys.exit(f"ERROR: ElevenLabs {e.code} — {e.read().decode()[:300]}")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB) "
          f"via voice {voice_id}")


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    text = None
    out = Path("speech.mp3")
    voice_id = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--out":
            out = Path(args[i + 1]); i += 2
        elif a == "--voice":
            voice_id = args[i + 1]; i += 2
        elif a == "--file":
            text = Path(args[i + 1]).read_text(); i += 2
        elif not a.startswith("--"):
            text = a; i += 1
        else:
            print(f"unknown flag {a}"); return 1

    if not text or not text.strip():
        print("ERROR: no text given"); return 1
    voice_id = voice_id or default_voice_id()
    if not voice_id:
        print("ERROR: no voice id (pass --voice or fix profile.json)"); return 1

    out.parent.mkdir(parents=True, exist_ok=True)
    synthesize(text.strip(), out, voice_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
