import unittest
from ..lib.dsp import BipolarTrigger


class TestBipolarTrigger(unittest.TestCase):

    def test_emits_nonzero_once(self):
        thresh = 1
        window = 5
        trigger = BipolarTrigger(rising_thresh=thresh,
                                 rising_window=window, lpf_weight=0)
        for _ in range(window):
            self.assertEqual(trigger.detect(thresh), 0)

        # Now that we've stayed at or above the threshold for the window length,
        # the next trigger.detect() should return the given sample:
        self.assertEqual(trigger.detect(thresh), thresh)
        # and then go back to outputting 0:
        self.assertEqual(trigger.detect(thresh), 0)
