from enum import Enum


class SimpleLPF:
    def __init__(self, weight=0.5):
        self.weight = weight
        self.prev = 0

    def filter(self, sample):
        self.prev = self.weight * self.prev + (1 - self.weight) * sample
        return self.prev


class BipolarTrigger:
    State = Enum('BipolarTriggerState', ['OFF', 'RISING', 'ON', 'FALLING'])

    def __init__(self, rising_thresh=0.2, falling_thresh=0.1, rising_window=100, falling_window=100, lpf_weight=0.1):
        self.rising_thresh = rising_thresh
        self.falling_thresh = falling_thresh
        self.rising_window = rising_window
        self.falling_window = falling_window
        self.state = BipolarTrigger.State.OFF
        self.countdown = 0
        self.lpf = SimpleLPF(lpf_weight)

    def detect(self, sample):

        filtered = self.lpf.filter(sample)
        absval = abs(filtered)

        print("=> RISING: %f %s" % (absval, self.rising_thresh))

        if self.state == BipolarTrigger.State.OFF:
            if absval >= self.rising_thresh:
                self.state = BipolarTrigger.State.RISING
                self.countdown = self.rising_window

        elif self.state == BipolarTrigger.State.RISING:
            if absval >= self.rising_thresh:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.state = BipolarTrigger.State.ON
                    # the only time this returns anything other than zero is the moment we transition to the ON state:
                    return filtered

            else:
                self.state = BipolarTrigger.State.OFF

        elif self.state == BipolarTrigger.State.ON:
            if absval <= self.falling_thresh:
                self.state = BipolarTrigger.State.FALLING
                self.countdown = self.falling_window

        elif self.state == BipolarTrigger.State.FALLING:
            if absval <= self.falling_thresh:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.state = BipolarTrigger.State.OFF
            else:
                self.state = BipolarTrigger.State.ON

        # if we didn't transition to ON, we always return 0
        return 0
