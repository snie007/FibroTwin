# Sensitivity + Emulation Diagnosis

- Training points: 18
- Candidate points screened (emulator): 260
- Best emulator: GaussianProcessRBF
- Best verified pass count: 3/6

## Top parameter sensitivities (Spearman vs objective)
- signaling_network.d_smad: rho=0.707
- cells.myo_switch_threshold: rho=0.633
- signaling_network.k_at1r_erk: rho=0.432
- infarct.dispersion_border: rho=0.342
- signaling_network.d_erk: rho=0.302
- infarct.signal_source: rho=-0.282
- cells.myo_switch_softness: rho=-0.150
- signaling_network.k_tgfr_smad: rho=-0.104

## Diagnosis
- Top objective-sensitive parameters: signaling_network.d_smad, cells.myo_switch_threshold, signaling_network.k_at1r_erk
- Current parameter space did not produce high calibration fit; likely structural/model-form limitation.
- Paper-anchored quantitative agreement remains low; missing pathway/detail complexity is a major contributor.

## Suggested model extensions
- Extend signaling modules with explicit VEGF/Notch/HIF axis where literature anchors are abundant.
- Introduce zone-specific infarct signaling/deposition kernels (core/border/remote separate kinetics).
- Separate phenotype activation vs matrix deposition coupling to reduce over-coupled tradeoffs.
- Use multi-wave history matching with adaptive bounds around top sensitive parameters only.