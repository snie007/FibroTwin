# History Matching Quick Guide for FibroTwin

This project uses AutoEmulate as a surrogate model to accelerate calibration.

## Prompt template to run
"Run emulation history matching with N=<n_train> simulator runs, M=<n_candidates> emulator candidate points, and report NROY bounds + best plausible parameter set with target pass count."

## Evaluation criteria
- Emulator quality: R2/RMSE on held-out points.
- Plausibility: size and stability of NROY region.
- Ground truth: full simulator confirms selected NROY points.
- Success condition: a candidate set passing all 6 calibration tasks in simulator checks.