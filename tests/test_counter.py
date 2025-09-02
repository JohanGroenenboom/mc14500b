import unittest

from counter import Counter

class TestCounter(unittest.TestCase):
    def test_initial_state(self):
        counter = Counter(bits=4)
        self.assertEqual(counter.count, 0)

    def test_execute(self):
        counter = Counter(bits=4)
        for i in range(16):
            self.assertEqual(counter.count, i)
            counter.execute()
        # After reaching max (15 for 4 bits), it should wrap around to 0
        self.assertEqual(counter.count, 0)

    def test_clock_rise(self):
        counter = Counter(bits=4)
        self.assertEqual(counter.count, 0)
        counter.clock_rise()
        self.assertEqual(counter.count, 1)
        counter.clock_rise()
        self.assertEqual(counter.count, 2)