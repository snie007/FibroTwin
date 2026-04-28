# Review plan

## Review A: Seasonality of cardiac size, shape, and function

### Question
What evidence exists for seasonal variation in cardiac structure or function in humans, across cardiac MRI, echocardiography, CT, nuclear imaging, ECG-derived phenotypes, or related physiological measures?

### Target outputs
- 20 to 30 papers
- Search log
- Screening log
- Extraction table
- Narrative synthesis

### Initial inclusion priorities
- Human studies
- Cardiac size, shape, mass, volumes, function, strain, remodeling, physiology closely tied to imaging
- Explicit seasonal, monthly, circannual, photoperiod, temperature-linked, or time-of-year analyses

### Likely exclusions
- Pure weather-event studies without seasonal analysis
- Non-cardiac outcomes
- Animal-only studies unless methodologically important

## Review B: Statistical methods for seasonality

### Question
Which statistical methods are most appropriate for testing seasonality in irregularly timed cardiac MRI-derived phenotypes collected across about three years?

### Target outputs
- 20 to 30 method references
- Method comparison table
- Recommended primary and sensitivity analyses

### Method classes to evaluate
- Harmonic regression / cosinor models
- Generalized additive models with cyclic smooths
- Circular statistics / tests
- Mixed-effects seasonal models
- Time-series decomposition / spectral methods
- Wavelets and modern machine learning approaches
- Permutation / resampling approaches for irregular sampling

## Cardiac MRI analysis problem
Data described by user: ~1000 images, random times during the year, spread across three years.

### Immediate design assumptions
- Outcome will be derived image phenotypes, not raw pixels alone
- Observation times are irregular
- Need adjustment for confounders: age, sex, body size, scanner/site, acquisition year, possibly temperature and daylight
- Multiple outcomes likely, so false-discovery control or multivariate shrinkage may be needed

### Candidate primary analysis
For each phenotype, fit a regression with a cyclic annual term:
- sine(day_of_year), cosine(day_of_year)
- year effect
- demographic and technical covariates
- mixed effects if repeated scans or center effects exist

### Sensitivity analyses
- cyclic GAM on day-of-year
- month factor model
- permutation test preserving year distribution
- temperature/daylight substitution if geolocation and dates are available
