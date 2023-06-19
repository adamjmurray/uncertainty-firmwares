import unittest
from ..lib.core import random_subset


class TestRandomSubset(unittest.TestCase):

    def test_random_subset(self):
        seen = set()
        items = list(range(10))
        for _ in range(100):
            subset = random_subset(items, 3)
            self.assertEqual(len(subset), 3)
            self.assertEqual(len(set(subset)), 3)  # there should be no duplicates
            seen = seen.union(subset)

        self.assertSetEqual(seen, set(items))
