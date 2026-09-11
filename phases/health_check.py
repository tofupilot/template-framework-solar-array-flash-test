from utils.recipe import IR_TEST_V


def health_check(measurements, bench, log):
    """Electrical health check per ECSS-E-ST-20-08: insulation resistance
    at 500 V on three paths and the panel capacitance. Done before the
    flash and repeated after environments; a value that moved is a crack."""
    measurements.ir_circuit_substrate_mohm = bench.insulation_mohm("circuit_substrate", IR_TEST_V)
    measurements.ir_adjacent_strings_mohm = bench.insulation_mohm("adjacent_strings", 250)
    measurements.ir_sensor_substrate_mohm = bench.insulation_mohm("sensor_substrate", IR_TEST_V)
    measurements.capacitance_nf = bench.capacitance_nf()
    log.info(f"IR circuit-substrate {measurements.ir_circuit_substrate_mohm} MOhm at {IR_TEST_V} V, capacitance {measurements.capacitance_nf} nF")
