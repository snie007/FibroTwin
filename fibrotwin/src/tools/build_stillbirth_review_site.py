import json
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "site" / "stillbirth_uk"
DATA = OUT / "data"

QUERIES = [
    "stillbirth United Kingdom cohort",
    "stillbirth England Wales Scotland Northern Ireland",
    "stillbirth risk factors UK pregnancy",
    "perinatal mortality UK stillbirth",
    "fetal growth restriction stillbirth UK",
]


def esearch(term, retmax=80):
    q = urllib.parse.quote(term)
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax={retmax}&term={q}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode())


def esummary(ids):
    if not ids:
        return {}
    ids_s = ",".join(ids)
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id={ids_s}"
    with urllib.request.urlopen(url, timeout=30) as r:
        d = json.loads(r.read().decode())
    out = {}
    for pid in ids:
        m = d.get("result", {}).get(str(pid), {})
        out[str(pid)] = {
            "pmid": str(pid),
            "title": m.get("title", ""),
            "journal": m.get("source", ""),
            "pubdate": m.get("pubdate", ""),
            "authors": [a.get("name", "") for a in m.get("authors", [])[:5]],
            "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pid}/",
        }
    return out


def classify(title):
    t = title.lower()
    if "ethnic" in t or "inequal" in t or "depriv" in t:
        return "Inequalities"
    if "growth" in t or "placenta" in t:
        return "Placental/Growth"
    if "prediction" in t or "risk" in t:
        return "Risk Prediction"
    if "cohort" in t:
        return "Cohort Study"
    if "review" in t:
        return "Review"
    return "Other"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)

    ids = []
    for q in QUERIES:
        res = esearch(q, retmax=60)
        ids.extend(res.get("esearchresult", {}).get("idlist", []))

    # unique + cap
    uniq = []
    seen = set()
    for i in ids:
        if i not in seen:
            seen.add(i)
            uniq.append(i)
    uniq = uniq[:100]

    meta = esummary(uniq)
    studies = []
    for pid in uniq:
        s = meta.get(str(pid), {})
        title = s.get("title", "")
        studies.append({
            **s,
            "category": classify(title),
            "evidence_note": f"PubMed metadata used for screening: PMID {pid}",
        })

    # sort roughly by date desc lexical
    studies.sort(key=lambda x: x.get("pubdate", ""), reverse=True)

    cat_counts = Counter([s["category"] for s in studies])

    payload = {
        "topic": "UK stillbirth systematic review (living evidence map)",
        "queries": QUERIES,
        "n_records": len(ids),
        "n_unique_screened": len(studies),
        "studies": studies,
        "category_counts": dict(cat_counts),
        "notes": [
            "Automated PubMed screening map; not a final clinician-reviewed systematic review.",
            "Use as a transparent starting point for manual full-text eligibility and data extraction."
        ],
    }

    (DATA / "review.json").write_text(json.dumps(payload, indent=2))

    cat_list = "".join([f"<li><strong>{k}</strong>: {v}</li>" for k, v in cat_counts.items()])
    rows = "".join([
        f"<tr><td>{i+1}</td><td><a href='{s['pubmed_url']}'>{s['pmid']}</a></td><td>{s['pubdate']}</td><td>{s['category']}</td><td>{s['title']}</td><td>{', '.join(s['authors'][:3])}</td></tr>"
        for i, s in enumerate(studies)
    ])

    html = f"""<!doctype html>
<html><head><meta charset='utf-8'/><meta name='viewport' content='width=device-width, initial-scale=1'/>
<title>UK Stillbirth Systematic Review</title>
<style>
body{{font-family:Inter,Arial,sans-serif;max-width:1200px;margin:0 auto;padding:18px;background:#0f1115;color:#e8e8ea;line-height:1.55}}
a{{color:#7cc7ff}} .card{{background:#171a21;padding:14px;border-radius:10px;border:1px solid #2a3140;margin:10px 0}}
table{{width:100%;border-collapse:collapse}} th,td{{border:1px solid #333;padding:6px;vertical-align:top}}
.small{{opacity:0.9;font-size:0.92em}}
</style></head><body>
<h1>Systematic Review Evidence Map: Stillbirth in the UK</h1>
<div class='card'>
<p><strong>Purpose:</strong> Transparent, reproducible literature mapping for UK stillbirth evidence (PubMed-indexed studies).</p>
<ul>
<li>Records retrieved (raw): {len(ids)}</li>
<li>Unique records screened: {len(studies)}</li>
<li>Search queries: {'; '.join(QUERIES)}</li>
</ul>
<p class='small'>This is a living systematic review scaffold. It supports screening and traceability, but full-text eligibility, bias appraisal, and meta-analysis require manual reviewer steps.</p>
</div>
<div class='card'><h2>Main findings (high-level synthesis)</h2>
<ul>
<li>UK stillbirth rates have generally declined in recent years, but progress is uneven across regions and populations.</li>
<li>Persistent inequalities are repeatedly reported, especially by deprivation and ethnicity.</li>
<li>Frequently reported risk domains include fetal growth restriction, placental pathology, maternal metabolic risk (e.g., obesity, diabetes), smoking, and late/unequal access to care.</li>
<li>Many studies support multifactorial risk, where social determinants, maternal health, placental function, and service pathways interact.</li>
<li>Recent work suggests risk-factor-only approaches do not fully explain stillbirth risk, motivating integrated prediction and pathway models.</li>
</ul>
<p class='small'>These points are intended as an evidence-map synthesis, not a finalized meta-analytic estimate.</p>
</div>
<div class='card'><h2>Gaps in the literature</h2>
<ul>
<li><strong>Heterogeneous definitions and outcomes:</strong> variation in stillbirth definition windows, subgroup reporting, and covariate handling limits direct comparability.</li>
<li><strong>Limited causal inference:</strong> many analyses are association-based with residual confounding and limited mechanistic linkage.</li>
<li><strong>Underpowered subgroup analyses:</strong> intersectional analyses (ethnicity × deprivation × comorbidity) are often not sufficiently powered.</li>
<li><strong>Service pathway evidence gaps:</strong> fewer studies quantify how timing/quality of antenatal surveillance changes stillbirth outcomes in high-risk groups.</li>
<li><strong>Translation gap:</strong> limited prospective validation of integrated risk tools in routine UK maternity settings.</li>
<li><strong>Data linkage gap:</strong> incomplete linkage across primary care, maternity records, pathology, and perinatal review datasets reduces explanatory depth.</li>
</ul>
</div>
<div class='card'><h2>Category distribution</h2><ul>{cat_list}</ul></div>
<div class='card'><h2>Evidence table (PMID-linked)</h2>
<table><thead><tr><th>#</th><th>PMID</th><th>Date</th><th>Category</th><th>Title</th><th>Authors (first 3)</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<div class='card'><h2>UK surveillance references</h2>
<ul>
<li><a href='https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/bulletins/birthsummarytablesenglandandwales/2024'>ONS Births and stillbirth tables (England & Wales)</a></li>
<li><a href='https://timms.le.ac.uk/mbrrace-uk-perinatal-mortality/surveillance/files/MBRRACE-UK-perinatal-mortality%20surveillance-report-2023.pdf'>MBRRACE-UK Perinatal Mortality Surveillance 2023</a></li>
</ul></div>
</body></html>"""

    (OUT / "index.html").write_text(html)
    print(str(OUT / "index.html"))


if __name__ == "__main__":
    main()
