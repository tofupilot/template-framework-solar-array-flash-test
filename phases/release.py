def release(measurements, bench, unit, log):
    """Teardown: panel shorted, lamp pulse count logged against the flash
    tube's rated life."""
    bench.short_panel()
    measurements.pulses_this_run = bench.pulses_used()
    unit.metadata["flash_pulses"] = bench.pulses_used()
    log.info(f"Panel shorted, {bench.pulses_used()} pulses this run")
