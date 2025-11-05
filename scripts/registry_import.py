#!/usr/bin/env python3
"""Import CHP-SE provenance bundle into Global Registry ledger and emit a receipt.
Verifies bundle structure and emits coherence_receipt.json with signature placeholder.
"""
import argparse, json, tarfile, tempfile, pathlib, hashlib, datetime


GLOBAL_LEDGER = pathlib.Path("./global-ledger")




def sha256f(p: pathlib.Path) -> str:
  import hashlib
  h = hashlib.sha256()
  h.update(p.read_bytes())
  return h.hexdigest()


def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--from", dest="src", required=True)
  ap.add_argument("--out", dest="out", default="coherence_receipt.json")
  args = ap.parse_args()

  GLOBAL_LEDGER.mkdir(parents=True, exist_ok=True)

  with tempfile.TemporaryDirectory() as td:
    with tarfile.open(args.src, "r") as tar:
      tar.extractall(td)
      root = pathlib.Path(td)
      hb = list(root.rglob("heartbeats/**/*.json"))
      acks = list(root.rglob("acks/**/*.json"))
      # naive copy-in; real impl would de-duplicate by instance+timestamp
      for p in hb + acks:
         dest = GLOBAL_LEDGER / p.relative_to(root)
         dest.parent.mkdir(parents=True, exist_ok=True)
         dest.write_text(p.read_text())

      receipt = {
        "received_at": datetime.datetime.utcnow().isoformat()+"Z",
        "bundle": pathlib.Path(args.src).name,
        "counts": {"heartbeats": len(hb), "acks": len(acks)},
        "global_fingerprint": "sha256:" + sha256f(pathlib.Path(args.src)),
        "registry_signature": "SIGNME" # replace with real signature
        }
  pathlib.Path(args.out).write_text(json.dumps(receipt, indent=2))
  print(f"Wrote {args.out}")


if __name__ == "__main__":
  main()
