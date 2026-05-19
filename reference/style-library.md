# Video Prompt Craft — Cross-Model Vocabulary

**Scope.** This document distills the *craft* of prompting modern text-to-video models — Sora 2, Veo 3 / 3.1, Kling 2.x, Runway Gen-4, Luma Dream Machine, Pika 2.x, MiniMax Hailuo, and Tencent HunyuanVideo — into a vocabulary that transfers cleanly to ByteDance Seedance 2.0. Seedance 2.0 takes a single free-form `prompt` string with no separate camera, lighting, style, or negative-prompt fields (see `00_canonical_schema.md`). Everything we want to control therefore has to be encoded in prose, in the right order, with the right diction. The patterns below are the diction working professionals (and the model documentation teams) actually publish.

A note on transferability. None of these models share weights, and none of them tokenize or attend identically. But they *do* share training data: cinematic stills, film stills with captions, professionally graded footage, and crawled pinterest/tumblr-style descriptions of films. A Roger Deakins reference triggers something on every model precisely because every model saw the same captioned stills. The vocabulary is largely portable. Where models diverge (audio prompting, dialogue formatting, multi-shot timestamps), this is called out per-model.

---

## Canonical structures

Every public guide converges on a slot-filling formula. The slot order varies, but the slots themselves are remarkably stable: **subject, action, scene/context, camera, lighting, style, audio**. Below are six canonical templates with attribution.

### 1. Runway Gen-4 — Subject Motion / Scene Motion / Camera Motion / Style

Runway's published Gen-4 video prompting guide (`help.runwayml.com/.../Gen-4-Video-Prompting-Guide`) frames a clip as four orthogonal "motion" axes plus a style descriptor:

> *Subject Motion (what the character/object is doing) + Scene Motion (how the environment reacts) + Camera Motion (how the lens moves through the scene) + Style Descriptor (the visual mood/aesthetic).*

Runway explicitly recommends **starting with the most essential motion only** and adding one element at a time. This iterative tightening is the dominant pattern across the whole industry.

Skeleton:
```
[subject] [primary action], [environmental motion], [camera move], [style/mood/lighting].
```

Example:
> *A lone fisherman casts his line into glass-flat water, ripples expanding across the reflection of distant peaks; slow dolly-in along the dock; muted dawn palette, 35mm film grain.*

### 2. OpenAI Sora 2 — Prose + Cinematography + Actions + Dialogue blocks

OpenAI's official Sora 2 cookbook (`cookbook.openai.com/examples/sora/sora2_prompting_guide`, updated March 2026) prescribes a *block-structured* prompt that separates prose from camera direction from action beats from dialogue:

```
[Prose scene description in plain language: characters, costumes,
scenery, weather, other details.]

Cinematography:
Camera shot: [framing and angle]
Mood: [overall tone]

Actions:
- [Beat 1]
- [Beat 2]
- [Beat 3]

Dialogue:
- Character A: "Line."
- Character B: "Response."
```

Two principles from the OpenAI guide are load-bearing: **"shorter prompts grant creative freedom; longer ones restrict it"**, and **"one action + one camera move per shot maximizes clarity."** Sora 2 is also explicit that visible nouns beat abstractions — *"wet asphalt, zebra crosswalk, neon reflections"* outperforms *"beautiful street."*

### 3. Google Veo 3 / 3.1 — Cinematography + Subject + Action + Context + Style/Ambiance

The Google DeepMind Veo prompt guide (`deepmind.google/models/veo/prompt-guide`) and the Vertex AI video-gen prompt guide list seven canonical ingredients: **shot framing & motion, style, lighting, character description, location, action, dialogue.** Google Cloud's "Ultimate Veo 3.1 prompting guide" condenses this to a five-part formula:

```
[Cinematography] + [Subject] + [Action] + [Context] + [Style & ambiance]
```

Veo 3.1 also supports *timestamp prompting* for multi-shot single-clip generations — a feature Seedance 2.0 does not officially support, but the same `[00:00–00:02]` syntax is sometimes interpreted by the LLM-prompt-rewriter pre-pass:

```
[00:00-00:02] Wide establishing, drone descent over coastline
[00:02-00:05] Cut to medium tracking of runner, gravel crunch, breath SFX
[00:05-00:08] Push-in to close-up, ambient swell, dialogue: "I made it."
```

### 4. Kling AI — Shot type / Subject / Action / Environment / Camera / Lighting / Style

Kling's published 2.x guide (Ambience AI tutorial; fal.ai Kling 2.6 Pro guide; Hixx 2.5 guide) recommends the most explicit slot order of any model:

```
[Shot type] of [subject] [action/movement], [environment/setting], [camera movement], [lighting/mood], [style/aesthetic]
```

Kling's distinguishing advice is **camera verbs over generic motion verbs**: *dolly push, whip-pan, shoulder-cam drift, crash zoom, snap focus* — *not* "moves" or "goes". Kling also takes a *real* negative prompt field, which is why its public examples often look the cleanest; we'll discuss the workaround below for Seedance.

### 5. Tencent HunyuanVideo — Subject + Motion + Scene + Shot + Camera + Lighting + Style + Atmosphere

The official HunyuanVideo 1.5 Prompt Handbook (`github.com/Tencent-Hunyuan/HunyuanVideo-1.5/.../HunyuanVideo_1_5_Prompt_Handbook_EN.md`) gives the most exhaustive slot list:

```
Text-to-Video: Subject + Motion + Scene + [Shot Type] + [Camera Movement] + [Lighting] + [Style] + [Atmosphere]
Image-to-Video: Subject Motion Dynamics + Scene Motion Dynamics + [Camera Movement]
```

Hunyuan also documents a **"first… then… next… meanwhile… finally…"** sequencing convention for multi-beat actions inside a single shot — useful when a single Seedance clip needs to depict a small narrative arc in 6–10 seconds.

### 6. Pika 2.x and MiniMax Hailuo — Subject + Action + Setting + Style (+ explicit camera modifier)

Pika exposes a `-camera` parameter (`pan_left`, `zoom_in`, `rotate_clockwise`, …) and a `-motion` strength dial 0–4. MiniMax Hailuo's "Director" mode recognizes ~15 named camera moves you can drop into prose. Both reduce to a four-slot prose formula:

```
[Subject] + [Action] + [Setting/Environment] + [Artistic Style]
```

…with the camera move appended as an inline phrase: *"…tracked by a slow dolly-in"* or *"…shot from a low angle, drone ascending."*

### Synthesis — a Seedance-friendly unified template

For Seedance 2.0 specifically (single prose field, ≤512 tokens in practice, native audio):

```
[Shot type & framing] of [subject with 2–3 concrete attributes],
[primary action verb + object], [environmental motion / weather],
[lighting + time of day], [color palette + film/style anchor],
[camera move with speed], [audio: dialogue in "double quotes",
SFX cue, ambient bed].
```

Aim for 60–120 words. Front-load the visual; place dialogue and SFX last. Keep one camera move and one primary action.

---

## Camera language glossary

The vocabulary below is what every guide above teaches the model. These tokens are the most frequently-captioned terms in the training corpora, so they trigger the cleanest behavior.

### Static shot framing

| Term | What it means | When to use |
|---|---|---|
| **Extreme wide / establishing** | Subject tiny in frame; environment dominates | Open a clip, set scale |
| **Wide shot (WS)** | Full subject head-to-toe with surroundings | Geography of action |
| **Medium wide / cowboy** | Mid-thigh up | Two characters in conversation |
| **Medium shot (MS)** | Waist up | Default talking-head framing |
| **Medium close-up (MCU)** | Chest up | Emotional dialogue |
| **Close-up (CU)** | Head and shoulders | Reaction, intent |
| **Extreme close-up (ECU)** | Eyes only, or single object detail | Tension; texture |
| **Over-the-shoulder (OTS)** | Camera behind one subject, looking at another | Conversation coverage |
| **Two-shot** | Two subjects framed equally | Relationship beats |
| **Insert** | Tight on a hand/object | Pickup detail |
| **POV** | First-person | Subjectivity, immersion |

### Camera angles

| Term | Effect |
|---|---|
| **Eye-level** | Neutral, conversational |
| **Low angle** | Subject feels powerful, looming |
| **High angle** | Subject feels small, vulnerable |
| **Bird's-eye / overhead** | God-view, geometric |
| **Worm's-eye** | Extreme low; alien |
| **Dutch angle / canted** | Off-kilter, unease, instability |
| **Top-down (90° overhead)** | Flat-lay, choreography |
| **Profile / 3/4 / front-on** | Portrait orientation |

### Camera movement

| Term | What the lens does | Connotation |
|---|---|---|
| **Dolly in / push-in** | Camera moves toward subject | Intimacy, intensification |
| **Dolly out / pull-back** | Camera retreats | Reveal, isolation |
| **Truck left/right** | Lateral on dolly tracks | Parallel reveal |
| **Pedestal up/down** | Vertical translation, body fixed | Scale change |
| **Tilt up/down** | Nod the camera body | Reveal vertical space |
| **Pan left/right** | Swivel the camera body | Survey horizontal space |
| **Whip pan** | Very fast pan, motion-blurred | Transition, energy |
| **Orbit / arc** | Camera circles subject | Showcase, suspense |
| **Crane / jib** | Vertical sweep, often with arc | Grandeur, scale reveal |
| **Crane down to eye-level** | God-view → human contact | Empathy beat |
| **Aerial / drone** | Free-flying overhead | Geography, awe |
| **Handheld** | Slight organic shake | Documentary, urgency |
| **Steadicam / gimbal** | Smooth following motion | "Walk-and-talk" |
| **Tracking shot** | Camera follows subject laterally | Continuous action |
| **Following shot / shoulder-cam** | Behind subject, matching gait | Immersion |
| **Rack focus / pulled focus** | Focus shifts between depth planes | Attention redirect |
| **Crash zoom** | Extremely fast in or out | Shock, comedic |
| **Slow zoom** | Lens zoom (not dolly) | Vertigo, dread |
| **Dolly zoom / Vertigo** | Dolly + opposite zoom | Psychological dislocation |
| **Snorricam / body-mount** | Camera fixed to actor | Disorientation |
| **Locked-off / static** | No movement | Composed; theatrical |

### Lens & optics

Lens references give a video model strong perceptual cues for compression, depth-of-field, and distortion:

- **14mm / 24mm / wide-angle** — broad FOV, edge curvature, exaggerated depth.
- **35mm** — naturalistic, slight environmental context. Default "cinematic" lens.
- **50mm "nifty fifty"** — close to human eye, neutral.
- **85mm / 100mm / portrait lens** — flattering compression, soft falloff.
- **135mm / 200mm telephoto** — strong compression, isolated subject, blurred background.
- **Anamorphic** — 2x horizontal squeeze, oval bokeh, horizontal lens flares (the "Blade Runner" lens).
- **Macro lens** — extreme close detail, razor-thin DOF.
- **Fisheye** — extreme distortion, near-180° FOV.
- **Tilt-shift / miniature** — selective plane focus, "diorama" look.
- **Probe lens / Laowa 24mm** — extreme low macro, deep focus.

Depth-of-field language: **shallow depth of field, creamy bokeh, deep focus, split diopter, hyperfocal, rack focus, soft focus, sharp focus throughout.**

Other optical descriptors that all major models recognize: **lens flare, anamorphic streaks, chromatic aberration, halation, light bloom, vignetting, film grain, gate weave, scan lines, motion blur, frame dragging.**

---

## Lighting glossary

Lighting language is where amateur prompts collapse into "cinematic lighting" mush. Every guide referenced — Sora 2's cookbook, the Veo Vertex guide, Hunyuan's handbook — pushes specific named lighting setups instead.

### Setups

- **Three-point lighting** — Key + Fill + Backlight. The default professional setup; produces clean, dimensional subjects.
- **Key light** — primary, brightest source. Specify direction (*camera-left, 45°, high*).
- **Fill light** — softer, opposite the key, lifts shadows. "Half-power fill" is a common phrasing.
- **Back light / hair light / kicker** — separates subject from background.
- **Rim light** — narrow back/side light that traces silhouette.
- **Rembrandt lighting** — key light high and ~45° to one side, producing a small triangle of light on the shadow-side cheek, under the eye. Painterly, dramatic.
- **Loop lighting** — key slightly less steep than Rembrandt; nose shadow loops down. Flattering portrait default.
- **Butterfly / Paramount lighting** — key light directly above, centered. Symmetrical nose shadow. Classic Hollywood glamour.
- **Split lighting** — key 90° to side; half the face in shadow. Noir, conflict.
- **Broad lighting** — face turned away from light source (broad side lit).
- **Short lighting** — face turned into the light (short side lit, more dramatic).
- **High-key** — overall bright, low contrast. Comedy, commercial, romance.
- **Low-key** — predominantly dark, high contrast. Noir, horror, drama.

### Quality and direction

- **Hard light** — direct sun, bare bulb; sharp shadows.
- **Soft light** — diffused (overcast, softbox, bounce); gentle gradient.
- **Diffused light** — through a scrim, frosted glass, fog.
- **Specular / glancing light** — skimming surface; reveals texture.
- **Top-down, side, underlit** — direction descriptors.
- **Backlit / contre-jour / silhouette** — light from behind subject; reads as mood/mystery.

### Time of day and color temperature

- **Golden hour** — first hour after sunrise / last before sunset; warm, low-angle, long shadows.
- **Magic hour** — alternative term for golden hour and the few minutes either side.
- **Blue hour** — civil twilight, ambient sky still glowing; cool palette.
- **High noon** — overhead sun, hard top-down shadows.
- **Overcast** — soft, omnidirectional, low contrast.
- **Tungsten / 3200K** — warm interior, incandescent.
- **Daylight / 5600K** — neutral.
- **Mixed temperature** — tungsten interior + daylight window; pro-cinematography signature.

### Atmospheric and motivated

- **Motivated lighting** — appears to come from in-scene sources.
- **Practical light** — visible in-frame light source (lamp, neon sign, window).
- **Volumetric / godrays / atmospheric haze** — visible light beams through fog, dust, smoke.
- **Bounce / fill from below** — soft, painterly.
- **Hard shadow / soft falloff / wraparound light** — falloff descriptors.
- **Chiaroscuro** — extreme bright/dark contrast (Caravaggio, noir).
- **Neon** — saturated colored point sources, often pink/magenta/cyan.
- **Sodium-vapor** — orange-yellow streetlight (the "Blade Runner 2049" Vegas sequences).
- **Mercury-vapor** — cool blue-green street/parking-garage tone.
- **Firelight / candlelight** — warm flickering, low.
- **Bioluminescent / phosphorescent** — soft glow from within subject.

### Reliable lighting prompt fragments

Snippets that appear in essentially every published example library:

- *"Soft window light, warm lamp fill on the right, cool rim from the hallway behind."*
- *"Golden hour backlight, lens flare, dust motes."*
- *"Single hard key from above, deep chiaroscuro shadows."*
- *"Sodium-vapor streetlight on wet asphalt, pink neon practical reflected in puddles."*
- *"Overcast diffuse light, no direct sun, low contrast."*

---

## Style references library (director / DP / stock / aesthetic)

Naming a director, cinematographer, film stock, or specific film is the single highest-leverage move in a video prompt because the model has seen the captioned stills. Below are 30+ references that work across at least two of the major models (Sora 2, Veo 3, Kling, Runway, Hunyuan), grouped by what they evoke.

### Cinematographer / DP names

1. **Roger Deakins** — naturalistic directional light, deep blacks, painterly silhouettes, single source (Blade Runner 2049, 1917, Sicario).
2. **Emmanuel Lubezki ("Chivo")** — natural-light handheld, very wide lens, long takes, golden-hour worship (The Revenant, Tree of Life, Children of Men).
3. **Greig Fraser** — desaturated photochemical look, IMAX scale, golden underexposure (Dune, The Batman).
4. **Bradford Young** — low-light, milk-coffee skin tones, silhouettes, deep amber (Arrival, Selma).
5. **Hoyte van Hoytema** — IMAX shallow DOF, available-light, dread (Oppenheimer, Interstellar, Dunkirk).
6. **Christopher Doyle** — handheld, smear-step-printing, neon Hong Kong, color saturation, motion blur (In the Mood for Love, Chungking Express).
7. **Robert Yeoman** — Wes Anderson's DP; centered planimetric symmetry, pastel palettes, snap zooms.
8. **Janusz Kamiński** — Spielberg's DP; high-contrast diffusion, blown highlights, smoke (Saving Private Ryan, Schindler's List).
9. **Gordon Willis ("Prince of Darkness")** — top-down key, deep shadows, amber (The Godfather).
10. **Vittorio Storaro** — color-coded narrative, theatrical (Apocalypse Now, The Conformist).
11. **Linus Sandgren** — saturated, theatrical color (La La Land's CinemaScope dusk).
12. **Rachel Morrison** — naturalistic available-light, intimate (Mudbound, Black Panther).
13. **James Laxton** — pastel teal/magenta, intimate skin tones (Moonlight).

### Director names (style + composition)

14. **Wes Anderson** — perfect symmetry, planimetric tableau, pastel palette, snap-zooms, dollhouse production design.
15. **Stanley Kubrick** — symmetrical one-point perspective, slow zoom, wide-angle interiors.
16. **David Fincher** — green-cyan grade, locked tripod, repeated coverage, cold sodium-fluorescent palette.
17. **Denis Villeneuve** — minimalist negative space, monumental scale, slow tension (Arrival, Dune).
18. **Christopher Nolan** — IMAX scale, available-light, time-folding cuts (Tenet, Interstellar).
19. **Wong Kar-wai** — step-printed motion, neon, longing close-ups.
20. **Andrei Tarkovsky** — long takes, water/mirror motifs, sepia + monochrome.
21. **Akira Kurosawa** — telephoto compression, weather as character (rain, wind, fog).
22. **Hayao Miyazaki / Studio Ghibli** — soft watercolor backgrounds, cumulus clouds, pastoral lighting, hand-drawn animation.
23. **Satoshi Kon** — match-cut surrealism, animation.
24. **Spike Lee** — double-dolly floating shot, saturated reds.
25. **Sofia Coppola** — diffuse window light, soft focus, melancholy pastel.
26. **Park Chan-wook** — Korean New Wave; symmetry plus baroque color.

### Specific films (color/light signatures)

27. **Blade Runner 2049** — neon magenta + sodium amber, monolithic interiors, anamorphic flares, rain-slick streets.
28. **Moonlight** — pastel teal-magenta nightscapes, intimate close-ups, available light on dark skin.
29. **The Grand Budapest Hotel** — pink-and-mint candy palette, perfect symmetry, dollhouse production design.
30. **Mad Max: Fury Road** — orange-and-teal grade, wind, dust, golden hour into blue night.
31. **Drive (2011)** — magenta neon, score-driven slow drives, lonely LA.
32. **In the Mood for Love** — saturated red/green, smear-printed motion, clock close-ups.
33. **The Lighthouse** — 1.19:1 aspect ratio, monochrome, hard chiaroscuro.
34. **Her (2013)** — pastel coral/peach palette, soft daylight, near-future Los Angeles.

### Film stocks and processes

35. **Kodak Portra 400 / 800** — warm peach skin tones, soft greens and blues, fine grain, natural-light portrait look.
36. **Cinestill 800T** — tungsten-balanced; halation around light sources; produces the iconic neon-night look.
37. **Kodak Vision3 500T** — modern motion-picture stock; clean shadows, lifted blacks.
38. **Kodak Ektachrome** — slide film; saturated and cool, vintage editorial.
39. **Fuji Velvia / Fuji 400H** — saturated greens, pastel skin (wedding photography signature).
40. **Polaroid SX-70** — square, soft, faded, warm shift.
41. **Super 8** — square gate, heavy grain, gate weave, color shift.
42. **16mm** — moderate grain, indie-doc feel.
43. **35mm anamorphic** — 2.39:1 widescreen, oval bokeh, horizontal flares.
44. **65mm / 70mm IMAX** — large-format clarity, deep field, scale.
45. **VHS / Hi8 / DV** — interlaced, low-res, magnetic dropouts, 1990s home-video.

### Movements and aesthetics

46. **A24 indie aesthetic** — naturalistic light, muted palette, slow pace, available-light interiors.
47. **Studio Ghibli** — see Miyazaki above; animation, painted skies.
48. **Pixar** — bouncy character animation, cinematic lighting on cartoon geometry.
49. **Stop-motion / Laika / Aardman** — handcrafted, slight frame stutter, tactile materials.
50. **Cyberpunk neon-noir** — magenta + cyan, rain, holograms, dense signage.
51. **Cottagecore / pastoral romanticism** — flowers, linen, golden light, gentle wind.
52. **Brutalist / monolithic** — concrete masses, hard shadows, ant-scale humans.
53. **Vaporwave** — pink + cyan, statues, palm trees, 80s pastel.
54. **Liminal space** — empty fluorescent corridors, off-hours, dreamlike.

A useful test: include exactly **one** named reference per prompt. Multiple references compete and dilute. *"Shot like Roger Deakins"* anchors better than *"Roger Deakins meets Wes Anderson meets Cinestill 800T."*

---

## Motion descriptor cookbook

Motion is where prompts most often produce uncanny output. The Atlabs / Sora 2 community guides, the LTX-2 warble guide, and HunyuanVideo handbook converge on five rules.

### Rules

1. **One primary action per shot.** Every guide repeats this. If you write *"she draws her sword, blocks an arrow, leaps onto her horse, and rides away,"* you are asking the model to choreograph four actions in 5 seconds with no temporal anchors. It will morph. Pick one: *"she draws her sword in a single fluid motion."*
2. **Verb-driven, not adjective-driven.** *Sprints, vaults, pivots, lunges, drops, flicks, scrubs, kneads, exhales* outperform *fast, dynamic, energetic, smooth, graceful*.
3. **Anatomical specificity for human motion.** Name the body part doing the work. *"Pivots on her left foot,"* *"raises her right hand to her temple,"* *"the dog's ears flatten as it lowers its head."* This grounds the model and prevents the "spaghetti limb" failure mode.
4. **Count the beats when you can.** OpenAI's example: *"Cyclist pedals three times, brakes, and stops at crosswalk."* Counts give the model temporal anchors. *"He takes four steps to the window"* beats *"he walks to the window."*
5. **Pair every action with its physical consequence.** If the wind is blowing, *"her hair lifts and falls"*; if it's raining, *"droplets run down the window in irregular tracks"*; if she's running, *"each footfall sprays dust."* Consequences pin the motion to physics and reduce flicker.

### Speed and quality modifiers (Kling-style)

| Adverb | Effect |
|---|---|
| *gracefully, smoothly, fluidly* | Eases curves; minimizes jitter |
| *rapidly, swiftly, sharply* | Higher frame-to-frame deltas; risks blur |
| *gradually, slowly, deliberately* | Long onset/offset; safe |
| *abruptly, suddenly, snap* | Encourages a single hard transition |
| *rhythmically, steadily, continuously* | Periodic motion; loops well |
| *erratically, jerkily, sporadically* | Use only for explicit chaos |

### Anti-patterns that produce morphing/jitter

- **Compound actions.** *"She turns, smiles, waves, and walks away."* — collapses to morphing.
- **Hands-doing-fine-detail.** *"Knitting,"* *"counting coins,"* *"playing piano arpeggios."* — extreme finger-morphing risk in current models.
- **Crowds in motion with named individuals.** *"The protagonist runs through the crowd while a child waves at her"* — identity drift across frames.
- **Generic fast motion.** *"Moves quickly,"* *"goes fast,"* *"in motion."* — model has nothing to anchor the trajectory.
- **Rotating-text prompts.** *"A spinning sign that reads 'OPEN'"* — text rendering breaks under any rotation.
- **Camera motion + complex subject motion + scene transformation simultaneously.** Pick at most two.
- **"He walks across the room, sits, and pours a drink."** Multi-stage. Replace with one stage: *"He pours a drink, ice clinking against the glass."*

---

## Temporal pacing

Seedance 2.0 supports 4–15s clips. Within that window, pacing is controllable but coarse — there's no per-keyframe control. Veo 3.1's `[MM:SS-MM:SS]` block syntax sometimes survives the prompt rewriter, but should not be relied upon.

### What works in single-shot models

- **Total duration framing.** *"Over the next 5 seconds, the dawn light slowly creeps across the floor."* The model interprets "slowly" relative to clip length.
- **Onset/sustain/release verbs.** *"She inhales, holds, then exhales as the sparks settle."* Three clear phases work in a 6–8s clip.
- **One inflection point.** *"Three seconds of stillness, then a sudden gust scatters the leaves."* Pinning an event roughly halfway is reliable.
- **Continuous loops.** *"The pendulum swings continuously, left, right, left, right."* Repetitive motion is the safest choice for short clips and is what looping models (Luma's `loop` keyword, Hailuo's loop generations) reward.

### What works in multi-shot models (Veo 3.1, sometimes Sora 2)

- **Timestamp blocks.** Veo's official syntax: `[00:00-00:02] establishing wide; [00:02-00:05] cut to medium tracking; [00:05-00:08] push-in to CU.`
- **Cut markers.** *"Cut to,"* *"smash cut,"* *"match cut on the lit match,"* *"crossfade,"* *"hard cut on impact."* These are recognized by Sora 2 and Veo but ignored or merged into a single shot by Seedance / Kling / Runway / Hunyuan.

### Pacing vocabulary that transfers everywhere

| Phrase | Effect on a 4–15s clip |
|---|---|
| *"slowly, over the full duration"* | Long, smooth motion |
| *"holds for 2 seconds, then…"* | Inserts a beat |
| *"a sudden, sharp"* | Single hard event |
| *"gradually accelerating"* | Ease-in trajectory |
| *"settling into stillness"* | Ease-out final beat |
| *"in real time"* | Discourages slow-mo bias |
| *"slowed and stretched"* | Encourages slow-mo |
| *"a single continuous take"* | Discourages cut hallucination |

### The slow-motion bias

Most modern video models exhibit a strong **slow-motion bias** — they interpret ambient or beautiful scenes as cinematic slow-mo and produce ~24fps slowed footage even when you wanted 1× speed. Mitigations: include *"in real time,"* *"natural pace,"* *"normal speed,"* *"observational,"* or specify visible fast motion (*"the fan spins at full speed, blades blurring"*). Conversely, if you *want* slow-mo, request *"shot at 120fps and conformed to 24,"* *"slow-motion, droplets visibly suspended,"* or *"phantom-cam slow-motion."*

---

## Negative-prompt-as-positive technique

Seedance 2.0 has **no negative-prompt field**. Neither does Sora 2 (the OpenAI cookbook never references one), Runway Gen-4 video (despite Gen-3 supporting one), Veo 3 (Google's published guidance is to phrase exclusions positively), or Hunyuan Video. Kling has a real negative prompt; MiniMax's API exposes one in some endpoints; Pika via Discord syntax (`-no <thing>`).

The cross-model best practice is to **describe what you want, not what you don't**. Google's Veo guide is explicit:

> *"To refine your output, describe what you wish to exclude. For example, specify 'a desolate landscape with no buildings or roads' instead of 'no man-made structures'."*

Reformulated as a recipe:

| Naive negative | Positive equivalent that actually works |
|---|---|
| *"no extra fingers"* | *"hands hidden behind her back"* or *"hands resting in lap, fingers relaxed and natural, five fingers visible"* |
| *"no morphing"* | *"steady, locked-off camera; subject moves smoothly without gaps"* |
| *"no text"* | *"a blank wall behind her"* / *"unlabeled signage"* |
| *"no cuts"* | *"a single continuous take"* |
| *"no slow-mo"* | *"in real time, natural pace"* |
| *"no flicker"* | *"consistent lighting throughout the clip"* |
| *"no people"* | *"an empty street at dawn, the city still asleep"* |
| *"no blur"* | *"sharp focus throughout, deep depth of field"* |
| *"no warp / no melt"* | *"solid, dimensionally stable [object], rigid materials"* |

The "no X, no Y" trick *inside* a positive prompt does work on some models — Kling's documented negatives literally read *"blur, distortion, watermark, text overlay, low quality, compression artifacts, flickering, inconsistent lighting, morphing faces, extra limbs, unnatural physics"* — but reliability across Sora 2 / Veo / Seedance is poor, and on Sora 2 in particular, mentioning "no fingers" tends to *increase* finger errors (the model gets primed on the noun). **Default to positive description.** Reserve "no X" only as a last resort and bury it at the end of the prompt: *"…cleanly composed, no on-screen text."*

---

## Audio prompting

Seedance 2.0 has native audio (`generate_audio=true` by default), as does Veo 3 / 3.1 and Sora 2. The audio surface decomposes into three things you can prompt for: **dialogue, sound effects (SFX), and ambient/score.**

### Dialogue

Conventions are remarkably consistent across the three audio-capable models:

- **Sora 2** — dedicated `Dialogue:` block after prose, one line per character, labeled.
- **Veo 3.1** — inline with `says, "…"` quotation, e.g. *A woman says, "We have to leave now."*
- **Seedance 2.0** — anything in **double quotes** is treated as voiced dialogue when `generate_audio=true`. Per the canonical schema doc: *"Use double quotes to specify dialogue."*

Best practice across all three:

1. **Keep lines short.** A 5–8 second clip can carry 1–2 short sentences total. Long monologues get truncated, paraphrased, or rushed.
2. **Match line length to clip length.** ~2 words per second is a safe ratio (English).
3. **Specify delivery in adjectives, not stage directions.** *"She whispers, hushed and conspiratorial: 'They're listening.'"* — better than `(whispering, scared)` parenthetical.
4. **Label the speaker if there are two.** Otherwise the model assigns voice randomly.
5. **Don't mix languages mid-line** unless explicitly requested — codeswitching breaks lipsync.
6. **For accents and voice character**, name them: *"a gravel-voiced older man with a Brooklyn accent,"* *"a young woman with a soft Irish lilt."*

For Seedance 2.0 specifically, since dialogue is just `"quoted text"` in the prose field, embed it inline:

> *Medium close-up. Maya, 30s, sits in a diner booth at dusk, neon reflections on her face. She looks up from her coffee and says, "I shouldn't have come back."*

### Sound effects (SFX)

Veo 3.1 documentation prescribes the explicit `SFX:` prefix: *"SFX: thunder cracks in the distance."* Sora 2 prefers describing the sound visually-and-aurally in prose: *"the kettle whistles sharply"* (the model infers SFX from cause). Seedance 2.0 follows Sora-style prose embedding.

Effective SFX prompting:

- **Cause and effect together.** *"The door slams; dust drifts down from the rafters."* The model adds the slam sound from the visual + verbal cue.
- **Position and distance.** *"Distant thunder rolls,"* *"footsteps echo close,"* *"a cymbal crashes off-camera."*
- **Timing.** *"A sudden snap on the third beat,"* *"a low rumble that builds throughout."*
- **Avoid onomatopoeia for naturalism.** *"Boom!"* and *"crash!"* prime cartoon-y mixing. Use *"a deep bass impact"* instead.

### Ambient bed / score

- **Ambient:** *"low traffic hiss and distant sirens,"* *"the quiet hum of a starship bridge,"* *"crickets and a single dog barking far off."* These produce the sound design that sells realism.
- **Score:** Veo and Sora 2 will attempt to generate underscore if asked. Be specific: *"a soft piano motif, melancholic, sparse"* > *"sad music."* Reference instruments, tempo, and dynamics: *"slow, fingerpicked acoustic guitar"* / *"swelling strings building over 4 seconds"* / *"a single sustained synthesizer drone."*
- **Hierarchy.** Sora 2 community guides note that default settings tend to mix ambient too loud relative to dialogue; explicitly state the mix: *"dialogue forward and clear; ambient bed soft underneath; no score."*

For reference-audio-driven generation (Seedance's `reference_audios`), the prompt should describe the visual that the audio drives: e.g. *"Maya speaks the line in [Audio1], her mouth movements matching exactly."*

---

## Failure modes & prompt mitigations

### Limb morphing & extra fingers

**Cause.** Hand and finger geometry has high configurational entropy and limited training-data frequency at clean caption granularity. Frame-to-frame, the model hallucinates plausible-but-different finger arrangements.

**Mitigations.**
- Hide hands when they're not the subject: *"hands resting on the table, palms down,"* *"hands in pockets,"* *"holding a coffee cup with both hands."*
- Anchor finger count and configuration: *"five fingers visible, fingers slightly curled."*
- Avoid actions that require articulated hands: typing, knitting, sign language, counting.
- For action with hands, freeze a pose: *"gripping the steering wheel at ten and two."*

### Flicker, warble, and high-frequency noise

**Cause.** Optical-flow estimation downstream of frame generation creates a feedback loop that amplifies small inconsistencies; sharpening filters in post amplify it further (LTX-2 warble guide).

**Mitigations.**
- *"Consistent lighting throughout,"* *"locked exposure,"* *"steady frame."*
- Avoid moiré-prone textures: *"plain wall background,"* not *"chain-link fence."*
- Avoid dense high-frequency motion: *"smooth water surface, gentle ripples,"* not *"choppy stormy sea with whitecaps."*

### Slow-motion bias

**Cause.** Training data over-represents cinematic slow-motion footage.

**Mitigation.** *"In real time,"* *"observational pace,"* *"natural speed,"* or specify visible fast motion (*"a moth's wings beat too fast to see clearly"*).

### Text rendering

**Cause.** Diffusion video models are spectacularly bad at coherent text, especially under camera motion or long words.

**Mitigations.**
- Avoid in-shot text. *"Unlabeled signage,"* *"a blank chalkboard."*
- Keep text very short (1–4 letters), front-on, and locked off: a stop sign at static eye-level is more reliable than a logo on a turning bus.
- For longer titles/typography, generate a still and composite in post.

### Identity drift across shots

**Cause.** The model has no persistent identity between generations; even within a clip, occluded reappearances can drift.

**Mitigations.**
- Use Seedance's `reference_images` (up to 9) and cite as `[Image1]` in prose.
- Describe distinguishing fixed features: *"a small scar above her left eyebrow,"* *"silver hair tied in a low braid,"* *"a faded blue work shirt."*
- Avoid fast occlusion-reveal patterns: don't have the character disappear behind something and reemerge in a 5s clip.

### Crowd morphing

**Cause.** Per-instance identity for many small subjects is unstable.

**Mitigations.**
- *"A crowd in soft focus,"* *"out-of-focus background figures,"* *"silhouettes against the window."*
- Reduce to small numbers: *"three people walking past."*

### Physics violations (cloth, liquid, hair)

**Cause.** Cloth and fluid simulation are emergent and weak.

**Mitigations.**
- Soft/gentle motion: *"a slight breeze,"* not *"a gale."*
- Avoid pouring/splashing/cloth-tearing as the focal action.
- Phrase consequences: *"her scarf lifts gently and falls,"* not just *"the wind blows."*

### Text-to-shot mismatch ("the model didn't do what I asked")

**Cause.** Long prompts dilute attention; the model's prompt-rewriter may simplify or reinterpret.

**Mitigations (per OpenAI Sora 2 cookbook).**
- Cut the prompt. *"Shorter prompts grant creative freedom; longer prompts restrict it."*
- Iterate: pin a working prompt, modify one element at a time.
- Lead with the visually-most-important element. The model attends most to the front of the prompt.

### Repetitive aesthetic ("everything looks the same")

**Cause.** Defaulting to "cinematic" gets you the model's prior, which is golden-hour shallow-DOF beige.

**Mitigation.** Force palette and stock anchors: *"high-contrast monochrome, hard noon sun, Tri-X grain"* / *"Cinestill 800T tungsten halation"* / *"flat overcast, no grade."*

---

## Sources

1. Runway. *Gen-4 Video Prompting Guide.* `help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide`.
2. Runway. *Gen-3 Alpha Prompting Guide.* `help.runwayml.com/hc/en-us/articles/30586818553107-Gen-3-Alpha-Prompting-Guide`.
3. Runway Academy. *Prompting Guide.* `academy.runwayml.com/guides/prompting-guide`.
4. OpenAI. *Sora 2 Prompting Guide* (Robin Koenig, Joanne Shin, Annika Brundyn; updated March 2026). `cookbook.openai.com/examples/sora/sora2_prompting_guide` (redirects to `developers.openai.com/cookbook/examples/sora/sora2_prompting_guide`).
5. fal.ai. *How to Write Prompts That Work for Sora 2.* `fal.ai/learn/devs/how-to-write-prompts-sora-2`.
6. Google DeepMind. *How to create effective prompts with Veo 3.* `deepmind.google/models/veo/prompt-guide/`.
7. Google Cloud. *Ultimate prompting guide for Veo 3.1.* `cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1`.
8. Google Cloud / Vertex AI. *Veo on Vertex AI video generation prompt guide.* `docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide`.
9. Tencent Hunyuan. *HunyuanVideo 1.5 Prompt Handbook (EN).* `github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/assets/HunyuanVideo_1_5_Prompt_Handbook_EN.md`.
10. Ambience AI. *Kling AI Prompt Guide (2026) — Camera & Negative Prompts.* `ambienceai.com/tutorials/kling-prompting-guide`.
11. fal.ai. *Kling 2.6 Pro Prompt Guide.* `fal.ai/learn/devs/kling-2-6-pro-prompt-guide`.
12. Hixx. *Kling 2.5 Prompt Guide: 70+ Camera Movement Commands.* `hixx.ai/blog/ai-industry-insights/kling-25-prompt`.
13. Luma Labs. *Dream Machine: Best Practices.* `lumalabs.ai/learning-hub/best-practices`.
14. Luma Labs. *Dream Machine: How to Use Camera Motion.* `lumalabs.ai/learning-hub/how-to-use-camera-motion`.
15. MiniMax. *Video Generation API Docs.* `platform.minimax.io/docs/guides/video-generation`.
16. getimg.ai. *Guide to Generating Videos with Hailuo MiniMax 01 Director.* `getimg.ai/guides/guide-to-generating-videos-with-hailuo-minimax-01-director`.
17. Higgsfield. *Prompt Guide to Cinematic AI Videos with Higgsfield Popcorn & Recast.* `higgsfield.ai/blog/Prompt-Guide-to-Cinematic-AI-Videos`.
18. Pika Labs. *Camera Parameters.* `pikalabs.org/camera-parameters/`.
19. StudioBinder. *Blade Runner 2049 Cinematography — Lighting, Color & Camera.* `studiobinder.com/blog/blade-runner-2049-cinematography-analysis/`.
20. PremiumBeat. *How Roger Deakins Shot and Lit Blade Runner 2049.* `premiumbeat.com/blog/blade-runner-2049-lighting-cinematography/`.
21. StudioBinder. *Roger Deakins Cinematography Style.* `studiobinder.com/blog/roger-deakins-cinematography/`.
22. Wikipedia. *Rembrandt lighting.* `en.wikipedia.org/wiki/Rembrandt_lighting`.
23. Fiveable. *Three-point lighting (Advanced Cinematography).* `fiveable.me/advanced-cinematography/unit-2/three-point-lighting/study-guide/e8LmJZ9P7j2gicjA`.
24. PetaPixel. *The Color Science Behind the Most Popular 35mm Films.* `petapixel.com/2025/11/17/the-color-science-behind-the-most-popular-35mm-films-available-today/`.
25. The Dark Room. *Portra 800 vs. Cinestill 800T.* `thedarkroom.com/portra-800-vs-cinestill-800t-which-is-best-for-you/`.
26. LTX. *How to Reduce Warble and AI Pattern Artifacts in LTX-2 Video Generation.* `ltx.io/model/model-blog/how-to-reduce-warble-and-ai-pattern-artifacts-in-ltx-2`.
27. Hailuo AI. *Recreate Wes Anderson Symmetry with AI Director Mode.* `hailuoai.video/pages/knowledge/wes-anderson-symmetry-ai-director-mode-guide-ed385`.
28. SmartScope. *Sora 2 Audio Engineering Guide.* `smartscope.blog/en/generative-ai/chatgpt/sora-2-audio-engineering-guide/`.
29. Skywork AI. *Sora 2 Audio Guide for Cameo and Import.* `skywork.ai/blog/sora-2-audio-guide-for-cameo-and-import/`.
30. Seedance Guide repo. `00_canonical_schema.md` (this project), Replicate API schema fetch 2026-05-04.
