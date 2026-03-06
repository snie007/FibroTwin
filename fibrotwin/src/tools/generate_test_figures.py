import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'
IMG = SITE / 'assets' / 'img'
CARDS = IMG / 'testcards'


def make_card(t):
    CARDS.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 2.2))
    ax.axis('off')
    score = t.get('model_score_0_to_3', 0)
    status = 'match-supported' if score == 3 else ('partial-support' if score == 2 else 'low-support')
    color = '#16a34a' if score == 3 else ('#f59e0b' if score == 2 else '#ef4444')

    title = t.get('title', 'N/A')[:120]
    pmid = t.get('pmid', 'NA')
    category = t.get('category', 'NA')
    expected = t.get('expected', '')[:110]

    ax.text(0.01, 0.83, f"{t.get('id')} | PMID {pmid} | {category}", fontsize=10, weight='bold')
    ax.text(0.01, 0.56, title, fontsize=9)
    ax.text(0.01, 0.34, f"Expected: {expected}", fontsize=8)
    ax.add_patch(plt.Rectangle((0.01, 0.08), 0.25, 0.12, color=color, transform=ax.transAxes))
    ax.text(0.015, 0.12, f"Score {score}/3: {status}", fontsize=8, color='white')
    ax.text(0.30, 0.12, "Confirmation: mapping + current model outputs/portfolio", fontsize=8)

    out = CARDS / f"{t.get('id')}.png"
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def main():
    st = ROOT / 'outputs' / 'systematic_test_catalog.json'
    if not st.exists():
        print('systematic_test_catalog.json missing')
        return
    data = json.loads(st.read_text())
    tests = data.get('tests', [])
    for t in tests:
        make_card(t)
    print(f"Generated {len(tests)} test cards in {CARDS}")


if __name__ == '__main__':
    main()
