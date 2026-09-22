"""Broker choice and connection checks. Glassbench's own code: no broker SDKs, paper endpoints only.

Orders are not placed yet (phase 4). This module records where they will go and
proves the connection works, so the choice is settled before strategy code exists.
"""

from __future__ import annotations

import json
import os
import socket

import httpx

from .settings import DATA_DIR

SETTINGS_FILE = DATA_DIR / "settings.json"

BROKERS = {
    "none": {"label": "No broker", "detail": "Runs produce ratings only. Nothing is sent anywhere."},
    "alpaca": {"label": "Alpaca", "detail": "Paper trading API. Keys come from .env."},
    "ibkr": {"label": "Interactive Brokers", "detail": "Paper account through IB Gateway or TWS running on this PC."},
}

ALPACA_PAPER_URL = "https://paper-api.alpaca.markets/v2/account"
IBKR_PAPER_PORTS = {4002: "IB Gateway paper", 7497: "TWS paper"}
IBKR_LIVE_PORTS = {4001: "IB Gateway live", 7496: "TWS live"}

DEFAULTS = {"broker": "none", "ibkr": {"host": "127.0.0.1", "port": 4002, "client_id": 17}}


def load_settings() -> dict:
    data = json.loads(json.dumps(DEFAULTS))
    if SETTINGS_FILE.exists():
        try:
            stored = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            data["broker"] = stored.get("broker", data["broker"])
            data["ibkr"].update(stored.get("ibkr") or {})
        except (json.JSONDecodeError, OSError):
            pass
    return data


def save_settings(broker: str, ibkr: dict | None) -> dict:
    if broker not in BROKERS:
        raise ValueError(f"Unknown broker '{broker}'")
    data = load_settings()
    data["broker"] = broker
    if ibkr:
        data["ibkr"].update({k: ibkr[k] for k in ("host", "port", "client_id") if k in ibkr})
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def check_connection(broker: str, ibkr: dict | None = None) -> dict:
    if broker == "none":
        return {"ok": True, "summary": "No broker selected", "details": []}
    if broker == "alpaca":
        return _check_alpaca()
    if broker == "ibkr":
        cfg = {**DEFAULTS["ibkr"], **(ibkr or {})}
        return _check_ibkr(str(cfg["host"]), int(cfg["port"]))
    return {"ok": False, "summary": f"Unknown broker '{broker}'", "details": []}


def _check_alpaca() -> dict:
    key, secret = os.environ.get("ALPACA_API_KEY", ""), os.environ.get("ALPACA_SECRET_KEY", "")
    if not key or not secret:
        return {"ok": False, "summary": "Alpaca keys missing", "details": ["Add ALPACA_API_KEY and ALPACA_SECRET_KEY to .env, then restart Glassbench."]}
    if not key.startswith("PK"):
        return {"ok": False, "summary": "These look like live keys", "details": ["Paper keys start with PK. Glassbench only connects to paper accounts."]}
    try:
        res = httpx.get(ALPACA_PAPER_URL, headers={"APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": secret}, timeout=8)
    except httpx.HTTPError as exc:
        return {"ok": False, "summary": "Alpaca unreachable", "details": [type(exc).__name__]}
    if res.status_code in (401, 403):
        return {"ok": False, "summary": "Alpaca rejected the keys", "details": ["Generate new paper keys in the Alpaca dashboard."]}
    if res.status_code != 200:
        return {"ok": False, "summary": f"Alpaca answered {res.status_code}", "details": [res.text[:200]]}
    acct = res.json()
    number = str(acct.get("account_number", ""))
    return {
        "ok": acct.get("status") == "ACTIVE",
        "summary": f"Connected · paper account ···{number[-4:]} · {acct.get('status', '').title()}",
        "details": [
            f"Equity {float(acct.get('equity', 0)):,.2f} {acct.get('currency', 'USD')}",
            f"Buying power {float(acct.get('buying_power', 0)):,.2f}",
            f"Shorting {'enabled' if acct.get('shorting_enabled') else 'disabled'}",
        ],
    }


def _check_ibkr(host: str, port: int) -> dict:
    if port in IBKR_LIVE_PORTS:
        return {"ok": False, "summary": f"Port {port} is {IBKR_LIVE_PORTS[port]}", "details": ["Glassbench only connects to paper: use 4002 (IB Gateway) or 7497 (TWS)."]}
    if host not in ("127.0.0.1", "localhost"):
        return {"ok": False, "summary": "Only a gateway on this PC is allowed", "details": ["Use host 127.0.0.1."]}
    try:
        with socket.create_connection((host, port), timeout=2):
            pass
    except OSError:
        return {
            "ok": False,
            "summary": f"Nothing listening on {host}:{port}",
            "details": [
                "Start IB Gateway and log in to the paper account.",
                "In Configure → Settings → API, enable socket clients and keep port 4002.",
            ],
        }
    label = IBKR_PAPER_PORTS.get(port, "a gateway")
    return {"ok": True, "summary": f"{label} reachable on {host}:{port}", "details": ["Account details are read once order routing is added in phase 4."]}
