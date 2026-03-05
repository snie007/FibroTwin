# 02 — Numerical Methods and Coupling Plan

## Discretization
- Mesh: structured rectangular grid split into linear triangles (P1).
- Mechanics unknowns: nodal displacement vector \(U\in\mathbb R^{2N_n}\).
- Collagen field: nodal scalar \(c\).
- Fibre fields: nodal unit vectors \(a, a_c\in\mathbb R^2\).
- Agents: Lagrangian particles.

## Time integration (operator splitting)
For each macro-step:
1. **Assemble mechanics** with current \(c,a,g\): element stiffness \(K_e\), global \(K\).
2. **Apply BCs** and solve \(KU=f\) (dense `torch.linalg.solve`, CPU/GPU).
3. **Compute cues** (element strain energy proxy mapped to nodes).
4. **Move agents** with persistent random walk + taxis on cue gradient.
5. **Deposit collagen** via Gaussian kernel to nodes; apply degradation.
6. **Update fibres** toward principal strain direction from mechanics step.
7. **Update growth proxy** from collagen and optional stress cue.
8. Save snapshot; render frame every `frame_every`.

## Stability/sanity constraints
- Clamp collagen: \(c\leftarrow\max(c,0)\).
- Normalize fibres each step.
- Small time steps and modest deposition rates.
- Reflective BC for agent motion.

## Validation plan
- Patch test for linear elasticity under affine displacement.
- Single-cell deposition radial symmetry.
- Fibre convergence to fixed target direction with expected exponential-like behavior.

## Extensibility path
- Replace dense solve with sparse iterative/preconditioned solver.
- Upgrade constitutive law to hyperelastic + growth tensor \(F_g\).
- Move deposition to quadrature points / FE-consistent projection.
- Extend to 3D tetrahedral meshes.
