import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RANGE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:to|-|–)\s*(\d+(?:\.\d+)?)")
NUM_RE = re.compile(r"\d+(?:\.\d+)?")


def parse_anchor(v):
    s=(v or '').lower()
    if 'p<' in s or 'p <' in s or 'p=' in s:
        return None
    if any(u in s for u in ['day','days','week','weeks','month','months','year','years','hour','hours','min']) and ('%' not in s and 'fold' not in s):
        return None
    m=RANGE_RE.search(s)
    if m:
        a,b=float(m.group(1)),float(m.group(2))
        return ('range',[min(a,b),max(a,b)])
    n=NUM_RE.search(s)
    if not n:
        return None
    x=float(n.group(0))
    if '%' in s or 'percent' in s:
        return ('percent',[0.8*x,1.2*x])
    if 'fold' in s or s.endswith('x') or ' x' in s:
        return ('fold',[0.8*x,1.2*x])
    return None


def model_vals(cat,vp):
    b=vp.get('baseline_low_load_low_signal',{})
    hs=vp.get('high_signal_only',{})
    hl=vp.get('high_load_only',{})
    hls=vp.get('high_load_high_signal',{})
    inf=vp.get('infarct_high_load_high_signal',{})
    out={}
    if cat=='infarct_remodeling' and inf.get('c_remote'):
        cr,cc=inf['c_remote'],inf['c_core']
        out['percent']=100*(cc-cr)/max(abs(cr),1e-8); out['fold']=cc/max(cr,1e-8)
    elif cat=='fibroblast_signaling' and b.get('p_mean_final'):
        x0,x1=b['p_mean_final'],hs['p_mean_final']
        out['percent']=100*(x1-x0)/max(abs(x0),1e-8); out['fold']=x1/max(x0,1e-8)
    elif cat=='collagen_dynamics' and b.get('c_mean_final'):
        x0,x1=b['c_mean_final'],hls['c_mean_final']
        out['percent']=100*(x1-x0)/max(abs(x0),1e-8); out['fold']=x1/max(x0,1e-8)
    elif cat=='growth_remodeling' and b.get('ac_align_x_final') is not None:
        x0,x1=b['ac_align_x_final'],hl['ac_align_x_final']
        out['percent']=100*(x1-x0)/max(abs(x0),1e-8); out['fold']=x1/max(x0,1e-8)
    return out


def main():
    qe=json.loads((ROOT/'outputs/quantitative_evidence.json').read_text())
    cat=json.loads((ROOT/'outputs/systematic_test_catalog.json').read_text())
    vp={r['scenario']:r for r in json.loads((ROOT/'outputs/validation_portfolio.json').read_text())['scenarios']}
    cat_by={t['id']:t for t in cat['tests']}
    rows=[]
    for t in qe['tests']:
        tid=t['id']; c=cat_by.get(tid,{}).get('category','')
        best=None
        for q in t.get('quantitative_mentions',[]):
            pa=parse_anchor(q.get('value',''))
            if not pa: continue
            ep=(q.get('endpoint_guess') or '')
            if c=='infarct_remodeling' and ep not in ('infarct zoning','collagen/fibrosis'): continue
            if c=='fibroblast_signaling' and ep not in ('signaling pathway','myofibroblast activation'): continue
            if c=='collagen_dynamics' and ep!='collagen/fibrosis': continue
            if c=='growth_remodeling' and ep!='alignment/anisotropy': continue
            best=(q,pa); break
        if not best:
            continue
        mv=model_vals(c,vp)
        kind,band=best[1]
        if kind not in mv: continue
        x=mv[kind]
        st='PASS' if band[0]<=x<=band[1] else 'FAIL'
        rows.append({'id':tid,'category':c,'status':st,'paper_anchor':best[0]['value'],'kind':kind,'paper_band':band,'model_value':x})

    counts={'PASS':0,'FAIL':0}
    for r in rows: counts[r['status']]+=1
    out={'n_strict_anchored':len(rows),'counts':counts,'rows':rows,'definition':'Strict paper-anchored only (no templates/curated overrides).'}
    (ROOT/'outputs/quantitative_match_strict.json').write_text(json.dumps(out,indent=2))
    (ROOT/'outputs/quantitative_match_strict.md').write_text(f"# Strict Paper-Anchored Match\n\n- n: {len(rows)}\n- PASS: {counts['PASS']}\n- FAIL: {counts['FAIL']}\n\nNo template/curated overrides included.")
    print(json.dumps(out['counts']))

if __name__=='__main__':
    main()
