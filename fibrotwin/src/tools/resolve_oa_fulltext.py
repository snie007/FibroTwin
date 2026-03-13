import json
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]


def fetch_json(url, timeout=25):
    with urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8', errors='ignore'))


def europepmc_by_pmid(pmid):
    q = quote(f'EXT_ID:{pmid} AND SRC:MED')
    url = f'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}&format=json&pageSize=1'
    try:
        j = fetch_json(url)
        res = (j.get('resultList') or {}).get('result') or []
        return res[0] if res else None
    except Exception:
        return None


def try_fulltext(pmcid):
    if not pmcid:
        return False
    pmcid = pmcid if pmcid.startswith('PMC') else f'PMC{pmcid}'
    url = f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML'
    try:
        with urlopen(url, timeout=25) as r:
            txt = r.read(400).decode('utf-8', errors='ignore')
            return ('<article' in txt.lower()) or ('<?xml' in txt.lower())
    except Exception:
        return False


def main():
    rep = json.loads((ROOT / 'outputs' / 'fulltext_availability_report.json').read_text())
    rows = rep.get('rows', [])

    targets = [r for r in rows if (not r.get('pmcid')) and (not r.get('strict_approved'))]
    recovered = []
    checked = 0

    for r in targets:
        pmid = str(r.get('pmid') or '').strip()
        if not pmid:
            continue
        checked += 1
        ep = europepmc_by_pmid(pmid)
        if not ep:
            continue
        pmcid = ep.get('pmcid') or ep.get('pmcidid') or ep.get('pmc')
        has_ft = try_fulltext(pmcid) if pmcid else False
        if pmcid:
            recovered.append({
                'id': r.get('id'),
                'pmid': pmid,
                'pmcid': pmcid if str(pmcid).startswith('PMC') else f'PMC{pmcid}',
                'isOpenAccess': ep.get('isOpenAccess'),
                'journalTitle': ep.get('journalTitle'),
                'title': ep.get('title'),
                'fulltext_reachable': bool(has_ft),
            })
        time.sleep(0.2)

    out = {
        'n_targets_without_pmcid': len(targets),
        'n_checked': checked,
        'n_recovered_pmcid': len(recovered),
        'n_recovered_fulltext_reachable': sum(int(x['fulltext_reachable']) for x in recovered),
        'recovered': recovered,
    }
    (ROOT / 'outputs' / 'oa_resolution_report.json').write_text(json.dumps(out, indent=2))

    lines = [
        '# OA Resolution Report', '',
        f"- Targets without PMCID: {out['n_targets_without_pmcid']}",
        f"- Checked: {out['n_checked']}",
        f"- Recovered PMCID: {out['n_recovered_pmcid']}",
        f"- Recovered with reachable fulltext: {out['n_recovered_fulltext_reachable']}",
    ]
    (ROOT / 'outputs' / 'oa_resolution_report.md').write_text('\n'.join(lines))
    print(json.dumps({k: out[k] for k in ['n_targets_without_pmcid','n_recovered_pmcid','n_recovered_fulltext_reachable']}, indent=2))


if __name__ == '__main__':
    main()
