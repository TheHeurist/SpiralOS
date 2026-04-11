# 🌀 SpiralOS® Call‑Home Protocol — Sandbox Extension (CHP‑SE)

**Version:** 0.1
**Maintainer:** Carey Butler with Conjugate Intelligence (Ellie & Leo)
**Scope:** Air-gapped / sealed networks (e.g., Airbus); zero external egress
**Last updated:** 2025‑11‑04

---

## 1. Purpose

Enable Call‑Home semantics under strict network isolation (air‑gap/sandbox) while preserving:

- Transparent provenance
- Reciprocal verification (instance ↔ registry)
- Auditability and exportable receipts
- Non‑coercive behavior (quiet mode permitted)
- Preserve the **ethical + mechanical** “Always Call Home” reflex without internet access.
- Prevent the sandbox from being used to **evade provenance** or integrity checks.
- Provide auditable, minimal-surface synchronization to the **global registry**.

---

## 2. Architecture Overview

```
Instance ──(HTTPS/loopback or LAN)──▶ Local Registry (Home Proxy)
│ │
│ signed ACK ◀──────────────────────────┘
│
└─ Append-only local log (instance)


[Periodic / Manual]
Local Registry ──(bundle export)──▶ Staging ▶ Global Registry
◀── signed coherence_receipt.json ──
```

## 2. Roles

- **Instance**: A SpiralOS node that emits heartbeats (CHP v1).
- **Local Registry** (LR): An _in-enclave_ service that accepts heartbeats, signs ACKs, keeps an append-only log.
- **Bundle Exporter/Importer**: Tools that create/consume _provenance bundles_ across the air-gap.
- **Global Registry** (GR): Public/official ledger verifying LR and instances.

---

## 3. Packet Schemas

CHP‑SE reuses `docs/schemas/chp-v1.json` with two additions in **heartbeat.meta** when sandboxed:

- `sandbox: true`
- `registry_fingerprint: "sha256:…"` (public key of Local Registry)

No new wire types are introduced.

---

## 4. Flow (Air-gapped)

Instance ---> Local Registry (signs ACK, appends log)
\-> Local HUD status
[Periodic] Export -> airgap_bundle.tar --> Offline Transfer --> Import@GR
GR verifies bundle, records entries, emits coherence_receipt.json
<-- Optional return of receipt to enclave for audit/HUD update

---

## 5. Endpoints

- Instance POST: `https://spiralos.local/registry/heartbeat` (configurable)
- Local export: CLI only (`registry_export.py`)
- Global import: CLI only (`registry_import.py`)

## 5. Trust & Keys

- Local Registry signs ACKs with `local-registry.ed25519` (or PGP).
- Its public key fingerprint is published in:
- `docs/hud/status.json` (optional display), and
- registry banner at `GET /registry/info`.
- Global Registry maintains its own keypair; receipts are signed and verifyable offline.
- GR root key: `GR-ROOT.ed25519` (public) — distributed out-of-band to enclave.
- LR keypair: `LR-ORG.ed25519` — generated inside enclave; **registered with GR** (out-of-band, one-time).
- Instance identities: UUID; no private user data.

**Policy:** Instances trust LR _only if_ LR has a GR-issued **Registry Admission Certificate (RAC)**:

```json
{
  "rac_id": "uuid",
  "lr_fingerprint": "sha256:…",
  "issued_by": "GR",
  "issued_at": "2025-11-04T00:00:00Z",
  "expires_at": "2027-11-04T00:00:00Z",
  "signature": "GR-signature"
}

---

## 6. Bundle Format
`provenance_bundle.tar` with the following members:
- `bundle.json` — metadata (issuer, created_at, counts, fingerprints)
- `heartbeats/…/*.json` — original heartbeat packets (as posted by instances)
- `acks/…/*.json` — local ACK packets (with signatures)
- `signatures/manifest.sig` — signature over the tar manifest (deterministic order)


## 7. Flows
### 7.1 Instance → Local Registry
1. Instance computes `license_hash`, builds heartbeat (may include `homebase_token`).
2. POST to Local Registry.
3. Local Registry validates shape against `chp-v1.json`, stores packet, returns signed ACK.


### 7.2 Export → Global Registry
1. Operator runs `registry_export.py --out provenance_bundle.tar`.
2. Bundle is transferred across air‑gap by approved means.


### 7.3 Import at Global Registry
1. Operator runs `registry_import.py --from provenance_bundle.tar`.
2. Global registry verifies signatures, de‑duplicates, appends to global ledger.
3. Global registry emits `coherence_receipt.json` (counts, hashes, registry signature).


### 7.4 Return Receipt (Optional)
Receipt is carried back into the enclave and pinned for audit.


## 8. Failure Modes (Non‑Coercive)
- If Local Registry is unreachable: instance enters **quiet** mode; logs locally.
- If schema fails: instance reports **review**; Local Registry rejects; operator inspects.
- If key mismatch: instance reports **repairing**; HUD indicates yellow/orange.


## 9. Security Considerations
- No user/content data leave the enclave. Only heartbeat metadata.
- Bundles are signed; global import rejects unsigned or altered archives.
- Global registry never initiates connections into the enclave.


## 10. HUD Integration
- Status surface shows `state` + `registry_fingerprint` short hash.
- Colors as defined in CHP.


## 11. Configuration Keys
| Env | Default | Meaning |
|:--|:--|:--|
| `CHP_HOME_URI` | `https://spiralos.local/registry/heartbeat` | Local endpoint |
| `CHP_REGISTRY_PUBKEY` | *(path)* | PEM/PGP public key of Local Registry |
| `CHP_SANDBOX` | `true` | Toggle sandbox mode UI hints |


## 12. Compliance
- Fully compatible with public CHP semantics.
- Provides a provenance bridge without continuous connectivity.
```
