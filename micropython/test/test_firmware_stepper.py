import unittest
from ..firmware.stepper import Stepper
from ..lib.core import NUM_OUTS


class MockOutput:
    num_outs = 8

    def __init__(self):
        self.reset()

    def output(self, index, value):
        self.calls.append((index, value))

    def reset(self):
        self.calls = []


class TestStepper(unittest.TestCase):

    def test_it_steps_forward_when_triggered(self):
        mock = MockOutput()

        def output(idx, val):
            return mock.output(idx, val)

        s = Stepper(output)
        self.assertEqual(mock.calls, [(idx, idx == 0) for idx in range(NUM_OUTS)])
        mock.reset()

        def reset():
            mock.reset()
            for _ in range(101):
                s.process(0, output)

        for _ in range(101):
            s.process(1, output)

        self.assertEqual(mock.calls, [(0, False), (1, True)])

        reset()
        for _ in range(101):
            s.process(2, output)

        self.assertEqual(mock.calls, [(1, False), (3, True)])

        reset()
        for _ in range(101):
            s.process(3, output)

        self.assertEqual(mock.calls, [(3, False), (6, True)])

        reset()
        for _ in range(101):
            s.process(4, output)

        # This time we stepped forward by 4, but after output index 7, we wrap around
        self.assertEqual(mock.calls, [(6, False), (2, True)])
