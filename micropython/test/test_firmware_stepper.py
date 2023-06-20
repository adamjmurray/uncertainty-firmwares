from test.case import FirmwareTestCase
from firmware.stepper import Stepper
from lib.core import NUM_OUTS


class TestStepper(FirmwareTestCase):

    def test_it_steps_forward_when_triggered(self):
        s = Stepper(self.output)
        self.assert_initial_gate_state([index == 0 for index in range(NUM_OUTS)])  # only first gate should be active

        self.trigger_on(s, volts=1)
        self.assertEqual(self.pop_output_calls(), [(0, False), (1, True)])

        self.trigger_off(s)
        # gates don't turn off until the next trigger on and another gate turns on:
        self.assertEqual(self.output_calls, [])

        # now that we've estbliahsed trigger_off doesn't change state, we'll use trigger()
        # to do a trigger on+off:
        self.trigger(s, volts=2)
        self.assertEqual(self.pop_output_calls(), [(1, False), (3, True)])

        self.trigger(s, volts=3)
        self.assertEqual(self.pop_output_calls(), [(3, False), (6, True)])

        self.trigger(s, volts=4)
        # This time we stepped forward by 4, but after output index 7, we wrap around
        self.assertEqual(self.pop_output_calls(), [(6, False), (2, True)])
