# Firmwares for Uncertainty

Alternate firmwares for the [Uncertainty Eurorack module](https://oamodular.org/products/uncertainty).

## Micropython Firmwares

### Setup

1. Install [Thonny](https://thonny.org/)
2. Hold down the boot button on the unpowered Uncertainty module while plugging it into your computer with USB
3. Run Thonny and go to Preferences -> Interpreter -> Install or Update Micropython. Choose:
   - Target volume probably looks like RPI-RP2, of family RP2
   - MicroPython variant: Raspberry Pi - Pico / Pico H
   - version: 1.20.0
4. Click install
5. Back in the Interpreter preferences, choose:
   - kind of interpreter: MicroPython (RP2040)
   - port: try to detect automatically

Also see https://github.com/oamodular/uncertainty#letss-write-a-simple-utility-in-micropython

Note: Once the Micropython runtime is installed, you don't need to hold the boot button when powering on. Just connect with USB and you're good to go.

### Running the firmware

With Uncertainty connected via USB:

1. Open one of the .py files in the micropython folder in Thonny
2. Click Run

Note you can call `print()` and see it in the Thonny shell. You can see the actual CV input values this way.

### Running Python tests

From the root of this repository (the folder containing the python_uncertainty folder), run:

```bash
python3 -m unittest discover -v micropython.test
```

### Coding in VS Code

I can't find a good, stable solution for runnning Micropython on the Uncertainty from VS Code.
The Pico-W-Go extension was documented in the official Raspberry Pi docs, but I found it to be very
buggy. It often couldn't run firmware on the device and didn't display any errors, and I eventually gave up.
But sometimes I write my Python code in VS Code anyway for code formatters and better autocomplete and such.

I followed these instructions to get things working well with Pylance:
https://micropython-stubs.readthedocs.io/en/main/22_vscode.html

And for installing stubs, I used `pip install -U micropython-rp2-stubs`
