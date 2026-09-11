"""Solar panel acceptance recipe: one smallsat wing panel, four strings of
18 triple-junction GaAs cells (30 % class, 26.6 cm2, Isc 0.52 A, Voc
2.70 V, Pmax 1.2 W per cell at 25 C, AM0, 1 solar constant), one bypass
diode per cell group of three.

The sequence follows ECSS-E-ST-20-08C Rev.2 Table 5-2 for a flight panel:
visual, health check (insulation resistance at 500 V > 100 MOhm circuit
to substrate, capacitance), electrical performance under a pulsed solar
simulator, corrected to 25 C and 1 SC AM0 with the cell's temperature
coefficients. The reference cell is a secondary working standard
traceable to a primary standard flown or balloon-calibrated; the flasher
is normalised to it on every pulse. Power limits are project-defined in
the specification, not in the standard."""

STRINGS = 4
CELLS_PER_STRING = 18
DIODES_PER_STRING = 6  # one bypass diode per three cells

CELL_ISC_A = 0.520
CELL_VOC_V = 2.70
CELL_PMAX_W = 1.20
D_ISC_A_PER_K = 0.00032  # per cell
D_VOC_V_PER_K = -0.0060  # per cell
STC_TEMP_C = 25.0
AM0_W_M2 = 1366.1

REFERENCE_CELL_ISC_A = 0.5182  # calibrated value at 1 SC AM0, 25 C
PULSE_REPEAT_PCT_MAX = 1.0

IR_TEST_V = 500
IR_MIN_MOHM = 100.0
CAPACITANCE_NF = (80.0, 160.0)

STRING_PMAX_MIN_W = 20.0  # 92.6 % of 21.6 W nominal, per the PVA specification
STRING_MATCH_PCT_MAX = 3.0
FILL_FACTOR_MIN = 0.80
DIODE_VF_MAX_V = 1.2
