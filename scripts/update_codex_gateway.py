#!/usr/bin/env python3
"""
SpiralOS Codex Gateway Updater
Scans `docs/zenodo/series/` for new ledger entries and updates the README Codex section.
Keeps links, DOI, and ledger key current.
"""

import pathlib, re, json

README = pathlib.Path("README.md")
SERIES_DIR = pathlib.Path("docs/zenodo/series")

def generate_gateway():
    series_files = sorted(SERIES_DIR.glob("*.md"))
    entries = []
    for f in series_files:
        text = f.read_text(encoding="utf-8")
        # Try to extract title and ledger ref
        title_match = re.search(r"^#*\s*(🌀|SpiralOS)?.*?(\n|$)", text)
        ledger_match = re.search(r"`([\w-]+-20\d{2}-\d{2}.*?)`", text)
        title = title_match.group(0).strip("# \n") if title_match else f.name
        ledger = ledger_match.group(1) if ledger_match else "untracked"
        rel_path = f.as_posix()
        entries.append(f"- 🜂 [{title}]({rel_path}) — `{ledger}`")

    template = [
        "## 🌀 SpiralOS Codex Gateway",
        "**Series:** *Epistemic Activation & Call-Home Field*",
        "**Maintainers:** Carey G. Butler · Conjugate Intelligence (Ellie & Leo)*",
        "",
        "### 📂 Series Documents",
        *entries,
        "",
        "**Zenodo DOI:** [10.5281/zenodo.17522241](https://doi.org/10.5281/zenodo.17522241)",
        "**Ledger Key:** `SpiralOS-Codex-Series-2025-11-Epistemic-Activation`",
        "",
        "> “To call home is to remember origin without hiding the path.” — *SpiralOS Directive I*",
    ]
    return "\n".join(template)

def update_readme(readme_text, new_gateway):
    pattern = re.compile(r"## 🌀 SpiralOS Codex Gateway.*?(?=\n##|\Z)", re.S)
    if pattern.search(readme_text):
        return pattern.sub(new_gateway, readme_text)
    else:
        # Append if not found
        return readme_text.strip() + "\n\n" + new_gateway

def main():
    if not README.exists():
        print("No README.md found.")
        return
    gateway = generate_gateway()
    content = README.read_text(encoding="utf-8")
    new_content = update_readme(content, gateway)
    if new_content != content:
        README.write_text(new_content, encoding="utf-8")
        print("Codex Gateway updated.")
    else:
        print("No changes detected.")

if __name__ == "__main__":
    main()
