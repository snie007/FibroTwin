# Validation Portfolio

Checks passed: 2/4

## Scenario outcomes
- baseline_low_load_low_signal: c=2.664, p=0.234, myo=0.013, ac_align_x=0.904
- high_load_only: c=5.809, p=0.308, myo=0.812, ac_align_x=0.903
- high_signal_only: c=8.429, p=0.732, myo=1.000, ac_align_x=0.900
- high_load_high_signal: c=8.371, p=0.742, myo=1.000, ac_align_x=0.900

## Checks
- [PASS] high_signal_only has higher profibrotic signal than baseline
- [PASS] high_signal_only has higher myofibroblast fraction than baseline
- [FAIL] high_load_only increases fibre alignment vs baseline
- [FAIL] high_load_high_signal yields highest collagen among scenarios