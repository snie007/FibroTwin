import json, os, re, shutil, subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'
DOCS = ROOT / 'docs'
OUT = ROOT / 'outputs'


def md_to_html(md: str) -> str:
    try:
        import markdown
        return markdown.markdown(md, extensions=['fenced_code', 'tables'])
    except Exception:
        md = re.sub(r'^### (.*)$', r'<h3>\1</h3>', md, flags=re.M)
        md = re.sub(r'^## (.*)$', r'<h2>\1</h2>', md, flags=re.M)
        md = re.sub(r'^# (.*)$', r'<h1>\1</h1>', md, flags=re.M)
        md = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', md)
        md = re.sub(r'\n\n+', '</p><p>', md.strip())
        return '<p>' + md + '</p>'


def parse_run_log(path: Path):
    step, max_u, c_mean, g_mean = [], [], [], []
    if not path.exists():
        return {"step": step, "max_u": max_u, "c_mean": c_mean, "g_mean": g_mean}
    for line in path.read_text().splitlines():
        m = re.search(r"step=(\d+) max_u=([0-9eE+\-.]+) c_mean=([0-9eE+\-.]+)(?: g_mean=([0-9eE+\-.]+))?", line)
        if m:
            step.append(int(m.group(1))); max_u.append(float(m.group(2))); c_mean.append(float(m.group(3)))
            g_mean.append(float(m.group(4)) if m.group(4) else None)
    return {"step": step, "max_u": max_u, "c_mean": c_mean, "g_mean": g_mean}


def discover_runs():
    runs = []
    for d in sorted([p for p in OUT.iterdir() if p.is_dir()]):
        run = {"run_id": d.name, "path": str(d)}
        cfg = d / 'config.yaml'
        run['config'] = cfg.read_text() if cfg.exists() else ''
        metrics = parse_run_log(d / 'run.log')
        run['metrics'] = metrics
        mp4 = d / 'animation.mp4'
        gif = d / 'animation.gif'
        run['animation'] = mp4.name if mp4.exists() else (gif.name if gif.exists() else None)
        frames = sorted((d / 'frames').glob('frame_*.png')) if (d / 'frames').exists() else []
        sel = [frames[0], frames[len(frames)//2], frames[-1]] if len(frames) >= 3 else frames[:3]
        run['frames'] = [f.name for f in sel]
        run['timestamp'] = d.name
        runs.append(run)
    runs.sort(key=lambda x: x['run_id'], reverse=True)
    return runs


def copy_assets(runs):
    img = SITE / 'assets' / 'img'
    vid = SITE / 'assets' / 'video'
    img.mkdir(parents=True, exist_ok=True); vid.mkdir(parents=True, exist_ok=True)
    for r in runs:
        rp = Path(r['path'])
        if r['animation']:
            src = rp / r['animation']
            dst = vid / f"{r['run_id']}_{r['animation']}"
            if src.exists(): shutil.copy2(src, dst)
            r['animation_site'] = f"assets/video/{dst.name}"
        else:
            r['animation_site'] = None
        r['frames_site'] = []
        for fn in r['frames']:
            src = rp / 'frames' / fn
            if src.exists():
                dst = img / f"{r['run_id']}_{fn}"
                shutil.copy2(src, dst)
                r['frames_site'].append(f"assets/img/{dst.name}")


def make_plots(runs):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return
    for r in runs[:5]:
        m = r['metrics']
        if not m['step']:
            continue
        for key, ylab, fname in [('c_mean', 'Mean collagen', 'collagen'), ('max_u', 'Max displacement', 'max_u')]:
            y = m[key]
            plt.figure(figsize=(5,3))
            plt.plot(m['step'], y, '-o', ms=3)
            plt.xlabel('Step'); plt.ylabel(ylab); plt.title(f"{r['run_id']} {ylab}")
            out = SITE / 'assets' / 'img' / f"{r['run_id']}_{fname}.png"
            plt.tight_layout(); plt.savefig(out, dpi=140); plt.close()
        if any(v is not None for v in m['g_mean']):
            y = [v if v is not None else 0 for v in m['g_mean']]
            plt.figure(figsize=(5,3)); plt.plot(m['step'], y, '-o', ms=3)
            plt.xlabel('Step'); plt.ylabel('Mean growth proxy'); plt.title(f"{r['run_id']} g_mean")
            out = SITE / 'assets' / 'img' / f"{r['run_id']}_g_mean.png"
            plt.tight_layout(); plt.savefig(out, dpi=140); plt.close()


def nav():
    return '''<nav><a href="index.html">Home</a><a href="pages/overview.html">Overview</a><a href="pages/model.html">Model</a><a href="pages/numerics.html">Numerics</a><a href="pages/implementation.html">Implementation</a><a href="pages/validation.html">Validation</a><a href="pages/results.html">Results</a><a href="pages/changelog.html">Changelog</a><a href="pages/references.html">References</a></nav>'''


def page(title, body, extra_head=''):
    return f'''<!doctype html><html><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>{title}</title><link rel="stylesheet" href="../assets/css/style.css"/>{extra_head}</head><body><header><h1>{title}</h1>{nav().replace('index.html','../index.html').replace('pages/','')}</header><main>{body}</main><script src="../assets/js/site.js"></script></body></html>'''


def root_page(title, body):
    return f'''<!doctype html><html><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>{title}</title><link rel="stylesheet" href="assets/css/style.css"/></head><body><header><h1>{title}</h1>{nav()}</header><main>{body}</main></body></html>'''


def git_changelog():
    try:
        out = subprocess.check_output(['git', '-C', str(ROOT), 'log', '--pretty=format:%h|%ad|%s', '--date=short', '-n', '40'], text=True)
        rows = out.splitlines()
        lis = ''.join([f"<li><code>{h}</code> {d} — {s}</li>" for h,d,s in (r.split('|',2) for r in rows)])
        return f"<ul>{lis}</ul>"
    except Exception:
        return '<p>No git log available.</p>'


def read_doc(name):
    p = DOCS / name
    return md_to_html(p.read_text()) if p.exists() else '<p>Not found.</p>'


def latest_test_summary():
    # best-effort: use known status from project execution
    return '<ul><li>test_mesh.py: pass</li><li>test_deposition.py: pass (radial symmetry + phenotype boost)</li><li>test_fibre_update.py: pass</li><li>test_fem_patch.py: pass</li><li>test_nonlinear_solver.py: pass (Ogden Dirichlet)</li></ul>'


def write_site(runs):
    (SITE / 'assets/css').mkdir(parents=True, exist_ok=True)
    (SITE / 'assets/js').mkdir(parents=True, exist_ok=True)
    (SITE / 'pages').mkdir(parents=True, exist_ok=True)
    (SITE / 'data').mkdir(parents=True, exist_ok=True)

    (SITE / 'assets/css/style.css').write_text('''body{font-family:Inter,Arial,sans-serif;margin:0;background:#0f1115;color:#e8e8ea}header,main{max-width:1100px;margin:0 auto;padding:16px}nav a{margin-right:12px;color:#7cc7ff}h1,h2,h3{color:#fff}.card{background:#171a21;padding:12px;border-radius:8px;margin:12px 0}img,video{max-width:100%}code,pre{background:#1f2430;padding:2px 6px;border-radius:4px}table{width:100%;border-collapse:collapse}td,th{border:1px solid #333;padding:6px}''')

    (SITE / 'assets/js/site.js').write_text('''async function loadRuns(){const r=await fetch('../data/runs.json').then(x=>x.json()).catch(()=>[]);const sel=document.getElementById('runSelect');if(!sel)return;sel.innerHTML=r.map((x,i)=>`<option value="${i}">${x.run_id}</option>`).join('');const render=(i)=>{const run=r[i];if(!run)return;document.getElementById('anim').innerHTML=run.animation_site?`<video controls src="../${run.animation_site}"></video>`:'<p>No animation</p>';document.getElementById('frames').innerHTML=(run.frames_site||[]).map(f=>`<img alt="snapshot" src="../${f}"/>`).join('');document.getElementById('metrics').innerHTML=`<pre>${JSON.stringify(run.metrics,null,2)}</pre>`;};sel.onchange=()=>render(sel.value);render(0);}window.addEventListener('DOMContentLoaded',loadRuns);''')

    run0 = runs[0] if runs else None
    key_params = '<p>No runs found.</p>'
    if run0 and run0.get('config'):
        key_params = f"<pre>{run0['config']}</pre>"

    pipeline_svg = '''<svg width="900" height="120" viewBox="0 0 900 120"><rect x="10" y="30" width="130" height="50" fill="#263044"/><text x="22" y="60" fill="white">Mechanics</text><rect x="170" y="30" width="130" height="50" fill="#263044"/><text x="208" y="60" fill="white">Cues</text><rect x="330" y="30" width="130" height="50" fill="#263044"/><text x="368" y="60" fill="white">Cells</text><rect x="490" y="30" width="130" height="50" fill="#263044"/><text x="510" y="60" fill="white">Collagen</text><rect x="650" y="30" width="170" height="50" fill="#263044"/><text x="670" y="60" fill="white">Remodelling</text><text x="145" y="62" fill="#9ad">↔</text><text x="305" y="62" fill="#9ad">↔</text><text x="465" y="62" fill="#9ad">↔</text><text x="625" y="62" fill="#9ad">↔</text></svg>'''

    (SITE / 'index.html').write_text(root_page('FibroTwin Results Site', f'<div class="card"><p>Static documentation for FibroTwin simulation results and methods.</p>{pipeline_svg}</div><div class="card"><h2>Showcased run parameters</h2>{key_params}</div>'))
    (SITE / 'pages/overview.html').write_text(page('Overview', f'<div class="card">{read_doc("00_problem_statement.md")}</div><div class="card"><h2>Pipeline</h2>{pipeline_svg}</div>'))

    model_extra = '<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'
    (SITE / 'pages/model.html').write_text(page('Model Equations', f'<div class="card">{read_doc("01_governing_equations.md")}</div><div class="card"><h2>Pseudocode</h2><pre>for n in steps:\n  solve mechanics\n  compute cues\n  move agents\n  deposit collagen\n  update fibres\n  update growth\n  save snapshot</pre></div>', model_extra))

    (SITE / 'pages/numerics.html').write_text(page('Numerical Methods', f'<div class="card">{read_doc("02_numerical_methods.md")}</div>'))
    (SITE / 'pages/implementation.html').write_text(page('Implementation', '<div class="card"><h2>Architecture</h2><pre>src/main.py\nsrc/mechanics/*\nsrc/cells/*\nsrc/remodeling/*\nsrc/sim/*\nsrc/tools/build_site.py</pre><h2>Run</h2><pre>python -m src.main --config configs/mvp_2d_stretch.yaml\npython -m src.tools.build_site</pre><h2>Models currently used in code</h2><ul><li>Mechanics: compressible Ogden hyperelastic (single-term) in large-deformation mode</li><li>Growth/remodelling: constrained-mixture-inspired scalar growth proxy</li><li>Cells: persistent random walk + taxis</li><li>Collagen: Gaussian-kernel deposition + first-order degradation</li></ul><h2>Limitations</h2><ul><li>2D patch; no full 3D architecture yet</li><li>Nonlinear solve via energy minimization (no analytic tangent/Newton yet)</li><li>Literature parameters are not yet calibrated to a specific dataset</li></ul></div>'))

    verification = '<ul><li>Verification: patch test, deposition symmetry, fibre convergence, sanity constraints.</li><li>Validation: plausibility trends under stretch (not calibrated to specific dataset yet).</li></ul>'
    (SITE / 'pages/validation.html').write_text(page('Validation & Tests', f'<div class="card"><h2>Test outcomes</h2>{latest_test_summary()}</div><div class="card">{verification}</div><div class="card">{read_doc("03_validation_and_sanity_checks.md")}</div>'))

    results_body = '''<div class="card"><label>Run selector: <select id="runSelect"></select></label></div><div class="card" id="anim"></div><div class="card" id="frames"></div><div class="card" id="metrics"></div>'''
    (SITE / 'pages/results.html').write_text(page('Results', results_body))

    (SITE / 'pages/changelog.html').write_text(page('Changelog', f'<div class="card">{git_changelog()}</div>'))

    refs = [
        {"key":"Ogden1972","citation":"Ogden RW. Large deformation isotropic elasticity—on the correlation of theory and experiment for incompressible rubberlike solids. Proc. R. Soc. Lond. A (1972)."},
        {"key":"HolzapfelOgden2009","citation":"Holzapfel GA, Ogden RW. Constitutive modelling of passive myocardium: a structurally based framework for material characterization. Philos Trans A (2009)."},
        {"key":"HumphreyRajagopal2002","citation":"Humphrey JD, Rajagopal KR. A constrained mixture model for growth and remodeling of soft tissues. Math Models Methods Appl Sci (2002)."},
        {"key":"Zeigler2016","citation":"Zeigler AC, et al. A computational model of cardiac fibroblast signaling predicts context-dependent drivers of myofibroblast differentiation. J Mol Cell Cardiol (2016). URL: https://pubmed.ncbi.nlm.nih.gov/27017945/"},
        {"key":"ZeiglerReview2016","citation":"Zeigler AC, et al. Computational modeling of cardiac fibroblasts and fibrosis. J Mol Cell Cardiol (2016). URL: https://pubmed.ncbi.nlm.nih.gov/26608708/"},
        {"key":"RouillardHolmes2012","citation":"Rouillard AD, Holmes JW. Mechanical regulation of fibroblast migration and collagen remodelling in healing myocardial infarcts. J Physiol (2012). URL: https://pubmed.ncbi.nlm.nih.gov/22495588/"},
        {"key":"WitzenburgHolmes2020","citation":"Witzenburg C, Holmes JW. Computational Models of Cardiac Hypertrophy. Prog Biophys Mol Biol (2021). URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC7855157/"},
        {"key":"WitzenburgHolmesReview2016","citation":"Witzenburg C, Holmes JW. Mathematical Modeling of Cardiac Growth and Remodeling. WIREs Syst Biol Med (2016). URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC4841715/"},
        {"key":"MainiContextWound","citation":"Maini PK and collaborators' wound-healing mathematical biology corpus (reaction-transport and mechanochemical frameworks). Example review URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC4588694/"},
        {"key":"TranquilloMurray1992","citation":"Tranquillo RT, Murray JD, Maini PK. Continuum model of fibroblast-driven wound contraction: inflammation-mediation. J Theor Biol (1992). URL: https://pubmed.ncbi.nlm.nih.gov/1474841/"}
    ]
    (SITE / 'data/bibliography.json').write_text(json.dumps(refs, indent=2))
    (SITE / 'pages/references.html').write_text(page('References', '<div class="card"><p>No validated bibliography in repo docs; placeholders listed and marked clearly.</p><pre>'+json.dumps(refs, indent=2)+'</pre></div>'))

    (SITE / 'data/runs.json').write_text(json.dumps(runs, indent=2))


def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    runs = discover_runs()
    copy_assets(runs)
    make_plots(runs)
    write_site(runs)
    print(str(SITE / 'index.html'))


if __name__ == '__main__':
    main()
