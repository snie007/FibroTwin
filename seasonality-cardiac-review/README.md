# Seasonality in Cardiac Imaging Review

This repository is being assembled to support a systematic review and analysis plan for seasonal effects in cardiac size, shape, and function, with emphasis on cardiac MRI and transferable statistical methods.

## Objectives

1. Systematic review of seasonality in heart size, shape, and function from any modality.
2. Systematic review of classical and modern statistical methods for detecting seasonality.
3. Practical analysis plan for testing seasonality in a cardiac MRI dataset with ~1000 scans acquired at irregular times across three years.
4. Overleaf-ready manuscript and supporting tables/figures.

## Planned structure

- `papers/pdfs/` downloaded PDFs, renamed sensibly
- `metadata/` paper tables and extraction sheets
- `notes/` summaries and synthesis notes
- `search/` search strategies, screening logs, PRISMA-style flow counts
- `overleaf/` LaTeX manuscript scaffold
- `scripts/` helper scripts for metadata and figures

## Current status

The repository now contains:
- a curated cardiac seasonality evidence table (`metadata/review_a_extraction.csv`)
- a curated seasonality methods table (`metadata/review_b_methods.csv`)
- a screening log and PRISMA-style count summary (`search/`)
- automatically retrieved open-access PDFs where available (`papers/pdfs/`)
- a PDF access manifest (`papers/review_a_extraction_pdf_manifest.csv`)
- narrative summaries and an MRI analysis plan (`notes/`)
- an Overleaf-ready manuscript scaffold and upload zip (`overleaf/`, `overleaf_project.zip`)
- a Python example for phenotype-level seasonality modeling (`scripts/example_seasonality_model.py`)

Remaining limitation:
- many included papers are not open access through Europe PMC, so the PDF repository is currently partial rather than complete.
