import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DESC = {
    'myofibro_fraction_high_signal': 'Checks fibroblast activation under high biochemical signaling.',
    'profibrotic_index_high_signal': 'Checks integrated profibrotic signaling index under high signal.',
    'alignment_high_load': 'Checks collagen/fibre alignment response under mechanical loading.',
    'collagen_fraction_load_signal': 'Checks fibrosis burden under combined load + signaling.',
    'infarct_core_collagen': 'Checks elevated collagen burden in infarct core.',
    'infarct_core_to_remote_ratio': 'Checks spatial contrast between infarct core and remote tissue.',
}


def plan_for(name, passed):
    if passed:
        return 'No immediate tuning required; retain as anchor constraint.'
    if name == 'myofibro_fraction_high_signal':
        return 'Activation is too high; reduce phenotype switching sensitivity (myo_switch_threshold up, k_switch down) and/or reduce TGFR->SMAD gain.'
    if name == 'profibrotic_index_high_signal':
        return 'Increase receptor-to-signaling gains (k_tgfr_smad, k_at1r_erk) or reduce signaling decay (d_smad/d_erk).'
    if name == 'alignment_high_load':
        return 'Increase mech alignment coupling (mech_align_gain) or reduce tau_collagen to accelerate alignment.'
    if name == 'collagen_fraction_load_signal':
        return 'Increase deposition gain terms (p_dep_gain/synergy_dep_gain) or reduce collagen degradation rate.'
    if name == 'infarct_core_collagen':
        return 'Increase infarct collagen source in core and/or reduce core dispersion to concentrate deposition.'
    if name == 'infarct_core_to_remote_ratio':
        return 'Increase core-specific signaling/deposition while reducing remote spillover (diffusion/decay tuning).'
    return 'Tune related gain/decay parameters and re-evaluate scenario outputs.'


def main(inp='outputs/calibration_report.json'):
    p = ROOT / inp
    if not p.exists():
        raise SystemExit('calibration_report.json missing')
    d = json.loads(p.read_text())
    checks = d.get('checks', [])

    cards = []
    failed = []
    for i, c in enumerate(checks, start=1):
        cid = f'C{i:03d}'
        name = c.get('name')
        passed = bool(c.get('pass'))
        item = {
            'id': cid,
            'name': name,
            'status': 'PASS' if passed else 'FAIL',
            'value': c.get('value'),
            'band': c.get('band'),
            'description': DESC.get(name, 'Calibration target check.'),
            'action_plan': plan_for(name, passed),
        }
        cards.append(item)
        if not passed:
            failed.append(item)

    out = {'n': len(cards), 'n_failed': len(failed), 'cards': cards, 'failed_cards': failed}
    (ROOT / 'outputs' / 'calibration_cards.json').write_text(json.dumps(out, indent=2))

    lines = ['# Calibration Cards', '', f"Pass: {len(cards)-len(failed)}/{len(cards)}", '', '## Failed-test action plan']
    if failed:
        for f in failed:
            lines.append(f"- {f['id']} {f['name']}: {f['action_plan']}")
        lines += [
            '',
            '## Execution plan (next tuning cycle)',
            '1. **C001 myofibro_fraction_high_signal**: reduce over-activation first (switch threshold/slope tuning), rerun high_signal_only.',
            '2. **C002 profibrotic_index_high_signal**: increase signaling strength after C001 correction by tuning receptor-to-node gains and selected decay constants.',
            '3. **C006 infarct_core_to_remote_ratio**: increase infarct spatial contrast by boosting core source terms and reducing remote spillover (diffusion/decay).',
            '4. Re-run full validation portfolio + calibration cards and accept only if all three checks enter target bands.'
        ]
    else:
        lines.append('- No failed calibration checks in this run.')
    (ROOT / 'outputs' / 'calibration_cards.md').write_text('\n'.join(lines))

    print(json.dumps({'n': out['n'], 'n_failed': out['n_failed']}, indent=2))


if __name__ == '__main__':
    main()
