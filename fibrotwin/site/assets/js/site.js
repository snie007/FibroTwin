function fmt(v){return (v===null||v===undefined)?'NA':(typeof v==='number'?v.toFixed(4):String(v));}
function parseStretch(cfg){const m=(cfg||'').match(/stretch_x:\s*([0-9.]+)/);return m?Number(m[1]):null;}
async function getRuns(){return fetch('../data/runs.json').then(x=>x.json()).catch(()=>[]);}

async function loadRuns(){
  const r=await getRuns();
  const sel=document.getElementById('runSelect'); if(!sel) return;
  sel.innerHTML=r.map((x,i)=>`<option value="${i}">${x.run_id}</option>`).join('');
  const render=(i)=>{
    const run=r[i]; if(!run) return;
    document.getElementById('anim').innerHTML=run.animation_site?`<video controls src="../${run.animation_site}"></video>`:'<p>No animation available for this run.</p>';
    document.getElementById('frames').innerHTML=`<div class="grid">${(run.frames_site||[]).map((f,j)=>`<figure><img alt="snapshot ${j+1}" src="../${f}"/><figcaption>Snapshot ${j+1}: spatial field state</figcaption></figure>`).join('')}</div>`;

    const m=run.metrics||{};
    const n=(m.step||[]).length; const last=n>0?n-1:null;
    const cLast=last!==null?m.c_mean[last]:null; const uLast=last!==null?m.max_u[last]:null; const gLast=last!==null?m.g_mean[last]:null;
    const plots=[`../assets/img/${run.run_id}_collagen.png`,`../assets/img/${run.run_id}_max_u.png`,`../assets/img/${run.run_id}_g_mean.png`,`../assets/img/${run.run_id}_alignment.png`,`../assets/img/${run.run_id}_agent_paths.png`,`../assets/img/${run.run_id}_montage6.png`];
    document.getElementById('metrics').innerHTML=`<div class="kpi"><div class="pill"><strong>Recorded steps</strong><br/>${n}</div><div class="pill"><strong>Final mean collagen</strong><br/>${fmt(cLast)}</div><div class="pill"><strong>Final max displacement</strong><br/>${fmt(uLast)}</div><div class="pill"><strong>Final growth proxy</strong><br/>${fmt(gLast)}</div></div><p><strong>Interpretation guide:</strong> collagen ↑ indicates fibrosis burden, alignment ↑ indicates reorientation toward loading, and agent paths show migration-driven deposition patterns.</p><div class="grid">${plots.map(p=>`<img src="${p}" onerror="this.style.display='none'"/>`).join('')}</div>`;
  };
  sel.onchange=()=>render(sel.value); render(0);
}

async function loadInteractiveLab(){
  const runs=await getRuns();
  const sel=document.getElementById('labRunSelect'); if(!sel) return;
  sel.innerHTML=runs.map((x,i)=>`<option value="${i}">${x.run_id}</option>`).join('');
  const stack=document.getElementById('sheetStack');
  const viewer=document.getElementById('labViewer');
  const comp=document.getElementById('labCompare');
  const sheets=['Displacement U','Collagen c','Fibre orientation a/ac','Fibroblast paths','Signaling nodes'];
  stack.innerHTML=sheets.map((s,i)=>`<div class="sheet" data-i="${i}" style="transform:translateY(${i*8}px) translateZ(${-i*8}px)">${s}</div>`).join('');
  stack.querySelectorAll('.sheet').forEach(el=>el.onclick=()=>{el.classList.toggle('expanded');});

  const render=(i)=>{
    const run=runs[i]; if(!run) return;
    viewer.innerHTML=`<div class="grid"><video controls src="../${run.animation_site||''}"></video><img src="../assets/img/${run.run_id}_montage6.png" onerror="this.style.display='none'"/><img src="../assets/img/${run.run_id}_alignment.png" onerror="this.style.display='none'"/><img src="../assets/img/${run.run_id}_agent_paths.png" onerror="this.style.display='none'"/></div>`;
    const stretch=parseStretch(run.config); const m=run.metrics||{}; const last=(m.step||[]).length-1;
    comp.innerHTML=`<table><thead><tr><th>Metric</th><th>Value</th><th>Boundary / Paper expectation</th></tr></thead><tbody><tr><td>stretch_x BC</td><td>${fmt(stretch)}</td><td>Overstretch should increase alignment/collagen in mechanobiology literature</td></tr><tr><td>Final collagen</td><td>${fmt(last>=0?m.c_mean[last]:null)}</td><td>Expected to rise under load + profibrotic signaling</td></tr><tr><td>Final max displacement</td><td>${fmt(last>=0?m.max_u[last]:null)}</td><td>Constrained by imposed displacement BC</td></tr><tr><td>Final growth proxy</td><td>${fmt(last>=0?m.g_mean[last]:null)}</td><td>Should track remodeling burden over time</td></tr></tbody></table>`;
  };
  sel.onchange=()=>render(sel.value); render(0);
}

window.addEventListener('DOMContentLoaded',()=>{loadRuns();loadInteractiveLab();});