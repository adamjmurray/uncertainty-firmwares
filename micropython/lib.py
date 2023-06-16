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


def read_cv():  # => clamped range (-1, 1) over approximately -5V to +5V of input
    # different modules may need different calibration
    normalized = (cv_in.read_u16() - 3470)/65500
    clamped = min(max(normalized, 0), 1)
    return 2 * clamped - 1


def write_out(index, value):
    try:
        outs[index].value(value)
    except IndexError:
        print("Invalid index %s" % index)
