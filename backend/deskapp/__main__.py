"""Command line: `python -m deskapp serve` or `python -m deskapp run NVDA [--date YYYY-MM-DD]`."""

from __future__ import annotations

import argparse
import sys
import threading
import time


def main() -> int:
    parser = argparse.ArgumentParser(prog="deskapp")
    sub = parser.add_subparsers(dest="command", required=True)

    serve = sub.add_parser("serve", help="start the Glassbench web app")
    serve.add_argument("--port", type=int, default=None)

    run = sub.add_parser("run", help="run one ticker headless and print events")
    run.add_argument("ticker")
    run.add_argument("--date", default=None)
    run.add_argument("--analysts", default="market,social,news,fundamentals")
    run.add_argument("--depth", type=int, default=1)

    args = parser.parse_args()
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    if args.command == "serve":
        import uvicorn

        from .settings import HOST, PORT

        port = args.port or PORT
        print(f"Glassbench running at http://{HOST}:{port}  (Ctrl+C to stop)")
        uvicorn.run("deskapp.api:app", host=HOST, port=port, log_level="warning")
        return 0

    from .events import EventBus
    from .keys import load_keys
    from .runner import RunManager
    from .settings import DB_PATH, default_trade_date
    from .store import Store

    load_keys()
    store = Store(DB_PATH)
    bus = EventBus(store)
    manager = RunManager(store, bus, workers=1)
    run_id = manager.submit(args.ticker, args.date or default_trade_date(), args.analysts.split(","), args.depth,
                            "deepseek-v4-pro", "deepseek-v4-flash")
    print(f"run {run_id}")
    seen = 0
    done = threading.Event()
    while not done.is_set():
        for event in store.events_since(run_id, seen):
            seen = event["seq"]
            if event["type"] != "llm.delta":
                p = event["payload"]
                detail = p.get("tool") or p.get("model") or p.get("label") or p.get("rating") or p.get("error") or ""
                print(f"{time.strftime('%H:%M:%S', time.localtime(event['ts']))} {event['type']:<20} {event['agent'] or '':<18} {detail}")
            if event["type"] in ("run.finished", "run.failed", "run.cancelled"):
                done.set()
        time.sleep(0.5)
    manager.pool.shutdown(wait=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
