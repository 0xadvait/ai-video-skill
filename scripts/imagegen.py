#!/usr/bin/env python3
"""Generate still images — first frames, reference plates, storyboard panels.

The front of the pipeline: a still feeds image-to-video (Seedance/Wan/Kling
i2v) or acts as a character reference. Defaults to Flux Schnell on Replicate;
Imagen 4 on Gemini is available for higher fidelity.

Usage:
    python imagegen.py "a prompt" [--out frame.png] [--model M]
                        [--aspect 16:9] [--n 1]

Models:
    flux-schnell  Replicate black-forest-labs/flux-schnell   (fast, default)
    flux-pro      Replicate black-forest-labs/flux-1.1-pro   (higher quality)
    imagen        Google Gemini imagen-4.0-generate-001      (top fidelity)

Env: REPLICATE_API_TOKEN (flux*), GEMINI_API_KEY (imagen).
"""
from __future__ import annotations

import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

FLUX_SCHNELL = "black-forest-labs/flux-schnell"
FLUX_PRO = "black-forest-labs/flux-1.1-pro"
IMAGEN = "imagen-4.0-generate-001"
ASPECTS = {"1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21"}


def run_flux(slug: str, prompt: str, aspect: str, n: int,
             out: Path) -> list[Path]:
    import replicate
    outputs = replicate.run(slug, input={
        "prompt": prompt,
        "aspect_ratio": aspect,
        "num_outputs": n,
        "output_format": "png",
    })
    if not isinstance(outputs, list):
        outputs = [outputs]
    paths = []
    for i, item in enumerate(outputs):
        p = out if n == 1 else out.with_name(f"{out.stem}_{i}{out.suffix}")
        p.write_bytes(item.read())
        paths.append(p)
    return paths


def run_imagen(prompt: str, aspect: str, n: int, out: Path) -> list[Path]:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.exit("ERROR: GEMINI_API_KEY is required for imagen")
    url = (f"https://generativelanguage.googleapis.com/v1beta/"
           f"models/{IMAGEN}:predict?key={key}")
    payload = json.dumps({
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": n, "aspectRatio": aspect},
    }).encode()
    req = urllib.request.Request(
        url, data=payload, method="POST",
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read())
    preds = data.get("predictions", [])
    if not preds:
        sys.exit(f"ERROR: imagen returned no images: {json.dumps(data)[:300]}")
    paths = []
    for i, pred in enumerate(preds):
        b64 = pred.get("bytesBase64Encoded") or pred.get("image", {}).get("bytesBase64Encoded")
        if not b64:
            continue
        p = out if n == 1 else out.with_name(f"{out.stem}_{i}{out.suffix}")
        p.write_bytes(base64.b64decode(b64))
        paths.append(p)
    return paths


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    prompt = None
    out = Path("frame.png")
    model = "flux-schnell"
    aspect = "16:9"
    n = 1
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--out":
            out = Path(args[i + 1]); i += 2
        elif a == "--model":
            model = args[i + 1]; i += 2
        elif a == "--aspect":
            aspect = args[i + 1]; i += 2
        elif a == "--n":
            n = int(args[i + 1]); i += 2
        elif not a.startswith("--"):
            prompt = a; i += 1
        else:
            print(f"unknown flag {a}"); return 1

    if not prompt or not prompt.strip():
        print("ERROR: no prompt given"); return 1
    if aspect not in ASPECTS:
        print(f"ERROR: --aspect must be one of {sorted(ASPECTS)}"); return 1
    out.parent.mkdir(parents=True, exist_ok=True)

    if model == "flux-schnell":
        paths = run_flux(FLUX_SCHNELL, prompt, aspect, n, out)
    elif model == "flux-pro":
        paths = run_flux(FLUX_PRO, prompt, aspect, n, out)
    elif model == "imagen":
        paths = run_imagen(prompt, aspect, n, out)
    else:
        print(f"ERROR: --model must be flux-schnell, flux-pro or imagen")
        return 1

    for p in paths:
        print(f"wrote {p} ({p.stat().st_size // 1024} KB)")
    print(f"\n{len(paths)} image(s) via {model}. "
          f"Feed one as the 'image' / 'reference_images' input to generate.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
