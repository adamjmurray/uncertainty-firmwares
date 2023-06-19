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

    def __init__(self, rising_thresh=0.2, falling_thresh=0.1, rising_window=100, falling_window=100):
        self.rising_thresh = rising_thresh
        self.falling_thresh = falling_thresh
        self.rising_window = rising_window
        self.falling_window = falling_window
        self.state = BipolarTrigger.STATE_OFF
        self.countdown = 0

    def detect(self, sample):
        absval = abs(sample)

        if self.state == BipolarTrigger.STATE_OFF:
            if absval >= self.rising_thresh:
                self.state = BipolarTrigger.STATE_RISING
                self.countdown = self.rising_window

        elif self.state == BipolarTrigger.STATE_RISING:
            if absval >= self.rising_thresh:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.state = BipolarTrigger.STATE_ON
                    return True  # True indicates the moment we transitioned to ON
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
                    return False  # False indicates the momen we transitioned to OFF
            else:
                self.state = BipolarTrigger.STATE_ON

        # if we didn't transition to ON or OFF, we always return None
        return None
