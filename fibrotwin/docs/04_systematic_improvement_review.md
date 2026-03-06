# 04 — Systematic Improvement Review for Validation Fidelity

This review synthesizes literature-grounded ideas to improve agreement between FibroTwin predictions and experimentally observed fibroblast/fibrosis behavior.

## Scope
- Improve model ability to reproduce validation tests for:
  - mechanosensitive fibroblast activation,
  - infarct core/border/remote collagen patterns,
  - load–signal interaction effects,
  - fiber/collagen alignment dynamics.

## Literature-informed improvement themes

## 1) Fibroblast signaling network depth (Saucerman-style)
**Rationale:** Cardiac fibroblast behavior is highly context dependent and regulated by interacting pathways (e.g., TGF-β, AngII, ROS, mechano-signaling crosstalk).

**Current model status:** reduced single profibrotic proxy `p`.

**Suggested upgrade:** small ODE network module:
- latent nodes: `Smad`, `MAPK/ERK`, `Calcineurin`, `ROS`;
- outputs: `myofibro_switch_rate`, `collagen_synthesis_rate`, `degradation_inhibition`.

**Expected benefit:** improves stimulus-specific responses and nonlinearity in validation matrix.

## 2) Explicit cytokine transport fields
**Rationale:** Current TGF-β/AngII are scenario-level inputs; local secretion and diffusion are not explicit.

**Suggested upgrade:** PDE fields
\[
\partial_t c_k = D_k\nabla^2 c_k + S_k(\text{cells,damage,load}) - \lambda_k c_k
\]
for `k in {TGFβ, chemokine, MMP/TIMP proxy}`.

**Expected benefit:** spatial gradients and border-zone behavior become more realistic and testable.

## 3) Constituent-specific constrained-mixture turnover
**Rationale:** Current growth proxy is scalar and does not distinguish collagen cohorts.

**Suggested upgrade:** constrained-mixture style collagen cohorts with deposition time and survival/turnover law.

**Expected benefit:** better long-horizon remodeling kinetics and hysteresis after perturbation changes.

## 4) Damage-driven infarct evolution
**Rationale:** Infarct is currently static mask.

**Suggested upgrade:** dynamic infarct state variables (inflammation, necrotic clearance, provisional matrix maturation).

**Expected benefit:** improved temporal agreement for infarct healing curves.

## 5) Calibration and UQ
**Rationale:** portfolio checks are trend-based, not quantitatively calibrated.

**Suggested upgrade:**
- Bayesian / multi-objective calibration on selected PMIDs,
- uncertainty intervals for outputs,
- VVUQ table per test category.

**Expected benefit:** publication-quality credibility and reproducible confidence bands.

## Prioritized implementation roadmap
1. Add explicit cytokine fields (highest biological realism gain).
2. Replace single `p` with 4–6 node signaling ODE subnetwork.
3. Introduce dynamic infarct maturation states.
4. Upgrade constrained-mixture collagen turnover.
5. Add UQ + calibrated scorecard with confidence intervals.

## Validation impact mapping
- **Signaling tests:** 1 + 2
- **Infarct spatial tests:** 2 + 4
- **Long-horizon remodeling tests:** 3 + 4
- **Mechanochemical interaction tests:** 1 + 2 + 5

## Note
This review is designed as an actionable model-development plan and should be iterated alongside the PubMed-linked test catalog and scorecard.
