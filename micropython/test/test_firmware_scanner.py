from test.case import FirmwareTestCase
from firmware.scanner import Scanner
from lib.core import NUM_OUTS
from test.util import repeat


class TestScanner(FirmwareTestCase):

    def test_it_scans_with_filtered_input_by_default(self):
        s = Scanner(self.output)
        self.assert_initial_gate_state([index == 0 for index in range(NUM_OUTS)])  # only first gate should be active

        for index, volts in enumerate([0.5, 1, 1.5, 2, 2.5, 3, 3.5]):
            s.process(volts + 0.01, self.output)  # This does nothing,
            self.assert_no_output_calls()  # because filtering is applied.
            s.process(volts + 0.01, self.output)  # But do it again and it triggers a gate change:
            self.assertEqual(self.pop_output_calls(), [(index, False), (index + 1, True)])

        # and now check in the negative direction

        # but first, make a big jump to get to gate 0 even with the filter:
        s.process(-5, self.output)
        self.assertEqual(self.pop_output_calls(), [(7, False), (0, True)])

        for index, volts in enumerate([-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5]):
            s.process(volts + 0.01, self.output)
            self.assert_no_output_calls()
            s.process(volts + 0.01, self.output)
            self.assertEqual(self.pop_output_calls(), [(index, False), ((index + 1) % NUM_OUTS, True)])
