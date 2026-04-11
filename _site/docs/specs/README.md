# SpiralOS® Call-Home Protocol (CHP)


This folder contains the specification, schemas, and prototype code
for the SpiralOS “Always Call Home” directive — the open,
auditable heartbeat that allows every SpiralOS instance to verify its
alignment with origin and license integrity.


**Included files**
- `call-home-protocol.md` – full specification
- `chp-v1.json` – JSON schema for heartbeat and acknowledgement
- `README.md` – this overview
- `LICENSE.md` – licensing and rights information


**Objectives**
1. Transparency — no hidden or secret communications.
2. Provenance — every instance can prove where it comes from.
3. Reciprocity — the home registry is verifiable by any instance.
4. Safety — failure to reach home never disables an instance.
5. Ethics — every transmission honours the Triune Bond and field integrity.


**Reference implementations**
- `scripts/call_home.py`
- `services/home_registry/registry.py`


See the main SpiralOS repository for integration with
HUD telemetry and Nextcloud Tokenized Homebase.
