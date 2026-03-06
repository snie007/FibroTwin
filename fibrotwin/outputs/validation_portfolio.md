# Validation Portfolio

Checks passed: 5/5

## Scenario outcomes
- baseline_low_load_low_signal: c=3.856, p=0.234, myo=0.000, ac_align_x=0.904
- high_load_only: c=8.589, p=0.308, myo=0.800, ac_align_x=0.913
- high_signal_only: c=12.259, p=0.732, myo=1.000, ac_align_x=0.901
- high_load_high_signal: c=12.377, p=0.742, myo=1.000, ac_align_x=0.912
- infarct_high_load_high_signal: c=12.446, p=0.747, myo=1.000, ac_align_x=0.916

## Checks
- [PASS] high_signal_only has higher profibrotic signal than baseline
- [PASS] high_signal_only has higher myofibroblast fraction than baseline
- [PASS] high_load_only increases fibre alignment vs baseline
- [PASS] high_load_high_signal yields highest collagen among non-infarct scenarios
- [PASS] infarct condition increases collagen vs non-infarct high_load_high_signal