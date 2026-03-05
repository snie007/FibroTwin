# FibroTwin (MVP)

Minimal multiscale cardiac fibrosis simulator (2D) with:
- Torch-based small-strain FEM (triangular elements)
- Agent fibroblast motion (persistent random walk + optional taxis)
- Collagen deposition field
- Fibre reorientation toward principal stretch direction
- Reproducible outputs and animation

## Quickstart

```bash
cd fibrotwin
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -m src.main --config configs/mvp_2d_stretch.yaml
```

Outputs are written to `outputs/<run_id>/` with snapshots, config copy, run log, and animation.

## Tests

```bash
pytest -q
```

## Notes
- Mechanics MVP is linear elasticity with dense global stiffness assembly (suitable for small meshes).
- Coupling architecture is modular to extend to nonlinear hyperelastic + sparse solvers later.
