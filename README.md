# Firmwares for Uncertainty

Alternate firmwares for the [Uncertainty Eurorack
module](https://oamodular.org/products/uncertainty).

## Micropython Firmwares

### Setup

1. Install [Thonny](https://thonny.org/)
2. Hold down the boot button on the unpowered Uncertainty module while plugging
   it into your computer with USB
3. Run Thonny and go to Preferences -> Interpreter -> Install or Update
   Micropython. Choose:
   - Target volume probably looks like RPI-RP2, of family RP2
   - MicroPython variant: Raspberry Pi - Pico / Pico H
   - version: 1.20.0
4. Click install
5. Back in the Interpreter preferences, choose:
   - kind of interpreter: MicroPython (RP2040)
   - port: try to detect automatically

Also see
https://github.com/oamodular/uncertainty#letss-write-a-simple-utility-in-micropython

Note: Once the Micropython runtime is installed, you don't need to hold the boot
button when powering on. Just connect with USB and you're good to go.

### Running the demo firmware

With Uncertainty connected via USB:

1. Open the `demo.py` file from the `micropython` folder in Thonny
2. Click Run

Note you can call `print()` and see it in the Thonny shell. You can see the
actual CV input values from the hardware this way. That's how I calibrated
reading CV input, as explained in the comments in `micropython/lib/io.py`.

### Installing shared lib code

`demo.py` contains everything needed to run the firmware so it's easy to get
started. By comparison, most of the firmwares don't contain everything they
need. That's because the `micropython/lib` folder contains resuable code used by
many of the firmwares. It's setup this way so we don't have to copy and paste
the same code over and over to every firmware file, which would make fixing bugs
and adding features a nightmare.

To use these firmwares, we have to first install the lib files onto the
hardware:

- Open Thonny with Uncertainty connected over USB
- Open `micropython/lib/io.py` in Thonny
- File -> Save as... -> RP2040 Device (if it's busy, click the stop button and
  try again)
- Save as `lib/io.py` on the device (create a `lib` folder and save `io.py`
  inside it)
- Do the same thing with `micropython/lib/core.py` (open, save as -> RP2040
  Device, save it in the `lib` folder on the device as `core.py`)

In case this README gets out-of-date, you might need to copy over anything else
in `micropython/lib`.

Now you can run the firmwares that import lib code.

IMPORTANT: Once you Save as onto the device, any edits you make also save onto
the device _and only the device_. This can be really nice for debugging and
adding more features, but you must make sure to save the changes back to the
file on the computer so you don't lose them! In the file tabs, Thonny shows
[square brackets] around files that are on the device.

### Running the other firmwares

After installing the shared lib code as explained above, we need to do the same
thing with the firmware files. Save any files of interest in the `micropython/firmware`
to a folder called `firmware` on the hardware.

Then we can use the general purpose `firmware_loader.py` script to run any of these
firmwares. Simply edit `firmware_loader.py` to load the firmware of your choice.

The firmware_loader script handles some basic boilerplate for setting up the main
loop of the firmware. All firmwares in the firmware folder are based on the simple
interface `process(volts, output)`, which is called for every iteration of the main
loop. It is given the current input voltage level as provided by the function in `lib/io.py`.
It is also give the `output()` function from `lib/io.py`. You can make your own
firmware by creating a class that implements this function.

Note: The reason `output()` is not imported directly is so unit tests of the firmware can be more
easily written by passing in a mock output function.

### Calibration

If the voltage levels are wrong for your hardware, take a look at the calibrate.py and
calibration_test.py firmwares.

### Using these firmwares away from the computer

If you want to disconnect from the computer and use the module normally in
your rack, use File -> Save As ... to save the firmware script as `main.py`
on the hardware. This file runs automatically when the module powers on.

Since most firmwares are designed to run via the `firmware_loader.py` script,
this is the one you will typically save as `main.py`.

### Running Python tests

From the root of this repository (the folder containing the python_uncertainty
folder), run:

```bash
python3 -m unittest discover -v micropython.test
```

These tests are focused on `lib` code that doesn't depend on the micropython
`machine` package. I'm not sure how to stub out the `machine` package for
testing purposes, so I just tried to structure the code to avoid needing that
package in tests.

### Coding in VS Code

I can't find a good, stable solution for runnning Micropython on the Uncertainty
from VS Code. The Pico-W-Go extension was documented in the official Raspberry
Pi docs, but I found it to be very buggy. It often couldn't run firmware on the
device and didn't display any errors, and I eventually gave up. But sometimes I
write my Python code in VS Code anyway for code formatters and better
autocomplete and such.

I followed these instructions to get things working well with Pylance:
https://micropython-stubs.readthedocs.io/en/main/22_vscode.html

And for installing stubs, I used `pip install -U micropython-rp2-stubs`
