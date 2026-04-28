#!/usr/bin/env python3
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / 'papers' / 'pdfs'
PDF_DIR.mkdir(parents=True, exist_ok=True)


def slug(text: str) -> str:
    text = re.sub(r'[^A-Za-z0-9]+', '_', text).strip('_')
    return text[:120]


def europepmc_lookup_pmid(pmid: str):
    url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?' + urllib.parse.urlencode({
        'query': f'EXT_ID:{pmid} AND SRC:MED',
        'format': 'json',
        'resultType': 'core',
    })
    with urllib.request.urlopen(url) as r:
        data = json.load(r)
    results = data.get('resultList', {}).get('result', [])
    return results[0] if results else None


def choose_pdf_url(item: dict):
    ft = item.get('fullTextUrlList') or {}
    urls = ft.get('fullTextUrl') or []
    for pref_site in ('Europe_PMC', 'Unpaywall', 'Publisher'):
        for u in urls:
            if u.get('documentStyle') == 'pdf' and u.get('availabilityCode') == 'OA' and u.get('site') == pref_site:
                return u.get('url')
    for u in urls:
        if u.get('documentStyle') == 'pdf' and u.get('availabilityCode') == 'OA':
            return u.get('url')
    return None


def download(url: str, path: Path):
    req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw/1.0'})
    with urllib.request.urlopen(req) as r:
        data = r.read()
    if not data.startswith(b'%PDF'):
        # still save if it's likely a redirected PDF response, but guard against html
        if b'<html' in data[:500].lower():
            raise RuntimeError('response was HTML, not PDF')
    path.write_bytes(data)


def process_csv(csv_path: Path):
    out_rows = []
    rows = list(csv.DictReader(csv_path.open()))
    for row in rows:
        status = row.get('full_text_status', '')
        filename = row.get('pdf_filename', '')
        pmid = row.get('pmid', '').strip()
        title = row.get('title', '')
        citation = row.get('citation', '')
        pdf_url = ''
        note = ''

        if filename and (PDF_DIR / filename).exists():
            out_rows.append({'id': row.get('id'), 'citation': citation, 'pmid': pmid, 'status': 'already_downloaded', 'pdf_filename': filename, 'pdf_url': '', 'note': ''})
            continue

        if pmid:
            try:
                item = europepmc_lookup_pmid(pmid)
                time.sleep(0.2)
            except Exception as e:
                out_rows.append({'id': row.get('id'), 'citation': citation, 'pmid': pmid, 'status': 'lookup_failed', 'pdf_filename': '', 'pdf_url': '', 'note': str(e)})
                continue
            if item:
                pdf_url = choose_pdf_url(item) or ''
                if pdf_url:
                    basename = f"{row.get('id','X')}_{slug(citation.split('.')[0])}_{row.get('year','')}_{slug(title)}.pdf"
                    try:
                        download(pdf_url, PDF_DIR / basename)
                        row['full_text_status'] = 'retrieved_open_access'
                        row['pdf_filename'] = basename
                        out_rows.append({'id': row.get('id'), 'citation': citation, 'pmid': pmid, 'status': 'downloaded', 'pdf_filename': basename, 'pdf_url': pdf_url, 'note': ''})
                    except Exception as e:
                        out_rows.append({'id': row.get('id'), 'citation': citation, 'pmid': pmid, 'status': 'download_failed', 'pdf_filename': '', 'pdf_url': pdf_url, 'note': str(e)})
                else:
                    note = 'No open-access PDF found via Europe PMC'
                    out_rows.append({'id': row.get('id'), 'citation': citation, 'pmid': pmid, 'status': 'not_open_access', 'pdf_filename': '', 'pdf_url': '', 'note': note})
            else:
                out_rows.append({'id': row.get('id'), 'citation': citation, 'pmid': pmid, 'status': 'not_found', 'pdf_filename': '', 'pdf_url': '', 'note': ''})
        else:
            out_rows.append({'id': row.get('id'), 'citation': citation, 'pmid': pmid, 'status': 'no_pmid', 'pdf_filename': '', 'pdf_url': '', 'note': ''})

    with csv_path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    manifest = ROOT / 'papers' / f'{csv_path.stem}_pdf_manifest.csv'
    with manifest.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'citation', 'pmid', 'status', 'pdf_filename', 'pdf_url', 'note'])
        writer.writeheader()
        writer.writerows(out_rows)
    print(f'Wrote manifest: {manifest}')
    counts = {}
    for r in out_rows:
        counts[r['status']] = counts.get(r['status'], 0) + 1
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: fetch_pdfs.py <csv> [<csv> ...]')
        sys.exit(1)
    for arg in sys.argv[1:]:
        process_csv((ROOT / arg).resolve() if not Path(arg).is_absolute() else Path(arg))
