from machine import ADC, Pin

_CV_IN = ADC(Pin(26))
_GATE_OUTS = [Pin(number, Pin.OUT) for number in [27, 28, 29, 0, 3, 4, 2, 1]]

num_outs = len(_GATE_OUTS)  # TODO: phase out in place of constants.NUM_OUTS

# To calibrate CV reads, I made some measurements:
# --------------------------------------
# input voltage | cv_in.read_u16() value
#           -5V | 3470
#           +5V | 64440
# --------------------------------------
# This leads to the formula for normalizing from (-1,1) over the input -5V to +5V:
# (cv_in.read_u16() - 3470)/(64440 - 3470)
# However, the range is stretched out when close to +/-5V, so I adjusted it
# trial and error to make it behave nice and linear from -3V to 3V where each
# volt is 0.2 of normalized cv value. This led me to change 64440 to 65500
# and arrive at the following normalization formula for read_cv().
# Different hardware may need different calibration here, so try sending
# your Uncertainty known voltages (from e.g. a Mordax DATA module) and
# adjusting the numbers in read_cv() until you get good results.


def read_cv():
    # Returns a normalize input value in the clamped range (-1, 1),
    # representing approximately -5V to +5V of input voltage.
    normalized = (_CV_IN.read_u16() - 3470)/62030
    clamped = min(max(normalized, 0), 1)
    return 2 * clamped - 1


def read_volts():
    # Returns a normalize input value in the clamped range (-5, 5),
    # representing approximately -5V to +5V of input voltage.
    # It tracks well over -4V to +4V but you may have to input 6V or 7V to hit 5.
    # It may not be possible to hit -5.
    normalized = (_CV_IN.read_u16() - 3470)/62030
    clamped = min(max(normalized, 0), 1)
    return 10 * clamped - 5


def output(index, value):
    try:
        _GATE_OUTS[index].value(value)
    except IndexError:
        print("Invalid output index: %s. Must be between %d and %d (inclusive)." % (index, 0, len(_GATE_OUTS)-1))
