import json
import os
import pathlib
import re
import time
import urllib.error
import urllib.request


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


def get_json(url, key):
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def api_error(error):
    body = error.read().decode("utf-8", errors="replace")[:500]
    return {"status": error.code, "body": body}


key = configured_key()
result: dict[str, object] = {"credential": "configured"}

try:
    credit_status, credits = get_json("https://openrouter.ai/api/v1/credits", key)
    raw_credit_data = credits.get("data", credits) if isinstance(credits, dict) else {}
    credit_fields = {}
    if isinstance(raw_credit_data, dict):
        for field in (
            "total_credits",
            "total_usage",
            "remaining",
            "available_credits",
            "credits",
            "limit",
        ):
            value = raw_credit_data.get(field)
            if isinstance(value, (int, float, str)):
                credit_fields[field] = value
    result["credits"] = {"status": credit_status, "values": credit_fields}
except urllib.error.HTTPError as error:
    result["credits"] = api_error(error)

# Respect the user's minimum five-second API interval.
time.sleep(5.2)

try:
    model_status, payload = get_json("https://openrouter.ai/api/v1/videos/models", key)
    models = payload.get("data", payload) if isinstance(payload, dict) else payload
    if isinstance(models, dict):
        models = models.get("data", models.get("models", []))
    model = next(
        (
            item
            for item in models
            if isinstance(item, dict) and item.get("id") == "heygen/avatar-iv"
        ),
        None,
    )
    if model is None:
        result["model"] = {"status": model_status, "found": False}
    else:
        result["model"] = {
            "status": model_status,
            "found": True,
            "id": model.get("id"),
            "supported_resolutions": model.get("supported_resolutions"),
            "supported_aspect_ratios": model.get("supported_aspect_ratios"),
            "supported_durations": model.get("supported_durations"),
            "pricing": model.get("pricing"),
            "supported_parameters": model.get("supported_parameters"),
        }
except urllib.error.HTTPError as error:
    result["model"] = api_error(error)

print(json.dumps(result, ensure_ascii=False, indent=2))
