# To use:
# - Connect Uncertainty via USB (and flash MicroPython if needed)
# - Open this file in Thonny
# - File -> Save as... -> RP2040 Device (if it's busy, click the stop button and try again)
# - Save as lib.py on the device
# - Now you can run scripts on the device that `from lib import ...`
#
# IMPORTANT: Once you Save as onto the device, any edits you make also save onto the device
# This can be really nice for debugging and adding more features, but you must make sure
# to save the changes back to the file on the computer and commit to git.

from machine import ADC, Pin

cv_in = ADC(Pin(26))

outs = [Pin(number, Pin.OUT) for number in [27, 28, 29, 0, 3, 4, 2, 1]]

num_outs = len(outs)

# To calibrate CV reads, I made some measurements:
# --------------------------------------
# input voltage | cv_in.read_u16() value
#           -5V | 3470
#           +5V | 64440
# --------------------------------------
# This leads to the formula for normalizing from (-1,1) over the input -5V to +5V:
# (cv_in.read_u16() - 3470)/(64440 - 3470)
# However, the range is stretched out when close to +/-5V, so I fudged things through
# trial and error to make it behave nice and linear from -3V to 3V where each
# volt is 0.2 of normalized cv value. This led me to change 64440 to 65500
# and arrive at the following normalization formula for read_cv().
# Different hardware may need different calibration here.


def read_cv():
    # Returns a normalize input value in the clamped range (-1, 1),
    # representing approximately -5V to +5V of input voltage.
    normalized = (cv_in.read_u16() - 3470)/62030
    clamped = min(max(normalized, 0), 1)
    return 2 * clamped - 1


def write_out(index, value):
    try:
        outs[index].value(value)
    except IndexError:
        print("Invalid index %s" % index)
