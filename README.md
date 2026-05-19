# ai-video

A [Claude Code](https://claude.com/claude-code) skill for **end-to-end AI
video generation** — write the prompt, create first-frame stills, run the
generation across six video models, synthesize voiceover, stitch clips into a
finished cut, upscale for delivery — with a quality-control loop that makes
the skill *improve over time*.

Built from the [ai-video-guide](https://github.com/0xadvait/ai-video-guide)
research corpus (a deep Seedance 2.0 prompting manual + cross-model craft
library).

---

## Install

Clone into your Claude Code skills directory:

```bash
git clone git@github.com:0xadvait/ai-video-skill.git ~/.claude/skills/ai-video
pip install -r ~/.claude/skills/ai-video/scripts/requirements.txt
```

`ffmpeg` + `ffprobe` must be on `PATH` (used by `review.py`, `assemble.py`,
`upscale.py`). The skill activates automatically whenever you ask Claude Code
to make or improve a video.

## The pipeline

A single clip needs only stages 2–4; a finished video runs the whole chain.

| # | Stage | Script | What it does |
|---|-------|--------|--------------|
| 1 | Still | `imagegen.py` | First-frame / reference images — Flux Schnell, Flux Pro, Imagen 4 |
| 2 | Prompt | `SKILL.md` + `reference/` | 5-part structure (Subject→Action→Camera→Style→Constraints) + time-coded blocks |
| 3 | Generate | `validate.py` → `generate.py` | Validate the request, run on the auto-routed model |
| 4 | QC + learn | `review.py` → `LESSONS.md` | Watch the clip, score it, record a prompting lesson |
| 5 | Voiceover | `tts.py` | ElevenLabs text-to-speech narration |
| 6 | Assemble | `assemble.py` | Stitch clips — cuts/crossfades + audio bed — from a JSON edit list |
| 7 | Finish | `upscale.py` | Upscale resolution + interpolate frame rate |

## Models

One canonical schema (Seedance 2.0's); `generate.py` translates it to whichever
model is chosen. `"model": "auto"` (the default) routes by intent.

| Model | Backend | Best for |
|-------|---------|----------|
| `seedance-2.0` | Replicate | Generalist — quad-modal refs, native audio, lip-sync, motion transfer |
| `kling-3.0-omni` | fal | t2v/i2v with a different moderation gateway (the `--fallback`) |
| `wan-2.7-i2v` | Replicate | Open-weights image-to-video |
| `veo-3.1` | Google Gemini | Highest-realism cinematic text-to-video |
| `omnihuman-1.5` | fal | Audio-driven talking avatar, gesture-rich |
| `veed-fabric-1.0` | fal | Mouth-only lip-sync (included; see `LESSONS.md`) |

## Self-improvement loop

Every generation ends with a QC pass: `review.py` extracts a frame contact
sheet, Claude watches the clip and scores it, and a distilled lesson is
appended to **`LESSONS.md`**. Step 0 of the workflow reads `LESSONS.md` back
in — so every future prompt is built on the accumulated record of what worked.
The loop closes without re-spending a generation; clips are only regenerated
when you ask.

## Layout

```
ai-video/
├── SKILL.md              workflow, model routing, QC loop, hard rules
├── LESSONS.md            the skill's growing prompting memory
├── reference/            schema, prompt-logic (10 categories), style library,
│                         real-person workflow, failure-mode catalog
├── examples/prompts.json 30 verified, paste-ready prompts
├── profile/              profile.example.json — copy to profile.json (local)
└── scripts/              imagegen · validate · generate · review · tts ·
                          assemble · upscale
```

## Environment

API keys are read from the environment — only the models you use need a key:

| Variable | Used by |
|----------|---------|
| `REPLICATE_API_TOKEN` | seedance-2.0, wan-2.7-i2v, Flux stills, ML upscale |
| `FAL_KEY` | kling-3.0-omni, veed-fabric-1.0, omnihuman-1.5 |
| `GEMINI_API_KEY` | veo-3.1, Imagen 4 stills |
| `ELEVENLABS_API_KEY` | `tts.py` voiceover |

## Notes

- The "a video of me" shortcut uses a personal profile. Copy
  `profile/profile.example.json` to `profile/profile.json` and fill in your
  avatar image, ElevenLabs voice id, and preferences. `profile.json` is
  git-ignored — your personal config never leaves your machine.
- Real-person video is policy-sensitive — only build around public figures in
  legitimate commentary/satire or consenting, tagged collaborators. See
  `reference/real-person.md`.

---

Generated with [Claude Code](https://claude.com/claude-code).
