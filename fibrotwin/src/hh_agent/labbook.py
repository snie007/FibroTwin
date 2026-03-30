from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict

from .experiment import ExperimentResult


@dataclass
class LabBook:
    root: Path
    title: str = 'HH Agent Lab'

    def __post_init__(self) -> None:
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        self.run_dir = self.root / 'reports' / 'hh_agent_lab' / timestamp
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.markdown_path = self.run_dir / 'lab_book.md'
        header = f"# {self.title} — Run {timestamp}\n\n"
        self.markdown_path.write_text(header, encoding='utf-8')

    def log_experiment(self, result: ExperimentResult, insights: Dict[str, str]) -> None:
        fig_path = self.run_dir / f"exp_{result.index:03d}.png"
        data_path = self.run_dir / f"exp_{result.index:03d}.npz"
        result.save_plot(fig_path)
        result.save_arrays(data_path)

        lines = [
            f"## Experiment {result.index:03d}: {result.label}",
            '',
            f"**Rationale:** {result.rationale}",
            '',
            f"**Mode:** {result.mode}",
            f"**Blocks:** Na={result.blocks['na']:.2f}, K={result.blocks['k']:.2f}",
            '',
            f"![exp {result.index:03d}]({fig_path.relative_to(self.run_dir)})",
            '',
        ]
        if insights:
            lines.append('**Insights:**')
            for key, value in insights.items():
                lines.append(f"- **{key}:** {value}")
            lines.append('')
        lines.append('---\n')
        with self.markdown_path.open('a', encoding='utf-8') as fp:
            fp.write('\n'.join(lines))

    def finalize(self, summary: str) -> None:
        with self.markdown_path.open('a', encoding='utf-8') as fp:
            fp.write(f"\n## Run Summary\n\n{summary}\n")

    @property
    def output_dir(self) -> Path:
        return self.run_dir
