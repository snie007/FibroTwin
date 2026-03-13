import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]

SCHEMAS = {
    'collagen_dynamics': ['collagen', 'fibrosis', 'hydroxyproline', '% fibrosis'],
    'fibroblast_signaling': ['smad', 'erk', 'alpha-sma', 'α-sma', 'myofibro'],
    'infarct_remodeling': ['infarct', 'core', 'border', 'remote', 'scar'],
    'growth_remodeling': ['alignment', 'anisotropy', 'fibre', 'fiber'],
}

NUM = re.compile(r"\b\d+(?:\.\d+)?\b")


def extract_from_xml(xml_path: Path):
    txt = ''
    try:
        root = ET.fromstring(xml_path.read_bytes())
        txt = ' '.join([t.strip() for t in root.itertext() if t and t.strip()])
    except Exception:
        return []
    out = []
    for m in NUM.finditer(txt):
        lo = max(0, m.start() - 80)
        hi = min(len(txt), m.end() + 80)
        sn = txt[lo:hi]
        out.append({'value': m.group(0), 'snippet': sn})
    return out


def match_schema(snippet: str, category: str):
    s = snippet.lower()
    kws = SCHEMAS.get(category, [])
    return any(k in s for k in kws)


def main(limit=20):
    cat = json.loads((ROOT / 'outputs' / 'systematic_test_catalog.json').read_text())
    tests = cat.get('tests', [])[:limit]

    rows = []
    for t in tests:
        tid = t.get('id')
        pmid = str(t.get('pmid'))
        catg = t.get('category')
        x = ROOT / 'data' / 'papers' / pmid / 'fulltext.xml'
        cand = extract_from_xml(x) if x.exists() else []
        matched = [c for c in cand if match_schema(c['snippet'], catg)]
        rows.append({
            'id': tid,
            'pmid': pmid,
            'category': catg,
            'n_candidates': len(cand),
            'n_schema_matched': len(matched),
            'schema_matched': matched[:25],
        })

    out = {'n': len(rows), 'rows': rows}
    (ROOT / 'outputs' / 'schema_extract_report.json').write_text(json.dumps(out, indent=2))
    (ROOT / 'outputs' / 'schema_extract_report.md').write_text(
        '# Schema Extraction Report\n\n' + '\n'.join([f"- {r['id']} ({r['category']}): matched {r['n_schema_matched']}" for r in rows])
    )
    print(json.dumps({'n': len(rows)}, indent=2))


if __name__ == '__main__':
    main()
