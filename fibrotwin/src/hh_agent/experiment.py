from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Sequence
import json

import numpy as np
import matplotlib.pyplot as plt

from .truth import HodgkinHuxleyTruth, SimulationData


@dataclass
class ExperimentResult:
    index: int
    label: str
    rationale: str
    protocol: List[Dict[str, float]]
    blocks: Dict[str, float]
    data: SimulationData
    mode: str

    def to_dict(self) -> Dict[str, object]:
        return {
            'index': self.index,
            'label': self.label,
            'rationale': self.rationale,
            'protocol': self.protocol,
            'blocks': self.blocks,
            'mode': self.mode,
            'metadata': self.data.metadata,
        }

    def save_arrays(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            path,
            time=self.data.time,
            voltage=self.data.voltage,
            clamp_current=self.data.clamp_current,
            I_na=self.data.ionic_currents['na'],
            I_k=self.data.ionic_currents['k'],
            I_l=self.data.ionic_currents['l'],
        )
        return path

    def save_plot(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
        ax[0].plot(self.data.time, self.data.voltage, color='tab:red')
        ax[0].set_ylabel('Voltage (mV)')
        ax[0].grid(True, alpha=0.3)
        ax[1].plot(self.data.time, self.data.clamp_current, color='tab:blue')
        ax[1].set_ylabel('Clamp current (µA/cm²)')
        ax[1].set_xlabel('Time (ms)')
        ax[1].grid(True, alpha=0.3)
        fig.suptitle(f"Experiment {self.index:03d}: {self.label}")
        fig.tight_layout()
        fig.savefig(path)
        plt.close(fig)
        return path


@dataclass
class ExperimentSession:
    truth: HodgkinHuxleyTruth
    root: Path
    dt_ms: float = 0.01
    _counter: int = 0
    _blocks: Dict[str, float] = field(default_factory=lambda: {'na': 0.0, 'k': 0.0})

    def apply_block(self, channel: str, level: float) -> None:
        level = max(0.0, min(1.0, level))
        if channel not in {'na', 'k'}:
            raise ValueError('channel must be na or k')
        self._blocks[channel] = level
        self.truth.set_block(channel, level)

    def clear_blocks(self) -> None:
        self._blocks = {'na': 0.0, 'k': 0.0}
        self.truth.reset_blocks()

    def run_voltage_clamp(self, protocol: Sequence[Dict[str, float]], label: str, rationale: str) -> ExperimentResult:
        return self._run(protocol, label, rationale, mode='voltage')

    def run_current_clamp(self, protocol: Sequence[Dict[str, float]], label: str, rationale: str) -> ExperimentResult:
        return self._run(protocol, label, rationale, mode='current')

    def _run(self, protocol: Sequence[Dict[str, float]], label: str, rationale: str, mode: str) -> ExperimentResult:
        self._counter += 1
        proto_series = [(seg['duration_ms'], seg['value']) for seg in protocol]
        data = self.truth.simulate_protocol(proto_series, mode=mode, dt_ms=self.dt_ms)
        result = ExperimentResult(
            index=self._counter,
            label=label,
            rationale=rationale,
            protocol=[dict(seg) for seg in protocol],
            blocks=dict(self._blocks),
            data=data,
            mode=mode,
        )
        # save raw arrays immediately for provenance
        run_dir = self.root / 'runs'
        run_dir.mkdir(parents=True, exist_ok=True)
        result.save_arrays(run_dir / f"exp_{self._counter:03d}.npz")
        result.save_plot(run_dir / f"exp_{self._counter:03d}.png")
        with (run_dir / f"exp_{self._counter:03d}.json").open('w', encoding='utf-8') as fp:
            json.dump(result.to_dict(), fp, indent=2)
        return result
