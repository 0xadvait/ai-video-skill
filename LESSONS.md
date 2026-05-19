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
