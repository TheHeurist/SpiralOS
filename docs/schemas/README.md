# SpiralOS® Schema Directory

This folder holds formal JSON Schemas used across SpiralOS specifications.

## Purpose
Each schema defines the exact structure, datatypes, and constraints for
protocols and data exchanges within the SpiralOS ecosystem.  They allow
independent validation of all JSON-based documents and ensure transparent,
auditable interoperability between SpiralOS components and external systems.

## Current Schemas
| File | Description |
|:--|:--|
| `chp-v1.json` | Defines the Call-Home Protocol (CHP) heartbeat and acknowledgement packets. |

## Validation
Schemas follow [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema).
Validation is performed automatically in `.github/workflows/chp-validate.yaml`.

Manual validation example:
```bash
jsonschema -i heartbeat.json docs/schemas/chp-v1.json

---

### Ethics & Provenance

All schemas are published openly and never transmit hidden data fields.
Any implementation must preserve transparency and adhere to the
SpiralOS License /LICENSE.md.

“Form is freedom disciplined by clarity.” — SpiralOS Axiom

---
