import numpy as np

from utils.correction import correct_to_stc, iv_metrics
from utils.recipe import STRINGS

POINTS = 200


def flash_iv(measurements, bench, log):
    """One pulse per string, the load sweeping short circuit to open
    circuit during the 2 ms flash, every curve corrected to 25 C and 1 SC
    AM0 from the reference cell's reading of the same pulse and the panel
    thermocouple. Four corrected curves in one measurement, Pmax and fill
    factor per string as aggregations, the string match as a scalar."""
    pmax = []
    for s in range(1, STRINGS + 1):
        cap = bench.flash_iv(s, POINTS)
        v, i, intensity = correct_to_stc(cap["voltage_v"], cap["current_a"], cap["ref_isc_a"], cap["panel_temp_c"])
        m = iv_metrics(v, i)
        pmax.append(m["pmax_w"])
        if s == 1:
            measurements.iv.x_axis = v.round(3).tolist()
        setattr(measurements.iv.y_axis, f"string_{s}", i.round(4).tolist())
        y = getattr(measurements.iv.y_axis, f"string_{s}")
        y.aggregations.pmax_w = m["pmax_w"]
        y.aggregations.isc_a = m["isc_a"]
        y.aggregations.voc_v = m["voc_v"]
        y.aggregations.fill_factor = m["fill_factor"]
        log.info(f"String {s}: pulse {cap['pulse']} at {intensity:.4f} SC, {cap['panel_temp_c']:.1f} C -> Isc {m['isc_a']:.4f} A, Voc {m['voc_v']:.2f} V, Pmax {m['pmax_w']:.2f} W, FF {m['fill_factor']:.3f}")

    pmax = np.array(pmax)
    match = float(100.0 * (pmax.max() - pmax.min()) / pmax.mean())
    measurements.panel_pmax_w = float(pmax.sum())
    measurements.string_match_pct = match
    log.info(f"Panel Pmax {pmax.sum():.1f} W corrected, string match {match:.2f} %")
