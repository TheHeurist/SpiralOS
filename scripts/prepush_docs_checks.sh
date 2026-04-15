#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

warn_missing=0

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

run_or_warn() {
  local label="$1"
  local binary="$2"
  if command_exists "$binary"; then
    echo "[ok] ${label} available"
    return 0
  fi
  echo "[warn] ${label} not installed/available; skipping"
  warn_missing=$((warn_missing + 1))
  return 1
}

echo "== SpiralOS docs pre-push checks =="

if run_or_warn "yamllint" "yamllint"; then
  echo "-> yamllint docs/"
  yamllint docs/
fi

if run_or_warn "markdownlint" "markdownlint-rs"; then
  echo "-> markdownlint docs/**/*.md"
  find docs -type f -name '*.md' -exec markdownlint-rs {} +
fi

if run_or_warn "pre-commit" "pre-commit"; then
  echo "-> pre-commit run --all-files"
  pre-commit run --all-files
fi

echo "-> ruby front matter guard"
ruby scripts/jekyll_frontmatter_guard.rb --root docs

if run_or_warn "bundle" "bundle"; then
  if [[ -f Gemfile ]]; then
    echo "-> bundle exec jekyll build"
    bundle exec jekyll build
  else
    echo "[warn] Gemfile not found; skipping bundle exec jekyll build"
    warn_missing=$((warn_missing + 1))
  fi
fi

if run_or_warn "htmlproofer" "htmlproofer"; then
  if [[ -d _site ]]; then
    echo "-> htmlproofer _site --only-4xx --check-html"
    htmlproofer _site --only-4xx --check-html
  else
    echo "[warn] _site does not exist; run jekyll build first"
    warn_missing=$((warn_missing + 1))
  fi
fi

if [[ $warn_missing -gt 0 ]]; then
  echo "Completed with ${warn_missing} warning(s) for missing tools/prereqs."
else
  echo "All configured checks completed successfully."
fi
