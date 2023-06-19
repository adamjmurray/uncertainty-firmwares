import machine
from lib.io import read_cv, output, num_outs
from lib.dsp import BipolarTrigger

machine.freq(250000000)  # 2x default

trigger = BipolarTrigger(rising_thresh=1.9)
active_gate = 0

while True:
    offset = 0
    volts = 5 * read_cv()
    trig = trigger.detect(volts)

    if trig != 0:
        # fine-tuning a bit because read_cv() is not perfectly normalized
        # This will advance by 1 around 2V, by 2 at 3V, by 3 at 4V, and by 4 at 5V
        if trig > 4.7:  # TODO: why is this so low, do we need to recalibrate?
            offset = 4
        elif trig > 3.9:
            offset = 3
        elif trig > 2.9:
            offset = 2
        elif trig > 0:
            offset = 1
        elif trig < -4.9:
            offset = -4
        elif trig < -3.9:
            offset = -3
        elif trig < -2.9:
            offset = -2
        elif trig < 0:
            offset = -1

        if offset != 0:
            # print("trigger=%.3fV, offset=%d" % (trig, offset))
            output(active_gate, 0)
            active_gate = (active_gate + offset) % num_outs
            output(active_gate, 1)
