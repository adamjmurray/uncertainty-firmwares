import unittest
from test.mock import MockOutput
from test.util import repeat
from lib.core import NUM_OUTS


class FirmwareTestCase(unittest.TestCase):
    def setUp(self):
        self.mock = MockOutput()

    def output(self, index, value):
        self.mock.output(index, value)

    @property
    def output_calls(self):
        return self.mock.calls

    def reset_output_calls(self):
        self.mock.reset()

    def pop_output_calls(self):
        output_calls = self.output_calls
        self.reset_output_calls()
        return output_calls

    def assert_initial_gate_state(self, gate_states):
        # Some firmwares set the state of all gates explicitly during initialization.
        # This assertion makes it easy to check that it did what was expected.
        self.assertEqual(len(gate_states), NUM_OUTS)
        self.assertEqual(self.pop_output_calls(), [(idx, value) for (idx, value) in enumerate(gate_states)])

    def trigger_on(self, firmware, volts, trigger_window_size=100):
        repeat(trigger_window_size + 1, lambda: firmware.process(volts, self.output))

    def trigger_off(self, firmware, trigger_window_size=100):
        repeat(trigger_window_size + 1, lambda: firmware.process(0, self.output))

    def trigger(self, firmware, volts, trigger_window_size=100, trigger_on_window_size=None, trigger_off_window_size=None):
        trigger_on_window_size = trigger_window_size if trigger_on_window_size is None else trigger_on_window_size
        trigger_off_window_size = trigger_window_size if trigger_off_window_size is None else trigger_off_window_size
        self.trigger_on(firmware, volts=volts, trigger_window_size=trigger_on_window_size)
        self.trigger_off(firmware, trigger_window_size=trigger_off_window_size)
