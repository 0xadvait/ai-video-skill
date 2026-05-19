#!/usr/bin/env python3
"""Run an AI-video generation job across six models from one schema.

Jobs are authored against the canonical Seedance 2.0 schema (see
reference/schema.md). This runner validates the job, auto-routes it to the
best model (or honours an explicit one), translates the body to that model's
API, uploads any local reference files, downloads the clip, and writes a
manifest. The next step in the skill is review.py — watch the clip, then
record a prompting lesson.

Usage:
    python generate.py JOB.json [--out DIR] [--model M] [--fallback]

JOB.json is {"id": "...", "model": "auto", "input": {...schema...}}
or a JSON array of such jobs (run sequentially).

Models:
    seedance-2.0    Replicate bytedance/seedance-2.0   (quad-modal, native audio)
    kling-3.0-omni  fal kling-video/o3                 (t2v + i2v, alt moderation)
    wan-2.7-i2v     Replicate wan-video/wan-2.7-i2v    (open-weights image-to-video)
    veo-3.1         Google Gemini veo-3.1              (native audio, top realism)
    veed-fabric-1.0 fal veed/fabric-1.0                (image+audio talking video)
    omnihuman-1.5   fal bytedance/omnihuman            (image+audio realistic avatar)
    auto            route by intent (default)

--model M    force every job to model M
--fallback   if a job is classifier-flagged, retry on kling-3.0-omni
--out DIR    output directory (default ./seedance_out)

Env: REPLICATE_API_TOKEN (seedance/wan), FAL_KEY (kling),
     GEMINI_API_KEY (veo). Only the models you actually use need a key.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import validate  # noqa: E402

MODELS = {"seedance-2.0", "kling-3.0-omni", "wan-2.7-i2v", "veo-3.1",
          "veed-fabric-1.0", "omnihuman-1.5"}
CLASSIFIER_HINTS = ("sensitive content", "e005", "real person", "content moderation")

REPLICATE_SEEDANCE = "bytedance/seedance-2.0"
REPLICATE_WAN = "wan-video/wan-2.7-i2v"
KLING_T2V = "fal-ai/kling-video/o3/standard/text-to-video"
KLING_I2V = "fal-ai/kling-video/o3/standard/image-to-video"
VEO_MODEL = "veo-3.1-generate-preview"
# fal slugs — if fal renames an endpoint, fix it here (single source of truth).
VEED_FABRIC = "fal-ai/veed/fabric-1.0"
OMNIHUMAN = "fal-ai/bytedance/omnihuman/v1.5"

REF_FIELDS = ("image", "last_frame_image", "reference_images",
              "reference_videos", "reference_audios")


def log(out_dir: Path, msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with (out_dir / "generate.log").open("a") as f:
        f.write(line + "\n")


def is_local_file(value: str) -> bool:
    return (isinstance(value, str)
            and not value.startswith(("http://", "https://", "data:"))
            and Path(value).is_file())


# --------------------------------------------------------------------------
# routing
# --------------------------------------------------------------------------
def route(body: dict) -> str:
    """Pick a model from the job's intent. See SKILL.md for the rationale."""
    if body.get("reference_audios"):
        return "seedance-2.0"                       # lip-sync — Seedance only
    if body.get("reference_videos"):
        return "seedance-2.0"                       # motion transfer
    if len(body.get("reference_images") or []) >= 2:
        return "seedance-2.0"                       # multi-ref consistency
    if body.get("image") and not body.get("reference_images"):
        return "wan-2.7-i2v"                        # pure image-to-video
    return "seedance-2.0"                           # text-to-video default


# --------------------------------------------------------------------------
# reference upload
# --------------------------------------------------------------------------
def upload_for_replicate(body: dict, out_dir: Path) -> dict:
    import replicate
    resolved = dict(body)
    for field in REF_FIELDS:
        val = resolved.get(field)
        if isinstance(val, list):
            new = []
            for v in val:
                if is_local_file(v):
                    with open(v, "rb") as f:
                        url = replicate.files.create(file=f).urls["get"]
                    log(out_dir, f"  uploaded {Path(v).name} -> replicate")
                    new.append(url)
                else:
                    new.append(v)
            resolved[field] = new
        elif is_local_file(val):
            with open(val, "rb") as f:
                resolved[field] = replicate.files.create(file=f).urls["get"]
            log(out_dir, f"  uploaded {Path(val).name} -> replicate")
    return resolved


def first_image(body: dict) -> str | None:
    if body.get("image"):
        return body["image"]
    refs = body.get("reference_images") or []
    return refs[0] if refs else None


# --------------------------------------------------------------------------
# adapters — each returns mp4 bytes
# --------------------------------------------------------------------------
def run_seedance(body: dict, out_dir: Path) -> bytes:
    import replicate
    resolved = upload_for_replicate(body, out_dir)
    output = replicate.run(REPLICATE_SEEDANCE, input=resolved)
    return output.read()


def run_wan(body: dict, out_dir: Path) -> bytes:
    import replicate
    img = first_image(body)
    if not img:
        raise ValueError("wan-2.7-i2v needs an 'image' (first frame)")
    resolved = upload_for_replicate({"image": img}, out_dir)
    duration = body.get("duration", 5)
    wan_input = {
        "prompt": body["prompt"],
        "first_frame": resolved["image"],
        "duration": 5 if duration in (-1, None) else max(4, min(15, duration)),
        "resolution": body.get("resolution", "720p"),
        "enable_prompt_expansion": True,
    }
    if isinstance(body.get("seed"), int):
        wan_input["seed"] = body["seed"]
    output = replicate.run(REPLICATE_WAN, input=wan_input)
    return output.read()


def run_kling(body: dict, out_dir: Path) -> bytes:
    import fal_client
    img = first_image(body)
    duration = body.get("duration", 5)
    kling_dur = "10" if isinstance(duration, int) and duration >= 8 else "5"
    aspect = body.get("aspect_ratio", "16:9")
    if aspect not in ("16:9", "9:16", "1:1"):
        aspect = "16:9"
    args = {"prompt": body["prompt"], "duration": kling_dur, "aspect_ratio": aspect}
    if img:
        if is_local_file(img):
            img = fal_client.upload_file(img)
            log(out_dir, "  uploaded reference image -> fal")
        args["image_url"] = img
        endpoint = KLING_I2V
    else:
        endpoint = KLING_T2V
    result = fal_client.subscribe(endpoint, arguments=args, with_logs=False)
    vurl = (result.get("video") or {}).get("url") or result.get("video_url")
    if not vurl:
        raise RuntimeError(f"kling returned no video: {json.dumps(result)[:200]}")
    req = urllib.request.Request(vurl, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def run_veo(body: dict, out_dir: Path) -> bytes:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is required for veo-3.1")
    base = "https://generativelanguage.googleapis.com/v1beta"
    instance: dict = {"prompt": body["prompt"]}
    img = first_image(body)
    if img and is_local_file(img):
        data = base64.b64encode(Path(img).read_bytes()).decode()
        mime = "image/png" if str(img).lower().endswith(".png") else "image/jpeg"
        instance["image"] = {"bytesBase64Encoded": data, "mimeType": mime}
    params = {"aspectRatio": body.get("aspect_ratio", "16:9")}
    payload = json.dumps({"instances": [instance], "parameters": params}).encode()
    req = urllib.request.Request(
        f"{base}/models/{VEO_MODEL}:predictLongRunning?key={key}",
        data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        op_name = json.loads(r.read())["name"]
    log(out_dir, f"  veo operation {op_name} — polling")
    deadline = time.time() + 600
    final = None
    while time.time() < deadline:
        time.sleep(10)
        with urllib.request.urlopen(f"{base}/{op_name}?key={key}", timeout=30) as r:
            data = json.loads(r.read())
        if data.get("done"):
            final = data
            break
    if not final:
        raise RuntimeError("veo generation timed out")
    if "error" in final:
        raise RuntimeError(f"veo error: {json.dumps(final['error'])[:300]}")
    resp = final.get("response", {})
    videos = (resp.get("generateVideoResponse", {}).get("generatedSamples")
              or resp.get("generatedSamples") or resp.get("videos") or [])
    if not videos:
        raise RuntimeError(f"veo returned no video: {json.dumps(resp)[:300]}")
    vid = videos[0]
    uri = (vid.get("video", {}).get("uri") or vid.get("uri")
           or vid.get("videoUri"))
    if uri:
        dl = uri if "key=" in uri else f"{uri}{'&' if '?' in uri else '?'}key={key}"
        req2 = urllib.request.Request(dl, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req2, timeout=300) as r:
            return r.read()
    b64 = vid.get("video", {}).get("data") or vid.get("bytesBase64Encoded")
    if b64:
        return base64.b64decode(b64)
    raise RuntimeError("veo response had no downloadable video")


def _fal_url(value: str, out_dir: Path, label: str):
    """Return a fal-hosted URL, uploading the file first if it is local."""
    import fal_client
    if is_local_file(value):
        url = fal_client.upload_file(value)
        log(out_dir, f"  uploaded {label} -> fal")
        return url
    return value


def _fal_video_bytes(result: dict) -> bytes:
    vurl = (result.get("video") or {}).get("url") or result.get("video_url")
    if not vurl:
        raise RuntimeError(f"fal returned no video: {json.dumps(result)[:200]}")
    req = urllib.request.Request(vurl, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def _talking_avatar(body: dict, out_dir: Path, endpoint: str,
                    with_prompt: bool) -> bytes:
    """Shared path for VEED Fabric / OmniHuman — image + audio -> talking clip."""
    import fal_client
    img = first_image(body)
    audios = body.get("reference_audios") or []
    if not img or not audios:
        raise ValueError(
            f"{endpoint} needs a face image (image / reference_images) "
            f"and a speech clip (reference_audios)")
    args = {
        "image_url": _fal_url(img, out_dir, "face image"),
        "audio_url": _fal_url(audios[0], out_dir, "speech audio"),
    }
    if with_prompt and body.get("prompt"):
        args["prompt"] = body["prompt"]
    result = fal_client.subscribe(endpoint, arguments=args, with_logs=False)
    return _fal_video_bytes(result)


def run_veed_fabric(body: dict, out_dir: Path) -> bytes:
    return _talking_avatar(body, out_dir, VEED_FABRIC, with_prompt=False)


def run_omnihuman(body: dict, out_dir: Path) -> bytes:
    return _talking_avatar(body, out_dir, OMNIHUMAN, with_prompt=True)


ADAPTERS = {
    "seedance-2.0": run_seedance,
    "kling-3.0-omni": run_kling,
    "wan-2.7-i2v": run_wan,
    "veo-3.1": run_veo,
    "veed-fabric-1.0": run_veed_fabric,
    "omnihuman-1.5": run_omnihuman,
}


# --------------------------------------------------------------------------
# job runner
# --------------------------------------------------------------------------
def run_one(job: dict, out_dir: Path, force_model: str | None,
            fallback: bool) -> dict:
    job_id = job.get("id", "clip")
    body = job.get("input", job)
    out = out_dir / f"{job_id}.mp4"

    if out.exists() and out.stat().st_size > 100_000:
        log(out_dir, f"SKIP {job_id} (exists)")
        return {"id": job_id, "status": "skipped", "path": str(out)}

    errors, warnings = validate(body)
    for w in warnings:
        log(out_dir, f"  warning [{job_id}] {w}")
    if errors:
        for e in errors:
            log(out_dir, f"  ERROR [{job_id}] {e}")
        return {"id": job_id, "status": "error",
                "error": "validation failed: " + "; ".join(errors)}

    model = force_model or job.get("model") or "auto"
    if model == "auto":
        model = route(body)
    if model not in MODELS:
        return {"id": job_id, "status": "error",
                "error": f"unknown model {model!r}"}

    log(out_dir, f"START {job_id} model={model} "
                 f"duration={body.get('duration', 5)}s "
                 f"{body.get('aspect_ratio', '16:9')}")
    t0 = time.time()
    try:
        data = ADAPTERS[model](body, out_dir)
        out.write_bytes(data)
        elapsed = round(time.time() - t0, 1)
        size_mb = round(out.stat().st_size / 1_000_000, 1)
        log(out_dir, f"DONE  {job_id} {elapsed}s {size_mb}MB via {model}")
        return {"id": job_id, "status": "ok", "model_used": model,
                "path": str(out), "wall_seconds": elapsed, "size_mb": size_mb,
                "warnings": warnings}
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        elapsed = round(time.time() - t0, 1)
        flagged = any(h in msg.lower() for h in CLASSIFIER_HINTS)
        log(out_dir, f"FAIL  {job_id} {elapsed}s err={msg[:200]}")
        if flagged and fallback and model != "kling-3.0-omni":
            log(out_dir, f"  classifier-flagged — retrying {job_id} on kling-3.0-omni")
            try:
                data = run_kling(body, out_dir)
                out.write_bytes(data)
                elapsed = round(time.time() - t0, 1)
                log(out_dir, f"DONE  {job_id} {elapsed}s via kling-3.0-omni (fallback)")
                return {"id": job_id, "status": "ok",
                        "model_used": "kling-3.0-omni", "fallback": True,
                        "path": str(out), "wall_seconds": elapsed}
            except Exception as exc2:  # noqa: BLE001
                return {"id": job_id, "status": "error", "model_used": model,
                        "error": f"primary+fallback failed: {str(exc2)[:200]}"}
        return {"id": job_id, "status": "error", "model_used": model,
                "classifier_flagged": flagged, "error": msg[:300]}


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    job_path = None
    out_dir = Path("./seedance_out")
    force_model = None
    fallback = False
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--out":
            out_dir = Path(args[i + 1]); i += 2
        elif a == "--model":
            force_model = args[i + 1]; i += 2
        elif a == "--fallback":
            fallback = True; i += 1
        elif not a.startswith("--"):
            job_path = a; i += 1
        else:
            print(f"unknown flag {a}"); return 1

    if not job_path:
        print("ERROR: no job file given"); return 1
    if force_model and force_model not in MODELS and force_model != "auto":
        print(f"ERROR: --model must be one of {sorted(MODELS)} or auto"); return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    obj = json.loads(Path(job_path).read_text())
    jobs = obj if isinstance(obj, list) else [obj]

    log(out_dir, f"Running {len(jobs)} job(s); out={out_dir}")
    results = []
    for j in jobs:
        results.append(run_one(j, out_dir, force_model, fallback))
        time.sleep(3)

    (out_dir / "manifest.json").write_text(json.dumps(results, indent=2))
    print("\n=== summary ===")
    for r in results:
        print(f"  {r['id']:<28} {r['status']:<8} "
              f"{r.get('model_used', '-'):<16} {r.get('error', '')[:70]}")
    ok = sum(1 for r in results if r["status"] in ("ok", "skipped"))
    print(f"\n{ok}/{len(results)} ready. Manifest: {out_dir / 'manifest.json'}")
    print("Next: run review.py on each clip to QC it and record a lesson.")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
