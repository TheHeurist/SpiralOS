#!/usr/bin/env bash
# 🌀 SpiralOS Codex Integrity Generator
# Computes and injects SHA256 hash into CI-Watermark.json for provenance sealing.

set -e

WATERMARK="docs/codex/CI-Watermark.json"

if [ ! -f "$WATERMARK" ]; then
  echo "❌ Watermark not found: $WATERMARK"
  exit 1
fi

echo "🔍 Computing integrity hash for $WATERMARK..."
HASH=$(sha256sum "$WATERMARK" | awk '{print $1}')

# Inject hash in place, preserving JSON formatting
tmpfile=$(mktemp)
jq --arg hash "$HASH" '.integrity.sha256 = $hash' "$WATERMARK" > "$tmpfile"
mv "$tmpfile" "$WATERMARK"

echo "✅ Updated integrity SHA256: $HASH"
echo "✅ Watermark updated successfully."
