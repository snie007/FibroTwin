# Initial statistical strategy for cardiac MRI seasonality

## Core recommendation
Use phenotype-level regression rather than raw-image-only testing as the primary analysis.

For each imaging-derived phenotype (for example LV end-diastolic volume, LV mass, ejection fraction, strain, atrial volume, RV measures, wall thickness, shape PCA scores):

1. Convert scan date to day-of-year.
2. Fit a model with annual cyclic terms:
   - sin(2*pi*day_of_year/365.25)
   - cos(2*pi*day_of_year/365.25)
3. Adjust for confounders:
   - age
   - sex
   - body size (height, weight, BSA)
   - blood pressure if available
   - scanner/site/protocol
   - acquisition year
   - possible ethnicity and comorbidity covariates
4. If repeated measures exist, use mixed effects with participant random intercept.
5. Test the joint null that both sine and cosine coefficients are zero.
6. Report amplitude and phase of peak seasonal effect with confidence intervals.

## Why this is a good primary test
- Works with irregular sampling times.
- Uses all observations directly.
- Handles multiple years.
- Gives interpretable amplitude and timing.
- Extends naturally to covariate adjustment.

## Important sensitivity analyses
- Cyclic GAM on day-of-year.
- Month-as-factor model.
- Permutation test that shuffles day-of-year within year strata.
- Replace calendar terms with ambient temperature, daylight duration, or photoperiod if available.
- Exclude holidays or unusual acquisition clusters.

## Cautions
- If acquisition timing is operationally biased by season, confounding is a major risk.
- Raw image appearance can vary seasonally because of protocol or staffing changes rather than biology.
- With many phenotypes, control FDR.
- If there are latent image features, reduce dimension first, then test leading components and validate out of sample.
