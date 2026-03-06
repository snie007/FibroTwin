import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'outputs'
SITE_IMG = ROOT / 'site' / 'assets' / 'img'


def fig_portfolio_bars(vp):
    rows = vp.get('scenarios', [])
    names = [r['scenario'] for r in rows]
    cvals = [r.get('c_mean_final', 0) for r in rows]
    pvals = [r.get('p_mean_final', 0) for r in rows]

    fig, ax1 = plt.subplots(figsize=(9, 4.5))
    x = range(len(names))
    ax1.bar(x, cvals, alpha=0.75, label='Final collagen (c_mean)')
    ax1.set_ylabel('Collagen mean')
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(names, rotation=25, ha='right')

    ax2 = ax1.twinx()
    ax2.plot(list(x), pvals, 'o-', color='crimson', label='Final profibrotic signal (p_mean)')
    ax2.set_ylabel('Profibrotic signal mean')

    ax1.set_title('Validation portfolio outcomes across scenarios')
    fig.tight_layout()
    fig.savefig(SITE_IMG / 'pubfig_portfolio_collagen_signal.png', dpi=220)
    plt.close(fig)


def fig_infarct_region(vp):
    rows = [r for r in vp.get('scenarios', []) if 'infarct' in r.get('scenario', '') and r.get('c_core') is not None]
    if not rows:
        return
    r = rows[-1]
    regs = ['core', 'border', 'remote']
    cvals = [r.get('c_core', 0), r.get('c_border', 0), r.get('c_remote', 0)]
    pvals = [r.get('p_core', 0), r.get('p_border', 0), r.get('p_remote', 0)]

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    x = range(3)
    ax.bar(x, cvals, width=0.45, label='Collagen c', color='#3b82f6')
    ax.plot(list(x), pvals, 'o-', color='#ef4444', lw=2, label='Profibrotic p')
    ax.set_xticks(list(x))
    ax.set_xticklabels(regs)
    ax.set_title('Infarct regional gradients (core / border / remote)')
    ax.legend()
    fig.tight_layout()
    fig.savefig(SITE_IMG / 'pubfig_infarct_regions.png', dpi=220)
    plt.close(fig)


def fig_systematic_scorecard(st):
    tests = st.get('tests', [])
    cats = {}
    for t in tests:
        c = t.get('category', 'other')
        cats.setdefault(c, []).append(t.get('model_score_0_to_3', 0))
    names = sorted(cats.keys())
    means = [sum(cats[k]) / max(len(cats[k]), 1) for k in names]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(names, means, color='#10b981')
    ax.set_ylim(0, 3)
    ax.set_ylabel('Mean model score (0–3)')
    ax.set_title('Systematic review scorecard by test category')
    ax.tick_params(axis='x', rotation=25)
    fig.tight_layout()
    fig.savefig(SITE_IMG / 'pubfig_scorecard_by_category.png', dpi=220)
    plt.close(fig)


def fig_model_story(vp):
    checks = vp.get('checks', [])
    labels = [c.get('check', '')[:45] + ('...' if len(c.get('check', '')) > 45 else '') for c in checks]
    vals = [1 if c.get('pass') else 0 for c in checks]

    fig, ax = plt.subplots(figsize=(10, 4.8))
    colors = ['#22c55e' if v == 1 else '#ef4444' for v in vals]
    ax.bar(range(len(vals)), vals, color=colors)
    ax.set_yticks([0, 1]); ax.set_yticklabels(['Fail', 'Pass'])
    ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, rotation=20, ha='right')
    ax.set_title('Validation storyline: hypothesis checks')
    fig.tight_layout()
    fig.savefig(SITE_IMG / 'pubfig_validation_storyline.png', dpi=220)
    plt.close(fig)


def main():
    SITE_IMG.mkdir(parents=True, exist_ok=True)
    vp_file = OUT / 'validation_portfolio.json'
    st_file = OUT / 'systematic_test_catalog.json'
    if not vp_file.exists() or not st_file.exists():
        print('Required portfolio/catalog files missing; generate them first.')
        return

    vp = json.loads(vp_file.read_text())
    st = json.loads(st_file.read_text())

    fig_portfolio_bars(vp)
    fig_infarct_region(vp)
    fig_systematic_scorecard(st)
    fig_model_story(vp)

    print('Publication figures written to', SITE_IMG)


if __name__ == '__main__':
    main()
