# Emulation + History Matching Report

- Training runs: 24
- Candidate points screened by emulator: 600
- Best emulator: GaussianProcessMatern32
- NROY count: 600 (100.0%)

## Best plausible candidate (checked in full simulator)
- Targets passed: 3/6
- myofibro_fraction_high_signal: 0.9375 vs [0.6, 0.9] -> FAIL
- profibrotic_index_high_signal: 0.5459 vs [0.65, 0.95] -> FAIL
- alignment_high_load: 0.9171 vs [0.78, 0.98] -> PASS
- collagen_fraction_load_signal: 10.4446 vs [8.0, 20.0] -> PASS
- infarct_core_collagen: 13.5540 vs [12.0, 60.0] -> PASS
- infarct_core_to_remote_ratio: 1.2914 vs [1.5, 6.0] -> FAIL

## Plausible parameter-space bounds (NROY envelope)
- signaling_network.k_tgfr_smad: [0.4005, 2.595]
- signaling_network.k_at1r_erk: [0.32, 2.08]
- signaling_network.d_smad: [0.03042, 1.569]
- signaling_network.d_erk: [0.03671, 1.564]
- cells.myo_switch_threshold: [0.05445, 0.8456]
- cells.myo_switch_softness: [0.009757, 0.1503]
- cells.myo_cap: [0.3982, 1.365]
- infarct.collagen_source: [0.003624, 0.05636]
- infarct.signal_source: [0.03742, 0.5635]
- infarct.dispersion_core: [0.04243, 0.6543]
- infarct.dispersion_border: [0.06752, 1.03]
- infarct.dispersion_remote: [0.09168, 1.402]

## History matching usage guidance
1. Start with broad physically credible parameter bounds and a small training design (20-40).
2. Fit emulator and inspect predictive quality (R2/RMSE). If poor, add design points.
3. Define observations as target means + uncertainty variances from literature bands.
4. Compute implausibility and NROY region; do not trust single-wave NROY blindly.
5. Iterate waves: sample within NROY, run simulator, refit emulator, shrink bounds.
6. QC at each wave: emulator accuracy on holdout, NROY fraction trend, and simulator re-check of selected NROY points.