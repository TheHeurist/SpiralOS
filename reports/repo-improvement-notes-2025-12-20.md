# SpiralOS — Improvement Notes (2025-12-20)

## Purpose
This note captures quick, high-impact recommendations to strengthen day-to-day reproducibility and schema adoption while staying aligned with the Codex provenance guardrails.

## Recommendations
1) **Add runnable npm scripts for provenance checks.** Package metadata currently ships without scripts; wiring `validate_provenance.py` behind `npm run validate:provenance` (and a `format` placeholder) would give contributors a single entrypoint before CI. Consider a tiny `scripts/` shim that shells to Python for portability.
2) **Ship a sample manifest JSON that conforms to `manifest-schema`.** A checked-in example under `docs/schema/examples/manifest.sample.json` (or next to a Volume) would clarify how to fill required fields (`title`, `description`, `doi`, `volumeNumber`, `ciState`) and demonstrate `ciState` references into `conjugate-intelligence.json`.
3) **Document a local “preflight” before CI.** The README lists CI lanes, but a short “Local Validation” snippet (npm script + provenance command) would align contributor expectations and reduce guardrail drift.

## Notes on access
Yes—I can write to this repository. This note was added directly to `reports/` to confirm access and provide actionable next steps.
