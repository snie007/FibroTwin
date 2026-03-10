# Emulation QC Checklist

- [ ] Training design covers full parameter ranges (no collapsed dimensions).
- [ ] Emulator holdout metrics acceptable (R2 not strongly negative across outputs).
- [ ] NROY fraction decreases across waves (or justified if not).
- [ ] At least 10 NROY points re-evaluated in full simulator and compared to emulator.
- [ ] Best candidate verified against all 6 calibration targets using full simulator.
- [ ] Parameter bounds for next wave generated from NROY with modest buffer (5-10%).