# VESPA methodology notes

## Repository purpose
VESPA is a long-lived evidence library for grant projects. Each project can have multiple dossiers, each with its own search log, evidence extraction file, and report outputs.

## Working rules
- Log every database query before screening.
- Record exact PMID-backed quantitative claims when possible.
- Keep raw exports immutable in `data/raw/`.
- Normalize reviewed evidence into `data/processed/` once screened.
- Draft report outputs from curated evidence only.

## Step-by-step workflow
1. Define the dossier question.
2. Run and log searches.
3. Screen results.
4. Extract quantitative evidence with PMIDs.
5. Draft Overleaf and/or web outputs.
6. Review and update the library.
