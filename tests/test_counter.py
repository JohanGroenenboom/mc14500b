import unittest

from counter import Counter

class TestCounter(unittest.TestCase):
    def test_initial_state(self):
        counter = Counter(bits=4)
        assert counter.count == 0

    def test_execute(self):
        counter = Counter(bits=4)
        for i in range(1, 16):
            counter.execute()
            assert counter.count == i
        # After reaching max (15 for 4 bits), it should wrap around to 0
        counter.execute()
        assert counter.count == 0