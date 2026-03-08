# Validation Card

Pass rate: 4/5 (0.80)

- VC01 [FAIL] Profibrotic signaling increase under high biochemical stimulus
  - Scenario: high_signal_only
  - Model: 0.5233303308486938
  - Experimental band: 0.65 .. 0.95
  - PMID hint: 27017945
- VC02 [PASS] Myofibroblast fraction elevated under profibrotic signaling
  - Scenario: high_signal_only
  - Model: 1.0
  - Experimental band: 0.55 .. 1.0
  - PMID hint: 26608708
- VC03 [PASS] Collagen/fibre alignment increases with mechanical loading
  - Scenario: high_load_only
  - Model: 0.9136166572570801
  - Experimental band: 0.75 .. 1.0
  - PMID hint: 22495588
- VC04 [PASS] Infarct core collagen exceeds remote/global non-infarct load+signal case
  - Scenario: infarct_high_load_high_signal
  - Model: 19.21731948852539
  - Experimental band: 10.0 .. 200.0
  - PMID hint: 7855157
- VC05 [PASS] Load+signal combined produces high collagen burden
  - Scenario: high_load_high_signal
  - Model: 10.667165756225586
  - Experimental band: 5.0 .. 120.0
  - PMID hint: 26608708