"""Avatar IV — Saúde Mental no Esporte de Elite: foto + áudio autorizado (lip-sync)."""
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

BASE = "https://openrouter.ai/api/v1"
MODEL = "heygen/avatar-iv"
IMAGE_URL = "https://herald-examining-thee-palm.trycloudflare.com/foto-saude-mental.png"
AUDIO_URL = "https://herald-examining-thee-palm.trycloudflare.com/audio-saude-mental.m4a"
DURATION = 65

RENDER_DIR = pathlib.Path("/data/content/drafts/heygen/renders")
VIDEO_PATH = RENDER_DIR / "2026-09-19-saude-mental-esporte-elite-avatar-iv.mp4"
RECORD_PATH = RENDER_DIR / "2026-09-19-saude-mental-esporte-elite-avatar-iv-job.json"

PROMPT = (
    "Vertical 9:16 talking-head. Chest-up framing, camera locked, natural subtle head and "
    "facial movements, neutral focused expression. Preserve the supplied person's identity, "
    "olive stand-collar jacket over black t-shirt and terracotta background. Mouth movement "
    "must follow the supplied audio track exactly. No text, graphics, overlay, pointing, "
    "cuts, B-roll or camera movement."
)

MOTION_PROMPT = (
    "Busto fixo, câmera travada, movimentos naturais e contidos de cabeça e expressão; "
    "sem texto, sem gesto de apontar, sem corte."
)


def configured_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    for candidate in (pathlib.Path("/data/.env"), pathlib.Path("/data/.hermes/.env")):
        if not candidate.is_file():
            continue
        match = re.search(
            r'^\s*OPENROUTER_API_KEY\s*=\s*["\']?([^\s"\']+)',
            candidate.read_text(errors="ignore"),
            re.MULTILINE,
        )
        if match:
            return match.group(1)
    raise RuntimeError("OPENROUTER_API_KEY_NOT_CONFIGURED")


def request_json(url, key, method="GET", body=None):
    headers = {"Authorization": f"Bearer {key}", "Accept": "application/json"}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, headers=headers, data=data, method=method)
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def write_record(record):
    RECORD_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECORD_PATH.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")


def fail(kind, message, exit_code=1):
    record = {"status": "failed", "kind": kind, "message": message[:1500]}
    write_record(record)
    print(json.dumps(record, ensure_ascii=False), flush=True)
    raise SystemExit(exit_code)


payload = {
    "model": MODEL,
    "prompt": PROMPT,
    "duration": DURATION,
    "resolution": "1080p",
    "aspect_ratio": "9:16",
    "generate_audio": True,
    "input_references": [
        {"type": "image_url", "image_url": {"url": IMAGE_URL}},
        {"type": "audio_url", "audio_url": {"url": AUDIO_URL}},
    ],
    "provider": {"heygen": {"motion_prompt": MOTION_PROMPT}},
}

if "--dry-run" in sys.argv:
    print(json.dumps(payload, ensure_ascii=False, indent=2), flush=True)
    raise SystemExit(0)

if "--submit" not in sys.argv:
    print(json.dumps({"status": "not_submitted", "reason": "explicit_submit_required"}), flush=True)
    raise SystemExit(0)

key = configured_key()

try:
    status_code, job = request_json(f"{BASE}/videos", key, method="POST", body=payload)
except urllib.error.HTTPError as error:
    fail(f"http_{error.code}", error.read().decode("utf-8", errors="replace"))
except Exception as error:
    fail("submit_exception", str(error))

job_id = job.get("id")
polling_url = job.get("polling_url")
if status_code != 202 or not job_id or not polling_url:
    fail("unexpected_submit_response", json.dumps(job, ensure_ascii=False))

job_id = str(job_id)
polling_url = str(polling_url)
if polling_url.startswith("/"):
    polling_url = "https://openrouter.ai" + polling_url

record = {
    "status": job.get("status", "pending"),
    "job_id": job_id,
    "model": MODEL,
    "resolution": "1080p",
    "aspect_ratio": "9:16",
    "requested_duration_seconds": DURATION,
    "audio_seconds": 64.56,
    "render_path": str(VIDEO_PATH),
}
write_record(record)
print(json.dumps({"submitted": True, "job_id": job_id, "status": record["status"]}), flush=True)

for attempt in range(60):
    time.sleep(20)
    try:
        _, current = request_json(polling_url, key)
    except urllib.error.HTTPError as error:
        fail(f"poll_http_{error.code}", error.read().decode("utf-8", errors="replace"))
    except Exception as error:
        fail("poll_exception", str(error))

    current_status = current.get("status")
    record["status"] = current_status
    if current.get("usage"):
        record["usage"] = current["usage"]
    write_record(record)
    print(json.dumps({"attempt": attempt, "status": current_status}), flush=True)

    if current_status == "completed":
        urls = current.get("unsigned_urls") or []
        download_url = urls[0] if urls else f"{BASE}/videos/{job_id}/content?index=0"
        headers = {}
        if download_url.startswith(BASE):
            headers["Authorization"] = f"Bearer {key}"
        download_request = urllib.request.Request(download_url, headers=headers)
        try:
            with urllib.request.urlopen(download_request, timeout=300) as response:
                VIDEO_PATH.parent.mkdir(parents=True, exist_ok=True)
                VIDEO_PATH.write_bytes(response.read())
        except Exception as error:
            fail("download_exception", str(error))

        record.update(
            {
                "status": "completed",
                "video_bytes": VIDEO_PATH.stat().st_size,
                "usage": current.get("usage", {}),
            }
        )
        write_record(record)
        print(
            json.dumps(
                {
                    "status": "completed",
                    "job_id": job_id,
                    "video_path": str(VIDEO_PATH),
                    "video_bytes": VIDEO_PATH.stat().st_size,
                    "usage": current.get("usage", {}),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        raise SystemExit(0)

    if current_status in {"failed", "cancelled", "expired"}:
        fail("provider_terminal_status", json.dumps(current, ensure_ascii=False))

fail("poll_timeout", "Timed out after 20 minutes")
