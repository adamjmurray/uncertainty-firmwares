from lib.core import NUM_OUTS, BipolarTrigger


class Stepper:

    def __init__(self):
        self.trigger = BipolarTrigger(rising_thresh=1)
        self.active_gate = 0

    def process(self, volts, output):
        if self.trigger.detect(volts):
            offset = min(max(int(volts), -4), 4)
            if offset != 0:
                output(self.active_gate, 0)
                self.active_gate = (self.active_gate + offset) % NUM_OUTS
                output(self.active_gate, 1)
