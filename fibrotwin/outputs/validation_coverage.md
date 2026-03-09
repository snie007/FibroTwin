# Validation Coverage Matrix Summary

- Studies (PMID-linked tests): 80
- Model domains: 6
- Distinct validation intents (mechanism/observable templates): 6

## Why 80 studies but few domains?
Domains are broad model modules (e.g., infarct_remodeling, fibroblast_signaling).
Each study is linked to one domain and one intent template. Multiple studies can support the same mechanistic intent.

## Domain distribution
| Domain | N studies |
|---|---:|
| collagen_dynamics | 27 |
| fibroblast_signaling | 23 |
| infarct_remodeling | 19 |
| growth_remodeling | 6 |
| cell_motion | 4 |
| fibre_alignment | 1 |

## Intent coverage (top)
| Intent ID | Domain | N studies | Expected template |
|---|---|---:|---|
| I001 | collagen_dynamics | 27 | Collagen should increase with deposition and remain nonnegative with turnover. |
| I002 | fibroblast_signaling | 23 | Higher profibrotic input should increase myofibroblast fraction and collagen deposition. |
| I003 | infarct_remodeling | 19 | Collagen and profibrotic signal should rise in infarct core and border zone. |
| I004 | growth_remodeling | 6 | Long-horizon loading should alter growth proxy and redistribute mechanical cues. |
| I005 | cell_motion | 4 | Fibroblast migration should shape spatial deposition patterns (trails/fronts). |
| I006 | fibre_alignment | 1 | Under sustained stretch, collagen/myofibre orientation should align with loading axis. |

## Interpretation
- Uniqueness should be read at the **study record** level and **intent ID** level.
- If many studies map to the same intent, this is evidence depth, not new mechanism breadth.
- To increase mechanism breadth, add new intent templates and corresponding simulation protocols.