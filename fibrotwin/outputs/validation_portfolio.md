# Validation Portfolio

Checks passed: 7/8

## Scenario outcomes
- baseline_low_load_low_signal: c=8.219, p=0.364, myo=0.913, ac_align_x=0.910
- high_load_only: c=8.798, p=0.399, myo=0.950, ac_align_x=0.917
- high_signal_only: c=10.323, p=0.460, myo=0.975, ac_align_x=0.911
- high_load_high_signal: c=10.309, p=0.485, myo=1.000, ac_align_x=0.917
- infarct_high_load_high_signal: c=10.358, p=0.485, myo=1.000, ac_align_x=0.918
- drug_tgfr_block: c=9.810, p=0.426, myo=0.988, ac_align_x=0.917
- drug_at1r_block: c=10.137, p=0.447, myo=0.988, ac_align_x=0.917
- drug_dual_block: c=9.406, p=0.386, myo=0.938, ac_align_x=0.917

## Checks
- [PASS] high_signal_only has higher profibrotic signal than baseline
- [PASS] high_signal_only has higher myofibroblast fraction than baseline
- [PASS] high_load_only increases fibre alignment vs baseline
- [FAIL] high_load_high_signal yields highest collagen among non-infarct baseline/mech/signal scenarios
- [PASS] infarct core collagen exceeds non-infarct high_load_high_signal global collagen
- [PASS] TGFβR blockade reduces profibrotic signal vs high_load_high_signal
- [PASS] AT1R blockade reduces collagen vs high_load_high_signal
- [PASS] Dual blockade gives strongest suppression (collagen) among drug scenarios