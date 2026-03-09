# Numerical Test Report

Collected: 18
Passed: 18
Exit code: 0

## Tests
- tests/test_collagen_cohort_analytic.py::test_collagen_cohort_matches_linear_system_reference
- tests/test_collagen_mixture.py::test_collagen_mixture_turnover_and_maturation
- tests/test_coupling_contracts.py::test_mech_signal_synergy_increases_profibrotic_output
- tests/test_cytokine_analytic.py::test_cytokine_zero_diffusion_matches_closed_form
- tests/test_cytokines.py::test_cytokine_diffusion_nonnegative_and_spreads
- tests/test_deposition.py::test_single_cell_radial_like
- tests/test_deposition.py::test_myofibro_switch_and_boost
- tests/test_deposition.py::test_motion_trail_deposition
- tests/test_fem_patch.py::test_fem_uniaxial_patch_like
- tests/test_fibre_update.py::test_fibre_converges_to_target
- tests/test_infarct_chain_analytic.py::test_infarct_chain_matches_matrix_exponential_reference
- tests/test_infarct_maturation.py::test_infarct_state_progression
- tests/test_mesh.py::test_mesh_counts
- tests/test_motion_advection.py::test_agent_advection_moves_with_tissue_increment
- tests/test_nonlinear_solver.py::test_ogden_solver_respects_dirichlet
- tests/test_signaling_analytic.py::test_smad_linear_closed_form_in_decoupled_case
- tests/test_signaling_network.py::test_tgf_increases_smad
- tests/test_signaling_network.py::test_mech_increases_ros_and_can

## pytest tail
```
..................                                                       [100%]
18 passed in 3.16s

```