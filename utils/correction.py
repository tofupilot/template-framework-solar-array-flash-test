"""Correction of a flashed IV curve to 25 C and 1 solar constant AM0 using
the cell temperature coefficients and the reference cell's reading of the
pulse. Translation per the usual practice: current scales with intensity
and shifts with temperature, voltage shifts with temperature."""

import numpy as np

from utils.recipe import (CELLS_PER_STRING, D_ISC_A_PER_K, D_VOC_V_PER_K, REFERENCE_CELL_ISC_A, STC_TEMP_C)


def correct_to_stc(voltage_v, current_a, ref_isc_a, panel_temp_c):
    intensity = ref_isc_a / REFERENCE_CELL_ISC_A
    dt = STC_TEMP_C - panel_temp_c
    v = np.array(voltage_v) + CELLS_PER_STRING * D_VOC_V_PER_K * dt
    i = np.array(current_a) / intensity + D_ISC_A_PER_K * dt
    return v, i, intensity


def iv_metrics(v, i):
    p = v * i
    k = int(np.argmax(p))
    isc = float(i[0])
    voc = float(np.interp(0.0, i[::-1], v[::-1]))
    pmax = float(p[k])
    return {"isc_a": isc, "voc_v": voc, "pmax_w": pmax, "vmp_v": float(v[k]), "imp_a": float(i[k]),
            "fill_factor": pmax / (isc * voc)}
