const evidence = window.EVIDENCE_DATA || [];
const graph = window.KNOWLEDGE_GRAPH || { nodes: [], edges: [], meta: {} };

const searchInput = document.getElementById('searchInput');
const perspectiveFilter = document.getElementById('perspectiveFilter');
const domainFilter = document.getElementById('domainFilter');
const typeFilter = document.getElementById('typeFilter');
const summaryStats = document.getElementById('summaryStats');
const resultCount = document.getElementById('resultCount');
const results = document.getElementById('results');
const graphSvg = document.getElementById('graph');

const unique = (items) => [...new Set(items)].sort();
const titleCase = (value) => value.replaceAll('_', ' ');

function populateSelect(select, values, label) {
  select.innerHTML = ['<option value="">All ' + label + '</option>']
    .concat(values.map(value => `<option value="${value}">${titleCase(value)}</option>`))
    .join('');
}

function setupFilters() {
  populateSelect(perspectiveFilter, unique(evidence.flatMap(item => item.perspectives || [])), 'perspectives');
  populateSelect(domainFilter, unique(evidence.flatMap(item => item.domains || [])), 'domains');
  populateSelect(typeFilter, unique(evidence.map(item => item.type)), 'types');
}

function matches(item, query, perspective, domain, type) {
  const haystack = [
    item.id, item.title, item.quote, item.summary, item.relevance, item.url,
    ...(item.hard_numbers || []), ...(item.perspectives || []), ...(item.domains || []),
    item.pmid || ''
  ].join(' ').toLowerCase();

  return (!query || haystack.includes(query))
    && (!perspective || (item.perspectives || []).includes(perspective))
    && (!domain || (item.domains || []).includes(domain))
    && (!type || item.type === type);
}

function renderSummary(filtered) {
  const pmidCount = filtered.filter(item => item.pmid).length;
  summaryStats.innerHTML = [
    ['records', filtered.length],
    ['PMID-tagged papers', pmidCount],
    ['graph nodes', graph.meta.evidence_count || 0],
    ['perspectives', graph.meta.perspective_count || 0],
    ['domains', graph.meta.domain_count || 0]
  ].map(([label, value]) => `<span class="chip">${label}: <strong>${value}</strong></span>`).join('');
}

function renderResults(filtered) {
  resultCount.textContent = `${filtered.length} record(s) shown`;
  results.innerHTML = filtered.map(item => {
    const pmid = item.pmid ? `<span class="chip type">PMID ${item.pmid}</span>` : '';
    const numbers = (item.hard_numbers || []).length
      ? `<div><strong>Hard numbers</strong><ul>${item.hard_numbers.map(x => `<li>${x}</li>`).join('')}</ul></div>`
      : '';

    return `
      <article class="record">
        <h3>${item.title}</h3>
        <div class="record-meta">
          <span class="chip type">${item.type}</span>
          <span class="chip type">${item.year || 'n.d.'}</span>
          ${pmid}
        </div>
        <blockquote>${item.quote || ''}</blockquote>
        <p>${item.summary || ''}</p>
        ${numbers}
        <p><strong>Why it matters</strong>: ${item.relevance || ''}</p>
        <p class="muted"><a href="../${item.local_copy}" target="_blank" rel="noreferrer">Local copy</a> · <a href="${item.url}" target="_blank" rel="noreferrer">Original source</a></p>
        <div class="tag-row">
          ${(item.perspectives || []).map(x => `<span class="chip perspective">${titleCase(x)}</span>`).join('')}
          ${(item.domains || []).map(x => `<span class="chip domain">${titleCase(x)}</span>`).join('')}
        </div>
      </article>
    `;
  }).join('');
}

function drawGraph(filtered) {
  const visibleEvidenceIds = new Set(filtered.map(item => `evidence:${item.id}`));
  const visibleEdges = graph.edges.filter(edge => visibleEvidenceIds.has(edge.source));
  const connectedNodeIds = new Set([...visibleEvidenceIds, ...visibleEdges.map(e => e.target)]);
  const visibleNodes = graph.nodes.filter(node => connectedNodeIds.has(node.id));

  const cx = 600;
  const cy = 360;
  const perspectiveNodes = visibleNodes.filter(node => node.kind === 'perspective');
  const domainNodes = visibleNodes.filter(node => node.kind === 'domain');
  const evidenceNodes = visibleNodes.filter(node => !['perspective', 'domain'].includes(node.kind));

  const layout = new Map();

  perspectiveNodes.forEach((node, i) => {
    const angle = (Math.PI * 2 * i) / Math.max(perspectiveNodes.length, 1);
    layout.set(node.id, { x: cx + Math.cos(angle) * 300, y: cy + Math.sin(angle) * 220 });
  });

  domainNodes.forEach((node, i) => {
    const angle = (Math.PI * 2 * i) / Math.max(domainNodes.length, 1) + 0.5;
    layout.set(node.id, { x: cx + Math.cos(angle) * 470, y: cy + Math.sin(angle) * 290 });
  });

  evidenceNodes.forEach((node, i) => {
    const cols = 5;
    const x = 240 + (i % cols) * 160;
    const y = 180 + Math.floor(i / cols) * 90;
    layout.set(node.id, { x, y });
  });

  const edgeMarkup = visibleEdges.map(edge => {
    const source = layout.get(edge.source);
    const target = layout.get(edge.target);
    return `<line class="edge" x1="${source.x}" y1="${source.y}" x2="${target.x}" y2="${target.y}"></line>`;
  }).join('');

  const nodeMarkup = visibleNodes.map(node => {
    const point = layout.get(node.id);
    const radius = node.kind === 'perspective' ? 11 : node.kind === 'domain' ? 10 : 7;
    const label = node.kind === 'publication' && node.pmid ? `PMID ${node.pmid}` : node.label;
    const shortLabel = label.length > 32 ? label.slice(0, 29) + '...' : label;
    return `
      <g>
        <circle class="node ${node.kind}" cx="${point.x}" cy="${point.y}" r="${radius}"></circle>
        <text class="node-label ${node.kind === 'publication' || node.kind === 'webpage' || node.kind === 'pdf' ? 'small' : ''}" x="${point.x + 14}" y="${point.y + 4}">${shortLabel}</text>
      </g>
    `;
  }).join('');

  graphSvg.innerHTML = edgeMarkup + nodeMarkup;
}

function render() {
  const query = searchInput.value.trim().toLowerCase();
  const filtered = evidence.filter(item => matches(item, query, perspectiveFilter.value, domainFilter.value, typeFilter.value));
  renderSummary(filtered);
  renderResults(filtered);
  drawGraph(filtered);
}

setupFilters();
[searchInput, perspectiveFilter, domainFilter, typeFilter].forEach(el => el.addEventListener('input', render));
render();
