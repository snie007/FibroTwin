# Review B summary: statistical methods for seasonality

## Best primary analysis for the MRI dataset

For each derived cardiac phenotype, fit a regression model with annual cyclic terms:

- sin(2*pi*day_of_year/365.25)
- cos(2*pi*day_of_year/365.25)

Then test the joint null that both coefficients are zero.

## Why this is the best primary choice

- Works naturally with **irregular acquisition dates**.
- Uses all observations directly without forcing monthly aggregation.
- Handles **multiple years** easily.
- Allows standard covariate adjustment.
- Produces interpretable **amplitude** and **phase**.
- Extends naturally to mixed-effects models if repeated measures or center effects exist.

## Recommended covariates

- age
- sex
- height / weight / body surface area
- year of acquisition
- scanner / site / protocol
- blood pressure and heart rate if available
- comorbidity burden if relevant

## Recommended sensitivity analyses

1. **Cyclic GAM** on day-of-year for non-sinusoidal shape.
2. **Month-as-factor** model for simple categorical seasonality.
3. **Permutation test** shuffling day-of-year within year strata.
4. Replace calendar terms with **temperature**, **daylight duration**, or **photoperiod** if location/date data exist.
5. For high-dimensional shape features, reduce dimension first, then test principal components or latent embeddings.

## What not to use as the main method

- Seasonal ARIMA on individual-level irregular MRI dates.
- STL decomposition on raw subject-level data.
- Pure periodogram methods as the only inferential analysis.
- Black-box machine learning without interpretable seasonal contrasts.

## Best method shortlist

### Primary
- Harmonic regression / cosinor-style regression

### Sensitivity
- GAM with cyclic smooths
- Mixed-effects harmonic models
- Permutation inference

### Exploratory only
- Lomb-Scargle periodogram
- Wavelet analysis
- STL decomposition on aggregated monthly summaries
