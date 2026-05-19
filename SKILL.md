---
name: ai-video
description: >-
  Generate AI video of any kind, end to end — write the prompt, create
  first-frame stills, run the generation across six video models (Seedance
  2.0, Kling 3.0, Wan 2.7, Veo 3.1, OmniHuman 1.5, VEED Fabric), synthesize
  voiceover, stitch clips into a finished cut, and upscale for delivery. Use
  whenever the user wants to make or improve a video: cinematic shots,
  character dialogue, action, dance, native SFX, image-to-video, motion
  transfer, lip-sync, talking-avatar / "a video of me", real-person parody,
  abstract motion graphics, montages and stitched episodes. Builds prompts
  with the canonical 5-part structure + time-coded blocks, validates against
  the schema, quality-controls every clip, and learns from each run.
---

# AI video — generation, any kind

An end-to-end AI video skill: prompt craft → first-frame stills → generation
across six models → voiceover → edit/stitch → upscale, with a quality-control
loop that makes the skill improve over time. The ByteDance Seedance 2.0 schema
is the **canonical interchange format** — jobs are authored against it and the
runner translates to whichever model fits. Treat every clip as a miniature
production brief, not an image caption.

## Full pipeline

Not every job needs every stage — a single clip is just stages 2–4 — but this
is the shape of a complete video:

1. **Still** (`scripts/imagegen.py`) — generate a first-frame image or
   character reference plate (Flux / Imagen). Skip for pure text-to-video.
2. **Prompt** — build the request with the 5-part structure (Workflow below).
3. **Validate + generate** (`validate.py` → `generate.py`) — run on the
   auto-routed model; local refs auto-upload.
4. **QC + learn** (`review.py` → `LESSONS.md`) — watch the clip, score it,
   record a lesson. Mandatory.
5. **Voiceover** (`scripts/tts.py`) — synthesize narration (e.g. the user's
   cloned voice) when a clip or cut needs spoken audio.
6. **Assemble** (`scripts/assemble.py`) — stitch multiple clips into a
   finished video with cuts/crossfades and an audio bed.
7. **Finish** (`scripts/upscale.py`) — upscale resolution + interpolate fps
   for delivery.

## Workflow (a single generation)

0. **Read `LESSONS.md` first.** It is the skill's growing memory of what has
   and hasn't worked. Apply its lessons when building the prompt.

1. **Pick a production mode** (the choice drives everything else):

   | Mode | When | Reference inputs |
   |------|------|------------------|
   | Text-to-video | Tone piece, action, abstract — no source media | none |
   | Native dialogue | A character speaks; voice is generated | none (`generate_audio=true`) |
   | Native SFX | Sound-led showcase (ASMR, ambience) | none |
   | Image-to-video | Animate a still / first frame → last frame | `image` (+ `last_frame_image`) |
   | Character consistency | Same character/object across shots | `reference_images` ≤9 |
   | Motion transfer | Keep a video's motion, swap the subject | `reference_videos` + `reference_images` |
   | Lip-sync | Match a face to a real voice clip | `reference_audios` + `reference_images` |
   | Real-person episode | Founder/figure parody, stitched 30–80s | `reference_images` (6–9 face set) |

2. **Build the prompt.** Use the 5-part canonical structure, in this order —
   earlier tokens carry more weight:

   > **Subject → Action → Camera → Style → Constraints**

   - **Subject**: the visible thing + 2–3 concrete traits.
   - **Action**: one visible verb, not plot.
   - **Camera**: shot size, angle, lens, movement (name them — "35mm handheld
     push-in", not "cinematic").
   - **Style**: lighting, palette, film stock, director, medium.
   - **Constraints**: production rules that pre-empt failures ("no subtitles",
     "single continuous take", "hands resting naturally").

   For anything longer than one simple shot, use **time-coded blocks**
   `[00:00-00:05]` — Seedance reads them as hard editorial cuts and they
   re-anchor identity/wardrobe/palette every few seconds. A 15s clip is
   usually **3 shots**, not 7. For the category-specific theory and
   paste-ready examples, read `reference/prompt-logic.md` (10 categories).

3. **Assemble the request body** per `reference/schema.md`. Respect the
   exclusivity rules in §"Hard rules" below.

4. **Validate** before spending a generation:
   ```
   python scripts/validate.py request.json
   ```
   Fix every ERROR; consider every WARNING.

5. **Generate:**
   ```
   python scripts/generate.py job.json --out ./seedance_out [--fallback]
   ```
   `job.json` is `{"id": "...", "model": "auto", "input": { ...schema... }}`
   or an array of such jobs. Local file paths in any reference field are
   auto-uploaded. The model is auto-routed by intent (see §"Models" below) —
   set `"model"` or `--model` to override. `--fallback` retries
   classifier-flagged jobs on Kling.

6. **Quality control + learn** (mandatory — this is what makes the skill
   improve). See §"Quality control & self-improvement" below.

7. **Iterate only if asked.** Record the lesson regardless; **do not
   regenerate unless the user asks for it.** If they do, remove one demand
   before adding three. Most fixes are in `reference/failure-modes.md`.

## Models & auto-routing

Six runnable models, one schema. `generate.py` translates the canonical
Seedance body to whichever model is chosen. With `"model": "auto"` (default)
it routes by intent:

| Job signal | Routes to | Why |
|------------|-----------|-----|
| `reference_audios` set (lip-sync, in a scene) | `seedance-2.0` | audio-ref lip-sync inside a full generated scene |
| `reference_videos` set (motion transfer) | `seedance-2.0` | quad-modal references |
| ≥2 `reference_images` (character bible) | `seedance-2.0` | 9-image consistency |
| native dialogue / SFX, text-only | `seedance-2.0` | native synchronized audio |
| single-image image-to-video, no other refs | `wan-2.7-i2v` | open-weights, permissive, strong i2v |
| classifier-flagged on Seedance (`--fallback`) | `kling-3.0-omni` | different moderation gateway |

The full model set, and when to **`--model`-override** to one:

- **`seedance-2.0`** — the generalist; quad-modal, native audio, scene-aware.
- **`kling-3.0-omni`** — t2v + i2v with a different moderation gateway; pick
  it directly for i2v when Seedance won't pass moderation.
- **`wan-2.7-i2v`** — open-weights, permissive image-to-video specialist.
- **`veo-3.1`** — highest-realism cinematic text-to-video, native audio; the
  free Gemini key is rate-limited (~5/day).
- **`veed-fabric-1.0`** — dedicated **talking-video** model (face image +
  speech audio → lip-synced clip). Best for a clean talking head when you do
  not need Seedance to generate a whole scene around it.
- **`omnihuman-1.5`** — realistic **audio-driven avatar** (face image +
  speech audio, optional prompt → full-body-aware talking human). The
  strongest pure lip-sync/gesture realism; use for founder/presenter clips.

Rule of thumb for lip-sync: if the shot is a *scene* with a speaking
character, keep `seedance-2.0`; if it is *just a person talking* from a still
+ a voice clip, override to `omnihuman-1.5` (or `veed-fabric-1.0`). Both need
a `reference_images` (or `image`) face and a `reference_audios` clip. When you
override, tell the user which model and why.

## Personal profile — "a video of me"

When the request means the user themselves ("a video of me", "my avatar",
"in my voice", "me talking"), load `profile/profile.json` and use it. That
file is personal and git-ignored — if it is absent, the profile is not set
up: tell the user to copy `profile/profile.example.json` to `profile.json`
and fill in their avatar image, ElevenLabs voice id, and preferences.

- **Avatar** → use `avatar.image` as the `reference_images`/`image` face.
  Honour every rule in `avatar.rules` (identity 100% faithful; mic to the
  side, mouth unobstructed; stylized studio look).
- **Voice** → generate narration with `scripts/tts.py` (defaults to the
  profile's ElevenLabs voice id), then feed the MP3 as `reference_audios`.
- **Model** → default talking-avatar clips to `model_preferences.talking_avatar_default`
  (`wan-2.7-i2v`); use the alternate for gesture-rich wider frames. **Never
  use `veed-fabric-1.0`** for the user's avatar — see `model_preferences.avoid`
  and `LESSONS.md`.

## Quality control & self-improvement

Every generation ends with a QC pass — this is not optional, it is how the
skill gets better:

1. **Extract frames:** `python scripts/review.py CLIP.mp4 --job job.json`
   — writes a contact sheet + sampled frames + a probe to
   `seedance_out/review/<id>/`.
2. **Watch the clip.** `Read` the `contact_sheet.jpg` and the individual
   `frame_*.jpg` files. Check the probe (`duration`, `has_audio`,
   `resolution`) against what the job asked for.
3. **Score it.** Fill `qc_template.json` — rate prompt fidelity, subject
   consistency, camera/motion, audio match, overall (1–5); list any failure
   modes from `reference/failure-modes.md` you can see in the frames.
4. **Distill a lesson** and append it to `LESSONS.md` in the documented
   format — a generalizable cause→effect rule, not a clip description.
5. **Report** the QC verdict to the user. Only regenerate if they ask.

Because step 0 reads `LESSONS.md` back in, every future prompt is built on the
accumulated record of what worked. The loop closes without re-spending a
generation.

## Hard rules (the request cannot get these wrong)

- **Mutually exclusive modes.** `image` / `last_frame_image` **cannot** be
  combined with `reference_images`. `last_frame_image` requires `image`.
  `reference_audios` requires at least one image OR video reference.
- **Citations.** Cite attached media in the prompt as `[Image1]…[Image9]`,
  `[Video1]…[Video3]`, `[Audio1]…[Audio3]` — and give each a *purpose*
  ("[Image1] defines face and hairline; [Image5] defines wardrobe"), never a
  bare mention.
- **Dialogue** goes in `"double quotes"` with `generate_audio=true`. Lead with
  emotional tone ("she whispers, trying not to cry") before the line. Keep
  lines 4–10 words.
- **Audio direction is mandatory** when `generate_audio=true`. Describe
  foreground SFX + ambient bed + score policy ("no music"), or the model
  invents a generic cinematic score.
- **Duration**: integer 4–15 or `-1` (auto). Safe set is `{4,5,6,8,10,12,15}`
  — avoid 7/9/11/13/14 (some endpoints silently reject them).
- **No negative-prompt field.** Encode exclusions as positive instructions
  ("hands resting in lap" > "no bad hands"), plus a short tail of direct
  negatives ("no subtitles, no on-screen text, no watermarks").
- **Word budget**: 50–90 for single shots, 120–280 for multi-shot/multimodal.
  Above 280, prompts develop internal contradictions.
- **Resolution** `480p|720p|1080p`; **aspect_ratio** `16:9|4:3|1:1|3:4|9:16|21:9|9:21|adaptive`.
  9:16 favors close-ups, 16:9 establishing wides, 21:9 epic scale, 1:1 product/loop.

## Reference files (load on demand)

- `reference/schema.md` — canonical Replicate schema, every field, gotchas.
- `reference/prompt-logic.md` — 10 prompt categories, theory + 3 perfect
  prompts each (cinematic, dialogue, action, dance, SFX, character
  consistency, motion transfer, lip-sync, real-person, abstract).
- `reference/style-library.md` — cross-model camera/lens/lighting/director
  vocabulary that transfers to Seedance prose.
- `reference/real-person.md` — Silicon Mania anatomy, the 4 production stacks,
  consent norms, paste-ready figure prompts.
- `reference/failure-modes.md` — the 15 failure modes + fixes + the
  classifier-flag escalation path.
- `examples/prompts.json` — verified prompt library, filterable by intent.

## Scripts

- `scripts/imagegen.py` — generate first-frame stills / reference plates
  (Flux Schnell, Flux Pro, Imagen 4).
- `scripts/validate.py` — stdlib-only; validates a request body against schema
  + exclusivity rules. Run before every generation.
- `scripts/generate.py` — runs a job on any of the six video models, uploads
  local refs, downloads clips, writes a manifest; `--fallback` routes
  classifier-flagged jobs to Kling.
- `scripts/review.py` — extracts a frame contact sheet + probe for the QC pass.
- `scripts/tts.py` — ElevenLabs text-to-speech; defaults to the profile voice.
- `scripts/assemble.py` — stitches clips into a finished cut (ffmpeg) with
  cuts/crossfades + an audio bed, from a JSON edit list.
- `scripts/upscale.py` — finishing pass: upscale + frame interpolation
  (local ffmpeg by default, optional Replicate ML upscaler).
- `scripts/requirements.txt` — `pip install -r` for `replicate` + `fal-client`.
  `imagegen.py`/`tts.py`/`veo-3.1` use stdlib only; `review.py`, `assemble.py`
  and `upscale.py` need `ffmpeg` + `ffprobe` on PATH.
- `profile/profile.json` — the user's avatar + voice + model preferences.

## Environment

Read API keys from the environment — never print key values:

- `REPLICATE_API_TOKEN` — seedance-2.0, wan-2.7-i2v, Flux stills, ML upscale
- `FAL_KEY` — kling-3.0-omni, veed-fabric-1.0, omnihuman-1.5
- `GEMINI_API_KEY` — veo-3.1, Imagen 4 stills
- `ELEVENLABS_API_KEY` — tts.py voiceover

Only the models actually used need their key. These live in the user's
global config.

## Real-person policy

Seedance is the most permissive major model, but real-person work is always
policy-sensitive. Only build workflows around **public figures in legitimate
commentary/satire** or **tagged, consenting collaborators**. No undisclosed
impersonation of private individuals. Respect voice-provider No-Go lists when
sourcing reference audio. See `reference/real-person.md`.
