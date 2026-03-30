from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Tuple
import math

import numpy as np

ClampMode = Literal['voltage', 'current']


@dataclass
class HHParams:
    g_na: float = 120.0  # mS/cm^2
    g_k: float = 36.0
    g_l: float = 0.3
    e_na: float = 50.0  # mV
    e_k: float = -77.0
    e_l: float = -54.387
    c_m: float = 1.0  # uF/cm^2
    temperature_c: float = 6.3  # match classic squid axon
    area_cm2: float = 1e-4  # effective patch area


@dataclass
class HHState:
    V: float = -65.0
    m: float = 0.0529
    h: float = 0.596
    n: float = 0.3177


@dataclass
class SimulationData:
    time: np.ndarray
    voltage: np.ndarray
    clamp_current: np.ndarray
    ionic_currents: Dict[str, np.ndarray]
    metadata: Dict[str, float | str]


@dataclass
class HodgkinHuxleyTruth:
    params: HHParams = field(default_factory=HHParams)

    def __post_init__(self) -> None:
        self._blocks = {'na': 0.0, 'k': 0.0}

    # --- Channel kinetics -------------------------------------------------
    @staticmethod
    def _alpha_m(V: float) -> float:
        return _safe_division(0.1 * (V + 40.0), 1.0 - math.exp(-(V + 40.0) / 10.0))

    @staticmethod
    def _beta_m(V: float) -> float:
        return 4.0 * math.exp(-(V + 65.0) / 18.0)

    @staticmethod
    def _alpha_h(V: float) -> float:
        return 0.07 * math.exp(-(V + 65.0) / 20.0)

    @staticmethod
    def _beta_h(V: float) -> float:
        return 1.0 / (1.0 + math.exp(-(V + 35.0) / 10.0))

    @staticmethod
    def _alpha_n(V: float) -> float:
        return _safe_division(0.01 * (V + 55.0), 1.0 - math.exp(-(V + 55.0) / 10.0))

    @staticmethod
    def _beta_n(V: float) -> float:
        return 0.125 * math.exp(-(V + 65.0) / 80.0)

    # --- Public controls --------------------------------------------------
    def set_block(self, channel: Literal['na', 'k'], level: float) -> None:
        self._blocks[channel] = min(max(level, 0.0), 1.0)

    def reset_blocks(self) -> None:
        self._blocks = {'na': 0.0, 'k': 0.0}

    # --- Simulation entry points -----------------------------------------
    def simulate_protocol(
        self,
        protocol: List[Tuple[float, float]],
        mode: ClampMode,
        dt_ms: float = 0.01,
        state: HHState | None = None,
    ) -> SimulationData:
        """Simulate a clamp protocol.

        Args:
            protocol: list of (duration_ms, value) pairs. Value = clamp voltage (mV) or
                applied current density (uA/cm^2) depending on mode.
            mode: 'voltage' or 'current'. All segments in a run share the same mode –
                mirroring the physical experiment setup.
            dt_ms: integration step.
        """

        if state is None:
            state = HHState()
        else:
            state = HHState(V=state.V, m=state.m, h=state.h, n=state.n)

        durations = [seg[0] for seg in protocol]
        values = [seg[1] for seg in protocol]
        n_total = int(sum(durations) / dt_ms)
        time = np.zeros(n_total, dtype=np.float64)
        voltage = np.zeros_like(time)
        clamp_current = np.zeros_like(time)
        I_na = np.zeros_like(time)
        I_k = np.zeros_like(time)
        I_l = np.zeros_like(time)

        index = 0
        t = 0.0
        for duration, value in zip(durations, values):
            n_steps = int(duration / dt_ms)
            for _ in range(n_steps):
                if index >= n_total:
                    break
                if mode == 'voltage':
                    V_cmd = value
                    V = V_cmd
                    # gating updates use clamp voltage
                    state.m = _rk1_gate(state.m, self._alpha_m(V), self._beta_m(V), dt_ms)
                    state.h = _rk1_gate(state.h, self._alpha_h(V), self._beta_h(V), dt_ms)
                    state.n = _rk1_gate(state.n, self._alpha_n(V), self._beta_n(V), dt_ms)
                    m, h, n = state.m, state.h, state.n
                    g_na = self.params.g_na * (1.0 - self._blocks['na'])
                    g_k = self.params.g_k * (1.0 - self._blocks['k'])
                    g_l = self.params.g_l
                    i_na = g_na * (m ** 3) * h * (V - self.params.e_na)
                    i_k = g_k * (n ** 4) * (V - self.params.e_k)
                    i_l = g_l * (V - self.params.e_l)
                    I_total = i_na + i_k + i_l
                    clamp = I_total  # equal and opposite to keep V fixed
                else:  # current clamp
                    g_na = self.params.g_na * (1.0 - self._blocks['na'])
                    g_k = self.params.g_k * (1.0 - self._blocks['k'])
                    g_l = self.params.g_l
                    m = state.m
                    h = state.h
                    n = state.n
                    i_na = g_na * (m ** 3) * h * (state.V - self.params.e_na)
                    i_k = g_k * (n ** 4) * (state.V - self.params.e_k)
                    i_l = g_l * (state.V - self.params.e_l)
                    I_ion = i_na + i_k + i_l
                    I_app = value
                    dV = (I_app - I_ion) / self.params.c_m
                    state.V += dt_ms * dV
                    V = state.V
                    state.m = _rk1_gate(m, self._alpha_m(V), self._beta_m(V), dt_ms)
                    state.h = _rk1_gate(h, self._alpha_h(V), self._beta_h(V), dt_ms)
                    state.n = _rk1_gate(n, self._alpha_n(V), self._beta_n(V), dt_ms)
                    clamp = I_app
                    i_na = g_na * (state.m ** 3) * state.h * (V - self.params.e_na)
                    i_k = g_k * (state.n ** 4) * (V - self.params.e_k)
                    i_l = g_l * (V - self.params.e_l)

                time[index] = t
                voltage[index] = V
                clamp_current[index] = clamp
                I_na[index] = i_na
                I_k[index] = i_k
                I_l[index] = i_l

                t += dt_ms
                index += 1
        metadata = {
            'mode': mode,
            'dt_ms': dt_ms,
            'g_na': self.params.g_na,
            'g_k': self.params.g_k,
            'g_l': self.params.g_l,
            'block_na': self._blocks['na'],
            'block_k': self._blocks['k'],
        }
        ionic = {'na': I_na, 'k': I_k, 'l': I_l}
        return SimulationData(time=time, voltage=voltage, clamp_current=clamp_current, ionic_currents=ionic, metadata=metadata)


def _rk1_gate(x: float, alpha: float, beta: float, dt_ms: float) -> float:
    return x + dt_ms * (alpha * (1.0 - x) - beta * x)


def _safe_division(num: float, denom: float) -> float:
    if abs(denom) < 1e-9:
        return num / 1e-9
    return num / denom
