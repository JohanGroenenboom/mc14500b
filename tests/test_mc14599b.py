import unittest

from mc14599b import MC14599B

class TestMC14599B(unittest.TestCase):
    def test_initial_state(self):
        mc = MC14599B()
        assert mc.q == 0

    def test_write_and_read(self):
        mc = MC14599B()
        mc.chip_enable = True
        mc.address = 0
        mc.data = True
        mc.write = True
        mc.write = False
        assert mc.q == 1
        mc.address = 1
        mc.data = True
        mc.write = True
        mc.write = False
        assert mc.q == 3
        mc.address = 7
        mc.data = True
        mc.write = True
        mc.write = False
        assert mc.q == 131
        # When writing with enable disabled, no change
        mc.chip_enable = False
        mc.address = 6
        mc.data = True
        mc.write = True
        mc.write = False
        assert mc.q == 131

    def test_read_without_enable(self):
        mc = MC14599B()
        mc.chip_enable = True
        mc.address = 0
        mc.data = 1
        mc.write = True
        mc.write = False
        mc.chip_enable = False
        assert mc.q == 1

    def test_read_in_write_mode(self):
        mc = MC14599B()
        mc.chip_enable = True
        mc.address = 0
        mc.data = True
        mc.write = True
        assert mc.data is None

    def test_invalid_address(self):
        mc = MC14599B()
        mc.chip_enable = True
        mc.address = 8
        mc.data = True
        mc.write = True
        mc.write = False
        assert mc.q == 1
