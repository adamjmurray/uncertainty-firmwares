import machine
import random
from lib.io import read_cv, output, num_outs
from lib.dsp import BipolarTrigger

machine.freq(250000000)  # 2x default

trigger = BipolarTrigger(rising_thresh=1.9)
gate_indexes = list(range(num_outs))

while True:
    num_gates = 0
    volts = 5 * read_cv()
    trig = trigger.detect(volts)

    if trig != 0:
        # fine-tuning a bit because read_cv() is not perfectly normalized
        # This will advance by 1 around 2V, by 2 at 3V, by 3 at 4V, and by 4 at 5V
        if trig > 4.7:  # TODO: why is this so low, do we need to recalibrate?
            num_gates = 4
        elif trig > 3.9:
            num_gates = 3
        elif trig > 2.9:
            num_gates = 2
        elif trig > 0:
            num_gates = 1
        elif trig < -4.9:
            num_gates = -4
        elif trig < -3.9:
            num_gates = -3
        elif trig < -2.9:
            num_gates = -2
        elif trig < 0:
            num_gates = -1

        num_gates %= num_outs

        # TODO: randomly select num_gates to be active
        # loop, selecting with probability num_gates/num_left until we have num_gates
        active_gates = random.sample(gate_indexes, num_gates)
        for index in range(num_outs):
            output(index, index in active_gates)
