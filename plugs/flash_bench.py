"""Solar panel flash test bench (mock): large-area pulsed solar simulator
with its reference cell, electronic load sweeping the string during the
pulse, megohmmeter, capacitance meter and panel thermocouples.

Maps to a Spectrolab LAPSS II-class flasher (2 ms xenon pulse, +-1 %
pulse-to-pulse, +-2 % uniformity over the plane), a fast IV load, a
Keysight B2985-class electrometer or a megohmmeter for the 500 V
insulation test, an LCR meter and type-T thermocouples. The mock
synthesizes a healthy panel at 23 C: four strings within 1 % of each
other on Pmax, one string 1.5 % low, all bypass diodes conducting, the
insulation at 2 GOhm. Swap for classes speaking the flasher's control
protocol and SCPI; the phases stay unchanged.
"""

import numpy as np

from utils.recipe import (AM0_W_M2, CELLS_PER_STRING, CELL_ISC_A, CELL_PMAX_W, CELL_VOC_V, DIODES_PER_STRING,
                          D_ISC_A_PER_K, D_VOC_V_PER_K, REFERENCE_CELL_ISC_A, STC_TEMP_C, STRINGS)


class FlashBench:
    def __init__(self):
        self._rng = np.random.default_rng(2008)
        self._panel_temp_c = 23.4
        self._string_gain = 1.0 + self._rng.normal(0.0, 0.005, STRINGS)
        self._string_gain[2] = 0.985  # string 3 a little low: one cell at the bottom of its grade
        self._intensity = 1.0  # solar constants delivered by the flasher this pulse
        self._ir_mohm = {"circuit_substrate": 2100.0, "adjacent_strings": 1800.0, "sensor_substrate": 3400.0}
        self._cap_nf = 118.0
        self._diode_vf = 0.82 + self._rng.normal(0.0, 0.03, STRINGS * DIODES_PER_STRING)
        self._pulses = 0
        # self.flasher = ...; self.load = pyvisa...; self.megger = pyvisa...; self.lcr = pyvisa...
        print("Flash bench ready, lamp warm, reference cell in the plane")

    def panel_temperature_c(self):
        return round(self._panel_temp_c + self._rng.normal(0.0, 0.1), 2)

    def _pulse(self):
        self._pulses += 1
        self._intensity = 1.0 + self._rng.normal(0.0, 0.004)
        return self._intensity

    def reference_pulse(self):
        """One pulse on the reference cell alone: its Isc says what the
        flasher delivered, in solar constants, via the calibrated value."""
        k = self._pulse()
        return {"isc_a": round(REFERENCE_CELL_ISC_A * k + self._rng.normal(0.0, 0.0003), 5), "pulse": self._pulses}

    def flash_iv(self, string, points):
        """One pulse with the load sweeping the string from short circuit
        to open circuit; the reference cell reads the same pulse."""
        k = self._pulse()
        i = string - 1
        dt = self._panel_temp_c - STC_TEMP_C
        isc = (CELL_ISC_A + D_ISC_A_PER_K * dt) * k * self._string_gain[i]
        voc = CELLS_PER_STRING * (CELL_VOC_V + D_VOC_V_PER_K * dt) + 0.026 * CELLS_PER_STRING * np.log(k)
        v = np.linspace(0.0, voc, points)
        # Single-diode shape with a fill factor near 0.85 for 3J cells.
        n_vt = 0.075 * CELLS_PER_STRING
        cur = isc * (1.0 - (np.exp((v - voc) / n_vt) - np.exp(-voc / n_vt)) / (1.0 - np.exp(-voc / n_vt)))
        cur = np.clip(cur, 0.0, None) + self._rng.normal(0.0, 0.0004, points)
        ref_isc = REFERENCE_CELL_ISC_A * k + self._rng.normal(0.0, 0.0003)
        return {"voltage_v": v.round(4).tolist(), "current_a": cur.round(5).tolist(), "ref_isc_a": round(ref_isc, 5),
                "panel_temp_c": self.panel_temperature_c(), "pulse": self._pulses}

    def insulation_mohm(self, path, volts):
        return round(self._ir_mohm[path] * (1.0 + self._rng.normal(0.0, 0.02)), 0)

    def capacitance_nf(self):
        return round(self._cap_nf + self._rng.normal(0.0, 0.5), 1)

    def bypass_diode_vf(self, string, diode, current_a):
        """Reverse-bias one cell group so its bypass diode carries the
        string current; the drop across it is the diode's forward voltage."""
        idx = (string - 1) * DIODES_PER_STRING + (diode - 1)
        return round(float(self._diode_vf[idx]) + 0.02 * np.log(current_a / 0.5) + self._rng.normal(0.0, 0.004), 3)

    def pulses_used(self):
        return self._pulses

    def short_panel(self):
        pass

    def __del__(self):
        print("Panel shorted, lamp idle")
