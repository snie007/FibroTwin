# 05 — Validation Gap Review (Literature-guided)

## What is already strong
- Mechanosensitive alignment behavior under loading.
- Signal-driven fibroblast activation trends.
- Infarct-region enhanced remodeling behavior.
- Coupled multiscale interactions reproducibly tested.

## Gaps still needing improvement
1. **Unit calibration gap**
   - Many outputs are nondimensional; direct comparison to measured units (kPa, collagen fraction, cell density) remains partial.
2. **Cytokine realism gap**
   - Current cytokine module is reduced-order diffusion/decay; does not yet include receptor occupancy and downstream kinetics by ligand.
3. **Scar architecture realism**
   - Collagen represented as field cohorts; no explicit fiber bundle topology or crosslink chemistry.
4. **Cell heterogeneity gap**
   - Fibroblasts currently represented by one agent class + phenotype switch; true subtype diversity is not yet modeled.
5. **Clinical validation gap**
   - No direct patient-specific calibration/validation dataset integrated.

## Priority improvements
1. Add unit-anchored calibration datasets and parameter inference workflow.
2. Extend signaling ODE network to receptor-level modules (TGFβR/AT1R proxy states).
3. Add scar microstructure descriptors (alignment dispersion, crosslink maturity index).
4. Include fibroblast subtype mixture and transition pathways.
5. Add prospective benchmark dashboard against published longitudinal datasets.

## Literature anchors (examples)
- Fibroblast signaling and context dependence: PMID 27017945, 26608708.
- Mechanoregulated infarct remodeling: PMID 22495588.
- Growth/remodeling review context and MI remodeling: PMC4851715, PMC7855157.
