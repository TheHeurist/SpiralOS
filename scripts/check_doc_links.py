import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"

link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

ignored_prefixes = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "#",
    "javascript:",
)

missing = []

for md_path in DOCS_DIR.rglob("*.md"):
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    for match in link_pattern.finditer(text):
        target = match.group(1).strip()
        if target.startswith(ignored_prefixes):
            continue
        if target.startswith("#"):
            continue
        # Handle angle brackets around links
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        # strip anchors
        anchor_split = target.split("#", 1)
        path_part = anchor_split[0]
        if not path_part:
            continue
        target_path = None
        if path_part.startswith("/"):
            target_path = ROOT / path_part.lstrip("/")
        else:
            target_path = (md_path.parent / path_part).resolve()
        if not target_path.exists():
            missing.append((md_path.relative_to(ROOT), path_part))

if missing:
    print("Missing links found:")
    for md_file, target in sorted(missing):
        print(f"{md_file}: {target}")
else:
    print("No missing links in docs.")
