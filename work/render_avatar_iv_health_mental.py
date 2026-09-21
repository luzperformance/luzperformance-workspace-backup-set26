import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://openrouter.ai/api/v1"
MODEL = "heygen/avatar-iv"
IMAGE_URL = "https://portland-movie-passive-likelihood.trycloudflare.com/avatar-reference.jpg"
VOICE_ID = None  # Set only after catalog validation and authorization.
VIDEO_PATH = pathlib.Path(
    "/data/content/drafts/heygen/renders/2026-09-18-saude-mental-esporte-elite-avatar-iv.mp4"
)
RECORD_PATH = pathlib.Path(
    "/data/content/drafts/heygen/renders/2026-09-18-saude-mental-esporte-elite-avatar-iv-job.json"
)

SCRIPT = """Treinar pesado não impede ninguém de piorar mentalmente.

A conta aparece assim: rendimento cai, irritabilidade sobe e todo mundo chama de cansaço.

O novo consenso do COI é claro: não é oito ou oitenta.

Carga de treino, pressão por resultado, lesão, ambiente da equipe e momento de carreira pesam nisso.

Não olha só para sono, fadiga e planilha. Olha humor, estresse e ansiedade também.

O atleta pode estar entregando muito e já estar desandando por dentro.

Queda de rendimento com mudança de humor não pede palpite. Pede investigação.

Redução de danos é não esperar o atleta quebrar para começar a cuidar.

Performance que custa saúde não é performance. Se isso está acontecendo, procure avaliação séria. Link da consultoria na bio."""

MOTION_PROMPT = (
    "Vertical 9:16 talking-head. Chest-up framing, camera locked, natural subtle head "
    "and facial movements, neutral focused expression. Preserve the supplied person's "
    "identity, olive jacket and terracotta background. No text, graphics, pointing, cuts, "
    "B-roll or camera movement."
)


def configured_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    for candidate in (pathlib.Path("/data/.env"), pathlib.Path("/data/.hermes/.env")):
        if not candidate.is_file():
            continue
        text = candidate.read_text(errors="ignore")
        match = re.search(
            r'^\s*OPENROUTER_API_KEY\s*=\s*["\']?([^\s"\']+)',
            text,
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
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def write_record(record):
    RECORD_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECORD_PATH.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")


def fail(kind, message, exit_code=1):
    record = {"status": "failed", "kind": kind, "message": message[:1000]}
    write_record(record)
    print(json.dumps(record, ensure_ascii=False))
    raise SystemExit(exit_code)


payload = {
    "model": MODEL,
    "prompt": SCRIPT,
    "duration": 53,
    "resolution": "1080p",
    "aspect_ratio": "9:16",
    "generate_audio": True,
    "input_references": [
        {"type": "image_url", "image_url": {"url": IMAGE_URL}},
    ],
    "provider": {
        "options": {
            "heygen": {
                "voice_id": VOICE_ID,
                "motion_prompt": MOTION_PROMPT,
            }
        }
    },
}

if "--dry-run" in sys.argv:
    heygen_options = payload["provider"]["options"]["heygen"]
    print(
        json.dumps(
            {
                "provider_shape": "provider.options.heygen",
                "has_voice_id": bool(heygen_options.get("voice_id")),
                "has_motion_prompt": bool(heygen_options.get("motion_prompt")),
                "duration": payload["duration"],
                "resolution": payload["resolution"],
                "aspect_ratio": payload["aspect_ratio"],
            }
        )
    )
    raise SystemExit(0)

if "--submit" not in sys.argv:
    print(
        json.dumps(
            {
                "status": "not_submitted",
                "reason": "explicit_submit_required",
            }
        )
    )
    raise SystemExit(0)

if not VOICE_ID:
    print(
        json.dumps(
            {
                "status": "blocked",
                "reason": "voice_id_not_validated",
                "next_step": "provide_authorized_audio_or_validate_a_live_voice_id",
            }
        )
    )
    raise SystemExit(2)

key = configured_key()

status_code = 0
job: dict = {}
try:
    status_code, job = request_json(f"{BASE}/videos", key, method="POST", body=payload)
except urllib.error.HTTPError as error:
    body = error.read().decode("utf-8", errors="replace")
    fail(f"http_{error.code}", body)
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
    "requested_duration_seconds": 53,
    "render_path": str(VIDEO_PATH),
}
write_record(record)

for attempt in range(31):
    time.sleep(30)
    try:
        _, current = request_json(polling_url, key)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        fail(f"poll_http_{error.code}", body)
    except Exception as error:
        fail("poll_exception", str(error))

    current_status = current.get("status")
    record.update({"status": current_status})
    if current.get("usage"):
        record["usage"] = current["usage"]
    write_record(record)

    if current_status == "completed":
        urls = current.get("unsigned_urls") or []
        download_url = urls[0] if urls else f"{BASE}/videos/{job_id}/content?index=0"
        headers = {}
        if download_url.startswith(BASE):
            headers["Authorization"] = f"Bearer {key}"
        download_request = urllib.request.Request(download_url, headers=headers)
        try:
            with urllib.request.urlopen(download_request, timeout=180) as response:
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
            )
        )
        raise SystemExit(0)

    if current_status in {"failed", "cancelled", "expired"}:
        fail("provider_terminal_status", json.dumps(current, ensure_ascii=False))

fail("poll_timeout", "Timed out after 15 minutes")
