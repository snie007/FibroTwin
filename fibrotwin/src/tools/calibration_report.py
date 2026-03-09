import json
from pathlib import Path
import yaml


def main(targets='data/calibration/targets.yaml', val='outputs/validation_portfolio.json'):
    t = yaml.safe_load(Path(targets).read_text())
    v = json.loads(Path(val).read_text())
    rows = {r['scenario']: r for r in v.get('scenarios', [])}

    checks = []
    # map a few calibrated checks
    hs = rows.get('high_signal_only', {})
    hl = rows.get('high_load_only', {})
    hls = rows.get('high_load_high_signal', {})
    inf = rows.get('infarct_high_load_high_signal', {})

    tg = t['targets']
    checks.append({'name':'myofibro_fraction_high_signal','value':hs.get('myo_frac_final'), 'band':tg['fibroblast_signaling']['myofibro_fraction_high_signal']})
    checks.append({'name':'profibrotic_index_high_signal','value':hs.get('p_mean_final'), 'band':tg['fibroblast_signaling']['profibrotic_index_high_signal']})
    checks.append({'name':'alignment_high_load','value':hl.get('ac_align_x_final'), 'band':tg['growth_remodeling']['alignment_high_load']})
    checks.append({'name':'collagen_fraction_load_signal','value':hls.get('c_mean_final'), 'band':tg['growth_remodeling']['collagen_fraction_load_signal']})
    checks.append({'name':'infarct_core_collagen','value':inf.get('c_core'), 'band':tg['infarct_remodeling']['infarct_core_collagen']})

    def ok(v,b):
        return (v is not None) and (b[0] <= v <= b[1])

    for c in checks:
        c['pass'] = ok(c['value'], c['band'])

    out = {'n':len(checks), 'n_pass':sum(int(c['pass']) for c in checks), 'checks':checks}
    Path('outputs/calibration_report.json').write_text(json.dumps(out, indent=2))

    lines=['# Calibration Report','',f"Pass: {out['n_pass']}/{out['n']}",'']
    for c in checks:
        lines.append(f"- {c['name']}: value={c['value']}, band={c['band']} -> {'PASS' if c['pass'] else 'FAIL'}")
    Path('outputs/calibration_report.md').write_text('\n'.join(lines))
    print(json.dumps({'n_pass':out['n_pass'],'n':out['n']}, indent=2))


if __name__ == '__main__':
    main()
