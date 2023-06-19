# This firmware reports the voltage at the CV input to Uncertainty.
# Try sending known calibrated voltages (such as from a Mordax DATA) to the module
# while running this firmware via Thonny so you can see the print() calls.
# From -4V to +4V, the voltage should be accurate within a few hundreths of a volt.
# If not, try the procedure in calibrate.py.

from machine import Timer
from lib.io import read_volts, output
from lib.dsp import MovingAverage, Counter


SAMPLERATE = 1000

averager = MovingAverage(samplecount=1000)
counter = Counter(max=SAMPLERATE)


def mainloop(_):
    volts = read_volts()
    avg = averager.process(volts)
    if counter.process():
        print("volts=%.2f" % avg)


Timer(
    mode=Timer.PERIODIC,
    freq=SAMPLERATE,
    callback=mainloop
)
