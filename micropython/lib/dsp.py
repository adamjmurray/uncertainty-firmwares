class SimpleLPF:
    def __init__(self, weight=0.5):
        self.weight = weight
        self.prev = 0

    def filter(self, sample):
        self.prev = self.weight * self.prev + (1 - self.weight) * sample
        return self.prev


class BipolarTrigger:
    STATE_OFF = "OFF"
    STATE_RISING = "RISING"
    STATE_ON = "ON"
    STATE_FALLING = "FALLING"

    def __init__(self, rising_thresh=0.2, falling_thresh=0.1, rising_window=100, falling_window=100, lpf_weight=0.1):
        self.rising_thresh = rising_thresh
        self.falling_thresh = falling_thresh
        self.rising_window = rising_window
        self.falling_window = falling_window
        self.state = BipolarTrigger.STATE_OFF
        self.countdown = 0
        self.lpf = SimpleLPF(lpf_weight)

    def detect(self, sample):
        filtered = self.lpf.filter(sample)
        absval = abs(filtered)

        if self.state == BipolarTrigger.STATE_OFF:
            if absval >= self.rising_thresh:
                self.state = BipolarTrigger.STATE_RISING
                self.countdown = self.rising_window

        elif self.state == BipolarTrigger.STATE_RISING:
            if absval >= self.rising_thresh:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.state = BipolarTrigger.STATE_ON
                    # the only time this returns anything other than zero is the moment we transition to the ON state:
                    return filtered

            else:
                self.state = BipolarTrigger.STATE_OFF

        elif self.state == BipolarTrigger.STATE_ON:
            if absval <= self.falling_thresh:
                self.state = BipolarTrigger.STATE_FALLING
                self.countdown = self.falling_window

        elif self.state == BipolarTrigger.STATE_FALLING:
            if absval <= self.falling_thresh:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.state = BipolarTrigger.STATE_OFF
            else:
                self.state = BipolarTrigger.STATE_ON

        # if we didn't transition to ON, we always return 0
        return 0
