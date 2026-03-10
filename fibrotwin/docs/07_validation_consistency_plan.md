# Validation Page Consistency Plan

## Goal
Create one coherent visual language across all validation artifacts (portfolio, numerical tests, calibration checks, per-study test cards, and emulation waves).

## Design system (single source of truth)
- Shared stylesheet: `site/assets/css/validation_theme.css`
- Standard blocks on every test detail page:
  1. **Standard test summary** (what is tested, domain, status)
  2. **Simulation setup** (BC/inputs/protocol)
  3. **Common visualization** (single focal image/plot)
  4. **Interpretation / pass analysis**
  5. **Back to validation**
- Common status badges (`PASS`/`FAIL`) and card hierarchy.

## Scope covered
- PMID-linked study test pages (`pages/tests/T001..T080.html`)
- Numerical verification detail pages (`pages/numerical_tests/*`)
- Calibration detail pages (`pages/calibration/*`)
- Validation landing sections and emulation sections.

## Content standards for every test
- What model mechanism is tested (not paper-title-only label)
- Which simulator scenario/protocol was used
- Main expected behavior and observed model outcome
- Evidence anchor (PMID or analytic reference)
- Pass/fail interpretation in one short paragraph

## QC checklist
- [ ] Every test page has all five standard blocks
- [ ] Every test has one primary visualization with consistent framing
- [ ] All status labels use shared badge style
- [ ] No unformatted raw lists when a table/card representation is intended
- [ ] New sections added in future reuse `validation_theme.css` classes

## Future-edit rule
When adding or editing validation content, use the shared style classes and keep the same block order to preserve coherence.
