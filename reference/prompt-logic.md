# Seedance 2.0 — Prompt Logic & Reference Library

## How to read this document
Seedance prompts work best as miniature production briefs, not image captions. The spine is a five-part structure: subject, action, camera, style, constraints. Put the visible subject first, give it one action, define the camera, anchor the look with lighting or film vocabulary, then close with constraints and audio. This order matters because early prompt tokens carry more weight.

Theory comes before examples because Seedance is sensitive to intent. A Wong Kar-wai tone piece, lip-synced founder reaction, motion-transfer dance clip, and storm-chaser dashcam cannot merely swap nouns into one template. Each category has different failure modes: face drift in real-person work, limb warping in action, beat slippage in dance, over-scored audio in SFX, or reference overfitting in motion transfer.

The categories move from text-only direction to reference-rich workflows. Categories 1-5 establish visual, temporal, and audio grammar. Categories 6-8 explain Seedance's differentiator: references cited as `[Image1]`, `[Video1]`, and `[Audio1]`. Category 9 is the production core for Silicon-Mania-style real-person likeness, where the same principles become stricter: short shots, medium close-ups, one speaker per shot, clean audio, repeated lighting language, and a locked post-grade.

## Category 1 — Cinematic / atmosphere / director pastiche
### Theory
Cinematic prompts reward specificity more than grand language. “Cinematic” alone usually produces a glossy default: shallow depth of field, warm grade, slow motion, generic faces. To get a real tone piece, load the prompt with production vocabulary that has a visual history: cinematographer names, film stocks, lenses, lighting setups, camera movement, and era-specific texture. A Wong Kar-wai prompt should mention step-printed motion, neon through rain, saturated red-green practicals, and smeared shutter drag. A Villeneuve-scale prompt should mention IMAX 70mm, desaturated negative space, monumental silhouettes, and restrained camera movement.

The model rewards a clean shot plan. For a 12- or 15-second cinematic clip, time-coded blocks act like editorial cuts: wide for geography, medium for character pressure, close-up for emotion, then an ending image. If you ask for one continuous atmosphere piece, use “single continuous take” and one camera move. If you want montage, use `[00:00-00:05]` blocks and name each cut. Avoid stacking three directors; one dominant reference plus one film-stock or lens reference is stronger than a taste salad.

Failure modes here are mostly drift and mush. Multiple style anchors can neutralize each other. Abstract mood words can override the physical scene. Slow-motion bias appears whenever the prompt says “beautiful,” “dreamlike,” or “epic” without “in real time.” The fix is concrete cinematography: “35mm handheld push-in,” “tungsten practicals,” “wet asphalt reflecting sodium-vapor streetlights,” “dialogue forward, rain soft underneath.”

### Three perfect prompts
#### 1. Rain Phone Booth, 1990s Hong Kong
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `16:9`
- duration: `10`
- generate_audio: `true`
- seed: `11001`

**Prompt:**
```text
[00:00-00:04] 1990s Hong Kong art-cinema tone piece. Medium shot through rain-streaked glass: a tired man in a khaki trench coat stands inside a red phone booth, holding the receiver without speaking. Neon smears red and green across the glass, Christopher Doyle handheld feel, Cinestill 800T halation.
[00:04-00:07] Cut to extreme close-up of his lips and one eye reflected in the wet glass. He whispers, "I kept the old number." Natural lip-sync, restrained emotion, rain ticking on metal.
[00:07-00:10] He hangs up and steps into the rainy crowd. Step-printed motion blur, slow shutter drag, no subtitles, no on-screen text.
```

**What this teaches:** One style anchor beats many.

#### 2. Desert Convoy Before the Wall
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `21:9`
- duration: `15`
- generate_audio: `true`
- seed: `11002`

**Prompt:**
```text
[00:00-00:05] Extreme wide IMAX 70mm desert shot in the Denis Villeneuve and Greig Fraser register: a tiny armored convoy races across hard salt flats while a mile-high sandstorm advances behind it, desaturated ochre palette, enormous negative space.
[00:05-00:10] Cut inside the lead rover, medium close-up of the driver gripping the wheel at ten and two, dashboard amber reflected in the visor. Camera shakes with engine vibration. He says, "Do not slow down." Sand hammers the windshield.
[00:10-00:15] Exterior low tracking shot as the rover crests a dune in real time, not slow motion. Dust swallows the frame, distant bass rumble, no gore, no text, hard cut to black.
```

**What this teaches:** Scale needs human pressure.

#### 3. Super 8 Summer Pool Memory
**Schema fields:**
- resolution: `720p`
- aspect_ratio: `4:3`
- duration: `8`
- generate_audio: `true`
- seed: `11003`

**Prompt:**
```text
Single continuous Super 8 home-movie shot, 1978 suburban pool party at golden hour. A child jumps once from the diving board into turquoise water while adults laugh out of focus behind patio chairs. Handheld 50mm equivalent, gate weave, dust specks, Kodak Ektachrome warmth, slight overexposure, water glittering in backlight. Audio: cicadas, pool splash, muffled laughter, no music, no modern objects, no text.
```

**What this teaches:** Single shots need one action.

## Category 2 — Character + dialogue (single character, no real-person)
### Theory
Single-character dialogue prompts live or die on restraint. Seedance can generate native speech from double-quoted lines, but it needs acting direction before the words. “She says, ‘I miss you’” produces a flat read; “she whispers, trying not to cry” gives the model facial tension, breath, and delivery. The best register for synthetic characters is the Japanese pure-love classroom style: warm light, tiny gestures, internal emotion, short dialogue, and ambient detail like cicadas, chalk dust, pen scratches, or hallway footsteps.

For one character, use medium close-up or close-up framing. A talking face is easiest to sync when the head is front or three-quarter, the camera is locked or slowly pushing in, and the line is 4-10 words. Avoid profile lip-sync unless the shot is silent. If the character must move, keep the action small: eyes lower, fingers pause on a notebook, shoulders rise with breath. The prompt should identify consistent hair, wardrobe, posture, and emotional arc even if no reference image is used.

The main failure modes are overacting, extra subtitles, and mouth mismatch. Seedance may invent captions during dialogue scenes, so close with “no subtitles, no on-screen text.” Long lines get rushed or paraphrased; split them into two short lines or use a 10-12 second duration. If you ask for fast acting and camera movement at the same time, the face softens. Keep the visual simple and spend the word budget on performance.

### Three perfect prompts
#### 1. Empty Classroom Confession
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `9:16`
- duration: `8`
- generate_audio: `true`
- seed: `12001`

**Prompt:**
```text
Medium close-up of a fictional Japanese high-school girl alone at a wooden classroom desk after sunset, summer uniform, straight black hair, silver hairpin, warm window light through blinds. Slow push-in. She looks at a half-written note, breathes in, then whispers with restrained embarrassment, "I waited after class again." Dust motes, cicadas, soft pen scratch, no music, no subtitles, natural lip-sync.
```

**What this teaches:** Restraint improves lip-sync.

#### 2. Diner Voice Memo
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `16:9`
- duration: `10`
- generate_audio: `true`
- seed: `12002`

**Prompt:**
```text
[00:00-00:05] Locked medium close-up of a fictional night-shift waitress in an empty roadside diner, early 30s, tired eyes, blue uniform, coffee steam rising in foreground, sodium-vapor parking-lot light through rain on the window.
[00:05-00:10] She raises her phone near her mouth, looks away from camera, and records softly, "I am fine. I just miss home." Natural breath before the second sentence. Audio: refrigerator hum, rain on glass, distant truck passing, dialogue forward and clear, no subtitles.
```

**What this teaches:** Room tone sells dialogue.

#### 3. Rooftop Apology
**Schema fields:**
- resolution: `720p`
- aspect_ratio: `3:4`
- duration: `6`
- generate_audio: `true`
- seed: `12003`

**Prompt:**
```text
Close-up of a fictional young man on an apartment rooftop at blue hour, wind lifting loose curls, plain gray hoodie, city lights blurred behind him. Camera is locked at eye level on an 85mm portrait lens, shallow depth of field, soft cool rim light and warm practical spill from the stairwell. He swallows, almost smiles, and says, "I should have called sooner." Gentle wind, distant traffic, no music, no extra characters, no subtitles.
```

**What this teaches:** One shot, one turn.

## Category 3 — Action / physics-heavy
### Theory
Action prompts need less mood and more choreography. The model can stage combat, racing, sport, and chase beats, but it is vulnerable to limb stretching, impossible contact, and unmotivated slow motion. The solution is to break the action into time-coded blocks and give each shot one physical task: “driver grips wheel,” “sprinter plants left foot,” “sword clash throws sparks.” Name body parts, count beats, and pair every movement with a consequence in the environment.

Slow-motion is a useful stabilizer but a bad default. If a full-speed parkour or fight move warps, ask for “one clear motion at medium speed” or “120fps slow motion conformed to 24fps.” If you need real-time urgency, state “in real time, natural pace” and keep the movement simpler. Avoid close-up hands during complex actions; show hands gripping a wheel or weapon, not articulating fine finger motion. For POV action, the phrase “single continuous take, no cuts, natural head movement” is essential because Seedance otherwise invents coverage.

Sound direction matters in action because it gives events weight. Tire spray, breath inside a helmet, crowd roar, shield impact, water pressure, thunder crack, and fabric snap all help the model bind motion to cause. The strongest action prompts choose a frame grammar: cockpit cam, low tracking shot, POV shoulder bash, overhead sport coverage. The weakest ask for “epic battle, dynamic camera, fast motion” without enough spatial rules.

### Three perfect prompts
#### 1. Wet Track Green Light
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `16:9`
- duration: `15`
- generate_audio: `true`
- seed: `13001`

**Prompt:**
```text
[00:00-00:05] Interior cockpit medium close-up of a veteran race driver at night, rain lashing the windshield, dashboard LEDs reflected in the visor. He tightens both gloved hands on the wheel at ten and two, breathing steady.
[00:05-00:10] Cut to rival cockpit, younger driver in the next car, jaw tense, eyes forward, engine vibration shaking the frame. He whispers, "Hold the line."
[00:10-00:15] Low exterior tracking shot as the green light hits and both cars accelerate in real time on wet asphalt. Massive water spray hits the lens, stadium lights stretch into motion blur, engines roar, no limb distortion, no text.
```

**What this teaches:** Fixed hands reduce warping.

#### 2. POV Arena Shield Bash
**Schema fields:**
- resolution: `720p`
- aspect_ratio: `16:9`
- duration: `8`
- generate_audio: `true`
- seed: `13002`

**Prompt:**
```text
Single continuous POV gladiator shot, no cuts, no zoom, natural head movement. The camera stands on sand inside a roaring arena. One armored opponent sprints toward camera with a raised sword. The camera braces; a round shield enters frame and slams into him once. He falls out of frame as sand kicks up. Camera turns right to reveal another fighter. Raw handheld realism, real-time pace, metal impact, crowd roar, breathing, no gore, no subtitles.
```

**What this teaches:** POV needs continuity rules.

#### 3. Water Versus Thunder Clash
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `21:9`
- duration: `12`
- generate_audio: `true`
- seed: `13003`

**Prompt:**
```text
[00:00-00:04] Moonlit forest, live-action anime adaptation look, dark samurai wardrobe, no gore. A swordsman lowers his center of gravity and draws one blade; blue water spirals around the steel as leaves lift from the mud.
[00:04-00:08] Opponent crouches in an iaijutsu posture and launches forward in a sharp Z-shaped thunder dash, golden arcs scattering wet leaves, medium speed to preserve body form.
[00:08-00:12] Their swords meet at center frame. Water and lightning collide into a blue-gold pressure wave, mud splashes toward camera, bass impact and thunder crack, no extra limbs, no text.
```

**What this teaches:** Effects need simple poses.

## Category 4 — Dance / beat-sync
### Theory
Dance is not “a person dancing.” It is a rhythmic shot list. Seedance responds well when the prompt describes center of gravity, shoulders, hips, knees, feet, and camera coverage in relation to the beat. The @ZetoGroovin-style vertical MV format works because it uses short cuts, full-body coverage at the start and end, inserts of hands or feet, and constrained choreography: not extreme breakdancing, not broad arm swings, not high jumps, but repeatable live-action movement that fabric and hair can follow.

The model cannot hear an uploaded music track unless you use reference audio, but with native audio it can generate a beat if you request one. Use BPM language, cut timing, and clear musical sections: intro groove, best steps in the middle, signature pose at the end. For 9:16, keep the body centered and define a full-body frame, otherwise Seedance may crop feet. For 16:9 group or couple dance, avoid complex crowd choreography; two bodies are already enough.

Failure modes include beat slippage, foot morphing, hands stretching, and sudden camera zooms. The fix is to keep the dancer at medium distance for footwork, cut to upper-body for hand gestures, and explicitly say “feet remain fully visible during full-body shots.” If you use a character reference, cite the image with purpose: `[Image1] defines face, hairstyle, outfit, colors, and silhouette.` Do not ask the model to invent twenty micro-cuts unless the duration is 15 seconds and the motion is simple.

### Three perfect prompts
#### 1. Vertical Character Dance MV
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `9:16`
- duration: `15`
- generate_audio: `true`
- reference_images: `[Image1]`
- seed: `14001`

**Prompt:**
```text
Generate a 15-second vertical live-action dance MV using the person or character from [Image1]. [Image1] defines face, hairstyle, outfit colors, and silhouette. Only one dancer, centered, feet visible in full-body shots. Soft natural light, realistic fabric sway, shallow depth of field.
[00:00-00:05] Full-body intro groove at 100 BPM, small shoulder bounce, knees bending lightly, hands close to torso.
[00:05-00:10] Beat-locked cuts between above-knees frame, face close-up, and feet doing two clean side steps; no jumps, no wide arm swings.
[00:10-00:15] Slow turn, hair sways, end in a lingering signature pose. Native pop beat, soft room reflections, no subtitles.
```

**What this teaches:** Choreography beats mood.

#### 2. Rooftop Footwork Loop
**Schema fields:**
- resolution: `720p`
- aspect_ratio: `9:16`
- duration: `8`
- generate_audio: `true`
- seed: `14002`

**Prompt:**
```text
Single dancer on a concrete rooftop at sunset, full-body vertical framing, feet visible throughout. He performs a clean four-count shuffle: right foot taps out, left foot crosses, both heels pivot, small shoulder pop, then repeats once. Camera is locked, 35mm equivalent, no zoom. Warm rim light, city skyline soft in background, upbeat 110 BPM house groove, shoe squeaks lightly on concrete, natural hands, no extra fingers, no text.
```

**What this teaches:** Counts stabilize feet.

#### 3. Ballroom Beat Cut
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `16:9`
- duration: `12`
- generate_audio: `true`
- seed: `14003`

**Prompt:**
```text
[00:00-00:04] Wide shot of a fictional ballroom couple in red and black formalwear on a marble floor, audience blurred in bokeh. They hold frame and sway once to a slow Latin rhythm.
[00:04-00:08] Medium tracking orbit as the lead guides one controlled spin; the red dress hem arcs through the light, feet remain natural.
[00:08-00:12] Close two-shot as they settle into a dip and hold eye contact. Brass percussion, soft crowd murmur, beat-synced camera cuts, no impossible lifts, no subtitles.
```

**What this teaches:** One partnered move per shot.

## Category 5 — SFX / native-audio showcase
### Theory
Seedance 2.0’s native audio is not decoration; it is a control surface. The strongest SFX prompts describe sound causes, sound distance, and mix hierarchy. “Audio: sizzle” is weaker than “fat renders, bubbles aggressively, butter foams, occasional pan clink, no music.” The model links what it sees to what it hears, so visible sources should produce the foreground sounds: steak on cast iron, rain on windshield, keys striking piano strings, thunder inside a funnel cloud.

For sound-led prompts, visual composition should be simpler than the audio. Macro ASMR works because the subject is stable and the ear carries complexity. Jazz-club prompts work when each instrument has a place in the scene: hands on piano, brushed snare behind, walking bass off-camera, crowd murmur low. Dashcam or documentary SFX prompts should keep the camera motivated: fixed dashboard, bodycam, handheld phone, lav mic, or field recorder. This gives audio a plausible recording perspective.

Failure modes are over-scoring, cartoon impacts, and dialogue hallucination. If you do not want music, say “no music, no voice.” If you want dialogue, keep it brief and define whether it is foreground or radio/background. Avoid onomatopoeia like “boom” as text; use “deep bass impact” or “sharp thunder crack.” When `generate_audio=true`, always mention ambient, foreground SFX, and score policy. Otherwise the model invents a generic cinematic bed that can flatten the realism.

### Three perfect prompts
#### 1. Cast-Iron Steak ASMR
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `9:16`
- duration: `8`
- generate_audio: `true`
- seed: `15001`

**Prompt:**
```text
Extreme macro close-up of a steak hitting a black cast-iron skillet, background fully blurred. Fat renders, bubbles along the crust, butter foams around rosemary and garlic, steam blooms into warm tungsten light. Slow dolly-in, probe-lens feel, razor-thin depth of field. Audio: aggressive sizzle, fat crackle, one tong clink at end, no music, no voice, no text.
```

**What this teaches:** Name the sound source.

#### 2. Smoky Jazz Keys
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `16:9`
- duration: `10`
- generate_audio: `true`
- seed: `15002`

**Prompt:**
```text
Close-up of a jazz pianist's hands moving across a grand piano in a small smoky club, amber stage lamps reflected in black lacquer, 35mm film grain, shallow depth of field. Fingers move with believable precision but never extreme close macro. Each phrase produces a subtle warm ripple across the piano surface. Audio: piano forward and dry, soft brushed snare behind, walking double bass off-camera, low audience murmur, no vocals, no subtitles.
```

**What this teaches:** Place every instrument.

#### 3. Storm-Chaser Dashcam
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `16:9`
- duration: `12`
- generate_audio: `true`
- seed: `15003`

**Prompt:**
```text
Dashboard-camera POV in a storm-chaser truck approaching a tornado on an empty rural road. Fixed wide lens through rain-streaked windshield, wipers crossing twice, vehicle vibration, gray-green sky, lightning inside the funnel. Rain escalates from steady to violent. Audio: loud windshield rain, rhythmic wipers, low wind buffeting, distant radio chatter saying "rotation is tightening", no music, no text.
```

**What this teaches:** Perspective shapes sound.

## Category 6 — Multimodal — character consistency via [Image1]...[Image9]
### Theory
Seedance’s nine-image reference ceiling is the practical engine for consistent characters. The model does not automatically know why each image exists, so the prompt must cite references with purpose. `[Image1]` can define the face, `[Image2]` the three-quarter angle, `[Image3]` wardrobe, `[Image4]` lighting, and so on. A bare mention of `[Image1]` is weaker than “face and hairstyle strictly follow [Image1] and [Image2]; wardrobe follows [Image5]; lighting follows [Image8].”

The best 9-image traversal prompts use the references as identity anchors across scene changes. They should not ask the character to transform into nine different people. Instead, keep one face, one wardrobe rule, and let the environment or style change. Time-coded blocks re-anchor the character every few seconds. If a 15-second clip contains three cuts, each block should repeat the identity lock in brief form or state at the top that identity is preserved throughout.

Failure modes include face flicker, wardrobe drift, and the model treating reference images as style moodboards instead of identity. To prevent that, separate identity references from environment references in the prompt. Do not combine `image` first-frame mode with `reference_images`; Replicate rejects that combination. If the character crosses nine art styles, the face will soften unless you state that facial geometry, hairline, and eye shape remain constant. Use medium shots, not extreme action, when testing identity preservation.

### Three perfect prompts
#### 1. Nine-Frame Character Bible Walk
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `16:9`
- duration: `15`
- generate_audio: `true`
- reference_images: `[Image1]...[Image9]`
- seed: `16001`

**Prompt:**
```text
Use [Image1], [Image2], [Image3], and [Image4] only for the same fictional woman's face, hairline, eye shape, and expressions. Use [Image5] for her blue jacket wardrobe. Use [Image6], [Image7], [Image8], and [Image9] as environment and lighting references. Preserve identity throughout.
[00:00-00:05] Medium shot as she walks through the rainy street from [Image6], blue jacket unchanged, soft neon reflections.
[00:05-00:10] Cut to a warm train carriage inspired by [Image7], same face and jacket, slow push-in.
[00:10-00:15] Cut to rooftop blue hour matching [Image8] and [Image9], she turns to camera and smiles once. Ambient rain-to-train-to-wind sound bridge, no dialogue, no text.
```

**What this teaches:** Assign reference jobs.

#### 2. Painting Traversal With Locked Face
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `9:16`
- duration: `12`
- generate_audio: `true`
- reference_images: `[Image1]...[Image9]`
- seed: `16002`

**Prompt:**
```text
A fictional girl steps through nine painted worlds while her face, hair, and yellow raincoat remain consistent. [Image1] defines her face and hair; [Image2] defines the yellow raincoat; [Image3] through [Image9] define painterly environments only, not her identity.
[00:00-00:04] Medium shot: she steps out of the first painting, brushstrokes moving around her.
[00:04-00:08] Match cut through three painted rooms, her face unchanged, medium close-up framing.
[00:08-00:12] She reaches the final night cafe painting and looks back. Soft canvas rustle, light footstep taps, no spoken dialogue, no on-screen text.
```

**What this teaches:** Protect identity from style.

#### 3. Product Mascot Across Ads
**Schema fields:**
- resolution: `720p`
- aspect_ratio: `1:1`
- duration: `10`
- generate_audio: `true`
- reference_images: `[Image1]...[Image4]`
- seed: `16003`

**Prompt:**
```text
Use [Image1] and [Image2] for the same original mascot character's face, proportions, and color palette. Use [Image3] for packaging shape and [Image4] for the clean studio lighting style.
[00:00-00:03] Centered product-table shot, mascot peeks from behind the package, exact colors preserved.
[00:03-00:07] Medium shot, mascot slides the package forward with simple hands, no finger detail, white seamless background.
[00:07-00:10] Hero pose beside the package, soft shadow, gentle camera push-in. Audio: small fabric rustle, cheerful two-note synth sting, no voice, no labels or text.
```

**What this teaches:** Separate shape and style.

## Category 7 — Multimodal — motion transfer via [Video1]
### Theory
Motion transfer is the Seedance differentiator: keep the motion of a reference video while replacing the subject with an image-defined character. The prompt must say exactly that, but good results need more than the famous short form. `[Video1]` should be cited for motion, camera path, and timing, while `[Image1]` should be cited for identity, outfit, and silhouette. If you leave the purpose ambiguous, Seedance may copy the source subject too closely or let the new identity drift.

Use short, clean source videos. A 3-5 second motion reference is easier to transfer than a busy 15-second montage. Because reference video duration is capped at 15 seconds total, do not waste it on lead-in or dead frames. If the source contains fast limbs, ask for “same overall motion timing, simplified natural body mechanics” rather than exact articulation. If the source has a camera move, decide whether to keep it. “Keep [Video1] camera motion and body timing” is different from “keep body choreography only, use a locked camera.”

Failure modes are over-copying, mismatched body proportions, and motion that works for one subject but not another. A skateboard trick mapped to a person in a long coat may break cloth and limbs; a dance move mapped to a robot can work if you describe rigid joints. The prompt should translate the motion into natural language so text and video agree. Use `reference_videos`, not `image` first-frame, when the motion source is the priority.

### Three perfect prompts
#### 1. Replace Dancer, Keep Groove
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `9:16`
- duration: `8`
- generate_audio: `true`
- reference_images: `[Image1]`
- reference_videos: `[Video1]`
- seed: `17001`

**Prompt:**
```text
Keep the body timing, rhythm, and camera movement of [Video1], but replace the dancer with the original character from [Image1]. [Image1] defines face, hairstyle, outfit, colors, and silhouette. Preserve the same step sequence from [Video1]: small side steps, shoulder bounce, half-turn, final pose. Make the motion natural for this character, with stable hands and feet, centered vertical composition. Native upbeat pop beat matching the movement, no subtitles, no text.
```

**What this teaches:** Split motion from identity.

#### 2. Product Orbit From Reference Move
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `16:9`
- duration: `6`
- generate_audio: `true`
- reference_images: `[Image1]`
- reference_videos: `[Video1]`
- seed: `17002`

**Prompt:**
```text
Use [Video1] only for camera orbit timing and speed. Replace the subject with the product in [Image1], keeping exact shape, material, and color. Clean studio hero shot: camera orbits 120 degrees, reflections glide across the surface, matte charcoal background. Subtle electronic hum, one soft bass hit on the final centered frame, no voice, no labels, no extra objects.
```

**What this teaches:** Video can guide camera only.

#### 3. Stunt Motion, Safer Body
**Schema fields:**
- resolution: `720p`
- aspect_ratio: `16:9`
- duration: `10`
- generate_audio: `true`
- reference_images: `[Image1]`
- reference_videos: `[Video1]`
- seed: `17003`

**Prompt:**
```text
Use [Video1] for parkour timing and shoulder-cam follow, but simplify body mechanics for the fictional athlete from [Image1]. [Image1] defines face, outfit, and proportions. The athlete runs three steps, plants the left foot, vaults one low concrete barrier, and lands cleanly. Real-time pace, no flips, no limb stretch. Audio: footsteps, breath, jacket fabric, city ambience, no music.
```

**What this teaches:** Counted actions reduce warp.

## Category 8 — Multimodal — lip-sync via [Audio1] + [Image1]
### Theory
Seedance’s reference-audio path is the native lip-sync workflow: provide a face reference and audio clip, then cite `[Audio1]` as the line to match. Replicate requires at least one image or video reference when using `reference_audios`; audio alone is invalid. Include the quoted line when possible, because it tells the model the semantic content and delivery. `[Audio1]` tells it timing and voice. Best line length is short: 4-10 words for a 5-6 second clip, maybe two short sentences in 8-10 seconds.

The visual setup should make lip-sync easy. Use locked medium close-up, front or three-quarter angle, mouth visible, no profile, no hands crossing the face, no extreme head turns. If the source image has mouth slightly open, it often helps the model calibrate speech shapes. Audio should be clean, trimmed to the intended duration, and no longer than 15 seconds total across references. Use `generate_audio=true`; the generated output should include the reference-driven speech and any prompted ambient bed.

Failure modes are mouth softness, line truncation, and conflicting audio directions. Do not ask for heavy music under a lip-sync test. Specify “dialogue forward and clear; ambient bed soft underneath.” If using a cloned or public-material voice, make sure you have consent or legal rights and respect voice-provider restrictions. For synthetic characters, the same technical rule applies: clean audio, short line, simple face shot.

### Three perfect prompts
#### 1. Studio Monologue From Voice Clip
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `9:16`
- duration: `6`
- generate_audio: `true`
- reference_images: `[Image1]`
- reference_audios: `[Audio1]`
- seed: `18001`

**Prompt:**
```text
Locked medium close-up of the fictional woman from [Image1] in a podcast studio, front three-quarter angle, mouth visible, headphones on, soft key from camera-left, dim purple practical behind. She speaks the exact line in [Audio1], matching mouth movements, with the intended words: "We need to talk about tomorrow." Dialogue forward, room tone soft underneath, no music, no subtitles, no head turn.
```

**What this teaches:** Audio timing, text meaning.

#### 2. Animated Character Voice-to-Face
**Schema fields:**
- resolution: `720p`
- aspect_ratio: `1:1`
- duration: `5`
- generate_audio: `true`
- reference_images: `[Image1]`
- reference_audios: `[Audio1]`
- seed: `18002`

**Prompt:**
```text
Square close-up portrait of the original animated character from [Image1], reinterpreted as polished 3D animation while preserving face shape, hair, eyes, and outfit colors. The character looks directly at camera and lip-syncs to [Audio1], saying "That was not in the plan." Small eyebrow lift on the final word, simple head stillness, clean studio background, dialogue clear, no extra captions, no music.
```

**What this teaches:** Keep the mouth readable.

#### 3. Video Reference Plus Audio Line
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `16:9`
- duration: `8`
- generate_audio: `true`
- reference_images: `[Image1]`
- reference_videos: `[Video1]`
- reference_audios: `[Audio1]`
- seed: `18003`

**Prompt:**
```text
Use [Image1] for the fictional man's face, hair, and wardrobe. Use [Video1] only for the slow seated lean-in and camera framing. He sits at a warm podcast desk, medium close-up, condenser microphone in foreground. He lip-syncs exactly to [Audio1], saying "I read the abstract twice." Keep the mouth visible, no hand covering face, shallow depth of field, soft studio room tone, no score, no subtitles.
```

**What this teaches:** One purpose per reference.

## Category 9 — REAL-PERSON LIKENESS
### Theory
The Silicon Mania format is rising because it turns public tech discourse into a recurring cast-driven show. Founders, investors, and public figures are recognizable not just by face, but by cadence, wardrobe, set grammar, and the kinds of lines they plausibly say. “The Buzzer” works because its real founder and investor cast members are tagged collaborators who amplify the joke. That participatory consent model is the standard to copy: use collaborators, public figures in legitimate commentary or satire, and people who know they are part of the piece. Do not build a workflow around private individuals or undisclosed impersonation.

The production method is strict. Build a 6-9 image face-reference set: front neutral, front mouth slightly open, three-quarter left, three-quarter right, one profile, expression range, consistent lighting, high resolution, and wardrobe anchor. Use the same set across a whole episode. For lip-sync, reference audio can come from public material such as interviews, podcasts, public speeches, or collaborator-provided recordings, but voice platforms have policies. ElevenLabs maintains No-Go voice restrictions and prohibits cloning without consent or legal right; active political figures and high-risk celebrity voices can be blocked. Public-material sourcing is a norm, not a permission slip.

Seedance is attractive because it is more permissive and reference-rich than Sora 2 and Veo 3.1, which hard-block many public-figure workflows unless official opt-in systems are used. ByteDance first-party tooling has a Real Human liveness gate; Replicate does not surface that gate today, but server-side classifiers can still flag identifiable people. Treat every real-person render as policy-sensitive.

Creatively, think in stitched clips: 30-80 second episodes are usually 4-10 Seedance shots, rendered at 4-15 seconds and trimmed to 2-6 seconds. Use medium close-ups, single-character coverage, cross-cut exchanges, 4-10 word lines, matched lighting, and a locked LUT. B-roll cutaways hide line extensions and continuity jumps. Audio bridges and a shared grade do as much work as the prompt.

### Three perfect prompts
#### 1. Tagged Founder Reaction Shot
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `9:16`
- duration: `5`
- generate_audio: `true`
- reference_images: `[Image1]`
- reference_audios: `[Audio1]`
- seed: `19001`

**Prompt:**
```text
Participatory creator-commentary shot featuring the tagged founder represented by [Image1], used with permission. Locked vertical medium close-up in a startup office, chest-up, front-three-quarter face, mouth visible, gray hoodie, laptop glow low on the face. The founder reacts to off-screen news and lip-syncs to [Audio1], saying "Wait, they raised at what valuation?" Dialogue forward, faint office HVAC, no music, no subtitles, no endorsement claim.
```

**What this teaches:** Consent, short line, MCU.

#### 2. Founder-Investor Buzzer Exchange
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `16:9`
- duration: `15`
- generate_audio: `true`
- reference_images: `[Image1], [Image2]`
- seed: `19002`

**Prompt:**
```text
Participatory Silicon-Mania-style founder-investor parody; both people are tagged collaborators. [Image1] defines the founder's face, hair, and wardrobe. [Image2] defines the investor. Cross-cut medium close-ups only, one person on screen at a time, same red-lit pitch room, locked LUT: slightly desaturated, blue-magenta shadows, fine grain.
[00:00-00:05] Founder MCU, warm key from camera-left, says "It is cake as a service."
[00:05-00:10] Investor reverse MCU, same lens and lighting, deadpan, says "How is that venture scale?"
[00:10-00:15] Founder MCU, tiny nervous smile, says "The frosting has AI." Ambient room tone, soft buzzer hum under final line, no subtitles, no public-figure impersonation beyond the cited collaborators.
```

**What this teaches:** Cross-cut real people.

#### 3. B-Roll Continuity Insert
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `16:9`
- duration: `6`
- generate_audio: `true`
- reference_images: `[Image1], [Image2]`
- seed: `19003`

**Prompt:**
```text
B-roll continuity shot for the same founder-investor episode. Use [Image1] and [Image2] only for wardrobe and lighting continuity, not close face generation. Empty red-lit pitch-room table: two water glasses, one laptop, small glowing buzzer center frame, blurred silhouettes at edges, no readable faces. Locked 50mm slow push-in, same desaturated blue-magenta LUT, fine grain, HVAC, chair creak, no dialogue, no music, no text.
```

**What this teaches:** B-roll hides continuity risk.

## Category 10 — Abstract / motion graphics / experimental
### Theory
Abstract prompts reward sequence logic. Because there may be no human subject to stabilize the frame, the prompt must define state changes: point becomes line, line becomes grid, grid becomes sphere, sphere collapses to logo. Numbered or time-coded transformations are better than poetic abstraction. For experimental loops, the beginning and ending state matter most; say “loop-ready, first and last frames match” if the asset is meant to repeat.

Motion graphics also need hard style constraints. “Vercel intro” implies black-and-white geometry, mathematical precision, UI panels, and high contrast. A mercury sphere loop implies rigid studio lighting, mirror surface, liquid metal deformation, and no extra particles unless requested. A living painting prompt should name brush texture, palette, and how motion follows the medium: paint flows with brushstrokes, not realistic wind.

The failure modes are logo/text hallucination, uncontrolled extra colors, and mushy transformations. Seedance is weak at readable typography, so do not ask for a brand wordmark unless you will replace it in post. Say “clean centered abstract mark” or “blank logotype placeholder” instead. With no human scale, camera language still matters: locked-off macro, centered orthographic, slow orbit, top-down, or full-bleed. For audio, motion graphics often work with minimal electronic pulses or no audio; if you leave audio open, the model may add cinematic music that makes a clean design piece feel like a trailer.

### Three perfect prompts
#### 1. Black-Line Interface Bloom
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `16:9`
- duration: `8`
- generate_audio: `true`
- seed: `20001`

**Prompt:**
```text
Pure black background, self-illuminating white geometric lines only, Vercel-style precision. [00:00-00:02] A white point pulses at center, ripple rings expand. [00:02-00:04] The point stretches into a line, then tiles into a 3x3 grid. [00:04-00:06] Grid bends into a rotating wireframe sphere. [00:06-00:08] Sphere unfolds into UI panels around a clean abstract mark, no readable letters. Audio: minimal ticks, one soft sub pulse, no voice.
```

**What this teaches:** Sequence the abstraction.

#### 2. Mercury Sphere Loop
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `1:1`
- duration: `6`
- generate_audio: `false`
- seed: `20002`

**Prompt:**
```text
Loop-ready studio macro shot of a perfect liquid mercury sphere on a black mirror surface. Locked camera, centered composition, cool white strip lights reflected across the metal. Over 6 seconds the sphere slowly deforms into a rounded cube under an invisible force, then returns exactly to the original sphere shape by the final frame. First and last frames match for seamless playback. No text, no logo, no extra objects, no camera movement.
```

**What this teaches:** Match first and last frames.

#### 3. Living Impasto Night
**Schema fields:**
- resolution: `1080p`
- aspect_ratio: `4:3`
- duration: `12`
- generate_audio: `true`
- seed: `20003`

**Prompt:**
```text
Living post-impressionist oil painting, thick impasto texture, saturated blue-yellow contrast, swirling brushstrokes. A night sky above a small sleeping town moves as if the wet paint itself is breathing. The cypress tree twists like a dark flame, yellow stars rotate in slow circular strokes, window lights pulse gently. Camera is locked, no 3D realism, no modern objects, no readable text. Audio: faint canvas creak, soft wind-like drone, no melody, painterly motion only.
```

**What this teaches:** Let medium drive motion.

## Cross-cutting principles
The universal pattern is the five-part structure: subject, action, camera, style, constraints. Subject is the object of attention with two or three concrete traits. Action is one visible verb, not plot. Camera is shot size, angle, lens, and movement. Style is lighting, palette, stock, director, or medium. Constraints are production rules that prevent common failures: no subtitles, single continuous take, no extra characters, hands resting naturally, dialogue clear over soft ambience.

Time-coded blocks are the highest-leverage format for anything longer than a simple single shot. In Seedance, `[00:00-00:05]` behaves like an editorial instruction even though the API exposes only one free-form prompt field. Use blocks to re-anchor identity, wardrobe, palette, and camera every few seconds. A 15-second clip should usually be three shots, not seven, unless it is a beat-sync montage. For stitched episodes, render 5-15 second clips and trim them to 2-6 seconds in the edit.

Audio direction is mandatory when `generate_audio=true`. Describe foreground sound, ambient bed, and score policy. Dialogue belongs in double quotes. If using reference audio, cite `[Audio1]` and keep total audio references within 15 seconds. Use short lines at roughly two words per second. Mix language matters: “dialogue forward and clear; room tone soft underneath; no music” often performs better than visual detail alone.

Seedance has no negative-prompt field, so exclusions must be embedded as positive production instructions. “Hands resting in lap, fingers relaxed” is stronger than “no bad hands.” “Single continuous take” is stronger than “no cuts.” Some direct negatives are still useful at the end of a prompt: “no subtitles, no on-screen text, no watermarks.” Keep them short and do not prime the model with long lists of unwanted artifacts.

Word budget should follow shot complexity. Single-shot prompts can be 50-90 words. Character dialogue and SFX prompts often land around 90-160. Multi-shot, multimodal, and real-person prompts can run 180-280 words, but contradictions rise after that. Repeating the same lighting phrase across shots is useful; repeating every detail is not. If a prompt fails, remove one demand before adding three more.

Aspect ratio changes composition. `9:16` favors medium close-ups, full-body centered dance, and social reactions. `16:9` supports cross-cut dialogue, cars, rooms, and action geography. `21:9` is best for epic landscapes and cinematic scale. `1:1` works for product, mascot, and loopable abstract assets. Put the same ratio logic into the prompt body when framing is critical: “vertical full-body, feet visible,” or “widescreen cross-cut medium close-ups.”

## Final notes for the build
The guide should make users choose a production mode before writing: text-only tone piece, native dialogue, native SFX, image reference, motion transfer, lip-sync, or real-person stitched episode. The UI should expose safe durations `{4, 5, 6, 8, 10, 12, 15}` and `-1`, show the mutually exclusive `image` versus `reference_images` rule, and note that `reference_audios` requires an image or video reference.

For the Silicon Mania lane, make conservative defaults easy: 1080p, MCU, 5 or 6 seconds, one character per shot, 4-10 word lines, locked lighting, bracket citations, and a B-roll generator. The theory is the manual for spending budget well.
