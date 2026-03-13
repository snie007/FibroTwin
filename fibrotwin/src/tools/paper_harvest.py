import json
import re
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]


def fetch(url, timeout=30, retries=4):
    for i in range(retries):
        try:
            with urlopen(url, timeout=timeout) as r:
                return r.read()
        except HTTPError as e:
            if e.code == 429 and i < retries - 1:
                import time
                time.sleep(1.5 * (i + 1))
                continue
            raise


def pubmed_meta(pmid):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
    xml = fetch(url)
    root = ET.fromstring(xml)
    art = root.find('.//PubmedArticle')
    if art is None:
        return {}
    title = art.findtext('./MedlineCitation/Article/ArticleTitle') or ''
    pmcid = ''
    doi = ''
    for aid in art.findall('./PubmedData/ArticleIdList/ArticleId'):
        t = (aid.attrib.get('IdType') or '').lower()
        v = (aid.text or '').strip()
        if t == 'pmc' and v:
            pmcid = v if v.startswith('PMC') else f'PMC{v}'
        if t == 'doi' and v:
            doi = v
    return {'title': title, 'pmcid': pmcid, 'doi': doi}


def harvest_pmc_assets(pmcid, outdir: Path):
    out = {'pmcid': pmcid, 'html_saved': False, 'xml_saved': False, 'images': []}
    if not pmcid:
        return out
    outdir.mkdir(parents=True, exist_ok=True)
    # html
    try:
        html = fetch(f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/")
        (outdir / 'article.html').write_bytes(html)
        out['html_saved'] = True
        # discover image urls quickly
        txt = html.decode('utf-8', errors='ignore')
        imgs = sorted(set(re.findall(r'https://pmc\.ncbi\.nlm\.nih\.gov/articles/%s/bin/[^"\']+' % re.escape(pmcid), txt)))
        for u in imgs[:40]:
            try:
                b = fetch(u)
                fn = u.split('/')[-1]
                (outdir / 'figures' / fn).parent.mkdir(parents=True, exist_ok=True)
                (outdir / 'figures' / fn).write_bytes(b)
                out['images'].append(fn)
            except Exception:
                pass
    except Exception:
        pass

    # europepmc xml fulltext
    try:
        xml = fetch(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{quote(pmcid)}/fullTextXML")
        (outdir / 'fulltext.xml').write_bytes(xml)
        out['xml_saved'] = True
    except Exception:
        pass

    return out


def main(limit=20):
    cat = json.loads((ROOT / 'outputs' / 'systematic_test_catalog.json').read_text())
    tests = cat.get('tests', [])[:limit]
    rows = []
    import time
    for t in tests:
        tid = t.get('id')
        pmid = str(t.get('pmid'))
        meta = pubmed_meta(pmid)
        pdir = ROOT / 'data' / 'papers' / pmid
        assets = harvest_pmc_assets(meta.get('pmcid'), pdir)
        rows.append({
            'id': tid,
            'pmid': pmid,
            'title': meta.get('title'),
            'pmcid': meta.get('pmcid'),
            'doi': meta.get('doi'),
            'harvest': assets,
        })
        time.sleep(0.34)

    out = {'n': len(rows), 'rows': rows}
    (ROOT / 'outputs' / 'paper_harvest_report.json').write_text(json.dumps(out, indent=2))
    (ROOT / 'outputs' / 'paper_harvest_report.md').write_text(
        '# Paper Harvest Report\n\n' + '\n'.join([f"- {r['id']} PMID {r['pmid']} PMCID {r['pmcid']} html={r['harvest']['html_saved']} xml={r['harvest']['xml_saved']} n_figs={len(r['harvest']['images'])}" for r in rows])
    )
    print(json.dumps({'n': len(rows)}, indent=2))


if __name__ == '__main__':
    main()
