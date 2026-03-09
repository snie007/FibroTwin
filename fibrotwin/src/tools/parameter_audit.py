import json
from pathlib import Path
import yaml


def flatten(d, prefix=''):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            p = f'{prefix}.{k}' if prefix else str(k)
            if isinstance(v, dict):
                out.update(flatten(v, p))
            else:
                out[p] = v
    return out


def main(cfg='configs/mvp_2d_stretch.yaml', reg='data/calibration/parameter_registry.yaml'):
    cfgd = yaml.safe_load(Path(cfg).read_text())
    regd = yaml.safe_load(Path(reg).read_text())
    flat = flatten(cfgd)
    params = regd.get('parameters', {})

    rows = []
    for k, v in flat.items():
        if isinstance(v, (int, float)):
            meta = params.get(k)
            status = 'mapped' if meta else 'missing'
            in_band = None
            if meta and isinstance(meta.get('literature_band'), list) and len(meta['literature_band']) == 2:
                lo, hi = meta['literature_band']
                in_band = (lo <= float(v) <= hi)
            rows.append({
                'parameter': k,
                'value': float(v),
                'status': status,
                'units': None if not meta else meta.get('units'),
                'literature_band': None if not meta else meta.get('literature_band'),
                'in_literature_band': in_band,
                'pmid': None if not meta else meta.get('pmid'),
            })

    mapped = [r for r in rows if r['status'] == 'mapped']
    inband = [r for r in mapped if r['in_literature_band'] is True]
    miss = [r for r in rows if r['status'] == 'missing']

    out = {
        'n_numeric_parameters': len(rows),
        'n_mapped': len(mapped),
        'n_missing': len(miss),
        'n_in_literature_band': len(inband),
        'coverage': 0.0 if not rows else len(mapped)/len(rows),
        'rows': rows,
    }
    Path('outputs/parameter_audit.json').write_text(json.dumps(out, indent=2))

    lines = [
        '# Parameter Quantitative Audit',
        '',
        f"- Numeric parameters: {out['n_numeric_parameters']}",
        f"- Mapped to literature/units: {out['n_mapped']}",
        f"- Missing mapping: {out['n_missing']}",
        f"- In declared literature band: {out['n_in_literature_band']}",
        f"- Coverage: {100*out['coverage']:.1f}%",
        '',
        '## Missing mappings (top)'
    ]
    for r in miss[:40]:
        lines.append(f"- {r['parameter']} = {r['value']}")
    lines.append('')
    lines.append('## Out-of-band mapped parameters')
    oob = [r for r in mapped if r['in_literature_band'] is False]
    for r in oob:
        lines.append(f"- {r['parameter']} = {r['value']} vs {r['literature_band']} (PMID {r['pmid']})")

    Path('outputs/parameter_audit.md').write_text('\n'.join(lines))
    print(json.dumps({k: out[k] for k in ['n_numeric_parameters','n_mapped','n_missing','n_in_literature_band','coverage']}, indent=2))


if __name__ == '__main__':
    main()
