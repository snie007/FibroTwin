#!/usr/bin/env python3
"""
build_tables_and_bibliography.py

Reproducible build script for the BHF AI Challenge literature package.

Inputs (all under data/):
  - intermediate/ai_ecg_candidates.json
  - intermediate/ai_cmr_candidates.json
  - intermediate/llm_cv_ai_clinic_candidates.json
  - intermediate/curated_extensions.json
  - evidence.json   (PMID-bearing items merged into the master corpus)

Outputs:
  - refs/references.bib                         (BibTeX, unique citation keys)
  - data/master_citations.json                  (canonical record per citation)
  - data/tables/citation_index.csv              (flat index)
  - data/tables/ai_ecg_top50.{csv,md,tex}
  - data/tables/ai_cmr_table.{csv,md,tex}
  - data/tables/ai_clinic_trials_table.{csv,md,tex}

Dedupe order:  PMID > DOI (lowercased) > normalized title.
"""

from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
INTERMEDIATE = DATA / "intermediate"
TABLES = DATA / "tables"
REFS = ROOT / "refs"

# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------

_WS = re.compile(r"\s+")
_PUNCT = re.compile(r"[^a-z0-9]+")


def norm_title(t: str | None) -> str:
    if not t:
        return ""
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = _PUNCT.sub(" ", t)
    return _WS.sub(" ", t).strip()


def norm_doi(d: str | None) -> str | None:
    if not d:
        return None
    d = d.strip().lower()
    d = d.replace("https://doi.org/", "").replace("http://doi.org/", "")
    return d or None


def norm_pmid(p) -> str | None:
    if p is None:
        return None
    s = str(p).strip()
    return s if s.isdigit() else None


def slugify(s: str, maxlen: int = 24) -> str:
    s = norm_title(s)
    s = s.replace(" ", "")
    return s[:maxlen]


def safe_text(s: str | None) -> str:
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", str(s)).strip()
    s = s.replace(" ", " ").replace("\r", " ").replace("\n", " ")
    return _WS.sub(" ", s)


def latex_escape(s: str | None) -> str:
    if s is None:
        return ""
    s = safe_text(s)
    out = []
    for ch in s:
        if ch == "\\":
            out.append(r"\textbackslash{}")
        elif ch in "&%$#_{}":
            out.append("\\" + ch)
        elif ch == "~":
            out.append(r"\textasciitilde{}")
        elif ch == "^":
            out.append(r"\textasciicircum{}")
        elif ch == "<":
            out.append(r"\textless{}")
        elif ch == ">":
            out.append(r"\textgreater{}")
        else:
            out.append(ch)
    return "".join(out)


def md_escape(s: str | None) -> str:
    if s is None:
        return ""
    s = safe_text(s)
    return s.replace("|", "\\|")


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_json(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_ecg() -> list[dict]:
    rows = load_json(INTERMEDIATE / "ai_ecg_candidates.json")
    out = []
    for r in rows:
        out.append({
            "title": r.get("title"),
            "year": r.get("year"),
            "pmid": norm_pmid(r.get("pmid")),
            "doi": norm_doi(r.get("doi")),
            "url": r.get("source_url"),
            "venue": None,
            "authors_short": None,
            "study_type": r.get("study_type"),
            "modality": r.get("modality"),
            "condition": r.get("condition"),
            "task": None,
            "domain": None,
            "setting": None,
            "cohort_n": r.get("cohort_n"),
            "outcomes_summary": r.get("outcomes_summary"),
            "validation_status": r.get("trial_status_or_validation"),
            "harvest_bucket": r.get("harvest_bucket"),
            "topic_tags": ["ai_ecg"],
            "source_origin": "ai_ecg_candidates",
            "suggested_citation_key": r.get("suggested_citation_key"),
        })
    return out


def load_cmr() -> list[dict]:
    rows = load_json(INTERMEDIATE / "ai_cmr_candidates.json")
    out = []
    for r in rows:
        out.append({
            "title": r.get("title"),
            "year": r.get("year"),
            "pmid": norm_pmid(r.get("pmid")),
            "doi": norm_doi(r.get("doi")),
            "url": None,
            "venue": None,
            "authors_short": None,
            "study_type": r.get("study_type"),
            "modality": "CMR",
            "condition": r.get("disease_area"),
            "task": r.get("task"),
            "domain": None,
            "setting": None,
            "cohort_n": r.get("cohort_n"),
            "outcomes_summary": r.get("outcomes_summary"),
            "validation_status": r.get("validation_or_trial_status"),
            "harvest_bucket": "AI-CMR",
            "topic_tags": ["ai_cmr"],
            "source_origin": "ai_cmr_candidates",
            "suggested_citation_key": r.get("suggested_citation_key"),
        })
    return out


def load_clinic() -> list[dict]:
    rows = load_json(INTERMEDIATE / "llm_cv_ai_clinic_candidates.json")
    out = []
    for r in rows:
        out.append({
            "title": r.get("title"),
            "year": r.get("year"),
            "pmid": norm_pmid(r.get("pmid")),
            "doi": norm_doi(r.get("doi")),
            "url": None,
            "venue": None,
            "authors_short": None,
            "study_type": r.get("study_type"),
            "modality": None,
            "condition": None,
            "task": None,
            "domain": r.get("domain"),
            "setting": r.get("setting"),
            "cohort_n": r.get("cohort_n"),
            "outcomes_summary": r.get("outcomes_summary"),
            "validation_status": r.get("trial_status"),
            "harvest_bucket": "LLM/AI-clinic",
            "topic_tags": ["ai_clinic"],
            "source_origin": "llm_cv_ai_clinic_candidates",
            "suggested_citation_key": r.get("suggested_citation_key"),
        })
    return out


def load_extensions() -> list[dict]:
    rows = load_json(INTERMEDIATE / "curated_extensions.json")
    out = []
    for r in rows:
        out.append({
            "title": r.get("title"),
            "year": r.get("year"),
            "pmid": norm_pmid(r.get("pmid")),
            "doi": norm_doi(r.get("doi")),
            "url": r.get("url"),
            "venue": r.get("venue"),
            "authors_short": r.get("authors_short"),
            "study_type": r.get("study_type"),
            "modality": None,
            "condition": None,
            "task": None,
            "domain": None,
            "setting": None,
            "cohort_n": None,
            "outcomes_summary": r.get("outcomes_summary"),
            "validation_status": None,
            "harvest_bucket": "curated_extension",
            "topic_tags": r.get("topic_tags", []),
            "source_origin": "curated_extensions",
            "suggested_citation_key": r.get("suggested_citation_key"),
        })
    return out


def load_evidence() -> list[dict]:
    """Pull PMID-bearing rows from existing evidence.json so the broader corpus benefits."""
    rows = load_json(DATA / "evidence.json")
    out = []
    for r in rows:
        pmid = norm_pmid(r.get("pmid"))
        if not pmid:
            continue  # skip non-PMID evidence (already covered as policy/commercial in extensions)
        out.append({
            "title": r.get("title"),
            "year": r.get("year"),
            "pmid": pmid,
            "doi": norm_doi(r.get("doi")) if r.get("doi") else None,
            "url": r.get("url"),
            "venue": None,
            "authors_short": None,
            "study_type": r.get("type"),
            "modality": None,
            "condition": None,
            "task": None,
            "domain": None,
            "setting": None,
            "cohort_n": None,
            "outcomes_summary": r.get("summary"),
            "validation_status": None,
            "harvest_bucket": "evidence_json",
            "topic_tags": (r.get("domains") or []) + (r.get("perspectives") or []),
            "source_origin": "evidence.json",
            "suggested_citation_key": None,
        })
    return out


# ---------------------------------------------------------------------------
# Dedupe + master assembly
# ---------------------------------------------------------------------------

def merge_record(into: dict, src: dict) -> None:
    """Fill empty fields of `into` with values from `src` and union list fields."""
    for k, v in src.items():
        if v in (None, "", [], {}):
            continue
        cur = into.get(k)
        if cur in (None, "", [], {}):
            into[k] = v
        elif isinstance(cur, list) and isinstance(v, list):
            into[k] = sorted(set(cur) | set(v))


def dedupe(records: list[dict]) -> list[dict]:
    """Dedupe in PMID > DOI > normalized title order."""
    by_pmid: dict[str, dict] = {}
    by_doi: dict[str, dict] = {}
    by_title: dict[str, dict] = {}
    out: list[dict] = []

    for r in records:
        pmid = r.get("pmid")
        doi = r.get("doi")
        nt = norm_title(r.get("title"))

        target = None
        if pmid and pmid in by_pmid:
            target = by_pmid[pmid]
        elif doi and doi in by_doi:
            target = by_doi[doi]
        elif nt and nt in by_title:
            target = by_title[nt]

        if target is None:
            r = dict(r)  # shallow copy
            out.append(r)
            if pmid:
                by_pmid[pmid] = r
            if doi:
                by_doi[doi] = r
            if nt:
                by_title[nt] = r
        else:
            merge_record(target, r)
            # update side indexes for any newly-known identifiers
            if r.get("pmid") and r["pmid"] not in by_pmid:
                by_pmid[r["pmid"]] = target
            if r.get("doi") and r["doi"] not in by_doi:
                by_doi[r["doi"]] = target
    return out


# ---------------------------------------------------------------------------
# Citation key generation (stable, unique)
# ---------------------------------------------------------------------------

_KEY_RE = re.compile(r"[^A-Za-z0-9]+")


def _author_token(rec: dict) -> str:
    s = rec.get("authors_short") or ""
    s = s.split(" et al")[0].split(",")[0]
    s = s.split(";")[0]
    s = s.strip()
    if s:
        s = s.split()[0]
    s = _KEY_RE.sub("", s).lower()
    return s


def _title_token(rec: dict) -> str:
    """Pick first content word of >3 chars, skipping common stopwords."""
    skip = {
        "the","an","and","for","with","from","using","into","onto","over","under",
        "via","of","on","in","to","by","at","as","is","are","be","or","not","new",
        "study","trial","review","analysis","based","artificial","intelligence",
        "machine","learning","deep","model","models","cardiac","cardiovascular",
        "ai","ml","large","language",
    }
    title = norm_title(rec.get("title") or "")
    for w in title.split():
        if len(w) > 3 and w not in skip:
            return w
    for w in title.split():
        if len(w) > 2:
            return w
    return "ref"


def _make_base_key(rec: dict) -> str:
    """Deterministic candidate key from author/year/title token."""
    auth = _author_token(rec)
    if not auth:
        # try suggested_citation_key as starter
        sug = rec.get("suggested_citation_key") or ""
        sug_l = re.sub(r"\d+$", "", sug)
        sug_l = re.sub(r"\d+", "", sug_l).strip("_")
        sug_l = re.sub(r"[^A-Za-z]", "", sug_l).lower()
        if sug_l:
            auth = sug_l[:14]
    if not auth:
        # fallback: first content word of title
        auth = _title_token(rec)[:14]
    yr = str(rec.get("year") or "nd")
    tok = _title_token(rec)
    base = f"{auth}{yr}{tok}"
    base = _KEY_RE.sub("", base)
    if not base:
        base = "ref"
    if not base[0].isalpha():
        base = "x" + base
    return base[:48]


def assign_citation_keys(records: list[dict]) -> None:
    used: set[str] = set()
    for r in records:
        base = _make_base_key(r)
        key = base
        i = 2
        while key in used:
            key = f"{base}{chr(ord('a') + i - 2)}" if i <= 26 else f"{base}{i}"
            i += 1
        used.add(key)
        r["citation_key"] = key


# ---------------------------------------------------------------------------
# BibTeX generation
# ---------------------------------------------------------------------------

def _tex_value(s: str) -> str:
    """Escape value for use inside a BibTeX field. Curly-protect title casing."""
    if s is None:
        return ""
    s = safe_text(s)
    s = s.replace("\\", "\\textbackslash{}")
    for ch in "&%$#_":
        s = s.replace(ch, "\\" + ch)
    s = s.replace("{", "\\{").replace("}", "\\}")
    return s


def bibtex_entry(rec: dict) -> str:
    pmid = rec.get("pmid")
    doi = rec.get("doi")
    url = rec.get("url")
    title = _tex_value(rec.get("title") or "")
    year = rec.get("year")
    venue = rec.get("venue")
    authors = rec.get("authors_short")
    key = rec["citation_key"]

    is_article = bool(pmid or doi)
    entry_type = "article" if is_article else "misc"

    fields: list[tuple[str, str]] = []
    if authors:
        fields.append(("author", _tex_value(authors)))
    fields.append(("title", "{" + title + "}"))
    if year is not None:
        fields.append(("year", str(year)))
    if venue:
        if entry_type == "article":
            fields.append(("journal", _tex_value(venue)))
        else:
            fields.append(("howpublished", _tex_value(venue)))
    if doi:
        fields.append(("doi", _tex_value(doi)))
    if pmid:
        fields.append(("note", f"PMID: {pmid}"))
    if url and not pmid:
        fields.append(("url", _tex_value(url)))

    body = ",\n  ".join(f"{k} = {{{v}}}" if not v.startswith("{") else f"{k} = {v}"
                       for k, v in fields)
    return f"@{entry_type}{{{key},\n  {body}\n}}"


def write_bib(records: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "% references.bib - generated by build_tables_and_bibliography.py\n"
        "% Do not edit by hand. Re-run the build script to refresh.\n\n"
    )
    sorted_recs = sorted(records, key=lambda r: r["citation_key"])
    with path.open("w", encoding="utf-8") as f:
        f.write(header)
        for r in sorted_recs:
            f.write(bibtex_entry(r))
            f.write("\n\n")


# ---------------------------------------------------------------------------
# Master citation JSON + flat index
# ---------------------------------------------------------------------------

def write_master_citations(records: list[dict], path: Path) -> None:
    out = []
    for r in sorted(records, key=lambda x: x["citation_key"]):
        out.append({
            "citation_key": r["citation_key"],
            "title": r.get("title"),
            "year": r.get("year"),
            "pmid": r.get("pmid"),
            "doi": r.get("doi"),
            "url": r.get("url"),
            "venue": r.get("venue"),
            "authors_short": r.get("authors_short"),
            "source_type": r.get("study_type") or r.get("harvest_bucket"),
            "topic_tags": r.get("topic_tags") or [],
            "harvest_bucket": r.get("harvest_bucket"),
            "source_origin": r.get("source_origin"),
            "outcomes_summary": r.get("outcomes_summary"),
            "validation_status": r.get("validation_status"),
            "modality": r.get("modality"),
            "condition": r.get("condition"),
            "task": r.get("task"),
            "domain": r.get("domain"),
            "setting": r.get("setting"),
            "cohort_n": r.get("cohort_n"),
            "bibtex": bibtex_entry(r),
        })
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)


def write_citation_index_csv(records: list[dict], path: Path) -> None:
    cols = [
        "citation_key", "title", "year", "pmid", "doi", "source_type",
        "topic_tags", "harvest_bucket", "source_origin", "venue",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in sorted(records, key=lambda x: x["citation_key"]):
            w.writerow([
                r["citation_key"],
                safe_text(r.get("title")),
                r.get("year") or "",
                r.get("pmid") or "",
                r.get("doi") or "",
                safe_text(r.get("study_type") or r.get("harvest_bucket")),
                ";".join(sorted(r.get("topic_tags") or [])),
                safe_text(r.get("harvest_bucket")),
                safe_text(r.get("source_origin")),
                safe_text(r.get("venue")),
            ])


# ---------------------------------------------------------------------------
# Evidence tables
# ---------------------------------------------------------------------------

ECG_PRIORITY_BUCKETS = [
    "Atrial fibrillation detection and prediction",
    "LV systolic dysfunction and heart failure",
    "Structural heart disease, cardiomyopathy, and ischemia",
    "Implementation, deployment, and enabling methods",
    "Reviews, methods, and reporting quality",
    "Commercial and real-world deployment signals",
]


def truncate(s: str | None, n: int) -> str:
    s = safe_text(s)
    if len(s) <= n:
        return s
    return s[: n - 1].rstrip() + "…"


def _study_priority(rec: dict) -> int:
    """Lower is more important for top50 selection."""
    st = (rec.get("study_type") or "").lower()
    val = (rec.get("validation_status") or "").lower()
    if "rct" in st or "randomized" in st or "pragmatic" in st:
        return 0
    if "external" in val or "external" in st or "multicenter" in val or "multicentre" in val:
        return 1
    if "prospective" in st or "real-world" in val or "deployment" in val:
        return 2
    if "validation" in val or "validation" in st:
        return 3
    if "model development" in st or "derivation" in st or "cohort" in st:
        return 4
    if "review" in st or "scoping" in st or "systematic" in st or "meta" in st:
        return 5
    return 6


def select_ecg_top50(all_records: list[dict]) -> list[dict]:
    ecg = [r for r in all_records if "ai_ecg" in (r.get("topic_tags") or [])
           or (r.get("source_origin") == "ai_ecg_candidates")
           or "ECG" in (r.get("modality") or "")]
    # Drop pure commercial product cards and pure narrative reviews when we have enough.
    primary = [r for r in ecg if r.get("harvest_bucket") != "Commercial and real-world deployment signals"]
    commercial = [r for r in ecg if r.get("harvest_bucket") == "Commercial and real-world deployment signals"]

    def sort_key(r):
        bucket = r.get("harvest_bucket") or ""
        try:
            bidx = ECG_PRIORITY_BUCKETS.index(bucket)
        except ValueError:
            bidx = len(ECG_PRIORITY_BUCKETS)
        return (_study_priority(r), bidx, -(int(r.get("year") or 0)), r.get("title") or "")

    primary.sort(key=sort_key)
    commercial.sort(key=sort_key)

    target = 50
    com_take = min(len(commercial), 3)
    prim_take = target - com_take
    chosen = primary[:prim_take] + commercial[:com_take]
    if len(chosen) < target:
        chosen = chosen + primary[prim_take:prim_take + (target - len(chosen))]
    return chosen[:target]


def select_cmr(all_records: list[dict]) -> list[dict]:
    cmr = [r for r in all_records if "ai_cmr" in (r.get("topic_tags") or [])
           or (r.get("source_origin") == "ai_cmr_candidates")
           or (r.get("modality") or "").upper() == "CMR"]
    cmr.sort(key=lambda r: (_study_priority(r), -(int(r.get("year") or 0)), r.get("title") or ""))
    return cmr


def select_ai_clinic(all_records: list[dict]) -> list[dict]:
    keep_origins = {"llm_cv_ai_clinic_candidates"}
    keep_tags = {"ai_clinic", "llm", "implementation", "ai_deployment", "policy", "regulation"}
    rows = []
    for r in all_records:
        if r.get("source_origin") in keep_origins:
            rows.append(r); continue
        if any(t in (r.get("topic_tags") or []) for t in keep_tags):
            rows.append(r); continue
    # Stable sort: trial/RCT > implementation > registry > review
    def k(r):
        st = (r.get("study_type") or "").lower()
        val = (r.get("validation_status") or "").lower()
        if "rct" in st or "randomized" in st or "pragmatic" in st:
            p = 0
        elif "trial" in st or "trial" in val.lower() or "recruit" in val:
            p = 1
        elif "registry" in st or "ongoing" in val or "not_yet" in val:
            p = 2
        elif "implementation" in st or "deployment" in val or "real-world" in val:
            p = 3
        elif "external" in val or "external" in st:
            p = 4
        else:
            p = 5
        return (p, -(int(r.get("year") or 0)), r.get("title") or "")
    rows.sort(key=k)
    return rows


# ---------------------------------------------------------------------------
# Table writers
# ---------------------------------------------------------------------------

def _write_table(rows, columns, headers, csv_path, md_path, tex_path,
                 caption: str, label: str, tex_colspec: str,
                 truncate_map: dict[str, int] | None = None):
    truncate_map = truncate_map or {}
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    # CSV
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        for r in rows:
            w.writerow([safe_text(r.get(c, "")) for c in columns])

    # Markdown
    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# {caption}\n\n")
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("|" + "|".join(["---"] * len(headers)) + "|\n")
        for r in rows:
            cells = []
            for c in columns:
                val = r.get(c, "")
                if c in truncate_map:
                    val = truncate(val, truncate_map[c])
                cells.append(md_escape(val))
            f.write("| " + " | ".join(cells) + " |\n")

    # LaTeX
    with tex_path.open("w", encoding="utf-8") as f:
        f.write("% Generated by build_tables_and_bibliography.py - do not edit\n")
        f.write("\\begin{table}[ht]\n\\centering\n\\small\n")
        f.write(f"\\caption{{{latex_escape(caption)}}}\n")
        f.write(f"\\label{{tab:{label}}}\n")
        f.write(f"\\begin{{tabular}}{{{tex_colspec}}}\n\\hline\n")
        f.write(" & ".join(latex_escape(h) for h in headers) + " \\\\\n\\hline\n")
        for r in rows:
            cells = []
            for c in columns:
                val = r.get(c, "")
                if c in truncate_map:
                    val = truncate(val, truncate_map[c])
                cells.append(latex_escape(val))
            f.write(" & ".join(cells) + " \\\\\n")
        f.write("\\hline\n\\end{tabular}\n\\end{table}\n")


def _row_for_ecg(r: dict) -> dict:
    return {
        "citation_key": r.get("citation_key", ""),
        "year": r.get("year") or "",
        "study_type": r.get("study_type") or "",
        "modality": r.get("modality") or "",
        "condition": r.get("condition") or "",
        "cohort_n": r.get("cohort_n") or "",
        "outcomes_summary": r.get("outcomes_summary") or "",
        "validation_status": r.get("validation_status") or "",
        "pmid": r.get("pmid") or "",
        "title": r.get("title") or "",
    }


def _row_for_cmr(r: dict) -> dict:
    return {
        "citation_key": r.get("citation_key", ""),
        "year": r.get("year") or "",
        "study_type": r.get("study_type") or "",
        "task": r.get("task") or "",
        "condition": r.get("condition") or "",
        "cohort_n": r.get("cohort_n") or "",
        "outcomes_summary": r.get("outcomes_summary") or "",
        "validation_status": r.get("validation_status") or "",
        "pmid": r.get("pmid") or "",
        "title": r.get("title") or "",
    }


def _row_for_clinic(r: dict) -> dict:
    return {
        "citation_key": r.get("citation_key", ""),
        "year": r.get("year") or "",
        "study_type": r.get("study_type") or "",
        "domain": r.get("domain") or "",
        "setting": r.get("setting") or r.get("condition") or "",
        "cohort_n": r.get("cohort_n") or "",
        "outcomes_summary": r.get("outcomes_summary") or "",
        "validation_status": r.get("validation_status") or "",
        "pmid": r.get("pmid") or "",
        "title": r.get("title") or "",
    }


def write_ecg_top50(rows, base):
    rows = [_row_for_ecg(r) for r in rows]
    _write_table(
        rows,
        columns=["citation_key", "year", "study_type", "modality", "condition",
                 "cohort_n", "outcomes_summary", "validation_status", "pmid"],
        headers=["Key", "Year", "Study type", "Modality", "Condition/use",
                 "Cohort n", "Outcome summary", "Validation/deployment", "PMID"],
        csv_path=base.with_suffix(".csv"),
        md_path=base.with_suffix(".md"),
        tex_path=base.with_suffix(".tex"),
        caption="Top 50 AI-ECG studies prioritised by trial design, external validation, and deployment relevance.",
        label="ai_ecg_top50",
        tex_colspec="lrp{2.6cm}p{2.0cm}p{2.4cm}p{1.6cm}p{4.5cm}p{2.4cm}r",
        truncate_map={"outcomes_summary": 220, "validation_status": 90,
                      "condition": 70, "modality": 50},
    )


def write_cmr(rows, base):
    rows = [_row_for_cmr(r) for r in rows]
    _write_table(
        rows,
        columns=["citation_key", "year", "study_type", "task", "condition",
                 "cohort_n", "outcomes_summary", "validation_status", "pmid"],
        headers=["Key", "Year", "Study type", "Task", "Disease area",
                 "Cohort n", "Outcome summary", "Validation status", "PMID"],
        csv_path=base.with_suffix(".csv"),
        md_path=base.with_suffix(".md"),
        tex_path=base.with_suffix(".tex"),
        caption="AI-CMR evidence: segmentation, diagnosis, scar/fibrosis, outcomes, workflow, and multicentre validation.",
        label="ai_cmr_table",
        tex_colspec="lrp{2.6cm}p{3.0cm}p{2.4cm}p{1.6cm}p{4.0cm}p{2.4cm}r",
        truncate_map={"outcomes_summary": 220, "task": 90, "condition": 60,
                      "validation_status": 90},
    )


def write_clinic(rows, base):
    rows = [_row_for_clinic(r) for r in rows]
    _write_table(
        rows,
        columns=["citation_key", "year", "study_type", "domain", "setting",
                 "cohort_n", "outcomes_summary", "validation_status", "pmid"],
        headers=["Key", "Year", "Study type", "Domain", "Setting/cohort",
                 "Cohort n", "Outcome summary", "Trial/deployment status", "PMID"],
        csv_path=base.with_suffix(".csv"),
        md_path=base.with_suffix(".md"),
        tex_path=base.with_suffix(".tex"),
        caption="AI-in-the-clinic evidence: completed and ongoing trials, registry studies, LLM workflow studies, and concrete workflow-deployment papers.",
        label="ai_clinic_trials",
        tex_colspec="lrp{2.6cm}p{2.4cm}p{3.0cm}p{1.6cm}p{4.0cm}p{2.4cm}r",
        truncate_map={"outcomes_summary": 220, "setting": 90, "domain": 60,
                      "validation_status": 60},
    )


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def main() -> int:
    ecg = load_ecg()
    cmr = load_cmr()
    clinic = load_clinic()
    ext = load_extensions()
    ev = load_evidence()

    raw_total = len(ecg) + len(cmr) + len(clinic) + len(ext) + len(ev)

    merged = dedupe(ecg + cmr + clinic + ext + ev)
    assign_citation_keys(merged)

    write_master_citations(merged, DATA / "master_citations.json")
    write_citation_index_csv(merged, TABLES / "citation_index.csv")
    write_bib(merged, REFS / "references.bib")

    ecg_top = select_ecg_top50(merged)
    write_ecg_top50(ecg_top, TABLES / "ai_ecg_top50")

    cmr_rows = select_cmr(merged)
    write_cmr(cmr_rows, TABLES / "ai_cmr_table")

    clinic_rows = select_ai_clinic(merged)
    write_clinic(clinic_rows, TABLES / "ai_clinic_trials_table")

    print(f"raw input rows : {raw_total}")
    print(f"unique citations: {len(merged)}")
    print(f"ai_ecg_top50    : {len(ecg_top)}")
    print(f"ai_cmr_table    : {len(cmr_rows)}")
    print(f"ai_clinic_table : {len(clinic_rows)}")
    print("outputs written under:")
    for p in [
        DATA / "master_citations.json",
        TABLES / "citation_index.csv",
        REFS / "references.bib",
        TABLES / "ai_ecg_top50.csv",
        TABLES / "ai_ecg_top50.md",
        TABLES / "ai_ecg_top50.tex",
        TABLES / "ai_cmr_table.csv",
        TABLES / "ai_cmr_table.md",
        TABLES / "ai_cmr_table.tex",
        TABLES / "ai_clinic_trials_table.csv",
        TABLES / "ai_clinic_trials_table.md",
        TABLES / "ai_clinic_trials_table.tex",
    ]:
        print("  -", p.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
