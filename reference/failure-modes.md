# Seedance 2.0 — Failure Modes & Fixes

The 15 catalogued failure modes (cross-referenced from VideoAI.me, Segmind, Higgsfield,
Cliprise, Promeai, and forum reports). Each entry: symptom → fix you embed in the prompt
or the request body. Apply these *before* a render, not after a bad one.

| # | Failure | Symptom | Fix |
|---|---------|---------|-----|
| 1 | Hand drift | Fingers multiply / bend in extreme close-ups | Frame hands at medium distance, never tight CU. "hands resting naturally, fingers relaxed". Finalize hand CUs in post. |
| 2 | Glyph-soup text | Signs / screens / shirts render incoherent characters | Never ask Seedance for typography. Generate with "no readable text" and add text in post. Use "clean abstract mark, no letters" for logos. |
| 3 | Fast-motion warping | Sprints / tricks / gymnastics → limb stretch | Slow to "medium speed", or "one clear motion", or "120fps slow motion conformed to 24fps". Counted actions ("plants left foot, vaults once") reduce warp. |
| 4 | Non-English lip-sync drift | Pronunciation / timing / lip alignment unreliable in non-English | Generate lip-sync in English, voice-clone the audio to the target language in post. |
| 5 | Crowd faces simplify | Background extras become generic | Sparse compositions; keep important faces foreground; let crowds be silhouettes. |
| 6 | Mirror physics break | Reflections don't match subject pose | Avoid mirrors, or expect multiple regens. (Can be used as a deliberate glitch effect.) |
| 7 | Plastic / CGI skin | Character CUs swing uncanny | Negatives: "no 3D, no cartoon, no VFX, real subtle skin texture, natural pore structure, warm film grain". |
| 8 | Unrequested cuts | Model switches angle on ambiguous shot blocks | State continuity explicitly: "single continuous take, no cuts, no zoom, natural head movement". |
| 9 | Over-stabilized camera | "Handheld" still renders smooth | "completely unstabilized, violent raw human movement, constant micro-jitters". |
| 10 | Content-mod false positive | `Output Video/Audio Sensitive Content` | Filter is intent-aware — it reads the whole scene. Simplify dialogue, swap real names for archetypes, or set `generate_audio=false` if the hit is audio-only. |
| 11 | Real-person detection | Identifiable real faces in refs flagged | Use AI-generated character refs, or crop faces. Seedance is the most permissive of the major models but still runs server-side classifiers. |
| 12 | Parameter validation | Silent rejection / hard reject | Underlying API safe duration set is `{4,5,6,8,10,12,15}` — avoid 7/9/11/13/14. `image` + `reference_images` is hard-rejected. `last_frame_image` requires `image`. `reference_audios` requires an image or video ref. |
| 13 | Silent failure (HTTP 200, empty) | Video with no lip-sync, or "Generation Failed" no diagnostic | Pre-convert reference audio to **MP3 44.1 kHz** before passing to `reference_audios`. |
| 14 | Motion-ref over-copy | Output looks like a re-skin of `[Video1]` | Describe the new subject's motion in natural-language detail to compete with the video pull; or use a shorter 3–5s clip of the 15s budget. |
| 15 | Style drift / face flicker | Face structure / palette drifts across 10s+ single shots | Break into time-coded blocks with explicit camera changes — cuts re-anchor the model. Add "consistent faces, clothing, hairstyles throughout, no deformation or drift". |

## The classifier-flag escalation path

When you hit failure #10 or #11 (`Output Video Sensitive Content` / `E005`):

1. **Simplify the prompt** — remove charged dialogue, swap named figures for archetypes.
2. **Disable audio** — `generate_audio=false` if the flag is on the audio track only.
3. **Use synthetic references** — generate the face with an image model instead of a real photo.
4. **Route to fal Kling** — `generate.py --fallback` retries on `fal-ai/kling-video/o3/standard/image-to-video`,
   whose moderation gateway differs from Replicate's. Needs an image reference (i2v).

## Quality anchors (use sparingly, at the END of a prompt)

`8K`, `Hyper-realistic`, `ARRI ALEXA aesthetic`, `shot on IMAX 70mm` — these act as
fallback weight. Put them last, not first; concrete cinematography earns more than adjectives.
