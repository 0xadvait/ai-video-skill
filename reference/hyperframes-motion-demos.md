# HyperFrames motion demos — cursor-driven product demos & composed video (HTML → MP4)

This skill *generates* clips. **HyperFrames** is the other half: a deterministic
HTML/CSS/SVG/GSAP → MP4 engine for *composed* video — cursor-driven product demos,
UI walkthroughs, kinetic typography, title/end cards, anything where you control
every frame. AI stills (`imagegen.py`) and AI clips (`generate.py`, i2v) drop in as
**assets on the HyperFrames timeline**.

Reach for HyperFrames (not `assemble.py`) whenever the deliverable is a *designed /
animated* piece, not just stitched AI footage. There is also a standalone
`hyperframes` skill for framework mechanics — this file is the distilled craft +
gotchas from real product-demo builds.

## The engine (gotchas first)
- A composition is one HTML file: `data-*` timing + a GSAP timeline registered on
  `window.__timelines["main"]` (built `{paused:true}`) + CSS. `data-duration` on the
  root drives length (not the GSAP timeline length).
- **Run the real binary.** `npx`/`npm` may be shell-aliased (e.g. a Socket security
  wrapper) — if so, call the actual Node `npx` directly (find it with `which -a npx`,
  e.g. `~/.<node-install>/bin/npx hyperframes …`), or the CLI silently does the wrong
  thing. Commands: `lint`, `inspect`, `snapshot --at 1.5,4`, `render`.
- **Deterministic only** — no `Date.now()`, `Math.random()`, no network fetches at
  render time. Seed any pseudo-randomness; pass timestamps in.
- **Hidden initial state belongs in CSS/attrs, NOT a late `tl.set(sel,{opacity:0},0)`.**
  A late set flashes the element visible during the previous scene's crossfade. (Cost
  us this bug 3×.)
- Render 4K: `render --resolution landscape-4k --fps 30 --quality high --crf 14`.
  A ported background shader canvas is native 3840×2160 — it (and any full-frame CSS
  `filter: blur`) is the render cost; expect ~60–90s. Mux music afterward:
  `ffmpeg -i v.mp4 -i music.mp3 -filter_complex "[1:a]volume=0.62,afade=t=in:st=0:d=1.5,afade=t=out:st=<end-3.5>:d=3.5,apad[a]" -map 0:v:0 -map "[a]" -t <dur> -c:v copy -c:a aac -b:a 256k -movflags +faststart out.mp4`.
- **Avoid full-frame linear gradients on dark** — H.264 bands them visibly. Use a
  radial gradient, or a solid fill + a localized glow.
- **Always run `hyperframes inspect`** (not just eyeball a contact sheet) before
  declaring done — it catches text overflowing a card / off-canvas drift you'll miss.
  The only "expected" overflow is a deliberately scrolling marquee.

## The "premium product demo" look (what actually lands)
Modeled on Ritual/Ollie-style demos tuned for phone-feed legibility. The levers that
repeatedly worked:
- **A floating app window over a REAL shader.** `#app`: `border-radius`, big shadow,
  `overflow:hidden`, `transform-origin:0 0`. Behind it, the brand's ACTUAL background
  (e.g. the landing page's WebGL vector-field gradient) ported to raw WebGL and driven
  deterministically by a GSAP proxy: `tl.to(bgp,{t:DUR,duration:DUR,ease:"none",onUpdate:()=>window.__drawBG(bgp.t)})`.
  Never invent a generic CSS gradient — port the real one.
- **Camera = a transform on `#app`** (origin 0 0). To frame app-point (Tx,Ty) at scale
  S: `x = 960 - S*Tx`, `y = 540 - S*Ty`. PUSH INTO each beat — big type + zoom = legible
  on a phone feed. Fill the frame; a pan that reveals a bright strip at the edge reads
  as a mistake.
- **Cursor + click ripples live INSIDE `#app`** so they stay aligned to elements under
  the camera transform. The **end card lives OUTSIDE `#app`** so the camera zoom never
  scales it.
- **Tactile motion:** springy entrances (`back.out(1.9–2.6)` + scale); a click effect
  (cursor presses to scale 0.74 → `back.out(3)` release + an expanding ripple/ring); a
  live-dot heartbeat so holds aren't dead-static.
- **Port the real design** — exact colors, fonts (Geist…), and the real logo *file* —
  from the source repo. Inventing a "close enough" page or logo gets rejected ("wrong
  logo" twice).

## Legibility & narrative (for a social / phone feed)
- **One idea on screen per beat**, big and high-contrast; hold each ~2–2.5s. Don't
  stack three things — push into the single thing that matters.
- **Length is flexible** — reading time beats hitting an exact round number (30s).
  Cut to the rhythm of comprehension, not a stopwatch. When in doubt, tighten.
- **Show, don't tell.** Animate the actual transformation (a request card travels a
  pipeline and visibly locks/redacts; an image resolves in) rather than narrating it
  with captions. Captions support the visual, they don't replace it.
- **Annotate the payoff, on-brand.** A ring-flash on the thing that just changed, or
  an underline drawn under the one payoff line, directs the eye — Ollie-style, but in
  the product's own palette.
- **Borrow a reference's STRUCTURE, not its gimmicks.** Steal the pacing and the
  camera-push discipline; drop the hand-cursor / sticky-notes / red-marker bits if
  they're off-brand for a premium product.

## UI-state composition & using the real product
- **Use the product's REAL models / assets / design**, never generic stand-ins. (For
  an image-tool demo, generate the hero from the *actual* models the app ships —
  reaching for a default like Flux when the app uses its own models got flagged hard.)
- **Declutter every state.** Cut suggestion chips, "Generating…" loaders, and literal
  intermediate steps that add nothing — they read as clutter and slow the piece.
- **Compose each UI state as ONE balanced, centred group.** A composer floating
  mid-screen with dead space below "looked gross"; title + input + subline as a single
  vertically-centred stack reads clean.
- **Put the result where the real app puts it.** A generated image should arrive in the
  app's real result view (in-canvas, with its real chrome), not as a card floating over
  the background — make it "arrive at the right place."

## Cursor discipline (the single most-flagged thing across builds)
- **Measure targets at runtime; never hardcode pixel coords.** When you restructure a
  panel, hardcoded clicks silently land on empty space. Use an offset-chain helper that
  returns an element's centre in `#app`-space (camera-independent):
  ```js
  function pt(sel,fx,fy){var el=document.querySelector(sel),app=document.getElementById("app"),x=0,y=0,e=el;
    while(e&&e!==app&&e!==document.body){x+=e.offsetLeft;y+=e.offsetTop;e=e.offsetParent;}
    return {x:Math.round(x+el.offsetWidth*(fx==null?0.5:fx)),y:Math.round(y+el.offsetHeight*(fy==null?0.5:fy))};}
  var P_BTN = pt("#generate-btn");   // exact, survives layout changes
  ```
- **Every cursor move must have a purpose.** No wandering, no drifting diagonally across
  empty canvas, no parking on element A while the camera looks at B. If the cursor has
  no job (e.g. *during typing*), HIDE it and reappear it on the next target — don't have
  it hover over the text or pre-emptively sit on the next button.
- `moveTo(x,y)` must subtract the SVG arrow's tip offset so the *tip* lands on the
  target, not the icon's bounding-box corner.

## Transitions & composition (where the glitches hide)
- **One full-frame element fully clears before another appears over the same area** — or
  you get ghosting/double-exposure (text bleeding through a fading-in image was the
  literal "wtf is going on here" frame a reviewer caught). Sequence: fade A out (snappy)
  → `display:none` A → then fade B in. Leave one clean intermediate frame.
- **Diving into an image and bringing it alive:** fade ALL surrounding UI chrome
  (sidebar, topbar, buttons, captions) BEFORE the zoom so only the clean image fills the
  frame; then crossfade to an i2v clip whose **first frame equals that still** → a
  seamless still→motion handoff with no pop.
- **Embed an AI i2v clip in the timeline:** `<video class="clip" data-start=T
  data-duration=D data-track-index=N muted playsinline>` inside a **non-timed wrapper
  div**; crossfade by animating the WRAPPER's opacity. The framework owns video
  playback/seeking — don't animate the `<video>` element directly. (i2v is usually
  720p; upscaled full-frame to 4K it's a touch soft — fine for a brief "comes alive"
  beat, regen higher if it's the hero.)
- **Bridge a hard scene/color cut with a bloom**, not a raw crossfade. Warm gallery
  video → cool cyan brand wall was jarring; a bright full-frame `#xflash` bloom ("she
  walks into the light") covers the seam and motivates it. Confirm it fires with a
  brightness probe (`ImageStat.Stat(frame).mean`) if you can't watch it.
- **Concept coherence beats spectacle.** Pick the still so motion + payoff connect — a
  *gallery* still → "walk into a wall of images" reads; a cyberpunk street → "walk into
  a cyber wall" was a stretch and got cut. A rotating "spiral world / cursor-as-spaceship"
  concept was rejected as "too weird"; "the UI blurs out and a 2D wall of images with a
  3D feel comes in" landed. When unsure, less literal-spectacle, more clean.

## Always watch it frame by frame (and how to when you can't)
- A render is **not done** until you've watched it densely. Build tile grids:
  `ffmpeg -i FINAL.mp4 -vf "fps=4,scale=300:169,tile=5x4:padding=2:color=0x222222" -frames:v 1 g.jpg`
  and read them. Coarse 0.5s samples miss transition jank — drop to 0.2s around suspect
  cuts (`-ss A -to B`). Run `hyperframes inspect` for overflow, don't just eyeball.
- **Keep every frame grid < 2000px in BOTH dimensions** or the image viewer rejects it
  (`scale=300:169, tile 5x4` = 1512×696, safe).
- **If your own context can no longer load images** (a long session hits a cumulative
  image cap — even tiny frames start getting rejected), launch a **fresh-context
  subagent** as the frame-by-frame reviewer; it has its own image budget. Give it: the
  intended per-beat flow *with timestamps*, a source-map (which element/tween owns each
  moment), the render + mux commands, and the loop "review → fix index.html → re-render
  → re-review → report a changelog." It catches and fixes what you can't see (it found a
  double-exposure ghost frame, an aimless cursor swoop, and a muddy background in one
  pass). Watch for a transient server rate-limit killing a freshly-spawned subagent —
  just relaunch.
- **Pacing: when in doubt, tighten.** "Parts too slow" and "the hero clip plays too
  long" were recurring notes — hold beats ~1–1.5s, keep an i2v "come alive" moment
  ~3–4s (not 6+), shorten dropdown/menu reveals to ~1.2s.
