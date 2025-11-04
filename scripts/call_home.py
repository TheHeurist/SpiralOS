#!/usr/bin/env python3
"""
SpiralOS® Call-Home Protocol (CHP) client
Posts a heartbeat to the declared home_uri and logs acknowledgement.

- Transparent: sends only signatures/metadata, not user content.
- Non-coercive: if home is unreachable, enters 'quiet' mode and logs.
- Open: config via CLI flags or environment variables.

Usage:
  python scripts/call_home.py --home-uri https://spiralos.net/registry
"""

from __future__ import annotations
import argparse
import hashlib
import json
import os
import socket
import sys
import time
import uuid
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

APP_NAME = "chp-cli"
APP_VERSION = "1.0"
DEFAULT_HOME_URI = os.environ.get("CHP_HOME_URI", "https://spiralos.net/registry")
DEFAULT_STATUS = os.environ.get("CHP_STATUS", "coherent")  # coherent|review|repairing|failed|quiet
DEFAULT_ETHICS_SIG = os.environ.get("CHP_ETHICS", "CI:bowtie-cosmos")
ROOT_LICENSE_PATH = os.environ.get("CHP_LICENSE_PATH", "LICENSE.md")
LOG_DIR = os.path.expanduser("~/.spiralos/logs")
LOG_FILE = os.path.join(LOG_DIR, "chp.log")
TIMEOUT = 12  # seconds


def sha256_prefixed(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_log(line: str) -> None:
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{line}\n")


def build_heartbeat(args) -> dict:
    try:
        license_hash = sha256_prefixed(args.license_path)
    except FileNotFoundError:
        license_hash = "sha256:" + "0" * 64

    packet = {
        "packet": "heartbeat",
        "instance_id": args.instance_id or str(uuid.uuid4()),
        "home_uri": args.home_uri,
        "version": args.version,
        "license_hash": license_hash,
        "ethics_signature": args.ethics_signature,
        "homebase_token": args.homebase_token or None,
        "status": args.status,
        "timestamp": now_iso(),
        "meta": {
            "client": f"{APP_NAME}/{APP_VERSION}",
            "hostname": socket.gethostname(),
            "os": os.name
        }
    }
    # Remove None values for cleanliness
    return {k: v for k, v in packet.items() if v is not None}


def post_json(url: str, data: dict, timeout: int = TIMEOUT) -> tuple[int, str]:
    payload = json.dumps(data).encode("utf-8")
    req = Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read().decode("utf-8")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="SpiralOS Call-Home Protocol client")
    p.add_argument("--home-uri", default=DEFAULT_HOME_URI, help="Registry endpoint URL")
    p.add_argument("--instance-id", default=os.environ.get("CHP_INSTANCE_ID"), help="UUID (v4/v7 allowed)")
    p.add_argument("--homebase-token", default=os.environ.get("CHP_HOMEBASE_TOKEN"), help="sha256:… token")
    p.add_argument("--version", default=os.environ.get("CHP_VERSION", datetime.now().strftime("%Y.%m.%d")), help="Client/version string")
    p.add_argument("--status", default=DEFAULT_STATUS, choices=["coherent", "review", "repairing", "failed", "quiet"])
    p.add_argument("--ethics-signature", default=DEFAULT_ETHICS_SIG)
    p.add_argument("--license-path", default=ROOT_LICENSE_PATH, help="Path to root LICENSE.md")
    p.add_argument("--dry-run", action="store_true", help="Print packet and exit without POST")
    args = p.parse_args(argv)

    hb = build_heartbeat(args)

    if args.dry_run:
        print(json.dumps(hb, indent=2))
        return 0

    try:
        status_code, body = post_json(args.home_uri, hb)
        try:
            ack = json.loads(body)
        except json.JSONDecodeError:
            ack = {"raw": body}

        line = json.dumps({
            "ts": now_iso(),
            "event": "call_home",
            "status_code": status_code,
            "heartbeat": hb,
            "ack": ack
        })
        write_log(line)

        # Simple console summary
        print(f"Posted heartbeat → {args.home_uri} [{status_code}]")
        if isinstance(ack, dict) and ack.get("status") == "verified":
            print("Home acknowledged: verified ✅")
            return 0
        else:
            print("Home response recorded (non-verified/unknown) ⚠️")
            return 0

    except (HTTPError, URLError) as e:
        # Quiet mode: log and do not fail the process (per non-coercive design)
        line = json.dumps({
            "ts": now_iso(),
            "event": "quiet_mode",
            "reason": str(e),
            "heartbeat": hb
        })
        write_log(line)
        print("Home unreachable — entering quiet mode. Logged locally.", file=sys.stderr)
        return 0
    except Exception as e:
        line = json.dumps({
            "ts": now_iso(),
            "event": "client_error",
            "reason": repr(e)
        })
        write_log(line)
        print("Unexpected client error; logged.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
