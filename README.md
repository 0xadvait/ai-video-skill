<div align="center">

# ai-video 🎬

**The AI video skill that learns.**

End-to-end video generation for [Claude Code](https://claude.com/claude-code) — across six models, from prompt to finished cut. It quality-controls every clip it makes, and gets better at prompting with each one.

![Claude Code](https://img.shields.io/badge/Claude%20Code-skill-d97757)
![Models](https://img.shields.io/badge/video%20models-6-1342ff)
![Pipeline](https://img.shields.io/badge/pipeline-7%20stages-fb6a59)
![Python](https://img.shields.io/badge/python-3.10%2B-3776ab)

</div>

---

Most AI-video tooling stops at "here's your clip." ai-video doesn't. Every
generation ends with a **quality-control pass** — Claude watches the rendered
clip, scores it against the prompt, and writes down what it learned. That
lesson is loaded back in before the next prompt is written. The skill is not
static; it compounds.

It also covers the *whole* job, not just the model call: generate a first
frame, write the prompt, run it on the right model, synthesize voiceover,
stitch the clips, upscale for delivery.

## Features

<table>
<tr>
<td width="50%"><b>🧠 Self-improving</b><br/>A built-in QC loop watches each clip and appends a prompting lesson to <code>LESSONS.md</code>. Every future prompt builds on it.</td>
<td width="50%"><b>🎥 Six models, one schema</b><br/>Seedance 2.0, Kling 3.0, Wan 2.7, Veo 3.1, OmniHuman 1.5, VEED Fabric — authored once, auto-routed by intent.</td>
</tr>
<tr>
<td><b>🪄 Full pipeline</b><br/>Image gen → prompt → generate → QC → voiceover → stitch → upscale. A single clip or a stitched episode.</td>
<td><b>📐 Real prompt craft</b><br/>The canonical 5-part structure, time-coded blocks, a 10-category prompt library, and a 15-entry failure-mode catalog.</td>
</tr>
<tr>
<td><b>🔁 Multimodal</b><br/>Character consistency, motion transfer, lip-sync, talking avatars — first-class, with schema validation before every spend.</td>
<td><b>🙂 "A video of me"</b><br/>A personal profile wires your avatar + cloned voice into any request. Stays local, never committed.</td>
</tr>
</table>

## Install

```bash
git clone https://github.com/0xadvait/ai-video-skill.git ~/.claude/skills/ai-video
pip install -r ~/.claude/skills/ai-video/scripts/requirements.txt
```

`ffmpeg` + `ffprobe` must be on `PATH` (frame QC, stitching, upscaling). The
skill activates automatically — just ask Claude Code to make a video.

> **Heads up:** API keys are read from the environment. You only need a key
> for the models you actually call (see [Environment](#environment)).

## The pipeline

A single clip needs only stages 2–4. A finished video runs the whole chain.

| # | Stage | Script | What it does |
|:-:|-------|--------|--------------|
| 1 | **Still** | `imagegen.py` | First-frame / reference images — Flux Schnell, Flux Pro, Imagen 4 |
| 2 | **Prompt** | `SKILL.md` + `reference/` | 5-part structure (Subject→Action→Camera→Style→Constraints) + time-coded blocks |
| 3 | **Generate** | `validate.py` → `generate.py` | Validate the request, run on the auto-routed model |
| 4 | **QC + learn** | `review.py` → `LESSONS.md` | Watch the clip, score it, record a prompting lesson |
| 5 | **Voiceover** | `tts.py` | ElevenLabs text-to-speech narration |
| 6 | **Assemble** | `assemble.py` | Stitch clips — cuts/crossfades + audio bed — from a JSON edit list |
| 7 | **Finish** | `upscale.py` | Upscale resolution + interpolate frame rate |

## Models

One canonical schema (Seedance 2.0's). `generate.py` translates it to whichever
model is chosen — `"model": "auto"` (default) routes by intent.

| Model | Backend | Best for |
|-------|---------|----------|
| `seedance-2.0` | Replicate | Generalist — quad-modal refs, native audio, lip-sync, motion transfer |
| `kling-3.0-omni` | fal | t2v / i2v with a different moderation gateway (the `--fallback`) |
| `wan-2.7-i2v` | Replicate | Open-weights image-to-video |
| `veo-3.1` | Google Gemini | Highest-realism cinematic text-to-video |
| `omnihuman-1.5` | fal | Audio-driven talking avatar, gesture-rich |
| `veed-fabric-1.0` | fal | Mouth-only lip-sync — included, but see `LESSONS.md` |

## The learning loop

This is the part that makes it more than a wrapper:

```
prompt ──▶ generate ──▶ review.py ──▶ Claude watches the clip
   ▲                                          │
   │                                          ▼
LESSONS.md ◀────────────── distill a generalizable lesson
```

`review.py` extracts a frame contact sheet; Claude scores the clip on prompt
fidelity, consistency, motion, and audio; a one-line cause→effect lesson is
appended to `LESSONS.md`. Step 0 of every workflow reads `LESSONS.md` back in.
**No regeneration is needed for the skill to improve** — clips are only re-run
when you ask.

## Documentation

| File | What's inside |
|------|---------------|
| [`SKILL.md`](SKILL.md) | The workflow, model routing, QC loop, hard rules |
| [`LESSONS.md`](LESSONS.md) | Seed lessons + the skill's growing memory |
| [`reference/schema.md`](reference/schema.md) | Canonical Seedance 2.0 request schema |
| [`reference/prompt-logic.md`](reference/prompt-logic.md) | 10 prompt categories, theory + perfect examples |
| [`reference/style-library.md`](reference/style-library.md) | Cross-model camera / lens / lighting / director vocabulary |
| [`reference/real-person.md`](reference/real-person.md) | Real-person workflow + production stacks |
| [`reference/failure-modes.md`](reference/failure-modes.md) | 15 failure modes and their fixes |
| [`examples/prompts.json`](examples/prompts.json) | 30 verified, paste-ready prompts |

## Environment

| Variable | Used by |
|----------|---------|
| `REPLICATE_API_TOKEN` | seedance-2.0, wan-2.7-i2v, Flux stills, ML upscale |
| `FAL_KEY` | kling-3.0-omni, veed-fabric-1.0, omnihuman-1.5 |
| `GEMINI_API_KEY` | veo-3.1, Imagen 4 stills |
| `ELEVENLABS_API_KEY` | `tts.py` voiceover |

## Personal profile

The "a video of me" shortcut uses a personal profile. Copy the template and
fill in your own assets:

```bash
cp profile/profile.example.json profile/profile.json
```

`profile.json` is git-ignored — your avatar paths and voice id never leave
your machine.

## A note on real-person video

Real-person generation is policy-sensitive. Only build around **public
figures in legitimate commentary or satire**, or **consenting, tagged
collaborators** — never undisclosed impersonation of private individuals.
Respect voice-provider restrictions when sourcing reference audio. See
[`reference/real-person.md`](reference/real-person.md).

---

<div align="center">

Built from the [ai-video-guide](https://github.com/0xadvait/ai-video-guide) research corpus.

🎬 Generated with [Claude Code](https://claude.com/claude-code)

</div>
