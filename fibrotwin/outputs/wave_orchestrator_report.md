# Wave Orchestrator Report

## Pipeline steps
- `/home/snie007/Documents/project/2026/freeze_combined_out7/.venv/bin/python -m src.tools.extract_quantitative_evidence` -> code 0
- `/home/snie007/Documents/project/2026/freeze_combined_out7/.venv/bin/python -m src.tools.quantitative_match_metric` -> code 0
- `emulation_waves.main(n_waves=4,n_train=24,n_candidates=300)` -> code 0
- `sensitivity_analysis.main(n_train=18,n_candidates=260,n_verify=10)` -> code 0

## Diagnosis
- Calibration targets pass: 6/6
- Paper-anchored quantitative match: PASS 2, PARTIAL 8, FAIL 39, UNMAPPED 2
- History matching wave pass trend: [5, 5, 3, 4]
- NROY fraction trend: [1.0, 1.0, 0.993, 1.0]

## Fail taxonomy
- parameter_miss: 37
- observation_mismatch: 10
- missing_mechanism_or_unmapped: 2

## Suggested next actions
- Add observation-model mapping layer (paper endpoint -> model observable transform) to reduce observation mismatch fails.
- Expand signaling complexity: VEGF/Notch/HIF modules for angiogenesis-related studies.
- Refine infarct zone kinetics (core/border/remote separate source/decay kernels).
- Constrain tuning to top sensitive parameters and re-run waves with narrowed bounds.