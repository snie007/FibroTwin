# 03 — Validation and Sanity Checks

1. **Linear patch test:** Affine displacement field under homogeneous material yields near-uniform strain.
2. **Nonlinear Ogden Dirichlet test:** nonlinear solver preserves imposed boundary displacements and returns finite solution.
3. **Uniaxial stretch sanity:** right-edge displacement increases mean \(\varepsilon_{xx}\).
4. **Deposition kernel:** single fixed cell gives radially decaying collagen map.
5. **Phenotype switch + deposition boost:** high-cue fibroblasts switch to myofibroblasts and deposit more collagen.
6. **Fibre normalization:** \(\|a\|=1\) after each update.
7. **Nonnegativity:** \(c\ge 0\).
8. **Run stability:** no NaN in displacement, collagen, fibres over long-horizon runs (target 600 steps).
