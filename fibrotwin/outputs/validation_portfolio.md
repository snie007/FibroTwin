# Validation Portfolio

Checks passed: 8/8

## Scenario outcomes (interpretable summary)

| Scenario | What was simulated | Main takeaway | Key endpoints |
|---|---|---|---|
| baseline_low_load_low_signal | Low mechanical stretch + low TGFβ/AngII baseline tissue remodeling. | Reference baseline profile. | collagen=8.20; p=0.535; myofibro=0.800; align=0.911 |
| high_load_only | Increased mechanical loading with low biochemical signaling. | Mechanical loading primarily increases alignment. | collagen=8.68; p=0.563; myofibro=0.875; align=0.917 |
| high_signal_only | High biochemical signaling (TGFβ/AngII) with low mechanical stretch. | Biochemical signaling strongly increases profibrotic activity. | collagen=10.29; p=0.651; myofibro=0.887; align=0.911 |
| high_load_high_signal | Combined high loading and high signaling (synergy condition). | Combined cues produce the strongest non-infarct profibrotic response. | collagen=10.31; p=0.671; myofibro=0.887; align=0.918 |
| infarct_high_load_high_signal | Synergy condition with infarct-zone maturation (core/border/remote). | Infarct core amplifies collagen burden over global non-infarct response. | collagen=10.42; p=0.672; myofibro=0.887; align=0.918 |
| drug_tgfr_block | Synergy condition with pharmacologic TGFβ receptor blockade. | TGFβR blockade suppresses signaling and collagen vs no-drug synergy. | collagen=9.91; p=0.652; myofibro=0.875; align=0.917 |
| drug_at1r_block | Synergy condition with pharmacologic AT1 receptor blockade. | AT1R blockade suppresses collagen vs no-drug synergy. | collagen=10.06; p=0.645; myofibro=0.887; align=0.918 |
| drug_dual_block | Synergy condition with dual receptor blockade (TGFβR + AT1R). | Dual blockade gives strongest suppression among drug scenarios. | collagen=9.69; p=0.624; myofibro=0.875; align=0.918 |

## How to interpret endpoints
- **collagen**: final fibrosis burden (higher = more fibrosis).
- **p**: integrated profibrotic signaling activity (higher = stronger fibrotic signaling).
- **myofibro**: final myofibroblast fraction (higher = more activated fibroblast phenotype).
- **align**: collagen/fibre alignment with loading axis (higher = more load-directed structure).

## Checks
- [PASS] high_signal_only has higher profibrotic signal than baseline
- [PASS] high_signal_only has higher myofibroblast fraction than baseline
- [PASS] high_load_only increases fibre alignment vs baseline
- [PASS] high_load_high_signal increases profibrotic signal over high_load_only and high_signal_only
- [PASS] infarct core collagen exceeds non-infarct high_load_high_signal global collagen
- [PASS] TGFβR blockade reduces profibrotic signal vs high_load_high_signal
- [PASS] AT1R blockade reduces collagen vs high_load_high_signal
- [PASS] Dual blockade gives strongest suppression (collagen) among drug scenarios