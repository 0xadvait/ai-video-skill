# Seedance 2.0 — Canonical Schema (from Replicate API)

**Source:** `GET https://api.replicate.com/v1/models/bytedance/seedance-2.0` on 2026-05-04
**Replicate slug:** `bytedance/seedance-2.0`
**Latest version:** `4631ca9b77b48db08836df4527a436455c4eddff6b25dbc12e541f262aaab774`
**Model URL:** https://replicate.com/bytedance/seedance-2.0
**Created:** 2026-04-05 — Run count (as of fetch): 143,009
**Cover example:** https://replicate.delivery/xezq/3Uc0eKT36R2dIiXkrse8tD822Mhne8AIAMV6ekMcDg8WnWkZB/tmp7_ephsht.mp4

**Description (official, 1 line):**
> ByteDance's multimodal video generation model with native audio, multimodal reference inputs, and intelligent duration control.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `prompt` | string | ✅ | — | Text prompt for video generation. Use **double quotes** to specify dialogue (will be voiced when `generate_audio=true`). Use `[Image1]`, `[Video1]`, `[Audio1]` to reference attached media. |
| `image` | URI | ❌ | null | First-frame image for image-to-video. **Cannot be combined with `reference_images`.** |
| `last_frame_image` | URI | ❌ | null | Last-frame image. Only valid when `image` is also provided. **Cannot be combined with `reference_images`.** |
| `reference_images` | URI[] (≤9) | ❌ | [] | Character consistency, style guidance, scene composition. Reference in prompt as `[Image1]`…`[Image9]`. **Mutually exclusive with `image` / `last_frame_image`.** |
| `reference_videos` | URI[] (≤3, total ≤15s) | ❌ | [] | Motion transfer, style reference, editing. Reference as `[Video1]`…`[Video3]`. |
| `reference_audios` | URI[] (≤3, total ≤15s) | ❌ | [] | Audio-driven generation + lip-sync. Reference as `[Audio1]`…`[Audio3]`. **Requires at least one reference image or video.** |
| `duration` | int | ❌ | 5 | Range `-1` or **4–15** seconds. `-1` = intelligent duration (model picks). (Empirical: `3` is rejected with E006 "Duration must be between 4 and 15 seconds, or -1".) |
| `resolution` | enum | ❌ | `720p` | `480p` \| `720p` \| `1080p` |
| `aspect_ratio` | enum | ❌ | `16:9` | `16:9` \| `4:3` \| `1:1` \| `3:4` \| `9:16` \| `21:9` \| `9:21` \| `adaptive` |
| `generate_audio` | bool | ❌ | `true` | When true, model generates synchronized audio: dialogue (from quoted strings in prompt), SFX, ambient/score. |
| `seed` | int | ❌ | null | For reproducibility. |

## Output

- A single `mp4` URL (string).
- Default example: 7s @ 720p / 16:9 with audio took **~115s wall** to generate (predict_time 114.97s).

## Capability map (derived from schema)

| Capability | How |
|---|---|
| **Text-to-video** | Just `prompt`. |
| **Image-to-video (first frame)** | `image` + `prompt`. |
| **Frame interpolation / "fill the gap"** | `image` + `last_frame_image` + `prompt`. |
| **Character consistency across shots** | `reference_images` (the same person/object across multiple refs) + cite as `[Image1]` in prompt. |
| **Style transfer** | `reference_images` (style frame) + describe content in prompt. |
| **Motion transfer** | `reference_videos` (motion source) + `[Video1]` cite + describe new subject. |
| **Lip-sync to a real voice** | `reference_audios` (speech) + `reference_images` (face) + `[Audio1]` cite. |
| **Native dialogue** | Wrap dialogue in `"double quotes"` in the prompt with `generate_audio=true`. |
| **Native SFX + score** | Describe in prompt with `generate_audio=true`. |
| **Intelligent length** | `duration=-1`. |

## Exclusivity rules (gotchas)

1. `image` / `last_frame_image` are **incompatible** with `reference_images`. Pick one mode.
2. `reference_audios` requires at least one reference image OR reference video.
3. Total reference video duration cannot exceed 15s; same for audio.
4. Min duration = 4s (3s and below rejected with `E006`).

## Sibling resources to investigate (not on Replicate page)

- ByteDance original announcement / blog (Volcano Engine / Doubao / Seedream lineage)
- Bytedance research paper (if any) — `paper_url` was null on Replicate; check arXiv "Seedance"
- Volcano Engine / 火山引擎 dashboard (where ByteDance hosts these models first-party)
