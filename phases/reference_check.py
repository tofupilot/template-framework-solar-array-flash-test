import numpy as np

from utils.recipe import PULSE_REPEAT_PCT_MAX, REFERENCE_CELL_ISC_A


def reference_check(measurements, bench, unit, log):
    """Setup: three pulses on the reference cell alone. Their spread is the
    flasher's pulse-to-pulse repeatability, their mean over the calibrated
    value is the intensity the lamp delivers; the panel temperature must
    sit in the window the correction is valid for."""
    isc = np.array([bench.reference_pulse()["isc_a"] for _ in range(3)])
    spread = 100.0 * (isc.max() - isc.min()) / isc.mean()
    measurements.pulse_repeat_pct = float(spread)
    measurements.lamp_intensity_sc = float(isc.mean() / REFERENCE_CELL_ISC_A)
    measurements.panel_temp_c = bench.panel_temperature_c()
    unit.metadata["reference_cell"] = "WS-2026-07, secondary standard"
    log.info(f"Panel {unit.serial_number}: lamp {isc.mean() / REFERENCE_CELL_ISC_A:.4f} SC, pulse spread {spread:.2f} % (limit {PULSE_REPEAT_PCT_MAX}), panel {measurements.panel_temp_c} C")
