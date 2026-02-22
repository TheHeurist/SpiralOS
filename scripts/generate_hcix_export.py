#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import tarfile
import subprocess
from collections import defaultdict, Counter
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT_DIR = ROOT / "_export_hcix" / "hcix_export"
MAX_FILE = 790 * 1024

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BOLD_DEF_RE = re.compile(r"^\s*[-*]?\s*\*\*([^*]{1,160})\*\*\s*[:\-–—]\s*(.+)$")
PLAIN_DEF_RE = re.compile(
    r"^\s*[-*]?\s*([A-Za-z0-9µφΦχψΩ⋈⋔↻⊙\-_/().,'\s]{2,120}?)\s+(is|are|means|denotes|refers to|is defined as|defines)\s+(.+)$",
    re.IGNORECASE,
)
SYMBOL_DEF_RE = re.compile(r"^\s*[-*]?\s*(\$[^$]+\$|[\u0370-\u03FF\u2200-\u22FF\u2100-\u214F][^:]{0,60})\s*:\s*(.+)$")
TOKEN_RE = re.compile(r"\*\*([^*]{2,120})\*\*|`([^`]{1,120})`")

GLYPH_HINT = re.compile(r"[µφΦχψΩ⋈⋔↻⊙ℋ𝕊∇∂∑∞πθλδζηκτνρσ]|")
EQUATION_HINT = re.compile(r"\$[^$]+\$|\\\(|\\\)|\\[a-zA-Z]+|=|∇|∑|∫|≈|≠|≤|≥")
SYMBOL_HINT = re.compile(r"[µφΦχψΩ⋈⋔↻⊙ℋ𝕊∇∂∑∞πθλδζηκτνρσ]|\$[^$]+\$")


@dataclass
class Defn:
    term: str
    definition: str
    path: str
    heading: str
    start: int
    end: int


@dataclass
class Mention:
    term: str
    path: str
    heading: str
    start: int
    end: int


@dataclass
class SourceDoc:
    path: Path
    kind: str  # md|pdf


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def norm_term(term: str) -> str:
    t = term.strip().strip("`*").strip()
    t = re.sub(r"\s+", " ", t)
    return t


def key_term(term: str) -> str:
    t = norm_term(term).lower()
    t = re.sub(r"[^a-z0-9µφχψω⋈⋔↻⊙]+", "", t)
    return t


def pick_sources() -> Tuple[List[SourceDoc], int, int]:
    md_files = sorted(DOCS.rglob("*.md"))
    md_by_dir_stem = defaultdict(set)
    for p in md_files:
        md_by_dir_stem[p.parent].add(p.stem.lower())

    pdf_files = sorted(DOCS.rglob("*.pdf"))
    picked_pdf = []
    for p in pdf_files:
        if p.stem.lower() not in md_by_dir_stem[p.parent]:
            picked_pdf.append(p)

    sources = [SourceDoc(p, "md") for p in md_files] + [SourceDoc(p, "pdf") for p in picked_pdf]
    return sources, len(md_files), len(picked_pdf)


def headings_from_lines(lines: List[str]) -> List[Tuple[int, str]]:
    hs = []
    for i, line in enumerate(lines, start=1):
        m = HEADING_RE.match(line)
        if m:
            txt = m.group(2).strip()
            if txt:
                hs.append((i, txt))
    return hs


def heading_at(line_no: int, hs: List[Tuple[int, str]]) -> str:
    cur = "(root)"
    for ln, h in hs:
        if ln <= line_no:
            cur = h
        else:
            break
    return cur


def first_nonempty(lines: List[str]) -> str:
    for ln in lines:
        t = ln.strip()
        if t:
            return t[:160]
    return "(pdf)"


def extract_pdf_text(path: Path) -> Tuple[List[str], str | None]:
    try:
        proc = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=25,
        )
    except subprocess.TimeoutExpired:
        return [], "pdftotext timeout (25s)"
    except Exception as e:
        return [], str(e)
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", errors="replace").strip()
        return [], err or f"pdftotext exit {proc.returncode}"
    txt = proc.stdout.decode("utf-8", errors="replace")
    lines = txt.splitlines()
    return lines, None


def maybe_term(term: str) -> bool:
    t = norm_term(term)
    if len(t) < 2 or len(t) > 140:
        return False
    if t.lower() in {"the", "and", "or", "this", "that", "where", "with", "from", "to", "for", "in"}:
        return False
    has_upper = any(c.isupper() for c in t)
    has_symbol = bool(SYMBOL_HINT.search(t))
    acronym = bool(re.fullmatch(r"[A-Z]{2,8}", t))
    return has_upper or has_symbol or acronym


def clean_defn(s: str) -> str:
    x = s.strip()
    x = re.sub(r"\s+", " ", x)
    return x[:600]


def extract_from_lines(path: Path, kind: str, lines: List[str], heading_seed: str | None = None):
    hs = headings_from_lines(lines) if kind == "md" else []
    defs: List[Defn] = []
    candidates: List[Mention] = []
    eqs: List[Mention] = []
    syms: List[Mention] = []
    protocols: List[Mention] = []
    metrics: List[Mention] = []

    max_elems = 9000
    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        heading = heading_at(i, hs) if hs else (heading_seed or "(pdf)")

        # Candidate terms from headings
        if kind == "md":
            hm = HEADING_RE.match(line)
            if hm:
                ht = hm.group(2).strip()
                if maybe_term(ht):
                    candidates.append(Mention(ht, rel(path), heading, i, i))

        # Bold-style definition
        m = BOLD_DEF_RE.match(line)
        if m:
            term, d = norm_term(m.group(1)), clean_defn(m.group(2))
            if maybe_term(term) and d:
                defs.append(Defn(term, d, rel(path), heading, i, i))
                candidates.append(Mention(term, rel(path), heading, i, i))

        # Plain explicit definition
        m2 = PLAIN_DEF_RE.match(line)
        if m2:
            term = norm_term(m2.group(1))
            verb = m2.group(2)
            tail = clean_defn(m2.group(3))
            if maybe_term(term) and tail:
                defs.append(Defn(term, f"{verb} {tail}", rel(path), heading, i, i))
                candidates.append(Mention(term, rel(path), heading, i, i))

        # Symbol specific definitions
        sm = SYMBOL_DEF_RE.match(line)
        if sm:
            term, d = norm_term(sm.group(1)), clean_defn(sm.group(2))
            if d:
                defs.append(Defn(term, d, rel(path), heading, i, i))
                candidates.append(Mention(term, rel(path), heading, i, i))
                if len(syms) < max_elems:
                    syms.append(Mention(term + " : " + d, rel(path), heading, i, i))

        # Candidate emphasized terms and code terms
        for tm in TOKEN_RE.finditer(line):
            t = norm_term(tm.group(1) or tm.group(2) or "")
            if maybe_term(t):
                candidates.append(Mention(t, rel(path), heading, i, i))

        # Equations
        if EQUATION_HINT.search(line) and ("$" in line or "equation" in line.lower() or "=" in line):
            if len(eqs) < max_elems:
                eqs.append(Mention(line.strip()[:500], rel(path), heading, i, i))

        # Symbols
        if SYMBOL_HINT.search(line):
            if len(syms) < max_elems:
                syms.append(Mention(line.strip()[:500], rel(path), heading, i, i))

        # Protocols / vows / laws
        low = line.lower()
        if any(k in low for k in ["protocol", "vow", "law", "clause", "safeguard", "ethic"]):
            if line.strip():
                if len(protocols) < max_elems:
                    protocols.append(Mention(line.strip()[:500], rel(path), heading, i, i))

        # Metrics / diagnostics
        if any(k in low for k in ["metric", "metrics", "diagnostic", "diagnostics", "rg", "rs", "pd", "eg", "tf"]):
            if line.strip():
                if len(metrics) < max_elems:
                    metrics.append(Mention(line.strip()[:500], rel(path), heading, i, i))

    return defs, candidates, eqs, syms, protocols, metrics


def md_entry(term: str, body: str) -> str:
    return f"## {term}\n\n{body}\n"


def render_sources(ms: List[Mention], limit: int = 3) -> str:
    out = []
    for m in ms[:limit]:
        out.append(f"- `{m.path}` | heading: `{m.heading}` | lines: {m.start}-{m.end}")
    return "\n".join(out) if out else "- (none)"


def write_split(base_path: Path, content: str, size_limit: int = MAX_FILE) -> List[Path]:
    base_path.parent.mkdir(parents=True, exist_ok=True)
    data = content.encode("utf-8")
    if len(data) <= size_limit:
        base_path.write_text(content, encoding="utf-8")
        return [base_path]

    header = ""
    body = content
    if content.startswith("#"):
        split_idx = content.find("\n\n")
        if split_idx != -1:
            header = content[: split_idx + 2]
            body = content[split_idx + 2 :]

    # Prefer splitting by glossary-style entries, fallback to lines.
    if "\n## " in body:
        raw_chunks = body.split("\n## ")
        units = [raw_chunks[0]] + ["## " + ch for ch in raw_chunks[1:]]
    else:
        units = body.splitlines(keepends=True)

    written: List[Path] = []
    idx = 1
    cur = header

    def next_name(n: int) -> Path:
        if n == 1:
            return base_path
        return base_path.with_name(f"{base_path.stem}_{n}{base_path.suffix}")

    for unit in units:
        candidate = cur + unit
        if len(candidate.encode("utf-8")) <= size_limit:
            cur = candidate
            continue

        # Flush current chunk if it has non-header content.
        if cur.strip() and cur.strip() != header.strip():
            p = next_name(idx)
            p.write_text(cur, encoding="utf-8")
            written.append(p)
            idx += 1
            cur = header

        # If a single unit is too large, split by lines.
        if len((header + unit).encode("utf-8")) > size_limit:
            line_buf = header
            for ln in unit.splitlines(keepends=True):
                if len((line_buf + ln).encode("utf-8")) > size_limit and line_buf.strip() != header.strip():
                    p = next_name(idx)
                    p.write_text(line_buf, encoding="utf-8")
                    written.append(p)
                    idx += 1
                    line_buf = header
                line_buf += ln
            cur = line_buf
        else:
            cur = header + unit

    if cur.strip() and cur.strip() != header.strip():
        p = next_name(idx)
        p.write_text(cur, encoding="utf-8")
        written.append(p)
    return written


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sources, md_count, picked_pdf_count = pick_sources()

    all_defs: List[Defn] = []
    all_candidates: List[Mention] = []
    all_eqs: List[Mention] = []
    all_syms: List[Mention] = []
    all_protocols: List[Mention] = []
    all_metrics: List[Mention] = []
    pdf_fail: List[Tuple[str, str]] = []

    for s in sources:
        if s.kind == "md":
            try:
                lines = s.path.read_text(encoding="utf-8", errors="replace").splitlines()
            except Exception as e:
                pdf_fail.append((rel(s.path), f"read error: {e}"))
                continue
            defs, cands, eqs, syms, protocols, metrics = extract_from_lines(s.path, "md", lines)
        else:
            lines, err = extract_pdf_text(s.path)
            if err is not None:
                pdf_fail.append((rel(s.path), err))
                continue
            heading_seed = first_nonempty(lines)
            defs, cands, eqs, syms, protocols, metrics = extract_from_lines(s.path, "pdf", lines, heading_seed)

        all_defs.extend(defs)
        all_candidates.extend(cands)
        all_eqs.extend(eqs)
        all_syms.extend(syms)
        all_protocols.extend(protocols)
        all_metrics.extend(metrics)

    # Consolidate definitions by term
    by_term: Dict[str, List[Defn]] = defaultdict(list)
    for d in all_defs:
        t = norm_term(d.term)
        by_term[t].append(d)

    # Candidate mentions by normalized key
    mentions_by_key: Dict[str, List[Mention]] = defaultdict(list)
    display_term_by_key: Dict[str, str] = {}
    for m in all_candidates:
        t = norm_term(m.term)
        k = key_term(t)
        if not k:
            continue
        mentions_by_key[k].append(m)
        display_term_by_key.setdefault(k, t)

    def_key_map = defaultdict(list)
    for t, ds in by_term.items():
        k = key_term(t)
        if k:
            def_key_map[k].extend(ds)

    # Build glossary entries
    glossary_entries = []
    needs_entries = []
    collisions = []

    # First explicit definitions
    for t in sorted(by_term.keys(), key=lambda x: x.lower()):
        ds = by_term[t]
        uniq_defs = []
        seen = set()
        for d in ds:
            kd = d.definition.strip().lower()
            if kd not in seen:
                seen.add(kd)
                uniq_defs.append(d)

        body_parts = []
        for d in uniq_defs[:5]:
            body_parts.append(f"- Definition: {d.definition}")
            body_parts.append(f"  - Source: `{d.path}` | heading: `{d.heading}` | lines: {d.start}-{d.end}")

        if len(uniq_defs) > 1:
            collisions.append((t, uniq_defs))

        glossary_entries.append((t, md_entry(t, "\n".join(body_parts))))

    # Then unresolved candidates with enough signal
    for k, mentions in mentions_by_key.items():
        if k in def_key_map:
            continue
        if len(mentions) < 3:
            continue
        term = display_term_by_key[k]
        top = sorted(mentions, key=lambda m: m.path)[:3]
        body = "\n".join(
            [
                "- Definition: NEEDS_DEFINITION (no explicit definition pattern found in selected sources)",
                "- Top sources:",
                render_sources(top, limit=3),
            ]
        )
        needs_entries.append((term, md_entry(term, body)))

    # Merge for master glossary
    all_master = glossary_entries + needs_entries
    all_master.sort(key=lambda x: x[0].lower())

    buckets = {
        "A-F": [],
        "G-L": [],
        "M-R": [],
        "S-Z": [],
    }
    for term, entry in all_master:
        c = term[:1].upper() if term else ""
        if "A" <= c <= "F":
            buckets["A-F"].append(entry)
        elif "G" <= c <= "L":
            buckets["G-L"].append(entry)
        elif "M" <= c <= "R":
            buckets["M-R"].append(entry)
        elif "S" <= c <= "Z":
            buckets["S-Z"].append(entry)

    written_files = []

    for name in ["A-F", "G-L", "M-R", "S-Z"]:
        header = (
            f"# HC IX Master Glossary {name}\n\n"
            f"Generated from `docs/**/*.md` plus selected `docs/**/*.pdf` (only when no sibling `.md` shares stem).\n"
        )
        content = header + "\n".join(buckets[name])
        if not buckets[name]:
            content += "\n_No entries in this range._\n"
        out = write_split(OUT_DIR / f"HCIX_Master_Glossary_{name}.md", content)
        written_files.extend(out)

    # TOC
    toc_lines = [
        "# HC IX Master Glossary TOC",
        "",
        "## Generated Artifacts",
    ]

    # Symbols
    sym_header = "# HC IX Symbols\n\n"
    sym_items = []
    for m in all_syms[:4000]:
        sym_items.append(f"- {m.term}\n  - Source: `{m.path}` | heading: `{m.heading}` | lines: {m.start}-{m.end}")
    sym_content = sym_header + ("\n".join(sym_items) if sym_items else "_No symbol lines extracted._\n")
    sym_out = write_split(OUT_DIR / "HCIX_Symbols.md", sym_content)
    written_files.extend(sym_out)

    # Equations
    eq_header = "# HC IX Equations\n\n"
    eq_items = []
    for m in all_eqs[:4000]:
        eq_items.append(f"- {m.term}\n  - Source: `{m.path}` | heading: `{m.heading}` | lines: {m.start}-{m.end}")
    eq_content = eq_header + ("\n".join(eq_items) if eq_items else "_No equation lines extracted._\n")
    eq_out = write_split(OUT_DIR / "HCIX_Equations.md", eq_content)
    written_files.extend(eq_out)

    # Protocols/Vows/Laws
    p_header = "# HC IX Protocols Vows Laws\n\n"
    p_items = []
    for m in all_protocols[:4000]:
        p_items.append(f"- {m.term}\n  - Source: `{m.path}` | heading: `{m.heading}` | lines: {m.start}-{m.end}")
    p_content = p_header + ("\n".join(p_items) if p_items else "_No protocol/vow/law lines extracted._\n")
    p_out = write_split(OUT_DIR / "HCIX_Protocols_Vows_Laws.md", p_content)
    written_files.extend(p_out)

    # Metrics Diagnostics
    m_header = "# HC IX Metrics Diagnostics\n\n"
    m_items = []
    for m in all_metrics[:4000]:
        m_items.append(f"- {m.term}\n  - Source: `{m.path}` | heading: `{m.heading}` | lines: {m.start}-{m.end}")
    m_content = m_header + ("\n".join(m_items) if m_items else "_No metrics/diagnostics lines extracted._\n")
    m_out = write_split(OUT_DIR / "HCIX_Metrics_Diagnostics.md", m_content)
    written_files.extend(m_out)

    # Collisions
    c_header = "# HC IX Collisions\n\n"
    c_items = []
    for term, defs in collisions:
        c_items.append(f"## {term}")
        for d in defs[:8]:
            c_items.append(f"- {d.definition}")
            c_items.append(f"  - Source: `{d.path}` | heading: `{d.heading}` | lines: {d.start}-{d.end}")
        c_items.append("")
    c_content = c_header + ("\n".join(c_items) if c_items else "_No definition collisions found._\n")
    c_out = write_split(OUT_DIR / "HCIX_Collisions.md", c_content)
    written_files.extend(c_out)

    # Needs definition
    n_header = "# HC IX Needs Definition\n\n"
    n_content = n_header + ("\n".join([e for _, e in needs_entries]) if needs_entries else "_No unresolved terms above threshold._\n")
    n_out = write_split(OUT_DIR / "HCIX_Needs_Definition.md", n_content)
    written_files.extend(n_out)

    # PDF fail
    f_header = "# HC IX PDF Fail\n\n"
    if pdf_fail:
        f_body = "\n".join([f"- `{p}` | error: {e}" for p, e in pdf_fail])
    else:
        f_body = "_No PDF extraction failures._"
    f_content = f_header + f_body + "\n"
    f_out = write_split(OUT_DIR / "HCIX_PDF_Fail.md", f_content)
    written_files.extend(f_out)

    # TOC finalization
    toc_lines.extend([f"- `{p.name}`" for p in sorted(written_files, key=lambda x: x.name)])
    toc_lines.extend(
        [
            "",
            "## Totals",
            f"- Concepts (explicit definitions): {len(glossary_entries)}",
            f"- NEEDS_DEFINITION concepts: {len(needs_entries)}",
            f"- Collisions: {len(collisions)}",
            f"- MD sources scanned: {md_count}",
            f"- PDF sources scanned (fallback only): {picked_pdf_count}",
            f"- PDF failures: {len(pdf_fail)}",
        ]
    )
    toc_content = "\n".join(toc_lines) + "\n"
    toc_out = write_split(OUT_DIR / "HCIX_Master_Glossary_TOC.md", toc_content)
    written_files.extend(toc_out)

    # Run summary
    summary = "\n".join(
        [
            "HCIX Run Summary",
            f"DONE | concepts={len(glossary_entries)} collisions={len(collisions)} gaps={len(needs_entries)} md={md_count} pdf={picked_pdf_count} pdf_fail={len(pdf_fail)}",
            f"output_dir={rel(OUT_DIR)}",
        ]
    ) + "\n"
    (OUT_DIR / "HCIX_Run_Summary.txt").write_text(summary, encoding="utf-8")

    # Tarball
    tar_path = ROOT / "_export_hcix" / "HCIX_outputs.tar.gz"
    tar_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(OUT_DIR, arcname="_export_hcix/hcix_export")

    print(summary.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
