import os
import torch
from ..mechanics.fem_assembly import assemble_stiffness, element_strain
from ..mechanics.solver import apply_dirichlet, solve_linear_system
from ..mechanics.nonlinear_solver import solve_quasistatic_ogden
from ..cells.motion import update_agents
from ..cells.deposition import deposit_collagen
from ..remodeling.fibre_reorientation import principal_direction_from_strain, update_fibres
from ..remodeling.mixture_growth import update_growth, element_E_from_fields
from .io import save_snapshot, log_line
from .viz import render_frame


def run_sim(config, nodes, elems, fields, agents, out_dir):
    dt = config['time']['dt']
    n_steps = config['time']['n_steps']
    Lx, Ly = config['mesh']['Lx'], config['mesh']['Ly']
    mech = config['mechanics']
    rem = config['remodeling']
    cel = config['cells']

    n = nodes.shape[0]
    ndof = 2 * n
    left = torch.where(torch.isclose(nodes[:, 0], torch.tensor(0.0, device=nodes.device)))[0]
    right = torch.where(torch.isclose(nodes[:, 0], torch.tensor(Lx, device=nodes.device)))[0]

    U_prev = torch.zeros(ndof, device=nodes.device, dtype=nodes.dtype)

    for step in range(n_steps):
        c_elem = fields.c[elems].mean(dim=1)
        g_elem = fields.g[elems].mean(dim=1)
        a_elem = fields.a[elems].mean(dim=1)

        ux_right = mech['stretch_x'] * Lx
        fixed_dofs = []
        fixed_vals = []
        for nid in left.tolist():
            fixed_dofs += [2 * nid, 2 * nid + 1]
            fixed_vals += [0.0, 0.0]
        for nid in right.tolist():
            fixed_dofs += [2 * nid]
            fixed_vals += [ux_right]
        fixed_dofs = torch.tensor(fixed_dofs, dtype=torch.long, device=nodes.device)
        fixed_vals = torch.tensor(fixed_vals, dtype=nodes.dtype, device=nodes.device)

        model = mech.get('model', 'linear')
        if model == 'ogden':
            mat = {
                'mu': mech.get('ogden_mu', 20.0),
                'alpha': mech.get('ogden_alpha', 8.0),
                'kappa': mech.get('ogden_kappa', 200.0),
            }
            U = solve_quasistatic_ogden(nodes, elems, fixed_dofs, fixed_vals, U0=U_prev, material=mat, max_iter=mech.get('nl_max_iter', 80))
        else:
            E_elem = element_E_from_fields(mech['E0'], c_elem, g_elem)
            K = assemble_stiffness(
                nodes, elems, E_elem, nu=mech['nu'], plane_stress=mech['plane_stress'],
                a_elem=a_elem, c_elem=c_elem, kf=mech.get('kf_aniso', 0.2)
            )
            f = torch.zeros(ndof, device=nodes.device)
            Kbc, fbc = apply_dirichlet(K, f, fixed_dofs, fixed_vals)
            U = solve_linear_system(Kbc, fbc)

        U_prev = U.detach()

        eps_e = element_strain(nodes, elems, U)
        energy_e = 0.5 * (eps_e ** 2).sum(dim=1)
        cue_node = torch.zeros(n, device=nodes.device)
        cnt = torch.zeros(n, device=nodes.device)
        for e, conn in enumerate(elems):
            cue_node[conn] += energy_e[e]
            cnt[conn] += 1
        cue_node = cue_node / torch.clamp(cnt, min=1)

        agents = update_agents(agents, nodes, cue_node, dt, cel, (Lx, Ly))
        fields.c = deposit_collagen(nodes, fields.c, agents.x, dt, cel['dep_rate'], cel['dep_sigma'], rem['k_deg'])

        pdir_e = principal_direction_from_strain(eps_e)
        pdir_n = torch.zeros((n, 2), device=nodes.device)
        for e, conn in enumerate(elems):
            pdir_n[conn] += pdir_e[e]
        pdir_n = pdir_n / (pdir_n.norm(dim=1, keepdim=True) + 1e-12)
        fields.a = update_fibres(fields.a, pdir_n, dt, rem['tau_fibre'])
        fields.ac = update_fibres(fields.ac, fields.a, dt, rem['tau_fibre'] * 1.5)
        fields.g = update_growth(fields.g, fields.c, dt, k_g=rem['k_growth'])

        if step % config['viz']['frame_every'] == 0:
            render_frame(
                os.path.join(out_dir, 'frames', f'frame_{step:04d}.png'),
                nodes, elems, U, fields.c, fields.a, agents,
                stride=config['viz']['quiver_stride'],
            )

        save_snapshot(out_dir, step, {
            'U': U.detach().cpu(),
            'c': fields.c.detach().cpu(),
            'a': fields.a.detach().cpu(),
            'ac': fields.ac.detach().cpu(),
            'g': fields.g.detach().cpu(),
            'agents_x': agents.x.detach().cpu(),
            'mechanics_model': model,
        })

        if step % 10 == 0:
            log_line(out_dir, f'step={step} max_u={U.abs().max().item():.4e} c_mean={fields.c.mean().item():.4e} g_mean={fields.g.mean().item():.4e} model={model}')

    return fields, agents
