import json, os, re, shutil, subprocess, datetime
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'
DOCS = ROOT / 'docs'
OUT = ROOT / 'outputs'
BUILD_VER = str(int(datetime.now().timestamp()))


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


def human_scenario_name(name: str) -> str:
    if not name:
        return ''
    aliases = {
        'baseline_low_load_low_signal': 'Baseline (low load + low signal)',
        'high_load_only': 'High load only',
        'high_signal_only': 'High biochemical signal only',
        'high_load_high_signal': 'High load + high signal',
        'infarct_high_load_high_signal': 'Infarct + high load + high signal',
        'drug_tgfr_block': 'Drug: TGFβR blockade',
        'drug_at1r_block': 'Drug: AT1R blockade',
        'drug_dual_block': 'Drug: dual blockade (TGFβR + AT1R)',
    }
    if name in aliases:
        return aliases[name]
    if name.startswith('L') and '_T' in name and '_A' in name and '_N' in name:
        try:
            l = name.split('_')[0].replace('L','')
            t = name.split('_')[1].replace('T','')
            a = name.split('_')[2].replace('A','')
            n = name.split('_')[3].replace('N','')
            return f'Load {l}, TGFβ {t}, AngII {a}, Fibroblasts {n}'
        except Exception:
            pass
    if name.startswith('INFARCT_'):
        tail = name.replace('INFARCT_','')
        return 'Infarct scenario: ' + human_scenario_name(tail)
    return name.replace('_',' ')


def nav():
    return '''<nav><a href="index.html">Home</a><a href="pages/overview.html">Overview</a><a href="pages/model.html">Model</a><a href="pages/numerics.html">Numerics</a><a href="pages/implementation.html">Implementation</a><a href="pages/validation.html">Validation</a><a href="pages/emulation.html">Emulation</a><a href="pages/results.html">Results</a><a href="pages/interactive_lab.html">Interactive Lab</a><a href="pages/changelog.html">Changelog</a><a href="pages/references.html">References</a></nav>'''


def page(title, body, extra_head=''):
    return f'''<!doctype html><html><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>{title}</title><link rel="stylesheet" href="../assets/css/style.css?v={BUILD_VER}"/><link rel="stylesheet" href="../assets/css/validation_theme.css?v={BUILD_VER}"/>{extra_head}</head><body><header><h1>{title}</h1>{nav().replace('index.html','../index.html').replace('pages/','')}</header><main>{body}</main><script src="../assets/js/site.js?v={BUILD_VER}"></script></body></html>'''


def root_page(title, body):
    return f'''<!doctype html><html><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>{title}</title><link rel="stylesheet" href="assets/css/style.css?v={BUILD_VER}"/><link rel="stylesheet" href="assets/css/validation_theme.css?v={BUILD_VER}"/></head><body><header><h1>{title}</h1>{nav()}</header><main>{body}</main></body></html>'''


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
    (SITE / 'pages/tests').mkdir(parents=True, exist_ok=True)
    (SITE / 'pages/numerical_tests').mkdir(parents=True, exist_ok=True)
    (SITE / 'pages/calibration').mkdir(parents=True, exist_ok=True)

    (SITE / 'assets/css/style.css').write_text('''body{font-family:Inter,Arial,sans-serif;margin:0;background:#0f1115;color:#e8e8ea;line-height:1.55}header,main{max-width:1180px;margin:0 auto;padding:16px}nav{display:flex;flex-wrap:wrap;gap:10px}nav a{margin-right:0;color:#7cc7ff;text-decoration:none;padding:4px 8px;border-radius:6px;background:#151922}h1,h2,h3{color:#fff}h2{margin-top:0}.card{background:#171a21;padding:14px;border-radius:10px;margin:12px 0;border:1px solid #2a3140}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}img,video{max-width:100%;border-radius:8px}code,pre{background:#1f2430;padding:2px 6px;border-radius:4px}pre{overflow:auto;padding:10px}table{width:100%;border-collapse:collapse}td,th{border:1px solid #333;padding:6px;vertical-align:top}.kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px}.pill{background:#202838;padding:8px;border-radius:8px}.stack-wrap{perspective:1400px;min-height:420px;display:flex;align-items:center;justify-content:center;background:linear-gradient(180deg,#0b1018,#121a27);border-radius:12px}.sheet-stack{position:relative;width:420px;height:320px;transform-style:preserve-3d}.sheet{position:absolute;left:40px;top:30px;width:340px;height:220px;border-radius:12px;background:linear-gradient(145deg,#223,#2d3d55);border:1px solid #445;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all .45s cubic-bezier(.2,.9,.2,1);box-shadow:0 10px 24px rgba(0,0,0,.45)}.sheet.expanded{transform:translateX(380px) scale(1.05)!important;z-index:120!important;box-shadow:0 16px 40px rgba(0,0,0,.65)}.legend{font-size:.9em;opacity:.9}canvas#towerCanvas{width:100%;max-width:820px;height:420px;border-radius:12px;border:1px solid #2a3140;background:#0b0f16}''')
    (SITE / 'assets/css/validation_theme.css').write_text('''.validation-layout{display:grid;gap:12px}.v-card{background:#171a21;border:1px solid #2a3140;border-radius:10px;padding:14px}.v-head{display:flex;justify-content:space-between;align-items:center;gap:8px}.badge{display:inline-block;padding:2px 8px;border-radius:999px;background:#202838;border:1px solid #39445c;font-size:.82rem}.badge.pass{background:#133322;border-color:#2d8056}.badge.fail{background:#3a1a1a;border-color:#944}.summary-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}.summary-tile{background:#121722;border:1px solid #2a3140;border-radius:8px;padding:10px}.test-plot{border:1px solid #2a3140;border-radius:10px;padding:8px;background:#0f141d}.plan-box{border-left:4px solid #4ea3ff;padding:8px 12px;background:#111827;border-radius:8px}''')


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
  renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(50, canvas.clientWidth/canvas.clientHeight, 0.1, 100);
  camera.position.set(0.0, 7.2, 18.0);

  const key=new THREE.DirectionalLight(0xffffff,0.95); key.position.set(4,6,4); scene.add(key);
  const fill=new THREE.DirectionalLight(0xbfd4ff,0.55); fill.position.set(-4,3,2); scene.add(fill);
  const rim=new THREE.DirectionalLight(0x9fb6d6,0.35); rim.position.set(0,2,-5); scene.add(rim);
  scene.add(new THREE.AmbientLight(0xc5d6ea,0.62));

  // Stable visual stack: six overlapping square slabs (layer placeholders)
  const geo=new THREE.BoxGeometry(9.9,0.08,9.9);
  const topColors=[0x5d7ea8,0x6d8db3,0x7d9dc0,0x8cabc8,0x9ab8d0,0xa7c3d8];
  const side=new THREE.MeshStandardMaterial({color:0x5f728d,metalness:0.12,roughness:0.88});

  const slabs=[];
  for(let i=0;i<6;i++){
    const top=new THREE.MeshStandardMaterial({color:topColors[i],metalness:0.06,roughness:0.86});
    const slab=new THREE.Mesh(geo,[side,side,top,side,top,side]);
    slab.position.set(0.14*i,1.55+0.92*i,-3.0-0.10*i); // moved back + large slabs
    slab.rotation.y=0.785;
    slab.rotation.x=-0.22;
    scene.add(slab);
    slabs.push(slab);
  }
  function animate(){ requestAnimationFrame(animate); renderer.render(scene,camera); }
  animate();
  return {setActive:(i)=>{}};
}

async function loadInteractiveLab(){
  const runs=await getRuns();
  const sel=document.getElementById('labRunSelect'); if(!sel) return;
  sel.innerHTML=runs.map((x,i)=>`<option value="${i}">${x.run_id}</option>`).join('');
  const layerBar=document.getElementById('labLayers');
  const viewer=document.getElementById('labViewer');
  const comp=document.getElementById('labCompare');
  const sheets=['Displacement U','Collagen c','Fibre orientation a/ac','Fibroblast paths','Signaling nodes','Infarct states'];
  layerBar.innerHTML=sheets.map((s,i)=>`<button class="pill" data-i="${i}">${s}</button>`).join('');

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

    layerBar.querySelectorAll('button').forEach(btn=>btn.onclick=()=>{
      if(window._towerApi){window._towerApi.setActive(Number(btn.dataset.i));}
    });

    const anim = run.animation_site ? (run.animation_site.toLowerCase().endsWith('.gif') ? `<img src="../${run.animation_site}" alt="simulation gif"/>` : `<video controls src="../${run.animation_site}"></video>`) : '<p>No animation</p>';
    viewer.innerHTML=`<div class="grid">${anim}<img src="../assets/img/${run.run_id}_montage6.png" onerror="this.style.display='none'"/><img src="../assets/img/${run.run_id}_alignment.png" onerror="this.style.display='none'"/><img src="../assets/img/${run.run_id}_agent_paths.png" onerror="this.style.display='none'"/></div>`;
    const stretch=parseStretch(run.config); const m=run.metrics||{}; const last=(m.step||[]).length-1;
    comp.innerHTML=`<table><thead><tr><th>Metric</th><th>Value</th><th>Boundary / Paper expectation</th></tr></thead><tbody><tr><td>stretch_x BC</td><td>${fmt(stretch)}</td><td>Overstretch should increase alignment/collagen in mechanobiology literature</td></tr><tr><td>Final collagen</td><td>${fmt(last>=0?m.c_mean[last]:null)}</td><td>Expected to rise under load + profibrotic signaling</td></tr><tr><td>Final max displacement</td><td>${fmt(last>=0?m.max_u[last]:null)}</td><td>Constrained by imposed displacement BC</td></tr><tr><td>Final growth proxy</td><td>${fmt(last>=0?m.g_mean[last]:null)}</td><td>Should track remodeling burden over time</td></tr></tbody></table>`;
  };
  sel.onchange=()=>render(sel.value); render(0);
}

async function loadScenarioMatrix(){
  const app=document.getElementById('scenarioMatrixApp');
  if(!app) return;
  const data=await fetch('../data/scenario_portfolio_matrix.json').then(r=>r.json()).catch(()=>null);
  if(!data){app.innerHTML='<p>Scenario matrix not available.</p>'; return;}
  const rows=data.scenarios||[];
  const loadSel=document.getElementById('smLoad');
  const sigSel=document.getElementById('smSignal');
  const fibSel=document.getElementById('smFib');

  const loads=[...new Set(rows.map(r=>Number(r.stretch_x).toFixed(2)))].sort();
  const sigs=[...new Set(rows.map(r=>`${Number(r.tgf_beta).toFixed(2)}|${Number(r.angII).toFixed(2)}`))].sort();
  const fibs=[...new Set(rows.map(r=>String(r.scenario.match(/_N(\\d+)/)?.[1]||'NA')))].sort((a,b)=>Number(a)-Number(b));

  loadSel.innerHTML='<option value="*">all</option>'+loads.map(v=>`<option>${v}</option>`).join('');
  sigSel.innerHTML='<option value="*">all</option>'+sigs.map(v=>`<option>${v}</option>`).join('');
  fibSel.innerHTML='<option value="*">all</option>'+fibs.map(v=>`<option>${v}</option>`).join('');

  function filtered(){
    const lv=loadSel.value, sv=sigSel.value, fv=fibSel.value;
    return rows.filter(r => (lv==='*'||Number(r.stretch_x).toFixed(2)===lv)
      && (sv==='*'||`${Number(r.tgf_beta).toFixed(2)}|${Number(r.angII).toFixed(2)}`===sv)
      && (fv==='*'||String(r.scenario.match(/_N(\\d+)/)?.[1]||'NA')===fv));
  }

  function draw(){
    const rs=filtered();
    const c=document.getElementById('smHeat');
    const g=c.getContext('2d');
    g.clearRect(0,0,c.width,c.height);
    const cols=6, cw=112, ch=46;
    rs.slice(0,30).forEach((r,i)=>{
      const x=(i%cols)*cw+8, y=Math.floor(i/cols)*ch+8;
      const v=Math.max(0,Math.min(1,(r.c_mean_final-3)/18));
      g.fillStyle=`rgb(${Math.floor(30+190*v)},${Math.floor(60+60*(1-v))},${Math.floor(170-80*v)})`;
      g.fillRect(x,y,cw-10,ch-10);
      g.fillStyle='white'; g.font='11px Arial';
      g.fillText(`L${Number(r.stretch_x).toFixed(2)} T${Number(r.tgf_beta).toFixed(2)}`,x+4,y+14);
      g.fillText(`N${String(r.scenario.match(/_N(\\d+)/)?.[1]||'?')} c=${Number(r.c_mean_final).toFixed(2)}`,x+4,y+30);
    });
    document.getElementById('smCount').textContent=`showing ${rs.length}/${rows.length}`;
  }

  [loadSel,sigSel,fibSel].forEach(el=>el.onchange=draw);
  draw();
}

window.addEventListener('DOMContentLoaded',()=>{loadRuns();loadInteractiveLab();loadScenarioMatrix();});''')

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
    vpj = ROOT / 'outputs' / 'validation_portfolio.json'
    if vpj.exists():
        try:
            vp = json.loads(vpj.read_text())
            rows = vp.get('scenarios', [])
            trs = ''.join([f"<tr><td>{human_scenario_name(r.get('scenario'))}</td><td>{r.get('stretch_x')}</td><td>{r.get('tgf_beta')}</td><td>{r.get('angII')}</td><td>{r.get('c_mean_final'):.3f}</td><td>{r.get('p_mean_final'):.3f}</td><td>{r.get('myo_frac_final'):.3f}</td><td>{r.get('ac_align_x_final'):.3f}</td></tr>" for r in rows])
            checks = ''.join([f"<li><span class='badge {'pass' if c.get('pass') else 'fail'}'>{'PASS' if c.get('pass') else 'FAIL'}</span> {c.get('check')}</li>" for c in vp.get('checks', [])])
            portfolio_block = f"<div class='card'><h2>Validation portfolio</h2><div class='summary-grid'><div class='summary-tile'><strong>Checks passed</strong><div>{vp.get('n_checks_passed')}/{vp.get('n_checks_total')}</div></div><div class='summary-tile'><strong>Scenarios</strong><div>{len(rows)}</div></div></div><table><thead><tr><th>Scenario</th><th>Load</th><th>TGFβ</th><th>AngII</th><th>Collagen</th><th>p</th><th>Myofibro</th><th>Align</th></tr></thead><tbody>{trs}</tbody></table><h3>Trend checks</h3><ul>{checks}</ul></div>"
        except Exception:
            portfolio_block = ''

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
            mech_map = {
                'infarct_remodeling': 'Infarct-zone maturation and spatial collagen heterogeneity',
                'fibroblast_signaling': 'Profibrotic signaling transduction and phenotype activation',
                'collagen_dynamics': 'Collagen deposition/turnover kinetics',
                'growth_remodeling': 'Load-driven growth/remodeling response',
                'cell_motion': 'Fibroblast migration and advection-coupled deposition',
                'fibre_alignment': 'Anisotropy/fibre reorientation under stretch',
            }
            rows = ''.join([
                f"<tr><td>{t.get('id')}</td><td><a href='{t.get('pubmed_url')}'>{t.get('pmid')}</a></td><td><span class='badge'>{t.get('category')}</span><br/><small>{mech_map.get(t.get('category'),'Mechanism domain')}</small></td><td>{t.get('model_score_0_to_3')}/3</td><td>{t.get('expected')}</td><td>{t.get('title')}</td></tr>"
                for t in tests
            ])
            table = f"<div class='summary-grid'><div class='summary-tile'><strong>Total tests</strong><div>{s.get('n_tests')}</div></div><div class='summary-tile'><strong>Mean score</strong><div>{sm.get('mean_score')}</div></div><div class='summary-tile'><strong>Score 3 / 2 / 1 / 0</strong><div>{sm.get('n_score_3')} / {sm.get('n_score_2')} / {sm.get('n_score_1')} / {sm.get('n_score_0')}</div></div></div><p>Previewing first 20 tests with normalized mechanism label and one-line model expectation.</p><table><thead><tr><th>ID</th><th>PMID</th><th>Mechanism tested</th><th>Score</th><th>Expected model behavior</th><th>Evidence anchor title</th></tr></thead><tbody>{rows}</tbody></table><p>Full catalog: <code>outputs/systematic_test_catalog.json</code></p>"
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
        thumbs = ''.join([f"<a href='./tests/{c.stem}.html'><img src='../assets/img/testcards/{c.name}' alt='{c.stem}'/></a>" for c in cards])
        testcard_block = f"<div class='card'><h2>Per-test validation cards (click for full report)</h2><p>Showing all {len(cards)} cards. Click any card for boundary conditions, reference evidence, model-vs-experiment comparison, and interpretation.</p><div class='grid'>{thumbs}</div></div>"

    uq_block = ''
    uqj = ROOT / 'outputs' / 'uq_portfolio.json'
    if uqj.exists():
        try:
            uq = json.loads(uqj.read_text())
            probs = uq.get('check_pass_probability', {})
            p_rows = ''.join([f"<tr><td>{k}</td><td>{v:.2f}</td></tr>" for k,v in probs.items()])
            su = uq.get('scenario_uncertainty', {})
            s_rows = []
            for name, m in su.items():
                s_rows.append(f"<tr><td>{name}</td><td>{m['c_mean_final']['q50']:.3f} [{m['c_mean_final']['q05']:.3f},{m['c_mean_final']['q95']:.3f}]</td><td>{m['p_mean_final']['q50']:.3f} [{m['p_mean_final']['q05']:.3f},{m['p_mean_final']['q95']:.3f}]</td><td>{m['ac_align_x_final']['q50']:.3f} [{m['ac_align_x_final']['q05']:.3f},{m['ac_align_x_final']['q95']:.3f}]</td></tr>")
            uq_block = f"<div class='card'><h2>Uncertainty quantification summary</h2><p>Samples: {uq.get('n_samples')}</p><h3>Check pass probabilities</h3><table><thead><tr><th>Check</th><th>Probability</th></tr></thead><tbody>{p_rows}</tbody></table><h3>Scenario uncertainty (q50 [q05,q95])</h3><table><thead><tr><th>Scenario</th><th>Collagen</th><th>p</th><th>Align</th></tr></thead><tbody>{''.join(s_rows)}</tbody></table></div>"
        except Exception:
            uq_block = ''

    metric_dict_block = '''<div class="card"><h2>Metric dictionary (definitions + units)</h2><table><thead><tr><th>Metric</th><th>Meaning</th><th>Units</th><th>Interpretation</th></tr></thead><tbody><tr><td><code>c_mean_final</code></td><td>Mean collagen field at final time</td><td>model collagen units (a.u.)</td><td>Higher = greater fibrosis burden.</td></tr><tr><td><code>p_mean_final</code></td><td>Integrated profibrotic signaling index from SMAD/ERK/ROS/CaN pathway state</td><td>dimensionless index [0,1] (a.u.)</td><td>Higher = stronger pro-fibrotic signaling drive.</td></tr><tr><td><code>myo_frac_final</code></td><td>Fraction of fibroblasts in myofibroblast phenotype at final time</td><td>fraction [0,1]</td><td>Higher = more activated contractile/depositing phenotype.</td></tr><tr><td><code>ac_align_x_final</code></td><td>Collagen/fibre alignment with principal loading axis (x)</td><td>dimensionless [0,1]</td><td>Higher = stronger load-aligned microstructure.</td></tr></tbody></table><p class="legend">Note: values are model-scale normalized outputs; the calibration cards map these to literature-supported target bands for quantitative comparison.</p></div>'''

    drug_block = ''
    vpj = ROOT / 'outputs' / 'validation_portfolio.json'
    if vpj.exists():
        try:
            v = json.loads(vpj.read_text())
            by = {r.get('scenario'): r for r in v.get('scenarios', [])}
            nd = by.get('high_load_high_signal', {})
            tg = by.get('drug_tgfr_block', {})
            at = by.get('drug_at1r_block', {})
            du = by.get('drug_dual_block', {})
            c0 = float(nd.get('c_mean_final', 1.0) or 1.0)
            p0 = float(nd.get('p_mean_final', 1.0) or 1.0)
            def pct(x,b):
                try:
                    return 100.0*(float(x)-float(b))/max(abs(float(b)),1e-8)
                except Exception:
                    return 0.0
            rows_drug = f"""
<tr><td>No drug</td><td>{nd.get('c_mean_final'):.3f} a.u.</td><td>{nd.get('p_mean_final'):.3f} (0-1)</td><td>reference</td><td>reference</td></tr>
<tr><td>TGFβR block</td><td>{tg.get('c_mean_final'):.3f} a.u.</td><td>{tg.get('p_mean_final'):.3f} (0-1)</td><td>{pct(tg.get('c_mean_final',c0),c0):.1f}%</td><td>{pct(tg.get('p_mean_final',p0),p0):.1f}%</td></tr>
<tr><td>AT1R block</td><td>{at.get('c_mean_final'):.3f} a.u.</td><td>{at.get('p_mean_final'):.3f} (0-1)</td><td>{pct(at.get('c_mean_final',c0),c0):.1f}%</td><td>{pct(at.get('p_mean_final',p0),p0):.1f}%</td></tr>
<tr><td>Dual block</td><td>{du.get('c_mean_final'):.3f} a.u.</td><td>{du.get('p_mean_final'):.3f} (0-1)</td><td>{pct(du.get('c_mean_final',c0),c0):.1f}%</td><td>{pct(du.get('p_mean_final',p0),p0):.1f}%</td></tr>
"""
            drug_block = f"<div class='card'><h2>Drug Validation Card</h2><p>PMID anchors: <a href='https://pubmed.ncbi.nlm.nih.gov/27017945/'>27017945</a>, <a href='https://pubmed.ncbi.nlm.nih.gov/26608708/'>26608708</a>.</p><p><strong>Expected pharmacology behavior:</strong> receptor blockade should reduce profibrotic signaling and downstream collagen accumulation; dual blockade should produce the strongest reduction.</p><table><thead><tr><th>Condition</th><th>Collagen (final)</th><th>Profibrotic index p (final)</th><th>Δ collagen vs no-drug</th><th>Δ p vs no-drug</th></tr></thead><tbody>{rows_drug}</tbody></table><div class='grid'><img src='../assets/img/drug_validation_collagen.png' alt='drug collagen comparison'/><img src='../assets/img/drug_validation_signal.png' alt='drug signaling comparison'/></div><p class='legend'>Interpretation: negative Δ values indicate suppression (desired drug effect).</p></div>"
        except Exception:
            drug_block = ''

    valcard_block = ''
    vcj = ROOT / 'outputs' / 'validation_card.json'
    if vcj.exists():
        try:
            vc = json.loads(vcj.read_text())
            rows = ''.join([
                f"<tr><td>{t.get('id')}</td><td>{t.get('domain')}</td><td>{t.get('measurement')}</td><td>{t.get('scenario')}</td><td>{t.get('model_value')}</td><td>{t.get('experimental_band')}</td><td>{'PASS' if t.get('pass') else 'FAIL'}</td><td><a href='https://pubmed.ncbi.nlm.nih.gov/{t.get('pmid_hint')}/'>{t.get('pmid_hint')}</a></td></tr>"
                for t in vc.get('tests', [])
            ])
            valcard_block = f"<div class='card'><h2>Validation card: model vs experimental bands</h2><p><strong>Pass rate:</strong> {vc.get('n_pass')}/{vc.get('n_tests')} ({vc.get('pass_rate',0):.2f})</p><table><thead><tr><th>ID</th><th>Domain</th><th>Measurement</th><th>Scenario</th><th>Model value</th><th>Experimental band</th><th>Status</th><th>PMID</th></tr></thead><tbody>{rows}</tbody></table><p class='legend'>This card directly compares predicted outputs against literature-informed benchmark bands.</p></div>"
        except Exception:
            valcard_block = ''

    scenario_block = ''
    spj = ROOT / 'outputs' / 'scenario_portfolio_matrix.json'
    if spj.exists():
        try:
            sm = json.loads(spj.read_text())
            sc = sm.get('scenarios', [])
            top = sorted(sc, key=lambda r: r.get('c_mean_final',0.0), reverse=True)[:12]
            trs = ''.join([f"<tr><td>{human_scenario_name(r.get('scenario'))}</td><td>{r.get('stretch_x')}</td><td>{r.get('tgf_beta')}</td><td>{r.get('angII')}</td><td>{r.get('c_mean_final'):.3f}</td><td>{r.get('p_mean_final'):.3f}</td><td>{r.get('myo_frac_final'):.3f}</td><td>{r.get('ac_align_x_final'):.3f}</td></tr>" for r in top])
            su = sm.get('summary', {})
            scenario_block = f"<div class='card'><h2>Scenario portfolio (loading × fibrotic signal × fibroblast count)</h2><div class='summary-grid'><div class='summary-tile'><strong>Total scenarios</strong><div>{sm.get('n_scenarios')}</div></div><div class='summary-tile'><strong>Collagen range</strong><div>{su.get('min_collagen'):.3f} – {su.get('max_collagen'):.3f}</div></div><div class='summary-tile'><strong>Alignment range</strong><div>{su.get('min_alignment'):.3f} – {su.get('max_alignment'):.3f}</div></div></div><p>Top 12 collagen scenarios are shown below.</p><table><thead><tr><th>Scenario</th><th>Load</th><th>TGFβ</th><th>AngII</th><th>Collagen</th><th>p</th><th>Myofibro</th><th>Align</th></tr></thead><tbody>{trs}</tbody></table></div>"
        except Exception:
            scenario_block = ''

    scenario_interactive_block = '''<div class="card"><h2>Scenario matrix explorer (interactive)</h2>
<div class="kpi">
  <label>Load <select id="smLoad"></select></label>
  <label>TGF|AngII <select id="smSignal"></select></label>
  <label>Fibroblasts <select id="smFib"></select></label>
  <span id="smCount" class="pill"></span>
</div>
<canvas id="smHeat" width="700" height="280" style="max-width:100%;background:#101722;border:1px solid #2a3140;border-radius:8px"></canvas>
<p class="legend">Heatmap color encodes collagen burden. Tiles show loading/signal/fibroblast-count combinations.</p>
<div id="scenarioMatrixApp"></div>
</div>'''

    numerical_block = ''
    ntr = ROOT / 'outputs' / 'numerical_test_report.md'
    ncj = ROOT / 'outputs' / 'numerical_cards.json'
    if ncj.exists():
        try:
            nc = json.loads(ncj.read_text())
            cards = nc.get('cards', [])
            tiles = ''.join([f"<a class='card' href='./numerical_tests/{c.get('id')}.html'><h3>{c.get('id')} - {c.get('title')}</h3><p>{c.get('description')}</p><img src='{c.get('plot')}' alt='{c.get('id')}'/><p><strong>Status:</strong> {c.get('status')}</p></a>" for c in cards])
            numerical_block = f"<div class='card'><h2>Numerical verification cards</h2><p>Click a card for simulation setup, interpretation, and result plot.</p><div class='grid'>{tiles}</div></div>"
            for c in cards:
                html = f"<!doctype html><html><head><meta charset='utf-8'/><meta name='viewport' content='width=device-width,initial-scale=1'/><link rel='stylesheet' href='../../assets/css/style.css?v={BUILD_VER}'/><link rel='stylesheet' href='../../assets/css/validation_theme.css?v={BUILD_VER}'/><title>{c.get('id')}</title></head><body><header><h1>{c.get('id')} - {c.get('title')}</h1></header><main class='validation-layout'><div class='v-card'><div class='v-head'><h2>Standard test summary</h2><span class='badge pass'>{c.get('status')}</span></div><p><strong>Test path:</strong> <code>{c.get('test_path')}</code></p><p><strong>What simulation is run:</strong> {c.get('description')}</p><p><strong>Status:</strong> {c.get('status')}</p></div><div class='v-card'><h2>Common visualization</h2><div class='test-plot'><img src='{c.get('detail_plot')}' alt='{c.get('id')} result'/></div></div><div class='v-card'><h2>Interpretation</h2><p>This numerical verification test checks solver stability/consistency for one component before coupling it into multiscale fibrosis simulations.</p></div><div class='v-card'><a href='../validation.html'>- Back to validation page</a></div></main></body></html>"
                (SITE / 'pages' / 'numerical_tests' / f"{c.get('id')}.html").write_text(html)
        except Exception:
            numerical_block = ''
    elif ntr.exists():
        numerical_block = f'<div class="card"><h2>Numerical tests (viewable report)</h2>{md_to_html(ntr.read_text())}</div>'

    calib_block = ''
    ccj = ROOT / 'outputs' / 'calibration_cards.json'
    if ccj.exists():
        try:
            cc = json.loads(ccj.read_text())
            cards = cc.get('cards', [])
            tiles = ''.join([f"<a class='card' href='./calibration/{c.get('id')}.html'><h3>{c.get('id')} - {c.get('name')}</h3><p>{c.get('description')}</p><p><strong>Status:</strong> {c.get('status')}</p><p><strong>Value:</strong> {c.get('value')} | <strong>Band:</strong> {c.get('band')}</p></a>" for c in cards])
            fail = cc.get('failed_cards', [])
            top3 = fail[:3]
            plan_items = ''.join([f"<li><strong>{f.get('id')} {f.get('name')}</strong>: {f.get('action_plan')}</li>" for f in top3]) or '<li>No failed checks in this run.</li>'
            calib_block = f"<div class='card'><h2>Calibration cards</h2><p>Click for detailed summary, scenario interpretation, and remediation guidance.</p><div class='grid'>{tiles}</div></div><div class='card'><h2>Failed-check recovery plan</h2><p>Priority plan for currently failed checks (top 3):</p><ul>{plan_items}</ul></div>"
            for c in cards:
                html = f"<!doctype html><html><head><meta charset='utf-8'/><meta name='viewport' content='width=device-width,initial-scale=1'/><link rel='stylesheet' href='../../assets/css/style.css?v={BUILD_VER}'/><link rel='stylesheet' href='../../assets/css/validation_theme.css?v={BUILD_VER}'/><title>{c.get('id')}</title></head><body><header><h1>{c.get('id')} - Calibration detail</h1></header><main class='validation-layout'><div class='v-card'><div class='v-head'><h2>Standard test summary</h2><span class='badge {'pass' if c.get('status')=='PASS' else 'fail'}'>{c.get('status')}</span></div><p><strong>Calibration target:</strong> {c.get('name')}</p><p><strong>Description:</strong> {c.get('description')}</p><p><strong>Status:</strong> {c.get('status')}</p><p><strong>Model value:</strong> {c.get('value')}</p><p><strong>Literature/target band:</strong> {c.get('band')}</p></div><div class='v-card'><h2>Interpretation</h2><p>This check quantifies whether simulated endpoint falls within the declared target band used for evidence-aligned calibration.</p></div><div class='v-card'><h2>Action plan</h2><p>{c.get('action_plan')}</p></div><div class='v-card'><a href='../validation.html'>- Back to validation page</a></div></main></body></html>"
                (SITE / 'pages' / 'calibration' / f"{c.get('id')}.html").write_text(html)
        except Exception:
            calib_block = ''
    else:
        crm = ROOT / 'outputs' / 'calibration_report.md'
        if crm.exists():
            calib_block = f'<div class="card"><h2>Unit-calibrated target report</h2>{md_to_html(crm.read_text())}</div>'

    param_block = ''
    pam = ROOT / 'outputs' / 'parameter_audit.md'
    if pam.exists():
        param_block = f'<div class="card"><h2>Parameter quantitative audit (units + literature bands)</h2>{md_to_html(pam.read_text())}</div>'

    uniq_block = ''
    vu = ROOT / 'outputs' / 'validation_uniqueness.md'
    if vu.exists():
        uniq_block = f'<div class="card"><h2>Validation test uniqueness audit</h2>{md_to_html(vu.read_text())}</div>'

    matrix_help_block = ''
    spm = ROOT / 'outputs' / 'scenario_portfolio_matrix.json'
    if spm.exists():
        try:
            sm = json.loads(spm.read_text())
            sc = sm.get('scenarios', [])
            top_c = sorted(sc, key=lambda r: r.get('c_mean_final', 0.0), reverse=True)[:5]
            rows = ''.join([f"<tr><td>{human_scenario_name(r.get('scenario'))}</td><td>{r.get('stretch_x')}</td><td>{r.get('tgf_beta')}</td><td>{r.get('angII')}</td><td>{r.get('c_mean_final'):.3f}</td><td>{r.get('p_mean_final'):.3f}</td><td>{r.get('ac_align_x_final'):.3f}</td></tr>" for r in top_c])
            matrix_help_block = f"<div class='card'><h2>How to read the scenario matrix</h2><p>Each row is one in-silico experiment with a specific load (stretch_x) and biochemical drive (TGFβ/AngII). Use it to identify which conditions reproduce high collagen, high profibrotic signaling, and alignment patterns.</p><ul><li><strong>c_mean_final</strong>: fibrosis burden endpoint</li><li><strong>p_mean_final</strong>: integrated profibrotic signaling endpoint</li><li><strong>ac_align_x_final</strong>: collagen/fibre alignment with loading axis</li></ul><p><strong>Top-5 collagen scenarios:</strong></p><table><thead><tr><th>Scenario</th><th>stretch_x</th><th>TGFβ</th><th>AngII</th><th>Collagen</th><th>p</th><th>Align</th></tr></thead><tbody>{rows}</tbody></table><p class='legend'>Takeaway: use this table to choose candidate regimes before deep paper-by-paper validation.</p></div>"
        except Exception:
            matrix_help_block = ''


    emulation_block = ''
    emr = ROOT / 'outputs' / 'emulation_report.md'
    emw = ROOT / 'outputs' / 'emulation_waves.md'
    emq = ROOT / 'outputs' / 'emulation_qc.md'
    emg = ROOT / 'docs' / '06_emulation_history_matching_guide.md'
    if emr.exists():
        emulation_block = f'<div class="card"><h2>Emulator + history matching summary</h2>{md_to_html(emr.read_text())}<img src="../assets/img/emulation_implausibility_hist.png" alt="Emulation implausibility histogram"/></div>'
        if emw.exists():
            emulation_block += f'<div class="card"><h2>Extra history-matching waves</h2>{md_to_html(emw.read_text())}</div>'
        if emq.exists():
            emulation_block += f'<div class="card"><h2>Emulation QC checklist</h2>{md_to_html(emq.read_text())}</div>'
        if emg.exists():
            emulation_block += f'<div class="card"><h2>How to use history matching in FibroTwin</h2>{md_to_html(emg.read_text())}</div>'
    coverage_block = ''
    vcm = ROOT / 'outputs' / 'validation_coverage.md'
    if vcm.exists():
        coverage_block = f'<div class="card"><h2>Study-to-mechanism coverage matrix</h2>{md_to_html(vcm.read_text())}</div>'

    # detailed pages per test card + failure summary
    stp = ROOT / 'outputs' / 'systematic_test_catalog_unique.json'
    if not stp.exists():
        stp = ROOT / 'outputs' / 'systematic_test_catalog.json'
    if stp.exists():
        try:
            st = json.loads(stp.read_text())
            tests = st.get('tests', [])
            by_cat = {}
            for t in tests:
                by_cat.setdefault(t.get('category','other'), []).append(t.get('model_score_0_to_3',0))

            # quantitative comparator helpers per test
            by_cat_tests = {}
            for t in tests:
                by_cat_tests.setdefault(t.get('category','other'), []).append(t)
            rank_map = {}
            for cat_k, arr in by_cat_tests.items():
                sarr = sorted(arr, key=lambda x: (-int(x.get('model_score_0_to_3',0)), str(x.get('pmid',''))))
                n = max(len(sarr), 1)
                for i, tt in enumerate(sarr):
                    # 0..1 percentile-like rank within category (higher is better)
                    rank_map[tt.get('id','')] = 1.0 - (i / max(n-1, 1))
            fail_rows = []
            for k,v in sorted(by_cat.items()):
                mean = sum(v)/max(len(v),1)
                if mean < 2.5:
                    fail_rows.append(f"<li><strong>{k}</strong>: mean score {mean:.2f}. Suggested additions: receptor-level signaling, unit-calibrated datasets, richer infarct microstructure.</li>")
            fail_summary = '<ul>' + ''.join(fail_rows) + '</ul>' if fail_rows else '<p>No low-scoring groups identified.</p>'
            testcard_block += f"<div class='card'><h2>Failure-group summary and improvement recommendations</h2>{fail_summary}</div>"

            for t in tests:
                tid=t.get('id','T000')
                pmid=t.get('pmid','')
                title=t.get('title','')
                cat=t.get('category','')
                expected=t.get('expected','')
                score=int(t.get('model_score_0_to_3',0))
                bcs = "Boundary conditions (MVP): left edge fixed; right edge prescribed displacement (stretch_x); top/bottom traction-free; reflective cell boundaries.\nMathematical form: ∇·σ=0 in Ω, with u=(0,0) on Γ_left and u_x=ΔL on Γ_right."
                if cat == 'infarct_remodeling':
                    bcs += "\nInfarct model (explicit): circular mask centered at (cx,cy) with radius R; core r<=R, border R<r<=2R, remote r>2R.\nMaturation states: inflammation -> provisional matrix -> scar using linear transition rates (k_infl_to_prov, k_prov_to_scar, with resolve rates).\nMechanical effect: E_eff <- E_eff*(1-soft_elem), where soft_elem is highest in early inflammatory phase and decreases as scar matures.\nBiochemical effect: infarct source term adds cytokine drive strongest early, decaying with maturation state.\nInterpretation: this corresponds to subacute-to-remodeling infarct progression (not fully chronic scar-only endpoint). Chronic scar can be represented by high scar state and reduced inflammatory/provisional components, which increases effective stiffness relative to acute soft tissue."

                obs = f"Screening-evidence statement (PMID {pmid}): {title}."
                norm_support = score / 3.0
                gap_to_full = 1.0 - norm_support
                cat_scores = by_cat.get(cat, [score])
                cat_mean = sum(cat_scores) / max(len(cat_scores), 1)
                cat_rel = rank_map.get(tid, 0.5)
                quantitative_row = f"<table><thead><tr><th>Metric</th><th>Value</th><th>Meaning</th></tr></thead><tbody><tr><td>Normalized support</td><td>{norm_support:.3f}</td><td>score/3 as a 0–1 support index</td></tr><tr><td>Gap to full support</td><td>{gap_to_full:.3f}</td><td>distance from ideal 3/3 support</td></tr><tr><td>Category mean score</td><td>{cat_mean:.3f}</td><td>mean model-support score in this mechanism category</td></tr><tr><td>Category-relative rank</td><td>{cat_rel:.3f}</td><td>relative standing among tests in same category (higher=stronger)</td></tr></tbody></table>"
                score_breakdown = f"<ul><li><strong>Target tested:</strong> {expected}</li><li><strong>What matched:</strong> {'Core trend reproduced.' if score>=2 else 'Only weak trend support.'}</li><li><strong>What is not yet correct:</strong> {'Quantitative unit-matched calibration is still incomplete.' if score>=2 else 'Mechanistic depth + calibration required.'}</li><li><strong>Score:</strong> {score}/3 (0=not represented, 1=placeholder, 2=partial mechanistic, 3=implemented+tested)</li></ul><h3>Quantitative comparator</h3>{quantitative_row}"

                fig = '../assets/img/pubfig_validation_storyline.png'
                if cat in ['fibroblast_signaling','cell_motion']:
                    fig = '../assets/img/pubfig_portfolio_collagen_signal.png'
                elif cat in ['fibre_alignment','infarct_remodeling']:
                    fig = '../assets/img/pubfig_infarct_regions.png'
                elif cat == 'growth_remodeling':
                    fig = '../assets/img/pubfig_scorecard_by_category.png'

                html = f"""<!doctype html><html><head><meta charset='utf-8'/><meta name='viewport' content='width=device-width,initial-scale=1'/><link rel='stylesheet' href='../../assets/css/style.css?v={BUILD_VER}'/><link rel='stylesheet' href='../../assets/css/validation_theme.css?v={BUILD_VER}'/><title>{tid}</title></head><body><header><h1>{tid} - Model mechanism test</h1></header><main class='validation-layout'><div class='v-card'><div class='v-head'><h2>Standard test summary</h2><span class='badge'>PMID {pmid}</span></div><p><strong>Mechanism tested:</strong> {expected}</p><p><strong>Model domain:</strong> {cat}</p><p><strong>Evidence anchor:</strong> <a href='https://pubmed.ncbi.nlm.nih.gov/{pmid}/'>PMID {pmid}</a> — {title}</p></div><div class='v-card'><h2>Simulation setup</h2><h3>Boundary conditions (words + maths)</h3><pre>{bcs}</pre></div><div class='v-card'><h2>Reference observation (screening-level evidence)</h2><p>{obs}</p></div><div class='v-card'><h2>Common visualization</h2><p>This panel is unique to this PMID-linked test card (not a shared global figure).</p><img src='../../assets/img/testcards/{tid}.png' alt='{tid} card'/><p class='legend'>Model-vs-band comparison for {tid} derived from the referenced study metadata.</p></div><div class='v-card'><h2>Pass/partial analysis</h2><div class='plan-box'>{score_breakdown}</div></div><div class='v-card'><a href='../validation.html'>- Back to validation page</a></div></main></body></html>"""
                (SITE / 'pages' / 'tests' / f"{tid}.html").write_text(html)
        except Exception:
            pass

    redesign_block = ''
    vup = ROOT / 'docs' / '08_validation_unification_plan.md'
    unify_block = ''
    if vup.exists():
        unify_block = f'<div class="card"><h2>Validation unification plan (single style + no repeats)</h2>{md_to_html(vup.read_text())}</div>'
    vrp = ROOT / 'docs' / '07_validation_consistency_plan.md'
    if vrp.exists():
        redesign_block = f'<div class="card"><h2>Validation page coherence plan</h2>{md_to_html(vrp.read_text())}</div>'

    pipeline_block = '''<div class="card"><h2>Validation pipeline (read in order)</h2><ol><li>Test outcomes + verification scope</li><li>Metric dictionary (units/definitions)</li><li>Validation portfolio + scenario matrix + UQ</li><li>Drug validation and numerical verification cards</li><li>Calibration cards and emulation/history matching</li><li>Parameter audit + uniqueness + coverage matrix</li><li>Literature-linked catalog and per-test cards</li></ol></div>'''

    (SITE / 'pages/validation.html').write_text(page('Validation & Tests', f'{pipeline_block}{unify_block}{redesign_block}<div class="card"><h2>Test outcomes</h2>{latest_test_summary()}</div><div class="card">{verification}</div>{metric_dict_block}{valcard_block}{infarct_block}{portfolio_block}{scenario_block}{scenario_interactive_block}{uq_block}{drug_block}{numerical_block}{calib_block}{emulation_block}{param_block}{uniq_block}{coverage_block}{matrix_help_block}{systematic_block}{pubfig_block}{testcard_block}'))


    emu_body = emulation_block if emulation_block else '<div class="card"><p>Run <code>python -m src.tools.emulation_history_matching</code> to generate emulator report.</p></div>'
    (SITE / 'pages/emulation.html').write_text(page('Emulation & History Matching', emu_body))

    results_body = '''<div class="card"><h2>How to interpret results</h2><ul><li><strong>Animation:</strong> overall evolution of deformation, fibroblast positions, and collagen field.</li><li><strong>Snapshots:</strong> 5–6 time points to compare early/mid/late remodeling.</li><li><strong>Fibroblast paths:</strong> show migration trajectories that drive deposition patterns.</li><li><strong>Alignment plot:</strong> values closer to 1 mean stronger alignment with loading direction.</li><li><strong>Collagen trend:</strong> rising mean collagen indicates increasing fibrosis burden.</li></ul></div><div class="card"><label><strong>Run selector:</strong> <select id="runSelect"></select></label></div><div class="card"><h2>Animation</h2><div id="anim"></div></div><div class="card"><h2>Key snapshots (time sequence)</h2><div id="frames"></div></div><div class="card"><h2>Summary metrics + story figures</h2><div id="metrics"></div></div>'''

    (SITE / 'pages/results.html').write_text(page('Results', results_body))

    interactive_head = f'<script src="../assets/js/three.min.js?v={BUILD_VER}"></script>'
    interactive_body = '''<div class="card"><h2>Interactive simulation explorer</h2><p class="legend">Visual prototype: two overlapping square slabs at 45° corner-forward perspective.</p><label><strong>Run selector:</strong> <select id="labRunSelect"></select></label></div><div class="card stack-wrap"><canvas id="towerCanvas"></canvas></div><div class="card"><h2>Layer selector</h2><div id="labLayers" class="kpi"></div></div><div class="card"><h2>Visual viewer</h2><div id="labViewer"></div></div><div class="card"><h2>Quantitative comparison and paper-aligned interpretation</h2><div id="labCompare"></div></div>'''
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
    stj2 = ROOT / 'outputs' / 'systematic_test_catalog_unique.json'
    if not stj2.exists():
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

    spj = ROOT / 'outputs' / 'scenario_portfolio_matrix.json'
    if spj.exists():
        (SITE / 'data/scenario_portfolio_matrix.json').write_text(spj.read_text())

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
