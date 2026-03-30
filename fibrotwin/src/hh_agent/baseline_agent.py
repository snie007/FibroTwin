from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import numpy as np

from .experiment import ExperimentSession, ExperimentResult
from .labbook import LabBook


@dataclass
class BaselineAgent:
    session: ExperimentSession
    labbook: LabBook
    summaries: List[str] = field(default_factory=list)

    def run(self) -> None:
        self._step_voltage_ladder()
        self.session.apply_block('na', 1.0)
        self._step_voltage_ladder(label='K-isolated voltage ladder')
        self.session.apply_block('na', 0.0)
        self.session.apply_block('k', 1.0)
        self._step_voltage_ladder(label='Na-isolated voltage ladder')
        self.session.clear_blocks()
        self._current_clamp_probe()
        summary = '\n'.join(f"- {text}" for text in self.summaries)
        self.labbook.finalize(summary)

    def _step_voltage_ladder(self, label: str = 'Voltage ladder sweep') -> None:
        steps = []
        for level in range(-80, 60, 20):
            steps.append({'duration_ms': 5.0, 'value': float(level)})
        result = self.session.run_voltage_clamp(steps, label=label, rationale='Steady-state IV sampling')
        insights = self._analyze_iv_curve(result)
        self.labbook.log_experiment(result, insights)

    def _current_clamp_probe(self) -> None:
        protocol = [
            {'duration_ms': 2.0, 'value': 0.0},
            {'duration_ms': 4.0, 'value': 10.0},
            {'duration_ms': 4.0, 'value': 20.0},
            {'duration_ms': 4.0, 'value': -10.0},
        ]
        result = self.session.run_current_clamp(protocol, label='Current clamp excitability', rationale='Probe spikes and membrane recovery')
        insights = self._analyze_current_response(result)
        self.labbook.log_experiment(result, insights)

    def _analyze_iv_curve(self, result: ExperimentResult) -> Dict[str, str]:
        time = result.data.time
        current = result.data.clamp_current
        voltage = result.data.voltage
        segment = int(1.0 / result.data.metadata['dt_ms'])
        steady_indices = []
        start = 0
        for seg in result.protocol:
            end = start + int(seg['duration_ms'] / result.data.metadata['dt_ms'])
            idx = slice(max(start, end - segment), end)
            steady_indices.append((seg['value'], current[idx].mean()))
            start = end
        voltages = np.array([v for v, _ in steady_indices])
        currents = np.array([i for _, i in steady_indices])
        coeffs = np.polyfit(voltages, currents, 1)
        slope, intercept = coeffs
        gl_est = slope
        el_est = -intercept / slope if slope != 0 else float('nan')
        insights = {
            'Conductance slope (approx g_total)': f"{gl_est:.2f} µS/cm²",
            'Reversal estimate': f"{el_est:.2f} mV",
            'Data points': ', '.join(f"({v:.0f}, {i:.1f})" for v, i in steady_indices),
        }
        self.summaries.append(f"IV slope {gl_est:.2f} µS/cm², reversal ~{el_est:.1f} mV")
        return insights

    def _analyze_current_response(self, result: ExperimentResult) -> Dict[str, str]:
        voltage = result.data.voltage
        time = result.data.time
        peak = voltage.max()
        min_v = voltage.min()
        spikes = int((voltage > 0).sum() / (result.data.metadata['dt_ms'] / 1.0))
        insights = {
            'Peak voltage': f"{peak:.1f} mV",
            'Minimum voltage': f"{min_v:.1f} mV",
            'Spike indicator': 'yes' if peak > 0 else 'no',
        }
        self.summaries.append(f"Current clamp peak {peak:.1f} mV, spike={'yes' if peak > 0 else 'no'}")
        return insights
