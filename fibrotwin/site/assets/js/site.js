function fmt(v){return (v===null||v===undefined)?'NA':(typeof v==='number'?v.toFixed(4):String(v));}
async function loadRuns(){
  const r=await fetch('../data/runs.json').then(x=>x.json()).catch(()=>[]);
  const sel=document.getElementById('runSelect'); if(!sel) return;
  sel.innerHTML=r.map((x,i)=>`<option value="${i}">${x.run_id}</option>`).join('');
  const render=(i)=>{
    const run=r[i]; if(!run) return;
    document.getElementById('anim').innerHTML=run.animation_site?`<video controls src="../${run.animation_site}"></video>`:'<p>No animation available for this run.</p>';
    document.getElementById('frames').innerHTML=`<div class="grid">${(run.frames_site||[]).map((f,j)=>`<figure><img alt="snapshot ${j+1}" src="../${f}"/><figcaption>Snapshot ${j+1}: spatial field state</figcaption></figure>`).join('')}</div>`;

    const m=run.metrics||{};
    const n=(m.step||[]).length; const last=n>0?n-1:null;
    const cLast=last!==null?m.c_mean[last]:null; const uLast=last!==null?m.max_u[last]:null; const gLast=last!==null?m.g_mean[last]:null;
    const plots=[
      `../assets/img/${run.run_id}_collagen.png`,
      `../assets/img/${run.run_id}_max_u.png`,
      `../assets/img/${run.run_id}_g_mean.png`,
      `../assets/img/${run.run_id}_alignment.png`,
      `../assets/img/${run.run_id}_agent_paths.png`,
      `../assets/img/${run.run_id}_montage6.png`
    ];
    document.getElementById('metrics').innerHTML=`
      <div class="kpi">
        <div class="pill"><strong>Recorded steps</strong><br/>${n}</div>
        <div class="pill"><strong>Final mean collagen</strong><br/>${fmt(cLast)}</div>
        <div class="pill"><strong>Final max displacement</strong><br/>${fmt(uLast)}</div>
        <div class="pill"><strong>Final growth proxy</strong><br/>${fmt(gLast)}</div>
      </div>
      <p><strong>Interpretation guide:</strong> collagen ↑ indicates fibrosis burden, alignment ↑ indicates reorientation toward loading, and agent paths show migration-driven deposition patterns.</p>
      <div class="grid">
        ${plots.map(p=>`<img src="${p}" onerror="this.style.display='none'"/>`).join('')}
      </div>
    `;
  };
  sel.onchange=()=>render(sel.value); render(0);
}
window.addEventListener('DOMContentLoaded',loadRuns);