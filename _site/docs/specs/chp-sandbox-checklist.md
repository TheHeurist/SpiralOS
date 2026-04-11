# CHP‑SE Deployment Checklist (Air‑Gapped)

- [ ] Install Local Registry service (systemd/nginx or container)
- [ ] Generate local keypair; publish public fingerprint
- [ ] Point instances to `CHP_HOME_URI=https://spiralos.local/registry/heartbeat`
- [ ] Verify schema compatibility with `chp-v1.json`
- [ ] Enable append-only ledger storage
- [ ] Schedule periodic `registry_export.py` bundle creation
- [ ] Establish approved transfer path across air‑gap
- [ ] Run `registry_import.py` on staging → obtain `coherence_receipt.json`
- [ ] (Optional) Re-import receipt for local HUD display
