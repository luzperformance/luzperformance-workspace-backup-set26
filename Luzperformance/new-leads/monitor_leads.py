#!/usr/bin/env python3
"""Monitor de novos leads em uma planilha Google Sheets.

Uso:
  python monitor_leads.py authorize
  python monitor_leads.py exchange 'URL_REDIRECIONADA_COMPLETA'
  python monitor_leads.py check

O comando check só escreve no stdout quando a última linha for diferente da
penúltima. Isso permite que o agendador envie apenas leads novos.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path(__file__).resolve().parent
SPREADSHEET_ID = "19SrwzlrcTT9ttRo_C_oVSmPqFzrWZ8wupYyZ7Ew9A1U"
CLIENT_SECRET_PATH = Path("/data/google_client_secret.json")
TOKEN_PATH = BASE_DIR / "google_token.json"
PENDING_PATH = BASE_DIR / "oauth_pending.json"
STATE_PATH = BASE_DIR / "last_notified_row.json"
REDIRECT_URI = "http://localhost:1"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
PHONE_HEADERS = ("telefone", "phone", "celular", "whatsapp", "fone")


def format_phone(value):
    digits = re.sub(r"\D", "", str(value or ""))
    if digits.startswith("55") and len(digits) in (12, 13):
        digits = digits[2:]
    if len(digits) not in (10, 11):
        return str(value or "").strip()
    ddd, number = digits[:2], digits[2:]
    if len(number) == 9:
        number = f"{number[:5]}-{number[5:]}"
    else:
        number = f"{number[:4]}-{number[4:]}"
    return f"({ddd}) {number}"


def is_phone_header(header):
    normalized = re.sub(r"[^a-z]", "", str(header).lower())
    return any(key in normalized for key in PHONE_HEADERS)


def row_as_fields(headers, row):
    fields = []
    for index, value in enumerate(row):
        label = str(headers[index]).strip() if index < len(headers) else f"Campo {index + 1}"
        value = str(value).strip()
        if not label or not value:
            continue
        if is_phone_header(label):
            value = format_phone(value)
        fields.append((label, value))
    return fields


def new_lead_message(headers, previous_row, current_row):
    if list(previous_row) == list(current_row):
        return None
    fields = row_as_fields(headers, current_row)
    if not fields:
        return None
    return "NOVO LEAD\n" + "\n".join(f"{label}: {value}" for label, value in fields)


def should_notify(current_row, last_notified_row):
    return list(current_row) != list(last_notified_row or [])


def load_last_notified_row():
    if not STATE_PATH.exists():
        return []
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_last_notified_row(row):
    STATE_PATH.write_text(json.dumps(list(row), ensure_ascii=False), encoding="utf-8")
    os.chmod(STATE_PATH, 0o600)


def _google_modules():
    try:
        from google_auth_oauthlib.flow import Flow
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise RuntimeError("Dependências Google ausentes. Rode a autorização novamente.") from exc
    return Flow, Credentials, build


def authorize():
    if not CLIENT_SECRET_PATH.exists():
        raise RuntimeError("Credencial OAuth não encontrada em /data/google_client_secret.json")
    Flow, _, _ = _google_modules()
    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRET_PATH), scopes=SCOPES, redirect_uri=REDIRECT_URI,
        autogenerate_code_verifier=True,
    )
    url, state = flow.authorization_url(access_type="offline", prompt="consent")
    PENDING_PATH.write_text(json.dumps({"state": state, "code_verifier": flow.code_verifier}), encoding="utf-8")
    os.chmod(PENDING_PATH, 0o600)
    print(url)


def exchange(callback):
    if not PENDING_PATH.exists():
        raise RuntimeError("Autorização pendente não encontrada. Rode authorize de novo.")
    pending = json.loads(PENDING_PATH.read_text(encoding="utf-8"))
    parsed = urlparse(callback)
    params = parse_qs(parsed.query)
    code = params.get("code", [callback])[0]
    state = params.get("state", [None])[0]
    if state and state != pending["state"]:
        raise RuntimeError("Estado OAuth inválido. Rode authorize de novo.")
    Flow, _, _ = _google_modules()
    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRET_PATH), scopes=SCOPES, redirect_uri=REDIRECT_URI,
        state=pending["state"], code_verifier=pending["code_verifier"],
    )
    flow.fetch_token(code=code)
    TOKEN_PATH.write_text(flow.credentials.to_json(), encoding="utf-8")
    os.chmod(TOKEN_PATH, 0o600)
    PENDING_PATH.unlink(missing_ok=True)
    print("AUTH_OK")


def fetch_rows():
    if not TOKEN_PATH.exists():
        raise RuntimeError("Planilha ainda não autorizada. Rode authorize e depois exchange.")
    _, Credentials, build = _google_modules()
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    service = build("sheets", "v4", credentials=creds, cache_discovery=False)
    response = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range="Lead!A:ZZ"
    ).execute()
    return [row for row in response.get("values", []) if any(str(cell).strip() for cell in row)]


def check():
    rows = fetch_rows()
    if len(rows) < 3:
        return
    message = new_lead_message(rows[0], rows[-2], rows[-1])
    if message and should_notify(rows[-1], load_last_notified_row()):
        print(message)
        save_last_notified_row(rows[-1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("authorize", "exchange", "check"))
    parser.add_argument("callback", nargs="?")
    args = parser.parse_args()
    try:
        if args.command == "authorize":
            authorize()
        elif args.command == "exchange":
            if not args.callback:
                parser.error("exchange exige a URL redirecionada pelo Google")
            exchange(args.callback)
        else:
            check()
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
