#!/usr/bin/env python3
"""Export CHP-SE provenance bundle from Local Registry ledger.
Creates provenance_bundle.tar with heartbeats, acks, and a signed manifest.
"""
import argparse, json, pathlib, tarfile, hashlib, datetime
LEDGER_DIR = pathlib.Path("./ledger")

def deterministic_listing(root: pathlib.Path):
  files = sorted([p for p in root.rglob("*.json") if p.is_file()])
  return files

def manifest_hash(files):
h = hashlib.sha256()

for p in files:
  h.update(p.read_bytes())
  return h.hexdigest()


def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--out", default="provenance_bundle.tar")
  args = ap.parse_args()


files = deterministic_listing(LEDGER_DIR)

bundle_meta = {
  "issuer": "local-registry",
  "created_at": datetime.datetime.utcnow().isoformat()+"Z",
  "counts": {"files": len(files)},
  "fingerprint": "sha256:" + manifest_hash(files)
}


with tarfile.open(args.out, "w") as tar:
  info = tarfile.TarInfo("bundle.json")
  data = json.dumps(bundle_meta, indent=2).encode()
  info.size = len(data)
  tar.addfile(info, fileobj=io.BytesIO(data))
  for p in files:
    tar.add(p, arcname=str(p))

print(f"Wrote {args.out} with {len(files)} files.")

if __name__ == "__main__":
  import io
main()
