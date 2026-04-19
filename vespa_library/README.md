# VESPA Literature Library

VESPA is a reusable literature and search library for grant-writing and
evidence synthesis. It is organised **by grant project** so that each
proposal has a traceable paper trail of queries, sources, and extracted
statistics — while the underlying corpus and processed records can be
re-used across projects.

## What this repo is

- A long-lived **evidence repository**: raw search exports, processed
  records, and a reviewed pool of citations.
- A **search log** for every database query, so reviewers can reproduce
  what was run, when, and why papers were included or excluded.
- A place to draft **grant-facing reports** (LaTeX / Overleaf) backed
  by PMID-indexed evidence entries.
- A tiny **static site** (`site/`) that indexes the dossiers produced
  from the library.

## Layout

```
vespa_library/
├── README.md                      # this file
├── data/
│   ├── raw/                       # untouched exports: PubMed .nbib, CSVs, PDFs
│   └── processed/                 # normalised evidence entries (JSON/YAML)
├── searches/
│   └── VESPA/
│       └── chd_usa_2026/          # first dossier: CHD USA statistics, 2026
│           ├── search_log.md
│           └── evidence_template.yaml
├── reports/
│   └── overleaf/
│       └── main.tex               # LaTeX starter for the CHD USA report
├── site/
│   └── index.html                 # landing page for the library
├── scripts/                       # helpers (fetchers, formatters)
└── docs/                          # methodology, conventions, change notes
```

## Conventions

- **One folder per grant project** under `searches/<project>/<dossier>/`.
- Every evidence entry carries a **PMID** (or a DOI + justification if
  no PMID exists). See `searches/VESPA/chd_usa_2026/evidence_template.yaml`.
- Every query is logged in `search_log.md` with database, date, exact
  query string, hit counts, and inclusion notes.
- Raw exports go in `data/raw/` read-only; cleaned records go in
  `data/processed/`.

## First dossier

`searches/VESPA/chd_usa_2026/` — congenital heart disease (CHD)
statistics for the United States, backing the report at
`reports/overleaf/main.tex`.
