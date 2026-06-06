# Prompting Lessons — the skill's growing memory

This file is how the skill improves. **Read it before building any prompt.**
After every quality-control pass (`review.py` → watch the clip → score it),
**append one distilled lesson** to "Accumulated lessons" below.

A lesson is a generalizable cause→effect rule, not a clip description.
Bad: "the dancer's feet looked wrong." Good: "9:16 dance: without 'feet
visible throughout' the model crops feet on close cuts — always state it."

**Append format** (newest at the bottom of its section):

```
- YYYY-MM-DD · model · category · overall N/5
  LESSON: <one generalizable rule>
  EVIDENCE: clip <id> — <what was observed in the frames>
```

Do not delete seed lessons. If experience contradicts one, append a new
lesson that supersedes it and note the conflict — don't silently overwrite.

---

## Seed lessons (from the corpus — verified, durable)

- **Five-part order is load-bearing.** Subject → Action → Camera → Style →
  Constraints. Earlier tokens win when the prompt contradicts itself.
- **Time-coded blocks `[00:00-00:05]` are the single highest-leverage tool.**
  They act as hard cuts and re-anchor identity/wardrobe/palette. A 15s clip
  is 3 shots, not 7.
- **One style anchor beats many.** One director + one film stock outperforms
  a "taste salad" of three directors — multiple anchors neutralize each other.
- **Restraint improves lip-sync.** Lead with delivery ("whispers, trying not
  to cry") before the line; keep lines 4–10 words; lock the camera.
- **Name the sound source.** "fat crackle, one tong clink" beats "sizzle".
  Audio direction is mandatory when generate_audio is on.
- **Fixed hands reduce warping.** Hands on a wheel/weapon, never fine finger
  articulation in close-up. Counted actions ("plants left foot, vaults once")
  reduce limb stretch.
- **Assign each reference a job.** "[Image1] = face; [Image5] = wardrobe" —
  a bare "[Image1]" is read as a vague moodboard.
- **Remove one demand before adding three.** Failed clips are usually
  over-specified, not under-specified.
- **Negatives as positives.** "hands resting in lap" > "no bad hands";
  "single continuous take" > "no cuts".

## Accumulated lessons (appended by QC — newest last)

- 2026-05-18 · veed-fabric-1.0 · lip-sync · overall 2/5
  LESSON: VEED Fabric only animates the mouth — the head stays static, which
  reads stiff and uncanny on a talking-head clip. For audio-driven talking
  video, prefer a model that also drives head motion, blinks and gestures
  (wan-2.7-i2v or omnihuman-1.5).
  EVIDENCE: side-by-side taster against the other talking-avatar models.

- 2026-05-18 · omnihuman-1.5 vs wan-2.7-i2v · talking-avatar · overall 4/5
  LESSON: In a head-to-head taster, Wan 2.7 i2v won for a clean
  head-and-shoulders talking shot; OmniHuman 1.5 used a wider frame that
  picked up hand/desk gestures — better when gesture is wanted, busier when
  it is not. Default talking-avatar clips to wan-2.7-i2v; reach for
  omnihuman-1.5 only when a gesture-rich wider frame is the goal.
  EVIDENCE: wan vs omnihuman tasters compared directly.

- 2026-05-18 · real-person · framing · overall 5/5
  LESSON: For a talking-avatar still, the mic must sit to one side at chest
  height — never across the mouth/chin — or lip-sync degrades. Keep facial
  identity 100% faithful across every shot.
  EVIDENCE: avatar accepted once the mouth was unobstructed.

- 2026-06-05 · gemini-3-pro-image-preview (Nano Banana 2) · first-frame still · overall 5/5
  LESSON: Best current photoreal first-frame/hero plate is Gemini "Nano Banana 2"
  = gemini-3-pro-image-preview (generateContent, responseModalities:["IMAGE"],
  base64 inlineData). gemini-3.1-pro-preview is GEO-BLOCKED on the free key
  ("Image generation is not available in your country") — fall back to
  3-pro-image-preview. Generate ~3 concept variants and let the user pick BEFORE
  spending the i2v that animates it.
  EVIDENCE: 3 gallery-hero variants; user picked the golden-atrium one as the
  i2v first frame.

- 2026-06-05 · grok-imagine-video (xai, Replicate) · image-to-video · overall 4/5
  LESSON: For "step INTO a still", Replicate `xai/grok-imagine-video` gives a
  clean forward dolly (input: image as data-URI + prompt + duration 1-15 +
  aspect_ratio). Prompt the camera explicitly AND redundantly —
  "the camera glides smoothly and steadily forward the whole time" + subject
  walking AWAY from camera — or it drifts/holds. Keep the "comes alive" beat
  ~3-4s; 6s+ reads as too long. Not yet wired into generate.py routing — call
  the Replicate model directly.
  EVIDENCE: gallery-walk i2v from a Nano-Banana-2 still, used as the hero
  "image comes alive" beat in a HyperFrames product demo.

- 2026-06-05 · pipeline · compose-not-stitch · overall 5/5
  LESSON: When the deliverable is a designed / cursor-driven piece (product demo,
  UI walkthrough, kinetic typography) — not just stitched AI footage — build it
  in HyperFrames (HTML→MP4) and drop AI stills/clips in as timeline assets, not
  assemble.py. See reference/hyperframes-motion-demos.md. Always do a
  frame-by-frame QC pass on dense ffmpeg grids; if your context can no longer
  load images, delegate the QC to a fresh-context subagent (its own image budget).
  EVIDENCE: OpenGradient Image Studio demo — Nano Banana 2 stills + grok i2v
  composed in HyperFrames, QC'd frame-by-frame by a subagent that caught a
  double-exposure ghost frame + an aimless cursor move I couldn't see.
