import unittest
from mc14512b import MC14512B

class TestMC14512B(unittest.TestCase):

    def setUp(self):
        self.device = MC14512B()
        self.address = 0
        self.data = 0
        self.device.connect_address_input(lambda: self.address)
        self.device.connect_data_inputs(lambda: self.data)

    def test_connect_single_input(self):
        ''' test the connect_data_input method '''
        # override some of the inputs that were connected in setUp(),
        # by calling connect_data_input.
        self.device.connect_data_input(0, lambda: True)
        self.assertEqual(self.device.data, True)
        self.device.connect_data_input(7, lambda: True)
        self.address = 7
        self.assertEqual(self.device.data, True)

    
    def test_connect_inputs(self):
        ''' test the connect_data_inputs and connect_address_input methods
            (see setUp)
        '''
        for input in [0xA5, 0x5A, 0xF0, 0x0F, 0x00, 0xFF]:
            self.data = input
            for i in range(8):
                self.address = i
                self.assertEqual(self.device.data, bool((self.data >> i) & 1))
