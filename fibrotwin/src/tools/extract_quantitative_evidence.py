import json
import re
import time
from pathlib import Path
from urllib.parse import urlencode, quote
from urllib.request import urlopen
from urllib.error import URLError
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]

NUM_PAT = re.compile(
    r"(?:"
    r"\b\d+(?:\.\d+)?\s?(?:%|percent|fold|x|mg|ug|μg|ng|pg|mmhg|kpa|pa|bpm|ms|s|min|h|hr|hours?|day|days|week|weeks|month|months|year|years)\b"
    r"|\b\d+(?:\.\d+)?\s?(?:to|-|–)\s?\d+(?:\.\d+)?\b"
    r"|\bp\s?[<=>]\s?0?\.\d+\b"
    r"|\b\d+(?:\.\d+)?\s?±\s?\d+(?:\.\d+)?\b"
    r")",
    re.I,
)


def fetch_text(url, timeout=35):
    with urlopen(url, timeout=timeout) as r:
        return r.read()


def fetch_pubmed_xml(pmids):
    q = urlencode({"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"})
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{q}"
    return fetch_text(url)


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

        pmcid = ''
        doi = ''
        for aid in art.findall('.//ArticleId'):
            t = (aid.attrib.get('IdType') or '').lower()
            v = (aid.text or '').strip()
            if t == 'pmc' and v:
                pmcid = v if v.startswith('PMC') else f'PMC{v}'
            if t == 'doi' and v:
                doi = v

        out[pmid] = {
            'title': title.strip(),
            'abstract': abstract.strip(),
            'pmcid': pmcid,
            'doi': doi,
        }
    return out


def fetch_europepmc_fulltext_by_pmcid(pmcid):
    if not pmcid:
        return ''
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{quote(pmcid)}/fullTextXML"
    try:
        xml = fetch_text(url, timeout=40)
        root = ET.fromstring(xml)
        txt = ' '.join([t.strip() for t in root.itertext() if t and t.strip()])
        return txt
    except Exception:
        return ''


def fetch_pmc_bioc_fulltext_by_pmcid(pmcid):
    """Fallback route: NCBI PMC BioC JSON endpoint."""
    if not pmcid:
        return ''
    pmc_num = pmcid.replace('PMC', '').strip()
    url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{quote(pmc_num)}/unicode"
    try:
        raw = fetch_text(url, timeout=45)
        j = json.loads(raw.decode('utf-8', errors='ignore'))
        texts = []
        for doc in j.get('documents', []):
            for p in doc.get('passages', []):
                t = p.get('text') or ''
                if t:
                    texts.append(t)
        return ' '.join(texts)
    except Exception:
        return ''


def fetch_pmc_html_fulltext_by_pmcid(pmcid):
    """Fallback route: scrape visible text from PMC HTML."""
    if not pmcid:
        return ''
    url = f"https://pmc.ncbi.nlm.nih.gov/articles/{quote(pmcid)}/"
    try:
        html = fetch_text(url, timeout=45).decode('utf-8', errors='ignore')
        # crude html->text fallback (no external parser dependency)
        txt = re.sub(r'<script[\s\S]*?</script>', ' ', html, flags=re.I)
        txt = re.sub(r'<style[\s\S]*?</style>', ' ', txt, flags=re.I)
        txt = re.sub(r'<[^>]+>', ' ', txt)
        txt = re.sub(r'\s+', ' ', txt).strip()
        return txt
    except Exception:
        return ''


def classify_endpoint(snippet):
    s = snippet.lower()
    if any(k in s for k in ['collagen', 'fibrosis', 'scar']):
        return 'collagen/fibrosis'
    if any(k in s for k in ['smad', 'tgf', 'erk', 'calcineurin', 'ros', 'signal']):
        return 'signaling pathway'
    if any(k in s for k in ['myofibro', 'fibroblast activation', 'alpha-sma', 'α-sma']):
        return 'myofibroblast activation'
    if any(k in s for k in ['infarct', 'core', 'border', 'remote']):
        return 'infarct zoning'
    if any(k in s for k in ['alignment', 'anisotropy', 'fibre', 'fiber']):
        return 'alignment/anisotropy'
    return 'other quantitative mention'


def extract_numbers(text, limit=14):
    if not text:
        return []
    matches = []
    for m in NUM_PAT.finditer(text):
        lo = max(0, m.start() - 70)
        hi = min(len(text), m.end() + 70)
        snippet = text[lo:hi].replace('\n', ' ').strip()
        matches.append({
            'value': m.group(0),
            'snippet': snippet,
            'endpoint_guess': classify_endpoint(snippet),
        })
    ded = []
    seen = set()
    for x in matches:
        k = (x['value'].lower(), x['snippet'][:120].lower())
        if k in seen:
            continue
        seen.add(k)
        ded.append(x)
    return ded[:limit]


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
        time.sleep(0.25)

    out_tests = []
    n_fulltext_hits = 0
    for t in tests:
        pmid = str(t.get('pmid', '')).strip()
        rec = pmid_data.get(pmid, {})
        abs_text = rec.get('abstract', '')
        pmcid = rec.get('pmcid', '')

        full_text = ''
        fulltext_route = ''
        if pmcid:
            full_text = fetch_europepmc_fulltext_by_pmcid(pmcid)
            if full_text:
                fulltext_route = 'EuropePMC fullTextXML'
            if not full_text:
                full_text = fetch_pmc_bioc_fulltext_by_pmcid(pmcid)
                if full_text:
                    fulltext_route = 'PMC BioC JSON fallback'
            if not full_text:
                full_text = fetch_pmc_html_fulltext_by_pmcid(pmcid)
                if full_text:
                    fulltext_route = 'PMC HTML fallback'
        if full_text:
            n_fulltext_hits += 1

        abstract_nums = extract_numbers(abs_text, limit=10)
        fulltext_nums = extract_numbers(full_text, limit=12)

        merged = abstract_nums + [x for x in fulltext_nums if x['value'] not in {a['value'] for a in abstract_nums}]
        merged = merged[:14]

        out_tests.append({
            'id': t.get('id'),
            'pmid': pmid,
            'pmcid': pmcid,
            'doi': rec.get('doi', ''),
            'title': rec.get('title', t.get('title', '')),
            'n_numeric_mentions': len(merged),
            'quantitative_mentions': merged,
            'has_fulltext_extraction': bool(full_text),
            'fulltext_route': fulltext_route,
            'source': 'PubMed abstract + OA fulltext mining with fallback routes (automated, screening-level)',
        })

    out = {
        'n_tests': len(out_tests),
        'n_with_numeric_mentions': sum(1 for x in out_tests if x['n_numeric_mentions'] > 0),
        'n_with_fulltext': n_fulltext_hits,
        'tests': out_tests,
        'notes': [
            'Automated extraction from PubMed abstract and OA full text where available.',
            'Values/snippets are screening-level; manual confirmation against full paper figures/tables is still required for publication-grade quantitative benchmarking.',
        ]
    }

    (ROOT / 'outputs' / 'quantitative_evidence.json').write_text(json.dumps(out, indent=2))
    lines = [
        '# Quantitative Evidence Extraction (Improved)',
        '',
        f"- Tests processed: {out['n_tests']}",
        f"- Tests with numeric mentions: {out['n_with_numeric_mentions']}",
        f"- Tests with OA fulltext extraction: {out['n_with_fulltext']}",
        '',
        'This is screening-level extraction (automated).'
    ]
    (ROOT / 'outputs' / 'quantitative_evidence.md').write_text('\n'.join(lines))
    print(json.dumps({'n_with_numeric_mentions': out['n_with_numeric_mentions'], 'n_with_fulltext': out['n_with_fulltext'], 'n_tests': out['n_tests']}, indent=2))


if __name__ == '__main__':
    main()
