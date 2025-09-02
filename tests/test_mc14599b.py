import unittest

from mc14599b import MC14599B

class TestMC14599B(unittest.TestCase):
    def setUp(self) -> None:
        self.mc = MC14599B()
        self.data_input = 0
        self.address_input = 0
        self.write_input = False
        self.chip_enable = True
        self.mc.connect_data_input(lambda: self.data_input)
        self.mc.connect_address_input(lambda: self.address_input)
        self.mc.connect_chip_enable(lambda: self.chip_enable)
        self.mc.connect_write_input(lambda: self.write_input)
        return super().setUp()
    
    def test_initial_state(self):
        self.assertEqual(self.mc.q, 0)

    def test_write_and_read(self):
        self.address_input = 0
        self.data_input = True
        self.write_input = True
        self.mc.execute()
        self.assertEqual(self.mc.q, 1)
        self.address_input = 1
        self.mc.execute()
        self.assertEqual(self.mc.q, 3)
        self.address_input = 7
        self.mc.execute()
        self.assertEqual(self.mc.q, 131)
        # When writing with enable disabled, no change
        self.chip_enable = False
        self.address_input = 6
        self.mc.execute()
        self.assertEqual(self.mc.q, 131)

    def test_read_without_enable(self):
        # GIVEN: a 1 at address 0
        self.address_input = 0
        self.data_input = True
        self.write_input = True
        self.mc.execute()
        # WHEN: chip_enable is low
        self.chip_enable = False
        # THEN: output can still be read
        self.assertEqual(self.mc.q, 1)
        self.write_input = False
        self.assertEqual(self.mc.q, 1)

    def test_read_in_write_mode(self):
        self.mc.data = True
        self.write_input = True
        self.mc.execute()
        self.assertIsNone(self.mc.data)

    def test_invalid_address(self):
        # GIVEN: an out-of-bounds address
        self.address_input = 8
        # WHEN: writing to that address
        self.data_input = True
        self.write_input = True
        self.mc.execute()
        # THEN: the modulo 8 address has the data
        self.assertEqual(self.mc.q, 1)
        self.address_input = 0
        self.mc.execute()
        self.assertEqual(self.mc.q, 1)
