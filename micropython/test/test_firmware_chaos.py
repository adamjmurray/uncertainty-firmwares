from test.case import FirmwareTestCase
from firmware.chaos import Chaos
from lib.core import NUM_OUTS
from test.util import repeat


class TestChaos(FirmwareTestCase):

    def test_it_is_chaotic(self):
        chaos = Chaos(self.output)
        self.assert_initial_gate_state([0 for _ in range(NUM_OUTS)])  # all gates off

        self.trigger(chaos, volts=3)
        output_calls = self.pop_output_calls()
        # The first time we do this, it should only turn a gate on, because none were on:
        self.assertEqual(len(output_calls), 1)
        self.assertTrue(output_calls[0][1])
        active_gate = output_calls[0][0]

        seen = {active_gate}

        for i in range(200):
            # Since this is a chaotic algorithm, the assertSetEqual() below
            # might occasionally fail. Reseeding should make that extremely unlikely.
            if i % 25 == 0:
                chaos.reseed()

            self.trigger(chaos, volts=3)
            output_calls = self.pop_output_calls()
            # every other time, it should turn the last gate off and turn another one on,
            # but only if they are different. It's possible the same gate stays acctive
            # and there are no output calls, so we guard with this > 0 check:
            if len(output_calls) > 0:
                self.assertEqual(len(output_calls), 2)
                self.assertEqual(output_calls[0][0], active_gate)
                self.assertFalse(output_calls[0][1])  # active gate turned off
                self.assertTrue(output_calls[1][1])  # another turned on
                active_gate = output_calls[1][0]
                seen.add(active_gate)

        self.assertSetEqual(seen, set(range(NUM_OUTS)))
