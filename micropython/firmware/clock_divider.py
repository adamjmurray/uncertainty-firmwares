from lib.core import NUM_OUTS, BipolarTrigger


class ClockDivider:

    def __init__(self, _output):
        self.trigger = BipolarTrigger(rising_thresh=1, window=10)
        self.divisions = [i+2 for i in range(NUM_OUTS)]
        self.reset()

    def reset(self):
        self.counts = [-1 for _ in range(NUM_OUTS)]

    def process(self, volts, output):
        if self.trigger.detect(volts):
            if volts < 0:
                self.reset()
            for i in range(NUM_OUTS):
                self.counts[i] = (self.counts[i] + 1) % self.divisions[i]
                output(i, self.counts[i] == 0)
