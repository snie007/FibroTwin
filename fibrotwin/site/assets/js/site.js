function fmt(v){return (v===null||v===undefined)?'NA':(typeof v==='number'?v.toFixed(4):String(v));}
function parseStretch(cfg){const m=(cfg||'').match(/stretch_x:\s*([0-9.]+)/);return m?Number(m[1]):null;}
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
  const camera=new THREE.PerspectiveCamera(48, canvas.clientWidth/canvas.clientHeight, 0.1, 100);
  camera.position.set(-1.4, 2.8, 8.6);
  const light=new THREE.DirectionalLight(0xffffff,1.0); light.position.set(3,5,6); scene.add(light);
  scene.add(new THREE.AmbientLight(0x8aa4ff,0.45));

  const loader = new THREE.TextureLoader();
  const mats=[]; const boxes=[];
  labels.forEach((label,i)=>{
    const color=[0x38527d,0x3f5d87,0x496a94,0x5277a3,0x5d86b5,0x6c95c2][i%6];
    const g=new THREE.BoxGeometry(4.4,0.65,3.1);
    const texPath = textureMap && textureMap[i] ? textureMap[i] : null;
    const tex = texPath ? loader.load(texPath) : null;
    if(tex){tex.colorSpace = THREE.SRGBColorSpace; tex.wrapS=THREE.ClampToEdgeWrapping; tex.wrapT=THREE.ClampToEdgeWrapping;}
    const mTex = new THREE.MeshStandardMaterial({map:tex||null,color:tex?0xffffff:color,metalness:0.12,roughness:0.68});
    const mSide = new THREE.MeshStandardMaterial({color:0x1a2740,metalness:0.25,roughness:0.75});
    // right,left,top,bottom,front,back -> place texture on top and front so it's visible
    const mats6 = [mSide,mSide,mTex,mSide,mTex,mSide];
    const b=new THREE.Mesh(g,mats6);
    b.position.set(0,i*0.62,0);
    b.userData={index:i,label,baseX:0,baseY:i*0.5};
    scene.add(b); boxes.push(b); mats.push(mTop);
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
      const targetX=(i===active)?4.0:0.0;
      b.position.x += 0.10*(targetX-b.position.x);
      const targetY=b.userData.baseY + (i===active?0.16:0);
      b.position.y += 0.10*(targetY-b.position.y);
      b.rotation.y += 0.02*(i===active?1:0);
    });
    scene.rotation.y=0.32;
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

window.addEventListener('DOMContentLoaded',()=>{loadRuns();loadInteractiveLab();});