import unittest
from ..lib.core import BipolarTrigger


class TestBipolarTrigger(unittest.TestCase):

    def test_emits_nonzero_once(self):
        thresh = 1
        window = 5
        trigger = BipolarTrigger(rising_thresh=thresh, window=window)
        for _ in range(window):
            self.assertFalse(trigger.detect(thresh))

        # Now that we've stayed at or above the threshold for the window length,
        # the next trigger.detect() should return the given sample:
        self.assertTrue(trigger.detect(thresh))
        # and then go back to outputting 0:
        self.assertFalse(trigger.detect(thresh))
