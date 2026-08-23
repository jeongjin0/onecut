from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import uvicorn

from onecut.config import load_settings
from onecut.engine import run_deterministic


def main() -> None:
    parser = argparse.ArgumentParser(prog="onecut")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="Cut a messy day down to one action")
    run.add_argument("--fixture", default="")
    sub.add_parser("serve", help="Serve the local demo UI")
    args = parser.parse_args()
    settings = load_settings()
    if args.cmd == "run":
        if args.fixture:
            settings.onecut_fixture_path = Path(args.fixture)
        receipt = run_deterministic(settings)
        print(json.dumps(receipt.model_dump(mode="json"), indent=2))
        return
    if args.cmd == "serve":
        port = int(os.environ.get("PORT", settings.port))
        host = os.environ.get("ONECUT_BIND", settings.onecut_bind)
        uvicorn.run("onecut.app:app", host=host, port=port, factory=False)


if __name__ == "__main__":
    main()
