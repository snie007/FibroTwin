# BHF AI challenge review workspace

This folder contains an expanded literature, policy, and market-review scaffold for the BHF Cardiovascular Grand Challenge AI theme, built from the preliminary abstract supplied in Slack plus public sources.

## Contents

- `data/evidence.json` - structured evidence records with PMIDs, quotes, hard numbers, tags, URLs, and local source-copy paths
- `docs/raw/webpages/` - downloaded copies of cited webpages, including policy pages and commercial AI-ECG product pages
- `docs/raw/pdfs/` - downloaded PDFs for the BHF call and related guideline material
- `docs/raw/publications/` - downloaded PubMed source pages for cited publications
- `notes/literature_review.md` - expanded review with:
  - broader studies on this kind of programme
  - AI-ECG academic review
  - AI-ECG commercial offering review
  - LLM-for-procedures review
  - tightened five-perspective synthesis
- `notes/background_tightened_for_overleaf.md` - compact paste-ready background section
- `notes/bhf_tailoring_notes.md` - BHF call-specific positioning notes
- `notes/reviewer_1_clinical_methodology_red_team.md` - aggressive reviewer checklist
- `notes/reviewer_2_implementation_policy_red_team.md` - aggressive reviewer checklist
- `notes/source_inventory.md` - inventory of locally saved source files
- `web/` - searchable local webpage and knowledge graph assets
- `scripts/` - build helpers

## Source note

The Overleaf project itself was not directly readable from this environment during collection, so the review was produced from:

- the preliminary abstract text provided in Slack
- public BHF challenge materials
- public policy and guideline webpages
- PubMed-indexed literature
- official commercial AI-ECG product pages

## Current positioning recommendation

The strongest framing is:

- one *generalizable decision platform*
- three exemplar cardiovascular decisions: intervention, surveillance, follow-up
- AI-ECG as a scalable *input and phenotyping layer*
- LLMs only as a *supervised communication and workflow layer*

## Next useful steps

1. convert the tightened review into Overleaf-ready background prose or LaTeX
2. decide exactly how much AI-ECG should appear in the main narrative versus a supporting paragraph
3. keep LLM claims narrow and explicitly non-autonomous
4. manually re-check key hard numbers against the saved PubMed and webpage copies before submission
5. add named datasets, sites, and implementation milestones directly into the outline application
