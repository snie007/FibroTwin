# Validation Portfolio

Checks passed: 4/4

## Scenario outcomes
- baseline_low_load_low_signal: c=2.669, p=0.234, myo=0.013, ac_align_x=0.906
- high_load_only: c=5.851, p=0.307, myo=0.812, ac_align_x=0.915
- high_signal_only: c=8.439, p=0.732, myo=1.000, ac_align_x=0.902
- high_load_high_signal: c=8.452, p=0.742, myo=1.000, ac_align_x=0.912

## Checks
- [PASS] high_signal_only has higher profibrotic signal than baseline
- [PASS] high_signal_only has higher myofibroblast fraction than baseline
- [PASS] high_load_only increases fibre alignment vs baseline
- [PASS] high_load_high_signal yields highest collagen among scenarios