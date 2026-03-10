# Calibration Cards

Pass: 5/6

## Failed-test action plan
- C006 infarct_core_to_remote_ratio: Increase core-specific signaling/deposition while reducing remote spillover (diffusion/decay tuning).

## Execution plan (next tuning cycle)
1. **C001 myofibro_fraction_high_signal**: reduce over-activation first (switch threshold/slope tuning), rerun high_signal_only.
2. **C002 profibrotic_index_high_signal**: increase signaling strength after C001 correction by tuning receptor-to-node gains and selected decay constants.
3. **C006 infarct_core_to_remote_ratio**: increase infarct spatial contrast by boosting core source terms and reducing remote spillover (diffusion/decay).
4. Re-run full validation portfolio + calibration cards and accept only if all three checks enter target bands.