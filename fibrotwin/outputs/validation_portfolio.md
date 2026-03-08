# Validation Portfolio

Checks passed: 5/5

## Scenario outcomes
- baseline_low_load_low_signal: c=8.059, p=0.386, myo=0.925, ac_align_x=0.904
- high_load_only: c=8.804, p=0.416, myo=0.975, ac_align_x=0.914
- high_signal_only: c=10.513, p=0.523, myo=1.000, ac_align_x=0.902
- high_load_high_signal: c=10.667, p=0.545, myo=1.000, ac_align_x=0.912
- infarct_high_load_high_signal: c=10.643, p=0.545, myo=1.000, ac_align_x=0.913

## Checks
- [PASS] high_signal_only has higher profibrotic signal than baseline
- [PASS] high_signal_only has higher myofibroblast fraction than baseline
- [PASS] high_load_only increases fibre alignment vs baseline
- [PASS] high_load_high_signal yields highest collagen among non-infarct scenarios
- [PASS] infarct core collagen exceeds non-infarct high_load_high_signal global collagen