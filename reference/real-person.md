# Real-Person / Public-Figure Video Workflow

This document describes the practical, end-to-end workflow for creators producing short-form video that features recognizable public figures (CEOs, politicians, athletes, actors) saying or doing specific things — the format pioneered by accounts like [@siliconmania](https://x.com/siliconmania) on X and the broader genre of AI-assisted tech satire and commentary. The focus is on what creators actually do to ship a clip, with Seedance 2.0 as the central engine and the rest of the stack scaffolded around it.

The schema reference for Seedance 2.0 throughout this doc is [`reference/schema.md`](schema.md). The canonical citation syntax in the prompt is **`[Image1]`, `[Video1]`, `[Audio1]`** (square brackets) — many third-party guides use `@image1`, but the Replicate input schema uses brackets, which is what we use below.

---

## Silicon Mania case study (what makes their format work)

**The account.** Silicon Mania ([@siliconmania](https://x.com/siliconmania), 21.3K followers as of 2026-05-04, joined Sept 2025) is run by the Silicon Mania team out of San Francisco. The bio is "the most entertaining tech media ever" and the running tagline is "make tech fun again." The broader studio work is openly built on a stack of Google Veo 3.1, Kling 3.0, and Seedance 2.0 ([siliconmania.tv](https://www.siliconmania.tv/)).

**The reference clip.** The pinned post the user linked ([x.com/siliconmania/status/2049671342136713651](https://x.com/siliconmania/status/2049671342136713651), posted 2026-04-29) is a 79-second tech-week recap captioned "last week in tech was looksmaxxed." Engagement at time of analysis: 2,078 likes / 188 reposts / 151K views / 436 bookmarks — typical for the channel. The video itself is `1906x1080`, served from `video.twimg.com/amplify_video/...`. The follow-up clip pinned 16h before this fetch is "guy pitches his AI generated movie to investor" — a recurring "The Buzzer" segment with named guest founder/investor avatars ([@sathaxe](https://x.com/sathaxe), [@maximusgrave](https://x.com/maximusgrave)).

**Format anatomy (what to copy).**

1. **Cold open in 1.5s.** A jolt — usually a recognizable face mid-sentence, mid-action, or a chyron with a punchline. No logo intro, no title card. The hook is the face plus the line.
2. **Shots are 2–6 seconds each.** This is below Seedance's 4–15s window, which means individual generations get *trimmed* in post — important for continuity strategy below. Total clip lengths cluster around 45–90s.
3. **Composition is tight.** ~80% of shots are medium close-up (chest-up) or close-up. Locked-off camera or slow dolly. This isn't accidental — Seedance's lip-sync is most reliable on locked, front-or-three-quarter framing ([Cutout.pro audio guide](https://www.cutout.pro/learn/blog-seedance-2-0-audio-guide/)). Profile angles are avoided.
4. **One personality per shot.** When two figures "interact," it's almost always cross-cut singles, not a two-shot. Two-shots are harder to keep on-model and harder to lip-sync; cross-cuts let each shot use its own dedicated reference set.
5. **Consistent grade.** Across a single video the color treatment is stable — slightly desaturated, blue-magenta shadow tilt, a hint of film grain. This is added in post (DaVinci/Premiere/CapCut LUT) so that mismatched generations match each other.
6. **Music + SFX layer.** Beds are subtle. Whoosh transitions, room-tone fills, occasional needle-drop. Music is low (~-22 LUFS) under dialogue.
7. **Dialogue is short.** Lines are 4–10 words. This is exactly what lip-sync engines handle reliably. Long monologues are split into multiple shots with cutaways.
8. **B-roll cutaways break sync risk.** When a line is too long for one Seedance shot, the back half plays over a cutaway (logo, building exterior, a chyron, an unrelated AI-generated insert) — same audio continues, picture is no longer a face, no lip-sync to fail.

There is no public step-by-step "how I make these" thread, but the visible production pattern and studio materials point to a Veo 3.1 + Kling 3.0 + Seedance pipeline.

---

## Voice sourcing & cloning

For "real person speaking" content, voice is half the job. The dominant pattern:

**Source material.** Public-figure voice samples are scraped from public, on-the-record material: keynote talks (YouTube), conference panels, podcast interviews (Lex Fridman, Joe Rogan, Acquired, All-In, Dwarkesh), shareholder calls, press conferences, post-game interviews. Rule of thumb is **5–10 minutes of clean audio per voice** if you only need short lines, **30 minutes minimum** for ElevenLabs *Professional Voice Cloning* and **2–3 hours** for the highest-quality clone ([ElevenLabs PVC docs](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning)). For *Instant Voice Cloning*, 1–2 minutes of pristine audio is usable.

**Audio prep.** Before you upload, you isolate the speaker (vocal-only stem with a tool like Adobe Enhance, ElevenLabs Voice Isolator, or iZotope RX), clip out applause/host interjections, normalize to -6 dBFS, and export 48kHz 24-bit WAV ([CrePal lip-sync guide](https://crepal.ai/blog/aivideo/blog-seedance-2-0-lip-sync-voiceover-fix/)). Garbage in, garbage out — a clone trained on a poor source will hiss and slur on every line you generate.

**Cloning tools (May 2026 landscape).**

- **ElevenLabs** is the default for English. PVC is the gold standard. Caveat: ElevenLabs maintains a "No-Go Voices" list that explicitly blocks voices of active political figures (especially during US/UK election cycles) and high-risk celebrities ([ElevenLabs Use Policy](https://elevenlabs.io/use-policy), [ElevenLabs Safety](https://elevenlabs.io/safety)). Their Prohibited Use Policy bans cloning a voice without consent or legal right. For tech-CEO commentary this is enforced inconsistently; expect Tier-1 names (Trump, Biden, Musk in some windows) to be blocked at upload.
- **Resemble AI** — similar quality, a bit more permissive on enterprise tier. Used for less mainstream voices.
- **PlayHT** — fast, decent, weaker on emotion. Good for utility lines.
- **OpenAI Voice (Voice Engine)** — limited rollout, gated. Not in most creator workflows.
- **Hume** — emotionally expressive, useful for reaction shots where a cloned line needs anger or excitement that the source material didn't contain.

**Quality benchmarks.** A "good" clone reads as the person on a 4-second line at first listen and on a 10-second line at second listen. Lines longer than ~12 words start to drift in cadence even on a great clone. Practical solve: write *short* lines that match the figure's known speech patterns. For Sam Altman that means quiet, hedged, technical; for Zuck, flatter affect, "uh"-stuffed; for Elon, halting, longer pauses, lower pitch.

**Legal posture.** Public figures in the context of news commentary, satire, and parody have a long tradition of being depicted (SNL, The Daily Show, etc.). The legal exposure is platform-policy first, defamation/right-of-publicity second. Practical mitigations creators use: clear "this is AI / parody" framing in caption or chyron, no commercial endorsement claims, no fabricated specific factual claims that could damage reputation. **None of this is legal advice; it is the documented behavioral norm.**

---

## Face reference set best practices

Seedance 2.0 accepts **up to 9 reference images** cited as `[Image1]…[Image9]`. Reference images can be combined with reference audios for lip-sync, but **not** with `image`/`last_frame_image` (that's first-frame-image-to-video mode — mutually exclusive per the schema).

**The "character bible" pattern.** For a recognizable figure, build a 6–9 image set:

1. **Front, neutral expression, mouth closed.** Eye-level, centered, head fills middle 50% of frame.
2. **Front, slight smile, mouth slightly open.** This is the **lip-sync calibration frame** — gives the model a clean phoneme reference.
3. **Three-quarter left, neutral.**
4. **Three-quarter right, neutral.**
5. **Profile (left or right).** Use one, not both — profiles are the least reliable for the model and you don't want to over-weight that geometry.
6. **Wide / waist-up.** Establishes body proportions and default wardrobe.
7. **Different lighting condition** that matches your target shot lighting (e.g., warm interior if your scene is a podcast set; cool fluorescent if your scene is a courtroom).
8. **Wardrobe-anchor frame.** The exact outfit you want them wearing in the generated shot. Even if Image 1 is the "real" them, this image overrides clothing.
9. **Optional: gesture / pose reference.** Hands visible, arm position you want.

**Sourcing.** Image sources are public press photos, conference photography (TechCrunch, Bloomberg, Getty for selection — not redistribution), Wikipedia/Wikimedia Commons (license-clean), and screen-captured frames from interview video. Goal: ≥1024px on the short edge, no heavy compression, even lighting, no extreme shadow.

**Practical floor.** You can get a recognizable figure from **2 references** (front + 3/4) if the figure is iconic, but quality and lip-sync accuracy improves materially up to about 5–6 references. Diminishing returns past 7. Cite them in the prompt explicitly: `"...the man's face strictly follows [Image1], wardrobe from [Image8]..."` — the model treats unreferenced images as ambient style hints, not as identity locks.

**Important: Seedance 2.0's "Real Human" verification.** ByteDance's first-party tooling (and ComfyUI's `ByteDance Create Image/Video Asset` node) implements a **liveness check** before a real person can appear in generations — you upload a portrait, get a verification link, and the actual person completes a phone-or-browser liveness check ([ComfyUI Real-Human docs](https://docs.comfy.org/tutorials/partner-nodes/bytedance/seedance-2-0-real-human), [Comfy blog](https://blog.comfy.org/p/unlock-seedance20-real-human-video-generation)). This is the official path and obviously requires the actual person's cooperation. The Replicate `bytedance/seedance-2.0` endpoint does not surface this verification step in its public schema and currently accepts arbitrary `reference_images` URIs — but it does run server-side safety classifiers that reject some uploads. Expect this gate to tighten over time. Silicon Mania-style commentary work plausibly uses a mix: native Seedance for non-face-recognizable shots, and the Sora 2 / Veo 3.1 / Kling pipeline (or pre-render then external lip-sync) for the figure-identifiable shots.

---

## End-to-end production stacks (A–D, compared)

### Stack A — Seedance 2.0 native (fewest steps)

**When it works:** the figure isn't on aggressive guardrail lists, you have a clean 5–9 image reference set, you have a clean voice clip (≤15s total) for `reference_audios`, and the line is short.

**Steps:**
1. Build the 9-image character bible (above). Host on a CDN that returns direct URIs (S3, Replicate uploads, Cloudflare R2).
2. Generate or clone a voice line in ElevenLabs. Trim to ≤15s. Re-encode to a Seedance-friendly format (mp3 or wav).
3. Single Replicate call:
   ```
   prompt: '<scene description>. The man\'s face and identity strictly follow [Image1], [Image2], [Image3]. Wardrobe matches [Image8]. He says "<short line>", lip-sync aligned with [Audio1]. Locked medium close-up, soft key from camera-left, shallow depth of field.'
   reference_images: [img1.jpg, ..., img9.jpg]
   reference_audios: [voice.mp3]
   duration: 6
   resolution: 1080p
   aspect_ratio: 9:16
   generate_audio: true
   ```
4. ~115s wall time per generation. Re-roll up to 2x with seed changes if lip-sync misses.

**Pros:** one API, one wall-clock, native audio, lip-sync inside the model.
**Cons:** lip-sync quality on long lines lags dedicated tools; identity drift on profile turns; subject to the ByteDance verification policy hardening.

### Stack B — Seedance 2.0 (silent) → Sync.so or Hedra → ElevenLabs voice

**When it works:** you want maximum lip-sync quality, you're willing to pay the extra render and seconds, or your line is too long for Seedance's audio path.

**Steps:**
1. Generate the shot in Seedance with `generate_audio: false` and **no** `reference_audios`. Just the visual — the figure on-screen, mouth doing some neutral talking-head motion. Duration 8–12s.
2. Generate the audio line in ElevenLabs (the cloned voice).
3. Run the Seedance MP4 + the ElevenLabs WAV through **[Sync.so](https://sync.so)** (best raw lip-sync accuracy, language-agnostic, ~$0.10–0.30/sec) or **[Hedra Character-3](https://www.hedra.com/blog/ai-lip-sync-video-guide)** (better at expressive face animation, weaker on naturalistic talking heads).
4. Export the lip-synced result.

**Pros:** lip-sync is noticeably better than Seedance's native sync on hard lines (long, fast, contractions, emotional). Voice is 100% under your control.
**Cons:** two extra API calls, two extra wall-clocks, a small risk of mouth-region softening on Sync's output that needs a touch-up.

### Stack C — Image-gen first → Seedance image-to-video → external lip-sync

**When it works:** you need a *very specific* opening frame the model isn't giving you reliably with reference_images alone (e.g., a precise composition, a specific gesture, a particular environment), or the figure is recognizable enough that a hand-curated frame is more reliable than 9 references.

**Steps:**
1. Use Flux 1.1 Pro / Flux Kontext / Imagen 4 / Nano Banana 2 to generate a single still — the figure in the exact composition you want. Identity transfer via Flux + PuLID workflows ([RunComfy Flux-PuLID](https://www.runcomfy.com/comfyui-workflows/flux-kontext-pulid-consistent-character-generation)) gets a recognizable face from one good source photo.
2. Feed that still as Seedance's `image` input (image-to-video mode). Note: this **excludes** `reference_images`.
3. Prompt the motion ("he turns to the camera and speaks").
4. `generate_audio: false`, then external lip-sync as Stack B.

**Pros:** dictate composition exactly. Useful for matching a real news photo.
**Cons:** lose the multi-reference identity lock; identity comes purely from the one curated frame; more steps.

### Stack D — Sora 2 / Veo 3.1 cameo features (the "official path")

**Sora 2 cameos.** OpenAI restricts public-figure depiction unless that figure has opted in via the Cameo system (a one-time video+audio capture, the figure controls who can use them) ([OpenAI launching Sora responsibly](https://openai.com/index/launching-sora-responsibly/), [OpenAI characters help](https://help.openai.com/en/articles/12435986-generating-content-with-characters)). After backlash in late 2025, Sora hard-blocks non-opted-in public figures ([Newsweek](https://www.newsweek.com/sora-2-openai-bans-celebrity-deepfakes-but-people-found-loophole-10912528)). Sora's 25s storyboard mode is the longest single-generation among major models.

**Veo 3.1.** Google blocks named public figures in the prompt and has aggressive image-conditioning safety classifiers — geo-gated stricter in EU/UK ([Google AI Developers Forum thread](https://discuss.ai.google.dev/t/so-google-veo-wont-let-me-use-images-of-realistic-people-because-i-am-in-england-even-though-the-images-are-generated-using-an-ai-so-they-are-not-real-people/98350)). Veo's appeal in this stack is broadcast-grade output (true 4K, cinema frame rate, top-tier native audio).

**Seedance vs. Sora-2/Veo for this use case.**
| Capability | Seedance 2.0 | Sora 2 | Veo 3.1 |
|---|---|---|---|
| Reference images | up to 9 | 1 | image + "ingredients" |
| Reference audio for lip-sync | yes (≤3, ≤15s) | no (uses cameo voice) | no public api |
| Public-figure policy | server-side classifiers, real-human verification path | hard-blocked unless cameo | hard-blocked, geo-stricter |
| Native audio | yes (dialogue + SFX + score) | yes | yes |
| Max single-clip duration | 15s | 25s (storyboard) | 8s typical |
| Resolution ceiling | 1080p | 1080p | 4K |

For a Silicon Mania-style satirical channel, **Seedance is the most permissive and the most reference-rich** — which is exactly why creators converge on it for figure-identifiable shots, and use Sora/Veo for B-roll, environments, crowds, and original characters.

---

## Prompt patterns library (paste-ready Seedance 2.0 prompts)

These assume `reference_images` is populated with a 6–9 image character bible per figure, and (where audio is cited) `reference_audios` contains a clean voice clip ≤15s. Citation syntax follows the canonical schema (square brackets).

### 1. CEO giving a quote at a conference

```
Medium close-up of the man on stage in a black t-shirt, soft stage key light from camera-left, blurred conference audience in background. His face and identity strictly follow [Image1], [Image2], [Image3]; wardrobe matches [Image7]. He looks slightly off-camera and says "we are not building a chatbot, we are building a coworker." Lip-sync aligned with [Audio1]. Locked tripod shot, shallow depth of field, 35mm look, subtle ambient room tone, no music. 8 seconds.
```

### 2. Politician walking down a hallway (B-roll, no dialogue, ambient only)

```
Tracking shot from behind, low angle, the woman in a navy pantsuit walks briskly down a marble Capitol-style hallway, two aides slightly behind her. Identity from [Image1], [Image2], [Image4]; wardrobe from [Image8]. Camera dollies forward at her pace. Late-afternoon window light streaks across the polished floor. Footsteps echo, distant murmurs, no music, no dialogue. 6 seconds, locked focus on her shoulders.
```

### 3. Athlete reacting in a locker room

```
Close-up of the basketball player on a wooden bench in a dim NBA locker room, towel around his neck, breathing hard, sweat on his temples. Face strictly follows [Image1], [Image2], [Image3]; jersey from [Image6]. He looks down, then up at the camera and says "we'll be back tomorrow." Lip-sync aligned with [Audio1]. Locked medium close-up, single overhead practical light, deep shadows on the lockers behind, faint air-handler hum. 7 seconds.
```

### 4. Two real people in conversation (cross-cut, two generations)

Generate as **two single-coverage shots**, not a two-shot. Cut them together in NLE.

Shot A (Person 1):
```
Medium close-up of the man across a small podcast desk, single condenser mic in foreground, warm key light from camera-right. Identity follows [Image1], [Image2], [Image3]. He leans in slightly and says "you didn't actually read the paper, did you?" Lip-sync aligned with [Audio1]. Locked, shallow DoF, dim studio bokeh behind. 6 seconds.
```

Shot B (Person 2 — different reference set, different audio):
```
Reverse medium close-up of the second man at the same podcast desk, his side of the same warm key light now from camera-left, matching dim bokeh background. Identity follows [Image1], [Image2], [Image3]. He smirks, looks up, and says "I read the abstract." Lip-sync aligned with [Audio1]. Locked, shallow DoF, matching color temperature. 6 seconds.
```

### 5. Real person reacting to a news headline (TV-on-screen reaction)

```
Medium shot of the man on a couch in a softly lit living room at night, glow of an off-screen TV flickering blue across his face. Identity from [Image1], [Image2], [Image4]; outfit from [Image8] (gray hoodie). He stares forward, expression hardening, shakes his head once and mutters "they actually did it." Lip-sync aligned with [Audio1]. Locked tripod, 50mm, faint TV news murmur in the background, no music. 8 seconds.
```

### 6. CEO at a product launch — keynote wide

```
Wide shot of the man center-stage on a black-floor keynote stage, single product silhouette behind him, audience silhouettes in foreground. Identity from [Image1], [Image2], [Image5]; wardrobe from [Image7]. He raises both arms and says "one more thing." Lip-sync aligned with [Audio1]. Slow push-in from a 12m distance to a 6m distance, cinematic 24fps, low ambient murmur, no music. 9 seconds.
```

### 7. Politician at a press gaggle — handheld documentary

```
Handheld medium shot, slight shoulder shake, the man being walked through a hotel lobby past a wall of microphones. Identity from [Image1], [Image2], [Image3]; coat from [Image8]. He half-stops, turns, says "I'll address that tomorrow," and continues walking. Lip-sync aligned with [Audio1]. Mixed tungsten/daylight, some lens flare from a TV camera light, overlapping shouted reporter voices low in the mix. 7 seconds.
```

### 8. Athlete post-game presser

```
Medium close-up of the soccer player at a press conference table, club-sponsored backdrop visible, water bottle in front of him. Identity from [Image1], [Image2], [Image3]; team jersey from [Image6]. He exhales, looks at the reporter and says "we played our game, that's all." Lip-sync aligned with [Audio1]. Locked tripod, even press-conference key light, faint shutter clicks. 8 seconds.
```

### 9. Real person delivering a podcast cold-open

```
Close-up of the woman in front of a Shure SM7B microphone, headphones on, dim purple LED accent on the studio wall behind her. Identity from [Image1], [Image2], [Image4]; headphones from [Image9]. She looks straight into the lens and says "we need to talk about what happened this week." Lip-sync aligned with [Audio1]. Locked, 50mm equivalent, shallow DoF, room tone only, no music. 6 seconds.
```

### 10. Real person reading from a phone (visual gag setup)

```
Medium close-up of the man on a Manhattan sidewalk in late-afternoon golden light, reading something on his phone. Identity from [Image1], [Image2], [Image3]; coat from [Image8]. He squints at the screen, looks up at the camera and says "wait, they raised at how much?" Lip-sync aligned with [Audio1]. Locked tripod, 35mm, shallow DoF, faint city traffic ambient, no music. 7 seconds.
```

### 11. CEO whispering to an assistant (over-shoulder)

```
Over-the-shoulder of the man seated at a glass conference table, whispering toward a second figure whose face is obscured. Identity from [Image1], [Image2], [Image3]; suit from [Image7]. He covers his mouth slightly, leans in and says "we kill the announcement." Lip-sync aligned with [Audio1]. Locked, dim conference-room key, faint HVAC hum, no music. 5 seconds.
```

### 12. Real person reacting silently (no audio, body language only)

```
Medium close-up of the man at a poker-style round table, face lit from below by a phone screen. Identity from [Image1], [Image2], [Image3]. He reads something on the screen, his jaw tightens, he closes his eyes for a beat, opens them looking off-camera. No dialogue. Locked tripod, room tone only, deep shadow, 8 seconds.
```

When using prompt 12, set `generate_audio: true` but include **no quoted dialogue** — the model will produce ambient sound and breathing, not speech. Don't pass `reference_audios` here; lip-sync is irrelevant.

---

## Continuity across multi-shot stitched videos

Seedance caps at 15s per generation. Silicon Mania-style 60–90s clips are stitched from 8–15 individual generations. Continuity is the hardest practical problem.

**Identity and wardrobe.** Reuse the **same 9-image character bible** for every shot of the same person across the entire video. Don't swap reference sets shot-to-shot — small differences in the bible cause noticeable jumps in face geometry. If wardrobe must change (e.g., scene change), generate a *new* bible image of the figure in the new outfit (use Flux + PuLID to forge a clean wardrobe-anchor) and swap in *only* that wardrobe slot, keeping the identity slots stable.

**Seed.** Reusing a seed across generations gives you closer-to-identical motion behavior, which sometimes helps continuity but often hurts it (you get the same gesture twice). Common practice: **vary the seed** but lock everything else.

**Lighting.** Describe lighting *identically* across shots in the same scene: "soft warm key from camera-left, slight rim from the window behind." The model is sensitive to this language. Using the same wording verbatim across shots reduces inter-shot drift more than any other single lever.

**Color grade in post.** Even with locked language, expect 5–10% inter-shot exposure and saturation drift. Apply a single LUT or grading node across all clips in DaVinci Resolve / Premiere / FCP — this resolves most residual mismatch and is faster than re-rolling generations.

**Audio bridges.** Carry music and ambient room-tone *across* cuts in the NLE. Smooth audio across a hard picture cut hides a lot of visual discontinuity — the brain interprets continuous audio as continuous scene.

**Cutaways are continuity insurance.** When a generation is "almost right" but inter-shot drift is visible, cutting away to a B-roll insert (logo, environment, a chyron) for 0.5–1s and then returning resets viewer attention. This is why news-style chyrons and "lower thirds" are a Silicon Mania staple — they double as continuity covers.

**Match aspect ratio + resolution at generate time, not in post.** Set `aspect_ratio: 9:16` and `resolution: 1080p` for every generation in a vertical-platform video. Up-resing or center-cropping in post degrades the lip-sync mouth region, which is the highest-cost area to lose pixels in.

---

## Post-production toolchain

The actual ship-pipeline after Seedance:

**Editing / NLE.**
- **CapCut** — most short-form creators' default. Free, web + desktop + mobile, strong auto-captions in the styles X/TikTok rewards. For Silicon Mania-style speed-of-iteration this is the right pick.
- **Descript** — transcript-driven editing wins when you're cutting around dialogue. Their *Overlord* AI agent will trim, caption, and even suggest B-roll from a brief. Strong for podcast-style face-to-face cross-cuts.
- **DaVinci Resolve** — free pro-grade NLE; the color page is the best option for matching mismatched Seedance generations into a single look.
- **Premiere Pro** / **Final Cut Pro** — standard pro paths, no special advantage for AI clips except integration with After Effects (Premiere) or Motion (FCP).

**Motion / VFX.**
- **After Effects** — for chyrons, lower thirds, news-style overlays, transitions, glitch frames between Seedance clips.
- **Motion** — FCP equivalent; lighter weight.

**Captions.**
- CapCut's auto-captions are state-of-the-art for short-form animated styles.
- Descript's caption styles are cleaner / more editorial.
- For paid pro look: **[Submagic](https://submagic.co/)**, **[Captions.ai](https://www.captions.ai/)** — both used by viral short-form accounts.

**Music.**
- **[Epidemic Sound](https://www.epidemicsound.com/)** — broadcast-clean licensing, cleared for YouTube/IG/TikTok; ~$15/mo creator plan.
- **[Artlist](https://artlist.io/)** — similar, slightly different catalog vibe.
- **[Suno](https://suno.com/)** — generates original tracks; Pro plan ($10/mo) gives commercial use rights. The right pick when you want a custom tempo/mood that no library match has, e.g., a specific 78-bpm piano-and-808 bed under a particular CEO line.

**SFX.**
- **Epidemic Sound SFX**, **[Soundly](https://getsoundly.com/)**, **[freesound.org](https://freesound.org/)** for whooshes, transitions, room tone, applause, keyboard clicks, etc. Native Seedance SFX is decent but inconsistent — most creators layer manually for finish.

**Voice mastering after generation.**
- **iZotope RX** for de-noise / de-click on Seedance native audio output.
- **ElevenLabs Voice Isolator** as a one-click pre-clean before re-uploading to a lip-sync engine.
- **Audacity / Adobe Audition** for fine cuts.

**Hosting / posting.**
- X / TikTok / Instagram Reels / YouTube Shorts for vertical 9:16 distribution.
- The Silicon Mania post under analysis is hosted natively on X via `video.twimg.com/amplify_video/` — direct upload to X (no compression-trip through cross-posting tools) preserves the most quality.

---

## Sources

- [Silicon Mania on X](https://x.com/siliconmania) — channel under study.
- [The reference video the user linked](https://x.com/siliconmania/status/2049671342136713651) — "last week in tech was looksmaxxed," 2026-04-29.
- [siliconmania.tv](https://www.siliconmania.tv/) — landing page.
- [Replicate `bytedance/seedance-2.0`](https://replicate.com/bytedance/seedance-2.0) — canonical schema source.
- [ComfyUI Seedance 2.0 Real Human node docs](https://docs.comfy.org/tutorials/partner-nodes/bytedance/seedance-2-0-real-human) — verification process.
- [ComfyUI blog: Real Human Video Generation in Seedance 2.0](https://blog.comfy.org/p/unlock-seedance20-real-human-video-generation).
- [Cutout.pro Seedance 2.0 audio guide](https://www.cutout.pro/learn/blog-seedance-2-0-audio-guide/) — dialogue, SFX, BGM, lip-sync prompt syntax.
- [CrePal: Seedance 2.0 Lip Sync + Voiceover — what works, what breaks](https://crepal.ai/blog/aivideo/blog-seedance-2-0-lip-sync-voiceover-fix/).
- [Higgsfield Seedance 2.0 Prompting Guide](https://higgsfield.ai/blog/seedance-prompting-guide).
- [Seaart Seedance 2.0 prompt examples](https://www.seaart.ai/blog/seedance-2-0-prompt).
- [Awesome Seedance 2 prompts (GitHub)](https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts).
- [WaveSpeedAI: Seedance 2.0 vs Sora 2 vs Veo 3.1](https://wavespeed.ai/blog/posts/seedance-2-0-vs-kling-3-0-sora-2-veo-3-1-video-generation-comparison-2026/).
- [ElevenLabs Use Policy](https://elevenlabs.io/use-policy) and [ElevenLabs Safety](https://elevenlabs.io/safety) — voice-cloning consent / no-go list.
- [ElevenLabs Professional Voice Cloning docs](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning) — sample-length requirements.
- [Sync.so vs Hedra comparison](https://lipsync.com/compare/sync-so-vs-hedra) and [Hedra lip-sync guide](https://www.hedra.com/blog/ai-lip-sync-video-guide).
- [OpenAI: Launching Sora responsibly](https://openai.com/index/launching-sora-responsibly/) and [Sora cameo / characters help](https://help.openai.com/en/articles/12435986-generating-content-with-characters).
- [Newsweek: Sora 2 bans celebrity deepfakes](https://www.newsweek.com/sora-2-openai-bans-celebrity-deepfakes-but-people-found-loophole-10912528).
- [Google AI Developers Forum: Veo geo-strict realistic-people block](https://discuss.ai.google.dev/t/so-google-veo-wont-let-me-use-images-of-realistic-people-because-i-am-in-england-even-though-the-images-are-generated-using-an-ai-so-they-are-not-real-people/98350).
- [TIME: Veo 3 deepfake capabilities](https://time.com/7290050/veo-3-google-misinformation-deepfake/).
- [Flux + PuLID consistent character workflow](https://www.runcomfy.com/comfyui-workflows/flux-kontext-pulid-consistent-character-generation).
- [Suno commercial-use FAQ](https://help.suno.com/en/articles/2746945) and [Suno royalty-free guide](https://suno.com/hub/royalty-free-music).
- [Descript vs CapCut comparison](https://www.descript.com/blog/article/how-to-use-capcut-to-edit-videos).
