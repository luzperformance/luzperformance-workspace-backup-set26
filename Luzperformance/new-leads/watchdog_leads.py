#!/usr/bin/env python3
"""Watchdog do cron de leads.

Roda periodicamente. Só escreve em stdout quando detecta 3+ falhas
consecutivas e não consegue consertar o monitor.
"""

import json
import os
import sys
import traceback
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = BASE_DIR / "watchdog_state.json"
TOKEN_PATH = BASE_DIR / "google_token.json"
LAST_NOTIFIED_PATH = BASE_DIR / "last_notified_row.json"
CLIENT_SECRET_PATH = Path("/data/google_client_secret.json")
SPREADSHEET_ID = "19SrwzlrcTT9ttRo_C_oVSmPqFzrWZ8wupYyZ7Ew9A1U"
MAX_FAILURES = 3


def load_state():
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            pass
    return {"consecutive_failures": 0, "total_failures": 0, "last_success": None, "last_check": None}


def save_state(state):
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, default=str), encoding="utf-8")
    os.chmod(STATE_PATH, 0o600)


def check_connectivity():
    """Tenta ler a planilha. Retorna (ok, erro)."""
    if not TOKEN_PATH.exists():
        return False, "google_token.json não encontrado — reautorização necessária"
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
    except ImportError as e:
        return False, f"Dependências ausentes: {e}"

    try:
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), ["https://www.googleapis.com/auth/spreadsheets.readonly"])
        service = build("sheets", "v4", credentials=creds, cache_discovery=False)
        response = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="Lead!A1:A3").execute()
        return True, None
    except Exception as e:
        return False, str(e)


def attempt_fix(failure_reason):
    """Tenta correções comuns. Retorna (fixed, message)."""
    fixes_tried = []

    # 1. Script do cron existe?
    script_locations = [
        Path("/data/scripts/monitor_leads_novos.sh"),
        Path("/data/.hermes/scripts/monitor_leads_novos.sh"),
    ]
    script_exists = any(p.exists() for p in script_locations)
    if not script_exists:
        # Recriar de /data/.hermes/scripts/ para /data/scripts/
        src = Path("/data/.hermes/scripts/monitor_leads_novos.sh")
        dst = Path("/data/scripts/monitor_leads_novos.sh")
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(src.read_bytes())
            dst.chmod(0o755)
            fixes_tried.append("script recriado em /data/scripts/")
        else:
            fixes_tried.append("script fonte perdido — impossível recriar")

    # 2. run_check.sh existe?
    run_check = BASE_DIR / "run_check.sh"
    if not run_check.exists():
        fixes_tried.append(f"run_check.sh ausente em {BASE_DIR}")

    # 3. Token expirado — tentar refresh
    if TOKEN_PATH.exists():
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), ["https://www.googleapis.com/auth/spreadsheets.readonly"])
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
                os.chmod(TOKEN_PATH, 0o600)
                fixes_tried.append("token OAuth renovado")
        except Exception as e:
            fixes_tried.append(f"falha ao renovar token: {e}")

    # 4. Tentar conectar de novo
    ok, err = check_connectivity()
    if ok:
        return True, "; ".join(fixes_tried) if fixes_tried else "conectividade restaurada sem ação específica"
    else:
        fixes_tried.append(f"ainda falhando: {err}")
        return False, "; ".join(fixes_tried)


def main():
    state = load_state()
    now = datetime.now(timezone.utc)

    ok, err = check_connectivity()
    state["last_check"] = now.isoformat()

    if ok:
        state["consecutive_failures"] = 0
        state["last_success"] = now.isoformat()
        save_state(state)
        return  # silencioso

    # Falhou
    state["consecutive_failures"] += 1
    state["total_failures"] += 1
    state["last_error"] = err

    if state["consecutive_failures"] >= MAX_FAILURES:
        fixed, fix_msg = attempt_fix(err)
        if fixed:
            state["consecutive_failures"] = 0
            state["last_success"] = now.isoformat()
            save_state(state)
            return  # consertado, silencioso
        else:
            # Não conseguiu consertar — alertar
            save_state(state)
            print(f"⚠️ Não foi possível consertar o Cron monitor-leads após {state['consecutive_failures']} falhas seguidas.")
            print(f"Último erro: {err}")
            print(f"Tentativas de correção: {fix_msg}")
    else:
        save_state(state)
        # Silencioso, ainda não atingiu 3 falhas


if __name__ == "__main__":
    main()