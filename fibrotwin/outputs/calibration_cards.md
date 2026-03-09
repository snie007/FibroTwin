# Calibration Cards

Pass: 3/6

## Failed-test action plan
- C001 myofibro_fraction_high_signal: Activation is too high; reduce phenotype switching sensitivity (myo_switch_threshold up, k_switch down) and/or reduce TGFR->SMAD gain.
- C002 profibrotic_index_high_signal: Increase receptor-to-signaling gains (k_tgfr_smad, k_at1r_erk) or reduce signaling decay (d_smad/d_erk).
- C006 infarct_core_to_remote_ratio: Increase core-specific signaling/deposition while reducing remote spillover (diffusion/decay tuning).

## Execution plan (next tuning cycle)
1. **C001 myofibro_fraction_high_signal**: reduce over-activation first (switch threshold/slope tuning), rerun high_signal_only.
2. **C002 profibrotic_index_high_signal**: increase signaling strength after C001 correction by tuning receptor-to-node gains and selected decay constants.
3. **C006 infarct_core_to_remote_ratio**: increase infarct spatial contrast by boosting core source terms and reducing remote spillover (diffusion/decay).
4. Re-run full validation portfolio + calibration cards and accept only if all three checks enter target bands.