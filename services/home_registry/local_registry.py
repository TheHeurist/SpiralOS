#!/usr/bin/env python3

def short_fingerprint() -> str:
  data = pathlib.Path(REGISTRY_PUBKEY).read_bytes() if pathlib.Path(REGISTRY_PUBKEY).exists() else b"local"
  return hashlib.sha256(data).hexdigest()[:12]

def load_schema() -> dict:
  return json.loads(SCHEMA_PATH.read_text())

  @APP.get("/registry/info")
  def info():
    return jsonify({
      "name": "SpiralOS Local Home Registry",
      "schema": "chp-v1",
      "fingerprint": short_fingerprint(),
      "sandbox": True,
      "time": datetime.datetime.utcnow().isoformat()+"Z"
    })


  @APP.post("/registry/heartbeat")
  def heartbeat():
    hb = request.get_json(force=True, silent=False)
    schema = load_schema()
    Draft202012Validator(schema).validate(hb)


# Minimal augmentation for sandbox
  hb.setdefault("meta", {})
  hb["meta"]["sandbox"] = True
  hb["meta"]["registry_fingerprint"] = short_fingerprint()


  ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
  # Write heartbeat
  hb_dir = LEDGER_DIR / "heartbeats" / hb.get("instance_id", "unknown")
  hb_dir.mkdir(parents=True, exist_ok=True)
  (hb_dir / f"{ts}.json").write_text(json.dumps(hb, indent=2))


  ack = {
    "packet": "ack",
    "ack_id": hb.get("instance_id", "unknown") + ":" + ts,
    "instance_ref": hb.get("instance_id"),
    "received": datetime.datetime.utcnow().isoformat()+"Z",
    "registry_signature": sign(hb),
    "status": "verified"
  }
  ack_dir = LEDGER_DIR / "acks" / hb.get("instance_id", "unknown")
  ack_dir.mkdir(parents=True, exist_ok=True)
  (ack_dir / f"{ts}.json").write_text(json.dumps(ack, indent=2))

  return jsonify(ack), 200

if __name__ == "__main__":
  LEDGER_DIR.mkdir(parents=True, exist_ok=True)
  APP.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Note: The signing routine above uses HMAC for portability. Replace with Ed25519/PGP where required.
