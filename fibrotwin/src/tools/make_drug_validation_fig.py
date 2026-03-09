import json
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'outputs'
IMG = ROOT / 'site' / 'assets' / 'img'


def main():
    vp = OUT / 'validation_portfolio.json'
    if not vp.exists():
        print('validation_portfolio.json missing')
        return
    d = json.loads(vp.read_text())
    rows = {r['scenario']: r for r in d.get('scenarios', [])}

    labels = ['high_load_high_signal', 'drug_tgfr_block', 'drug_at1r_block', 'drug_dual_block']
    nice = ['No drug', 'TGFβR block', 'AT1R block', 'Dual block']

    cvals = [rows.get(k, {}).get('c_mean_final', 0.0) for k in labels]
    pvals = [rows.get(k, {}).get('p_mean_final', 0.0) for k in labels]

    IMG.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    x = range(len(nice))
    ax.bar(x, cvals, color=['#6b7280', '#4f46e5', '#0ea5e9', '#16a34a'])
    ax.set_xticks(list(x)); ax.set_xticklabels(nice)
    ax.set_ylabel('Final collagen mean (a.u.)')
    ax.set_title('Drug validation: collagen suppression vs no-drug condition')
    fig.tight_layout(); fig.savefig(IMG / 'drug_validation_collagen.png', dpi=220); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar(x, pvals, color=['#6b7280', '#4f46e5', '#0ea5e9', '#16a34a'])
    ax.set_xticks(list(x)); ax.set_xticklabels(nice)
    ax.set_ylabel('Final profibrotic index p (dimensionless, 0-1)')
    ax.set_title('Drug validation: signaling suppression vs no-drug condition')
    fig.tight_layout(); fig.savefig(IMG / 'drug_validation_signal.png', dpi=220); plt.close(fig)

    print('drug figures generated')


if __name__ == '__main__':
    main()
