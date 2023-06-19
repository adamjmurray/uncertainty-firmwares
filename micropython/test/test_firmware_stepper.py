import unittest
from ..firmware.stepper import Stepper


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
        s = Stepper()
        mock = MockOutput()
        num_outs = MockOutput.num_outs

        def output(idx, val):
            return mock.output(idx, val)

        def reset():
            mock.reset()
            for _ in range(101):
                s.process(0, output, num_outs)

        for _ in range(101):
            s.process(1, output, num_outs)

        self.assertEqual(mock.calls, [(0, 0), (1, 1)])

        reset()
        for _ in range(101):
            s.process(2, output, num_outs)

        self.assertEqual(mock.calls, [(1, 0), (3, 1)])

        reset()
        for _ in range(101):
            s.process(3, output, num_outs)

        self.assertEqual(mock.calls, [(3, 0), (6, 1)])

        reset()
        for _ in range(101):
            s.process(4, output, num_outs)

        # This time we stepped forward by 4, but after output index 7, we wrap around
        self.assertEqual(mock.calls, [(6, 0), (2, 1)])
