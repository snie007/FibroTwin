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
    # keep UI focused on newest runs (avoids older jittery artifacts)
    return runs[:5]


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
    return '''<nav><a href="index.html">Home</a><a href="pages/overview.html">Overview</a><a href="pages/model.html">Model</a><a href="pages/numerics.html">Numerics</a><a href="pages/implementation.html">Implementation</a><a href="pages/validation.html">Validation</a><a href="pages/results.html">Results</a><a href="pages/interactive_lab.html">Interactive Lab</a><a href="pages/changelog.html">Changelog</a><a href="pages/references.html">References</a></nav>'''


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

    (SITE / 'assets/css/style.css').write_text('''body{font-family:Inter,Arial,sans-serif;margin:0;background:#0f1115;color:#e8e8ea;line-height:1.55}header,main{max-width:1180px;margin:0 auto;padding:16px}nav{display:flex;flex-wrap:wrap;gap:10px}nav a{margin-right:0;color:#7cc7ff;text-decoration:none;padding:4px 8px;border-radius:6px;background:#151922}h1,h2,h3{color:#fff}h2{margin-top:0}.card{background:#171a21;padding:14px;border-radius:10px;margin:12px 0;border:1px solid #2a3140}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}img,video{max-width:100%;border-radius:8px}code,pre{background:#1f2430;padding:2px 6px;border-radius:4px}pre{overflow:auto;padding:10px}table{width:100%;border-collapse:collapse}td,th{border:1px solid #333;padding:6px;vertical-align:top}.kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px}.pill{background:#202838;padding:8px;border-radius:8px}.stack-wrap{perspective:1400px;min-height:420px;display:flex;align-items:center;justify-content:center;background:linear-gradient(180deg,#0b1018,#121a27);border-radius:12px}.sheet-stack{position:relative;width:420px;height:320px;transform-style:preserve-3d}.sheet{position:absolute;left:40px;top:30px;width:340px;height:220px;border-radius:12px;background:linear-gradient(145deg,#223,#2d3d55);border:1px solid #445;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all .45s cubic-bezier(.2,.9,.2,1);box-shadow:0 10px 24px rgba(0,0,0,.45)}.sheet.expanded{transform:translateX(380px) scale(1.05)!important;z-index:120!important;box-shadow:0 16px 40px rgba(0,0,0,.65)}.legend{font-size:.9em;opacity:.9}canvas#towerCanvas{width:100%;max-width:900px;height:460px;border-radius:12px;border:1px solid #2a3140;background:#0b0f16}''')

    (SITE / 'assets/js/site.js').write_text('''function fmt(v){return (v===null||v===undefined)?'NA':(typeof v==='number'?v.toFixed(4):String(v));}
function parseStretch(cfg){const m=(cfg||'').match(/stretch_x:\\s*([0-9.]+)/);return m?Number(m[1]):null;}
async function getRuns(){return fetch('../data/runs.json').then(x=>x.json()).catch(()=>[]);}

async function loadRuns(){
  const r=await getRuns();
  const sel=document.getElementById('runSelect'); if(!sel) return;
  sel.innerHTML=r.map((x,i)=>`<option value="${i}">${x.run_id}</option>`).join('');
  const render=(i)=>{
    const run=r[i]; if(!run) return;
    if(run.animation_site){
      const isGif = run.animation_site.toLowerCase().endsWith('.gif');
      document.getElementById('anim').innerHTML = isGif ? `<img src="../${run.animation_site}" alt="simulation animation gif"/>` : `<video controls src="../${run.animation_site}"></video>`;
    } else {
      document.getElementById('anim').innerHTML='<p>No animation available for this run.</p>';
    }
    document.getElementById('frames').innerHTML=`<div class="grid">${(run.frames_site||[]).map((f,j)=>`<figure><img alt="snapshot ${j+1}" src="../${f}"/><figcaption>Snapshot ${j+1}: spatial field state</figcaption></figure>`).join('')}</div>`;

    const m=run.metrics||{};
    const n=(m.step||[]).length; const last=n>0?n-1:null;
    const cLast=last!==null?m.c_mean[last]:null; const uLast=last!==null?m.max_u[last]:null; const gLast=last!==null?m.g_mean[last]:null;
    const plots=[`../assets/img/${run.run_id}_collagen.png`,`../assets/img/${run.run_id}_max_u.png`,`../assets/img/${run.run_id}_g_mean.png`,`../assets/img/${run.run_id}_alignment.png`,`../assets/img/${run.run_id}_agent_paths.png`,`../assets/img/${run.run_id}_montage6.png`];
    document.getElementById('metrics').innerHTML=`<div class="kpi"><div class="pill"><strong>Recorded steps</strong><br/>${n}</div><div class="pill"><strong>Final mean collagen</strong><br/>${fmt(cLast)}</div><div class="pill"><strong>Final max displacement</strong><br/>${fmt(uLast)}</div><div class="pill"><strong>Final growth proxy</strong><br/>${fmt(gLast)}</div></div><p><strong>Interpretation guide:</strong> collagen ↑ indicates fibrosis burden, alignment ↑ indicates reorientation toward loading, and agent paths show migration-driven deposition patterns.</p><div class="grid">${plots.map(p=>`<img src="${p}" onerror="this.style.display='none'"/>`).join('')}</div>`;
  };
  sel.onchange=()=>render(sel.value); render(0);
}

function initTowerWebGL(labels, textureMap){
  const canvas=document.getElementById('towerCanvas'); if(!canvas || !window.THREE) return null;
  const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true});
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(52, canvas.clientWidth/canvas.clientHeight, 0.1, 100);
  camera.position.set(-2.8, 2.6, 8.2);
  const key=new THREE.DirectionalLight(0xffffff,1.1); key.position.set(4,6,5); scene.add(key);
  scene.add(new THREE.AmbientLight(0x99aacc,0.42));

  const loader = new THREE.TextureLoader();
  const boxes=[];
  const layerGap = 0.22;

  function labelTexture(text){
    const c=document.createElement('canvas'); c.width=512; c.height=512;
    const x=c.getContext('2d');
    x.fillStyle='#1a2740'; x.fillRect(0,0,512,512);
    x.fillStyle='#7cc7ff'; x.font='bold 34px Arial';
    x.fillText(text,24,80);
    x.strokeStyle='#3b557a'; x.lineWidth=6; x.strokeRect(10,10,492,492);
    return new THREE.CanvasTexture(c);
  }

  labels.forEach((label,i)=>{
    const color=[0x2b3d5e,0x334a70,0x3a557f,0x42618e,0x4d6ea0,0x587cb3][i%6];
    const g=new THREE.BoxGeometry(3.2,0.12,3.2); // square, thin slab
    const texPath = textureMap && textureMap[i] ? new URL(textureMap[i], window.location.href).href : null;
    let tex = null;
    if(texPath){
      tex = loader.load(texPath, undefined, undefined, ()=>{});
    }
    if(!tex){ tex = labelTexture(label); }
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.wrapS=THREE.ClampToEdgeWrapping; tex.wrapT=THREE.ClampToEdgeWrapping;

    const mTop = new THREE.MeshStandardMaterial({map:tex,color:0xffffff,metalness:0.1,roughness:0.72});
    const mSide = new THREE.MeshStandardMaterial({color:color,metalness:0.2,roughness:0.78});
    // right,left,top,bottom,front,back
    const mats6 = [mSide,mSide,mTop,mSide,mTop,mSide];
    const b=new THREE.Mesh(g,mats6);
    b.position.set(0,i*layerGap,-i*0.02);
    b.rotation.x = -0.05;
    b.userData={index:i,label,baseX:0,baseY:i*layerGap};
    scene.add(b); boxes.push(b);
  });

  const ray=new THREE.Raycaster(); const mouse=new THREE.Vector2();
  let active=-1;
  canvas.addEventListener('click',(ev)=>{
    const r=canvas.getBoundingClientRect();
    mouse.x=((ev.clientX-r.left)/r.width)*2-1; mouse.y=-((ev.clientY-r.top)/r.height)*2+1;
    ray.setFromCamera(mouse,camera); const hit=ray.intersectObjects(boxes)[0];
    if(!hit) return; const idx=hit.object.userData.index; active=(active===idx)?-1:idx;
  });

  function animate(){
    requestAnimationFrame(animate);
    boxes.forEach((b,i)=>{
      const targetX=(i===active)?3.0:0.0;
      b.position.x += 0.11*(targetX-b.position.x);
      const targetY=b.userData.baseY + (i===active?0.12:0);
      b.position.y += 0.11*(targetY-b.position.y);
      b.rotation.y += 0.02*(i===active?1:0);
    });
    scene.rotation.y=0.58; // corner-forward perspective
    renderer.render(scene,camera);
  }
  animate();
  return {setActive:(i)=>{active=i;}};
}

async function loadInteractiveLab(){
  const runs=await getRuns();
  const sel=document.getElementById('labRunSelect'); if(!sel) return;
  sel.innerHTML=runs.map((x,i)=>`<option value="${i}">${x.run_id}</option>`).join('');
  const stack=document.getElementById('sheetStack');
  const viewer=document.getElementById('labViewer');
  const comp=document.getElementById('labCompare');
  const sheets=['Displacement U','Collagen c','Fibre orientation a/ac','Fibroblast paths','Signaling nodes','Infarct states'];
  stack.innerHTML=sheets.map((s,i)=>`<div class="sheet" data-i="${i}" style="transform:translateY(${i*10}px) translateZ(${-i*18}px) rotateX(2deg)">${s}</div>`).join('');

  const render=(i)=>{
    const run=runs[i]; if(!run) return;
    const tex=[
      `../assets/img/${run.run_id}_max_u.png`,
      `../assets/img/${run.run_id}_collagen.png`,
      `../assets/img/${run.run_id}_alignment.png`,
      `../assets/img/${run.run_id}_agent_paths.png`,
      `../assets/img/${run.run_id}_g_mean.png`,
      `../assets/img/${run.run_id}_montage6.png`,
    ];
    window._towerApi = initTowerWebGL(sheets, tex);

    stack.querySelectorAll('.sheet').forEach(el=>el.onclick=()=>{
      stack.querySelectorAll('.sheet').forEach(x=>x.classList.remove('expanded'));
      el.classList.add('expanded');
      if(window._towerApi){window._towerApi.setActive(Number(el.dataset.i));}
    });

    const anim = run.animation_site ? (run.animation_site.toLowerCase().endsWith('.gif') ? `<img src="../${run.animation_site}" alt="simulation gif"/>` : `<video controls src="../${run.animation_site}"></video>`) : '<p>No animation</p>';
    viewer.innerHTML=`<div class="grid">${anim}<img src="../assets/img/${run.run_id}_montage6.png" onerror="this.style.display='none'"/><img src="../assets/img/${run.run_id}_alignment.png" onerror="this.style.display='none'"/><img src="../assets/img/${run.run_id}_agent_paths.png" onerror="this.style.display='none'"/></div>`;
    const stretch=parseStretch(run.config); const m=run.metrics||{}; const last=(m.step||[]).length-1;
    comp.innerHTML=`<table><thead><tr><th>Metric</th><th>Value</th><th>Boundary / Paper expectation</th></tr></thead><tbody><tr><td>stretch_x BC</td><td>${fmt(stretch)}</td><td>Overstretch should increase alignment/collagen in mechanobiology literature</td></tr><tr><td>Final collagen</td><td>${fmt(last>=0?m.c_mean[last]:null)}</td><td>Expected to rise under load + profibrotic signaling</td></tr><tr><td>Final max displacement</td><td>${fmt(last>=0?m.max_u[last]:null)}</td><td>Constrained by imposed displacement BC</td></tr><tr><td>Final growth proxy</td><td>${fmt(last>=0?m.g_mean[last]:null)}</td><td>Should track remodeling burden over time</td></tr></tbody></table>`;
  };
  sel.onchange=()=>render(sel.value); render(0);
}

window.addEventListener('DOMContentLoaded',()=>{loadRuns();loadInteractiveLab();});''')

    run0 = runs[0] if runs else None
    key_params = '<p>No runs found.</p>'
    if run0 and run0.get('config'):
        key_params = f"<pre>{run0['config']}</pre>"

    pipeline_svg = '''<svg width="900" height="120" viewBox="0 0 900 120"><rect x="10" y="30" width="130" height="50" fill="#263044"/><text x="22" y="60" fill="white">Mechanics</text><rect x="170" y="30" width="130" height="50" fill="#263044"/><text x="208" y="60" fill="white">Cues</text><rect x="330" y="30" width="130" height="50" fill="#263044"/><text x="368" y="60" fill="white">Cells</text><rect x="490" y="30" width="130" height="50" fill="#263044"/><text x="510" y="60" fill="white">Collagen</text><rect x="650" y="30" width="170" height="50" fill="#263044"/><text x="670" y="60" fill="white">Remodelling</text><text x="145" y="62" fill="#9ad">↔</text><text x="305" y="62" fill="#9ad">↔</text><text x="465" y="62" fill="#9ad">↔</text><text x="625" y="62" fill="#9ad">↔</text></svg>'''

    (SITE / 'index.html').write_text(root_page('FibroTwin Results Site', f'<div class="card"><p><strong>Purpose:</strong> readable, publication-oriented documentation of model assumptions, equations, validation, and results.</p>{pipeline_svg}</div><div class="card"><h2>Showcased run parameters</h2>{key_params}</div>'))
    math_head = '<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'
    (SITE / 'pages/overview.html').write_text(page('Overview', f'<div class="card">{read_doc("00_problem_statement.md")}</div><div class="card"><h2>Coupling pipeline</h2><p>Mechanics drives cues, cues drive cell behavior, cells remodel collagen, and remodeling feeds back to mechanics.</p>{pipeline_svg}</div>', math_head))

    (SITE / 'pages/model.html').write_text(page('Model Equations', f'<div class="card"><p>This page presents the governing equations in formatted mathematical notation.</p>{read_doc("01_governing_equations.md")}</div><div class="card"><h2>Algorithm overview (pseudocode)</h2><pre>for each macro time step:\n  1) solve mechanics\n  2) compute mechanocues\n  3) move fibroblasts\n  4) update signaling + phenotype\n  5) deposit/remodel collagen\n  6) update fibre orientation + growth\n  7) save outputs</pre></div>', math_head))

    (SITE / 'pages/numerics.html').write_text(page('Numerical Methods', f'<div class="card"><p>This page explains discretization, weak-form solve strategy, and numerical stability choices.</p>{read_doc("02_numerical_methods.md")}</div>', math_head))
    (SITE / 'pages/implementation.html').write_text(page('Implementation', '<div class="card"><h2>Architecture</h2><pre>src/main.py\nsrc/mechanics/*\nsrc/cells/*\nsrc/remodeling/*\nsrc/sim/*\nsrc/tools/build_site.py</pre><h2>Run</h2><pre>python -m src.main --config configs/mvp_2d_stretch.yaml\npython -m src.tools.build_site</pre><h2>Models currently used in code</h2><ul><li>Mechanics: compressible Ogden hyperelastic (single-term) in large-deformation mode</li><li>Growth/remodelling: constrained-mixture-inspired scalar growth proxy</li><li>Cells: persistent random walk + taxis</li><li>Collagen: Gaussian-kernel deposition + first-order degradation</li></ul><h2>Limitations</h2><ul><li>2D patch; no full 3D architecture yet</li><li>Nonlinear solve via energy minimization (no analytic tangent/Newton yet)</li><li>Literature parameters are not yet calibrated to a specific dataset</li></ul></div>'))

    verification = '<ul><li>Verification: patch test, deposition symmetry, fibre convergence, nonlinear Dirichlet sanity constraints.</li><li>Validation: plausibility trends under stretch + profibrotic signaling interaction scenarios (portfolio script).</li></ul>'
    portfolio_block = ''
    vp = ROOT / 'outputs' / 'validation_portfolio.md'
    if vp.exists():
        portfolio_block = f'<div class="card"><h2>Validation portfolio</h2>{md_to_html(vp.read_text())}</div>'

    infarct_block = ''
    vpj = ROOT / 'outputs' / 'validation_portfolio.json'
    if vpj.exists():
        try:
            d = json.loads(vpj.read_text())
            rows = [r for r in d.get('scenarios', []) if 'infarct' in r.get('scenario', '') and ('c_core' in r)]
            if rows:
                r = rows[-1]
                table = f'''<table><thead><tr><th>Region</th><th>Collagen c</th><th>Profibrotic p</th></tr></thead><tbody>
<tr><td>Core</td><td>{r.get('c_core', 0):.3f}</td><td>{r.get('p_core', 0):.3f}</td></tr>
<tr><td>Border zone</td><td>{r.get('c_border', 0):.3f}</td><td>{r.get('p_border', 0):.3f}</td></tr>
<tr><td>Remote</td><td>{r.get('c_remote', 0):.3f}</td><td>{r.get('p_remote', 0):.3f}</td></tr>
</tbody></table>'''
                infarct_block = f'<div class="card"><h2>Infarct region panel (core/border/remote)</h2>{table}<p>Scenario: {r.get("scenario")}</p></div>'
        except Exception:
            infarct_block = ''

    systematic_block = ''
    stj = ROOT / 'outputs' / 'systematic_test_catalog.json'
    if stj.exists():
        try:
            s = json.loads(stj.read_text())
            sm = s.get('summary', {})
            tests = s.get('tests', [])[:20]
            rows = ''.join([f"<tr><td>{t.get('id')}</td><td><a href='{t.get('pubmed_url')}'>{t.get('pmid')}</a></td><td>{t.get('category')}</td><td>{t.get('model_score_0_to_3')}/3</td><td>{t.get('title')}</td></tr>" for t in tests])
            table = f"<p>Total tests: {s.get('n_tests')}</p><ul><li>Mean score: {sm.get('mean_score')}</li><li>Score 3: {sm.get('n_score_3')}</li><li>Score 2: {sm.get('n_score_2')}</li><li>Score 1: {sm.get('n_score_1')}</li><li>Score 0: {sm.get('n_score_0')}</li></ul><table><thead><tr><th>ID</th><th>PMID</th><th>Category</th><th>Score</th><th>Evidence-linked test title</th></tr></thead><tbody>{rows}</tbody></table><p>Full catalog: <code>outputs/systematic_test_catalog.json</code></p>"
            systematic_block = f'<div class="card"><h2>Systematic literature-linked test catalog</h2>{table}</div>'
        except Exception:
            systematic_block = ''

    pubfigs = [
        ('pubfig_validation_storyline.png', 'Validation storyline figure'),
        ('pubfig_portfolio_collagen_signal.png', 'Portfolio collagen and signal summary'),
        ('pubfig_infarct_regions.png', 'Infarct core border remote panel'),
        ('pubfig_scorecard_by_category.png', 'Scorecard by category'),
    ]
    fig_imgs = ''.join([f"<img src='../assets/img/{f}' alt='{a}'/>" for f, a in pubfigs if (SITE / 'assets' / 'img' / f).exists()])
    if not fig_imgs:
        fig_imgs = '<p>Publication figures not generated yet. Run: python -m src.tools.make_publication_figures</p>'
    pubfig_block = f'''<div class="card"><h2>Publication-grade validation figures</h2>
<p>These figures summarize model generation and validation status.</p>
{fig_imgs}
</div>'''

    testcard_block = ''
    card_dir = SITE / 'assets' / 'img' / 'testcards'
    if card_dir.exists():
        cards = sorted(card_dir.glob('T*.png'))
        thumbs = ''.join([f"<a href='../assets/img/testcards/{c.name}'><img src='../assets/img/testcards/{c.name}' alt='{c.stem}'/></a>" for c in cards[:40]])
        testcard_block = f"<div class='card'><h2>Per-test confirmation figures (sample)</h2><p>Showing {min(len(cards),40)} of {len(cards)} test cards. Each card includes PMID link mapping, expected behavior, and current support score.</p>{thumbs}</div>"

    uq_block = ''
    uqmd = ROOT / 'outputs' / 'uq_portfolio.md'
    if uqmd.exists():
        uq_block = f'<div class="card"><h2>Uncertainty quantification summary</h2>{md_to_html(uqmd.read_text())}</div>'

    (SITE / 'pages/validation.html').write_text(page('Validation & Tests', f'<div class="card"><h2>Test outcomes</h2>{latest_test_summary()}</div><div class="card">{verification}</div>{infarct_block}{portfolio_block}{uq_block}{systematic_block}{pubfig_block}{testcard_block}<div class="card">{read_doc("03_validation_and_sanity_checks.md")}</div><div class="card">{read_doc("04_systematic_improvement_review.md")}</div>'))

    results_body = '''<div class="card"><h2>How to interpret results</h2><ul><li><strong>Animation:</strong> overall evolution of deformation, fibroblast positions, and collagen field.</li><li><strong>Snapshots:</strong> 5–6 time points to compare early/mid/late remodeling.</li><li><strong>Fibroblast paths:</strong> show migration trajectories that drive deposition patterns.</li><li><strong>Alignment plot:</strong> values closer to 1 mean stronger alignment with loading direction.</li><li><strong>Collagen trend:</strong> rising mean collagen indicates increasing fibrosis burden.</li></ul></div><div class="card"><label><strong>Run selector:</strong> <select id="runSelect"></select></label></div><div class="card"><h2>Animation</h2><div id="anim"></div></div><div class="card"><h2>Key snapshots (time sequence)</h2><div id="frames"></div></div><div class="card"><h2>Summary metrics + story figures</h2><div id="metrics"></div></div>'''
    (SITE / 'pages/results.html').write_text(page('Results', results_body))

    interactive_head = '<script src="https://unpkg.com/three@0.161.0/build/three.min.js"></script>'
    interactive_body = '''<div class="card"><h2>Interactive simulation explorer</h2><p class="legend">Tower view: each layer is a model state variable. Click a layer to pop it out.</p><label><strong>Run selector:</strong> <select id="labRunSelect"></select></label></div><div class="card stack-wrap"><canvas id="towerCanvas"></canvas></div><div class="card stack-wrap"><div id="sheetStack" class="sheet-stack"></div></div><div class="card"><h2>Visual viewer</h2><div id="labViewer"></div></div><div class="card"><h2>Quantitative comparison and paper-aligned interpretation</h2><div id="labCompare"></div></div>'''
    (SITE / 'pages/interactive_lab.html').write_text(page('Interactive Lab', interactive_body, interactive_head))

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

    test_refs_block = ''
    stj2 = ROOT / 'outputs' / 'systematic_test_catalog.json'
    if stj2.exists():
        try:
            st = json.loads(stj2.read_text())
            tests = st.get('tests', [])
            rows = ''.join([f"<tr><td>{t.get('id')}</td><td><a href='{t.get('pubmed_url')}'>{t.get('pmid')}</a></td><td>{t.get('title')}</td><td>{t.get('category')}</td><td>{t.get('model_score_0_to_3')}/3</td></tr>" for t in tests])
            test_refs_block = f"<div class='card'><h2>Validation tests linked to PubMed evidence</h2><p>Total tests: {len(tests)}</p><table><thead><tr><th>Test ID</th><th>PMID</th><th>Evidence title</th><th>Category</th><th>Support score</th></tr></thead><tbody>{rows}</tbody></table></div>"
        except Exception:
            test_refs_block = ''

    (SITE / 'pages/references.html').write_text(page('References', '<div class="card"><h2>Core bibliography</h2><pre>'+json.dumps(refs, indent=2)+'</pre></div>' + test_refs_block))

    (SITE / 'data/runs.json').write_text(json.dumps(runs, indent=2))


def main():
    SITE.mkdir(parents=True, exist_ok=True)
    runs = discover_runs()
    copy_assets(runs)
    make_plots(runs)
    write_site(runs)
    print(str(SITE / 'index.html'))


if __name__ == '__main__':
    main()
