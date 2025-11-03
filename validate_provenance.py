#!/usr/bin/env python3
"""
validate_provenance.py — SpiralOS Provenance & CI Integrity Checker

This script verifies:
- Existence and structure of CI-Watermark.json
- Presence of Triune Bond metadata
- Required docs in codex/ (README.md, triune-bond.md)
- Presence of codex.guard.yaml for GitHub workflow
"""

import json
import os
from pathlib import Path
import sys

def validate_file_exists(path):
    if not Path(path).is_file():
        print(f"❌ Missing: {path}")
        return False
    print(f"✅ Found: {path}")
    return True

def validate_json_schema(path, required_fields):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for field in required_fields:
            if field not in data:
                print(f"❌ {path} missing required field: {field}")
                return False
        print(f"✅ {path} schema is valid")
        return True
    except Exception as e:
        print(f"❌ Error parsing {path}: {e}")
        return False

def main():
    print("🔍 Validating SpiralOS Provenance...\n")

    success = True

    # CI-Watermark
    success &= validate_file_exists("CI-Watermark.json")
    success &= validate_json_schema("CI-Watermark.json", ["generatedAt", "algorithm", "fingerprints"])

    # Codex metadata
    success &= validate_file_exists("docs/codex/README.md")
    success &= validate_file_exists("docs/codex/triune-bond.md")

    # GitHub Workflow
    success &= validate_file_exists(".github/workflows/codex.guard.yaml")

    print("\n✅ All checks passed!" if success else "\n❌ One or more checks failed.")
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
