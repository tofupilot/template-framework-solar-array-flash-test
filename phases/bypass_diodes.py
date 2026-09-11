import numpy as np

from utils.recipe import CELL_ISC_A, DIODES_PER_STRING, STRINGS


def bypass_diodes(measurements, bench, log):
    """Every bypass diode carries the string current once, its forward
    drop recorded. An open diode reads the reverse breakdown of the
    shaded cells it was meant to protect; a shorted one reads zero."""
    vf = []
    for s in range(1, STRINGS + 1):
        for d in range(1, DIODES_PER_STRING + 1):
            vf.append(bench.bypass_diode_vf(s, d, CELL_ISC_A))
    vf = np.array(vf)
    measurements.diodes.x_axis = list(range(1, len(vf) + 1))
    measurements.diodes.y_axis.vf = vf.tolist()
    measurements.diodes.y_axis.vf.aggregations.max_v = float(vf.max())
    measurements.diodes.y_axis.vf.aggregations.min_v = float(vf.min())
    log.info(f"{len(vf)} bypass diodes: Vf {vf.min():.3f}..{vf.max():.3f} V at {CELL_ISC_A:.2f} A")
