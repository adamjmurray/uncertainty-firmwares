# A firmware for calibrating an Uncertainty module.
#
# Procedure:
# 1. Load this firmware onto your Uncertainty. You need lib/dsp.py installed on the microcontroller's file system (see README).
# 2. Let your system warm up for 20+ minutes.
# 3. Plug a device that can generate calibrated voltages (such as Mordax DATA) and connect it to Uncertainty's input.
# 4. Note the the readings printed out at -4V and +4V. A moving average is used to smooth it out, but it constantly fluxuates
#    due to noise, so try to choose a number the value is centered around.
# 5. Update the NEG_4V_READING and POS_4V_READING constants based on your readings and re-run this firmware.
# 6. Send -4V, -3V, -2V, -1V, 0V, +1V, +2V, +3V, and +4V inputs to the Uncertainty.
#    The estimated volts value should be within a few hundreths of the actual voltage.
#    If not, try adjusting the NEG_4V_READING and POS_4V_READING constants until you get acceptable results.
#    In my experience it is not possible to accurately read +5V, so don't worry about it.
#    This is analog so it won't be prefect. Decide what is good enough for your needs and move on.
# 7. Update lib/io.py with your calibrated settings. Now all firmwares in this project are calibrated.
# 8. Confirm lib/io.py works correctly via the calibration_test.py firmware in this folder

from machine import ADC, Pin, Timer
from lib.core import MovingAverage, Counter

CV_IN = ADC(Pin(26))

SAMPS_PER_SEC = 100

averager = MovingAverage(samplecount=SAMPS_PER_SEC)
counter = Counter(max=SAMPS_PER_SEC)

NEG_4V_READING = 9720
POS_4V_READING = 59010


def mainloop(_):
    raw_reading = CV_IN.read_u16()
    avg = averager.process(raw_reading)
    if counter.process():
        print("reading=%i, estimated volts=%.2f" %
              (avg, (raw_reading - NEG_4V_READING) / (POS_4V_READING - NEG_4V_READING) * 8 - 4))


Timer(
    mode=Timer.PERIODIC,
    freq=SAMPS_PER_SEC,
    callback=mainloop
)
