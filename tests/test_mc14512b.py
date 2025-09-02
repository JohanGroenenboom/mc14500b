import unittest
from mc14512b import MC14512B

class TestMC14512B(unittest.TestCase):

    def setUp(self):
        self.device = MC14512B()

    def test_connect_inputs(self):
        address = 0
        data = 0xA5
        self.device.connect_address_input(lambda: address)
        self.device.connect_data_inputs(data)
        for i in range(8):
            address = i
            self.assertEqual(self.device.data, bool((data >> i) & 1))
