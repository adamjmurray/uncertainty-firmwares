from machine import ADC, Pin, Timer

# print(machine.freq()) # 125000000, 125MHz, plenty for running a high sample rate, and we can overclock
SAMPLERATE = 5

# different modules may need different calibration
CALIB_NEG5 = 3470
# I measured this at 64440, but fudged it because 0-4V were all a bit high
CALIB_POS5 = 65500
CALIB_RANGE = CALIB_POS5 - CALIB_NEG5


# convert to range (-1, 1) over approximately -5V to +5V of input
def normalize(read_u16_val):
    normalized = (read_u16_val - CALIB_NEG5)/CALIB_RANGE
    clamped = min(max(normalized, 0), 1)
    return 2 * clamped - 1


def voltage(read_u16_val):
    return 5 * normalize(read_u16_val)


class LPF:
    def __init__(self, weight=0.5):
        self.weight = weight
        self.prev = 0

    def filter(self, sample):
        self.prev = self.weight * self.prev + (1 - self.weight) * sample
        return self.prev


cv_in = ADC(Pin(26))
outs = [Pin(number, Pin.OUT) for number in [27, 28, 29, 0, 3, 4, 2, 1]]

num_outs = len(outs)
lpf = LPF(0.1)


def mainloop(_timer):
    raw = cv_in.read_u16()
    cv = lpf.filter(normalize(raw))  # (-1, 1) range for -5V to +5V input

    active_gate = abs(round(cv * (num_outs-1)))

    # Slow down the sample rate (e.g. SAMPLERATE=1) to print:
    print("raw=%i, voltage=%.2f, cv=%.2f, gate=%i" %
          (raw, voltage(raw), cv, active_gate))

    for num in range(8):
        if num != active_gate:
            outs[num].value(0)

    outs[active_gate].value(1)


Timer(freq=SAMPLERATE, mode=Timer.PERIODIC, callback=mainloop)
