#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'evidence.json'
GRAPH_PATH = ROOT / 'data' / 'knowledge_graph.json'
WEB_DATA_PATH = ROOT / 'web' / 'data.js'


def build_graph(evidence):
    perspectives = sorted({p for item in evidence for p in item.get('perspectives', [])})
    domains = sorted({d for item in evidence for d in item.get('domains', [])})

    nodes = []
    edges = []

    for perspective in perspectives:
        nodes.append({
            'id': f'perspective:{perspective}',
            'label': perspective.replace('_', ' '),
            'kind': 'perspective',
        })

    for domain in domains:
        nodes.append({
            'id': f'domain:{domain}',
            'label': domain.replace('_', ' '),
            'kind': 'domain',
        })

    for item in evidence:
        nodes.append({
            'id': f"evidence:{item['id']}",
            'label': item['title'],
            'kind': item['type'],
            'pmid': item.get('pmid'),
            'year': item.get('year'),
        })
        for perspective in item.get('perspectives', []):
            edges.append({
                'source': f"evidence:{item['id']}",
                'target': f'perspective:{perspective}',
                'kind': 'supports_perspective',
            })
        for domain in item.get('domains', []):
            edges.append({
                'source': f"evidence:{item['id']}",
                'target': f'domain:{domain}',
                'kind': 'supports_domain',
            })

    return {
        'nodes': nodes,
        'edges': edges,
        'meta': {
            'evidence_count': len(evidence),
            'perspective_count': len(perspectives),
            'domain_count': len(domains),
        }
    }


def main():
    evidence = json.loads(DATA_PATH.read_text())
    graph = build_graph(evidence)
    GRAPH_PATH.write_text(json.dumps(graph, indent=2))
    WEB_DATA_PATH.write_text(
        'window.EVIDENCE_DATA = ' + json.dumps(evidence, indent=2) + ';\n\n'
        + 'window.KNOWLEDGE_GRAPH = ' + json.dumps(graph, indent=2) + ';\n'
    )
    print(f'Wrote {GRAPH_PATH}')
    print(f'Wrote {WEB_DATA_PATH}')


if __name__ == '__main__':
    main()
