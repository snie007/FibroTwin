# 02 — Numerical Methods and Coupling Plan (Updated)

## Discretization
- Mesh: structured rectangular grid split into linear triangles (P1).
- Mechanics unknowns: nodal displacement vector \(U\in\mathbb R^{2N_n}\).
- Collagen field: nodal scalar \(c\).
- Fibre fields: nodal unit vectors \(a, a_c\in\mathbb R^2\).
- Agents: Lagrangian particles.

## Mechanics solver options
1. **Linear MVP mode**: assembled dense stiffness \(KU=f\).
2. **Large-deformation mode (current default)**: total potential minimization with compressible Ogden energy and Dirichlet constraints using LBFGS on free DOFs.

### Weak-form / energy route
- Residual comes from \(\delta\Pi=0\).
- Instead of hand-coding tangent matrix, we use torch autograd + LBFGS to minimize \(\Pi(U)\).
- This is robust for small meshes and allows rapid constitutive prototyping.

## Time integration (operator splitting)
For each macro-step:
1. Solve mechanics (linear or Ogden nonlinear) with current state.
2. Compute mechanical cue (strain-energy proxy) on elements → nodes.
3. Move agents (persistent random walk + taxis).
4. Deposit collagen with Gaussian kernels + degradation.
5. Reorient fibres toward principal direction proxy.
6. Update growth/remodelling proxy \(g\).
7. Save snapshots and render periodic frames.

## Performance notes
- Main cost in large-deformation mode: nonlinear mechanics solve (LBFGS + per-element energy evaluations).
- Cost reduction options:
  - coarser mesh for parameter sweeps,
  - lower nonlinear iterations for early exploration,
  - render frames less frequently,
  - future sparse/tangent-based Newton implementation.

## Stability/sanity constraints
- Clamp collagen: \(c\leftarrow\max(c,0)\).
- Normalize fibres each step.
- Reflective boundaries for agents.
- Positive-definite spectral clamps in Ogden energy evaluation.
