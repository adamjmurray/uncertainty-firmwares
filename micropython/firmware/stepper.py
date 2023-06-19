# "Stepper" Firmware
# ------------------
# This firmware always has one active gate.
# Input signals of more than +/- 1 volt will trigger the module.
# A positive trigger steps forward to the next gate.
# A negative trigger steps backward.
# Triggers with a magnitude of approximately 1-2 volts step by 1.
# Triggers between 2-3 volts step by 2, between 3-4 volts step by 3,
# and anything greater than 4 volts steps by 4.

from lib.core import NUM_OUTS, BipolarTrigger


class Stepper:

    def __init__(self, output):
        self.trigger = BipolarTrigger(rising_thresh=1)
        self.active_gate = 0
        for index in range(NUM_OUTS):
            output(index, index == self.active_gate)

    def process(self, volts, output):
        if self.trigger.detect(volts):
            offset = min(max(int(volts), -4), 4)
            if offset != 0:
                output(self.active_gate, False)
                self.active_gate = (self.active_gate + offset) % NUM_OUTS
                output(self.active_gate, True)
