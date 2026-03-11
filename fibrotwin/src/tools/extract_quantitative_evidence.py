import json
import re
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]

NUM_PAT = re.compile(r"(?:\b\d+(?:\.\d+)?\s?(?:%|fold|x|mg|ug|ng|mmhg|kpa|pa|ms|s|min|h|day|days|week|weeks|month|months|year|years)\b|\b\d+(?:\.\d+)?\s?(?:to|-|–)\s?\d+(?:\.\d+)?\b)", re.I)


def fetch_pubmed_xml(pmids):
    q = urlencode({"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"})
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{q}"
    with urlopen(url, timeout=30) as r:
        return r.read()


def parse_articles(xml_bytes):
    root = ET.fromstring(xml_bytes)
    out = {}
    for art in root.findall('.//PubmedArticle'):
        pmid = art.findtext('.//PMID') or ''
        title = ' '.join([t.text or '' for t in art.findall('.//ArticleTitle//')]) or (art.findtext('.//ArticleTitle') or '')
        abs_parts = []
        for a in art.findall('.//Abstract/AbstractText'):
            label = a.attrib.get('Label')
            txt = ''.join(a.itertext()).strip()
            if txt:
                abs_parts.append(f"{label}: {txt}" if label else txt)
        abstract = ' '.join(abs_parts)
        out[pmid] = {'title': title.strip(), 'abstract': abstract.strip()}
    return out


def extract_numbers(text):
    if not text:
        return []
    matches = []
    for m in NUM_PAT.finditer(text):
        lo = max(0, m.start() - 55)
        hi = min(len(text), m.end() + 55)
        snippet = text[lo:hi].replace('\n', ' ').strip()
        matches.append({'value': m.group(0), 'snippet': snippet})
    # deduplicate by value+snippet
    ded = []
    seen = set()
    for x in matches:
        k = (x['value'].lower(), x['snippet'][:80].lower())
        if k in seen:
            continue
        seen.add(k)
        ded.append(x)
    return ded[:8]


def main():
    catalog_path = ROOT / 'outputs' / 'systematic_test_catalog.json'
    if not catalog_path.exists():
        raise SystemExit('missing systematic_test_catalog.json')
    cat = json.loads(catalog_path.read_text())
    tests = cat.get('tests', [])
    pmids = sorted({str(t.get('pmid', '')).strip() for t in tests if t.get('pmid')})

    pmid_data = {}
    for i in range(0, len(pmids), 40):
        batch = pmids[i:i+40]
        try:
            xml = fetch_pubmed_xml(batch)
            pmid_data.update(parse_articles(xml))
        except Exception:
            pass
        time.sleep(0.34)

    out_tests = []
    for t in tests:
        pmid = str(t.get('pmid', '')).strip()
        rec = pmid_data.get(pmid, {})
        abs_text = rec.get('abstract', '')
        nums = extract_numbers(abs_text)
        out_tests.append({
            'id': t.get('id'),
            'pmid': pmid,
            'title': rec.get('title', t.get('title', '')),
            'n_numeric_mentions': len(nums),
            'quantitative_mentions': nums,
            'source': 'PubMed abstract mining (automated, screening-level)',
        })

    out = {
        'n_tests': len(out_tests),
        'n_with_numeric_mentions': sum(1 for x in out_tests if x['n_numeric_mentions'] > 0),
        'tests': out_tests,
        'notes': [
            'Automated extraction from PubMed abstract text only.',
            'Values/snippets are screening-level and require manual confirmation against full text/figures for publication-grade quantitative benchmarking.'
        ]
    }

    (ROOT / 'outputs' / 'quantitative_evidence.json').write_text(json.dumps(out, indent=2))
    lines = ['# Quantitative Evidence Extraction (Screening)', '',
             f"- Tests processed: {out['n_tests']}",
             f"- Tests with numeric mentions in abstract: {out['n_with_numeric_mentions']}", '']
    (ROOT / 'outputs' / 'quantitative_evidence.md').write_text('\n'.join(lines))
    print(json.dumps({'n_with_numeric_mentions': out['n_with_numeric_mentions'], 'n_tests': out['n_tests']}, indent=2))


if __name__ == '__main__':
    main()
