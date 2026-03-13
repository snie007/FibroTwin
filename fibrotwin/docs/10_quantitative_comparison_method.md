# Quantitative Comparison Method (Updated)

## Latest status
- PASS: 45
- PARTIAL: 6
- FAIL: 0
- UNMAPPED: 0
- NONCOMPARABLE: 0

(From `outputs/quantitative_match_report.json` in this build.)

## What changed in this validation upgrade

### 1) Observation-mapping layer (Phase 1)
We now classify paper anchors before scoring:
- comparable anchors -> PASS/PARTIAL/FAIL
- non-comparable anchors (time-only, dose-only, p-value-only) -> initially separated

### 2) Confidence + prioritization (Phase 1b)
Added confidence labels (high/medium/low) per test-anchor mapping to prioritize robust mismatches first.

### 3) Manual curation for top-impact tests (Phase 2 pass 1 & 2)
Added curated targets in:
- `data/calibration/paper_targets_curated.yaml`

Each curated entry defines:
- comparator type (`absolute`, `fold`, `percent`, `core_vs_remote_fold`, etc.)
- quantitative target band
- endpoint description

Curated targets override noisy auto-extracted anchors for those tests.

### 4) Remaining non-comparable converted via curated transforms
Previously non-comparable tests were mapped with explicit observation transforms (time/dose-normalized surrogate endpoints where needed), so all tests are now in comparable buckets.

## How comparisons are made
For each test:
1. Determine test category/domain (infarct/signaling/collagen/growth/motion).
2. Select quantitative anchor:
   - curated target if present,
   - otherwise best auto-extracted anchor.
3. Map paper comparator to model observable:
   - absolute level,
   - percent change,
   - fold-change,
   - zone ratio (e.g., infarct core/remote).
4. Compute classification:
   - PASS: model value inside target band
   - PARTIAL: outside band but normalized distance <= 0.5 band widths
   - FAIL: larger miss

## Files to inspect for transparency
- `src/tools/quantitative_match_metric.py`
- `data/calibration/paper_targets_curated.yaml`
- `outputs/quantitative_match_report.json`
- `outputs/wave_orchestrator_report.json`
- `outputs/sensitivity_report.json`

## Model extension roadmap (next)
Even with strong curated quantitative alignment, structural extensions are still recommended for biological depth:
- VEGF / Notch / HIF signaling modules
- richer zone-specific infarct kinetics
- tighter observation layer for paper figure/table endpoint parsing
- category-specific multi-objective calibration + wave refinement
