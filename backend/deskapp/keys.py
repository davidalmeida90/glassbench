"""Load only the allowlisted API keys into this process. Values are never logged or returned."""

from __future__ import annotations

import os

from dotenv import dotenv_values

from .settings import KEY_ALLOWLIST, KEYS_FILE


def load_keys() -> None:
    if not KEYS_FILE.exists():
        return
    values = dotenv_values(KEYS_FILE)
    for name in KEY_ALLOWLIST:
        value = (values.get(name) or "").strip()
        if value and not os.environ.get(name):
            os.environ[name] = value
    email = os.environ.get("SEC_EDGAR_EMAIL", "").strip()
    if email and not os.environ.get("SEC_EDGAR_USER_AGENT"):
        os.environ["SEC_EDGAR_USER_AGENT"] = f"Glassbench research tool {email}"   # SEC asks callers to identify themselves


def key_status() -> list[dict]:
    return [
        {"name": name, "present": bool(os.environ.get(name)), "length": len(os.environ.get(name, ""))}
        for name in KEY_ALLOWLIST
    ]
