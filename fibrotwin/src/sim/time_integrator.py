import os
import torch
from ..mechanics.fem_assembly import assemble_stiffness, element_strain
from ..mechanics.solver import apply_dirichlet, solve_linear_system
from ..mechanics.nonlinear_solver import solve_quasistatic_ogden
from ..cells.motion import update_agents
from ..cells.deposition import deposit_collagen, update_phenotype
from ..remodeling.fibre_reorientation import principal_direction_from_strain, update_fibres
from ..remodeling.mixture_growth import update_growth, element_E_from_fields
from ..remodeling.cytokines import build_knn_weights, update_cytokine_fields
from ..remodeling.signaling_network import update_signaling_network
from ..remodeling.infarct_maturation import (
    init_infarct_states,
    update_infarct_states,
    infarct_softening_factor,
    infarct_signal_source,
)
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

    inf = config.get('infarct', {})
    infarct_enabled = bool(inf.get('enabled', False))
    if infarct_enabled:
        cx = inf.get('center_x', 0.5 * Lx)
        cy = inf.get('center_y', 0.5 * Ly)
        rad = inf.get('radius', 0.2 * min(Lx, Ly))
        r = torch.sqrt((nodes[:, 0] - cx) ** 2 + (nodes[:, 1] - cy) ** 2)
        infarct_node_mask = (r <= rad).to(nodes.dtype)
        infarct_elem_mask = infarct_node_mask[elems].mean(dim=1)
        fields.infl, fields.prov, fields.scar = init_infarct_states(infarct_node_mask)
    else:
        infarct_node_mask = torch.zeros(n, device=nodes.device, dtype=nodes.dtype)
        infarct_elem_mask = torch.zeros(elems.shape[0], device=nodes.device, dtype=nodes.dtype)

    cyt = config.get('cytokines', {})
    use_cyt = bool(cyt.get('enabled', True))
    nbr, w_knn = build_knn_weights(nodes, k=cyt.get('k_neighbors', 8), sigma=cyt.get('kernel_sigma', 0.7))

    for step in range(n_steps):
        if infarct_enabled:
            fields.infl, fields.prov, fields.scar = update_infarct_states(
                fields.infl,
                fields.prov,
                fields.scar,
                dt,
                infarct_node_mask,
                params=inf,
            )

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
            if infarct_enabled:
                soft_node = infarct_softening_factor(fields.infl, fields.prov, fields.scar, base_softening=inf.get('softening', 0.6))
                soft_elem = soft_node[elems].mean(dim=1)
                E_elem = E_elem * (1.0 - soft_elem)
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
        if infarct_enabled:
            cue_node = cue_node + inf.get('cue_boost', 0.15) * (0.8 * fields.infl + 0.4 * fields.prov)

        sig = config.get('signaling', {})

        if use_cyt:
            src_tgf = sig.get('tgf_beta', 0.25) * torch.ones_like(cue_node)
            src_chemo = (0.2 * cue_node)
            if infarct_enabled:
                inf_src = infarct_signal_source(fields.infl, fields.prov, fields.scar, base_signal=inf.get('signal_source', 0.20))
                src_tgf = src_tgf + inf_src
                src_chemo = src_chemo + 0.4 * inf_src
            fields.tgf, fields.chemo = update_cytokine_fields(
                fields.tgf,
                fields.chemo,
                dt,
                nbr,
                w_knn,
                src_tgf_node=src_tgf,
                src_chemo_node=src_chemo,
                D_tgf=cyt.get('D_tgf', 0.15),
                D_chemo=cyt.get('D_chemo', 0.25),
                decay_tgf=cyt.get('decay_tgf', 0.08),
                decay_chemo=cyt.get('decay_chemo', 0.12),
            )
            tgf_eff = fields.tgf
            ang_eff = torch.clamp(sig.get('angII', 0.2) + 0.3 * fields.chemo, 0.0, 1.0)
        else:
            tgf_eff = torch.full_like(cue_node, sig.get('tgf_beta', 0.25))
            ang_eff = torch.full_like(cue_node, sig.get('angII', 0.2))

        net = config.get('signaling_network', {})
        fields.smad, fields.erk, fields.ros, fields.can, fields.p = update_signaling_network(
            fields.smad,
            fields.erk,
            fields.ros,
            fields.can,
            dt,
            tgf=tgf_eff,
            ang_eff=ang_eff,
            mech_cue=cue_node,
            params=net,
        )

        agents = update_agents(agents, nodes, cue_node, dt, cel, (Lx, Ly))
        agents = update_phenotype(
            agents,
            nodes,
            cue_node,
            profibrotic_node=fields.p,
            threshold=cel.get('myo_switch_threshold', 0.45),
            k_switch=cel.get('myo_switch_softness', 0.08),
            deact_threshold=cel.get('myo_deact_threshold', 0.20),
        )
        idx_nn = torch.argmin(torch.cdist(agents.x, nodes), dim=1)
        agent_p = fields.p[idx_nn]
        agent_cue = cue_node[idx_nn]
        fields.c = deposit_collagen(
            nodes,
            fields.c,
            agents.x,
            agents.is_myofibro,
            dt,
            cel['dep_rate'],
            cel['dep_sigma'],
            rem['k_deg'],
            myo_boost=cel.get('myo_dep_boost', 2.0),
            agent_p=agent_p,
            agent_cue=agent_cue,
            p_gain=cel.get('p_dep_gain', 1.0),
            mech_gain=cel.get('mech_dep_gain', 0.5),
            synergy_gain=cel.get('synergy_dep_gain', 0.6),
            agent_v=agents.v,
            trail_gain=cel.get('trail_gain', 0.4),
            trail_len=cel.get('trail_len', 0.6),
        )

        pdir_e = principal_direction_from_strain(eps_e)
        pdir_n = torch.zeros((n, 2), device=nodes.device)
        for e, conn in enumerate(elems):
            pdir_n[conn] += pdir_e[e]
        pdir_n = pdir_n / (pdir_n.norm(dim=1, keepdim=True) + 1e-12)
        fields.a = update_fibres(fields.a, pdir_n, dt, rem['tau_fibre'])
        tau_c = rem.get('tau_collagen', rem['tau_fibre'] * 1.5)
        cue_scale = cue_node.mean().item()
        tau_c_eff = tau_c / (1.0 + rem.get('mech_align_gain', 1.0) * cue_scale)
        fields.ac = update_fibres(fields.ac, pdir_n, dt, tau_c_eff)
        fields.g = update_growth(fields.g, fields.c, dt, k_g=rem['k_growth'])

        viz_enabled = config.get('viz', {}).get('enable', True)
        if viz_enabled and step % config['viz']['frame_every'] == 0:
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
            'p': fields.p.detach().cpu(),
            'tgf': fields.tgf.detach().cpu(),
            'chemo': fields.chemo.detach().cpu(),
            'smad': fields.smad.detach().cpu(),
            'erk': fields.erk.detach().cpu(),
            'ros': fields.ros.detach().cpu(),
            'can': fields.can.detach().cpu(),
            'infl': fields.infl.detach().cpu(),
            'prov': fields.prov.detach().cpu(),
            'scar': fields.scar.detach().cpu(),
            'agents_x': agents.x.detach().cpu(),
            'agents_is_myofibro': agents.is_myofibro.detach().cpu(),
            'mechanics_model': model,
        })

        if step % 10 == 0:
            myo_frac = agents.is_myofibro.float().mean().item()
            ex = torch.tensor([1.0, 0.0], device=nodes.device, dtype=nodes.dtype)
            a_align = torch.abs((fields.a * ex).sum(dim=1)).mean().item()
            ac_align = torch.abs((fields.ac * ex).sum(dim=1)).mean().item()
            p_mean = fields.p.mean().item()
            tgf_mean = fields.tgf.mean().item()
            chemo_mean = fields.chemo.mean().item()
            smad_mean = fields.smad.mean().item()
            erk_mean = fields.erk.mean().item()
            infl_mean = fields.infl.mean().item()
            scar_mean = fields.scar.mean().item()
            log_line(out_dir, f'step={step} max_u={U.abs().max().item():.4e} c_mean={fields.c.mean().item():.4e} g_mean={fields.g.mean().item():.4e} p_mean={p_mean:.4f} tgf_mean={tgf_mean:.4f} chemo_mean={chemo_mean:.4f} smad_mean={smad_mean:.4f} erk_mean={erk_mean:.4f} infl_mean={infl_mean:.4f} scar_mean={scar_mean:.4f} myo_frac={myo_frac:.4f} a_align_x={a_align:.4f} ac_align_x={ac_align:.4f} model={model}')

    return fields, agents
