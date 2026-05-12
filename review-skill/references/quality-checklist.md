# Quality Assessment Checklist for Included Studies

Use this checklist to grade the methodological quality and risk of bias for each included study. Grade as: **Strong**, **Moderate**, or **Weak**.

## Criteria for Grading

### Strong Evidence

- [ ] Methods clearly described and reproducible
- [ ] Appropriate study design for research question
- [ ] Large or well-defined sample
- [ ] Results validated prospectively or in multiple cohorts
- [ ] Clinical deployment or regulatory approval (FDA, CE mark, etc.)
- [ ] Limitations honestly acknowledged and addressed
- [ ] Peer-reviewed publication in recognized venue
- [ ] No major conflicts of interest or bias indicators

### Moderate Evidence

- [ ] Methods described but some gaps in detail
- [ ] Reasonable study design, but not ideal
- [ ] Moderate sample size or mixed validation approaches
- [ ] Retrospective validation only
- [ ] Limited generalizability acknowledged
- [ ] Published in peer-reviewed venue
- [ ] Some limitations not fully addressed

### Weak Evidence

- [ ] Methods poorly described; hard to reproduce
- [ ] Small sample size or poor design choice
- [ ] No independent validation (single-author, single-center)
- [ ] Preprint or gray literature with no peer review
- [ ] Major limitations not acknowledged
- [ ] Claimed results exceed what data support
- [ ] Potential conflicts of interest

## Domain-Specific Quality Criteria

### For Mechanistic (Physics-Based) Models

- [ ] Underlying equations justified by biological principles
- [ ] Parameter values sourced from literature or measurement
- [ ] Sensitivity analysis conducted (which parameters affect output?)
- [ ] Model predictions validated against independent data
- [ ] Uncertainty quantification included
- [ ] Code/model availability for reproducibility

### For Data-Driven (ML) Models

- [ ] Training/test split properly separated (not leaking)
- [ ] Hyperparameter tuning described and not overfitted
- [ ] Cross-validation or hold-out test set used
- [ ] Multiple metrics reported (accuracy, sensitivity, specificity, AUC, etc.)
- [ ] Baseline comparisons included
- [ ] Feature importance or interpretability addressed
- [ ] External validation on independent cohort

### For Hybrid Models

- [ ] Both mechanistic and ML components clearly described
- [ ] How they integrate explained (physics as constraint, loss term, etc.)
- [ ] Advantages over pure mechanistic or pure ML demonstrated
- [ ] Validation combines both approaches

### For Clinical Translation

- [ ] Patient-specific personalization method described
- [ ] Prospective validation on real patients (not just retrospective)
- [ ] Clinical workflow integration explained
- [ ] Safety/liability framework addressed
- [ ] Regulatory pathway clear (if applicable)
- [ ] Deployed in actual clinical setting (not just research)

## Bias Risk Assessment

Rate each bias category as: Low / Unclear / High

| Bias Type | Risk Level | Justification |
|-----------|-----------|---------------|
| Selection bias (sample not representative) | | |
| Measurement bias (how data collected/processed) | | |
| Reporting bias (cherry-picking positive results) | | |
| Conflict of interest | | |
| Generalizability (results apply beyond original population?) | | |

## Final Quality Grade

Based on the above criteria, assign an overall grade:

- **Strong**: Methodologically rigorous; results reliable for synthesis
- **Moderate**: Some limitations but overall reasonable; use with context
- **Weak**: Significant concerns; report separately or exclude if criteria warrant

---

## Notes for Evidence Table

When documenting this study in the evidence table, note:
- Which quality criteria drove the overall grade
- Any limitations that affect interpretation (e.g., "Small sample, single center")
- Whether findings are contradicted by other studies
- Whether this is primary evidence or supporting evidence
