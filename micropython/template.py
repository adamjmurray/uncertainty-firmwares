import machine
from machine import ADC, Pin

machine.freq(250000000)  # 2x default
cv_in = ADC(Pin(26))
outs = [Pin(number, Pin.OUT) for number in [27, 28, 29, 0, 3, 4, 2, 1]]
num_outs = len(outs)


def read_cv():  # => clamped range (-1, 1) over approximately -5V to +5V of input
    # different modules may need different calibration
    normalized = (cv_in.read_u16() - 3470)/65500
    clamped = min(max(normalized, 0), 1)
    return 2 * clamped - 1


while (True):
    cv = read_cv()
    active_gate = abs(round(cv * num_outs-1))
    for num in range(num_outs):
        outs[num].value(num == active_gate)
