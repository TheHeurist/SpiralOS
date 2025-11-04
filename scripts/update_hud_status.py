#!/usr/bin/env python3
"""
SpiralOS® HUD Pulse Updater
Reads Codex Guard outputs (lint_errors_python.json) and updates
docs/hud/status.json with the appropriate color/state mapping.
"""

import json, datetime, pathlib

def classify_state(lint_file: pathlib.Path) -> tuple[str, str]:
    """Return (state, color) from lint report."""
    if not lint_file.exists():
        return "coherent", "10B981"
    data = lint_file.read_text()
    if "IndentationError" in data or "E9" in data:
        return "repairing", "EAB308"
    if "warning" in data or "W" in data:
        return "review", "F97316"
    if "error" in data or "E" in data:
        return "failed", "EF4444"
    return "coherent", "10B981"

def update_status():
    lint_path = pathlib.Path("lint_errors_python.json")
    status_path = pathlib.Path("docs/hud/status.json")

    state, color = classify_state(lint_path)
    status = {
        "schema_version": 1,
        "label": "HUD Pulse",
        "message": f"Codex Guard – {state.capitalize()} 🌀",
        "color": color,
        "emoji": "🌀",
        "state": state,
        "last_update": datetime.datetime.utcnow().isoformat() + "Z"
    }
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status, indent=2))
    print(f"HUD status updated: {state} ({color})")

if __name__ == "__main__":
    update_status()
