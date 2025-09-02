import unittest

from rom import Rom

class TestRom(unittest.TestCase):

    def setUp(self) -> None:
        self.address = 0
        self.rom = Rom(data_bits=4, address_bits=2, contents=[1, 2, 3, 0])
        self.rom.connect_address_input(lambda: self.address)

    def test_rom_read_out_of_range(self):
        self.address = 4  # will wrap around to address 0
        self.assertEqual(self.rom.data, 1)

    def test_rom_with_contents(self):
        # GIVEN: a rom with initial contents
        initial_contents = [0x00, 0x01, 0x02, 0x03]
        address = 0
        rom = Rom(data_bits=4, address_bits=2, contents=initial_contents)
        rom.connect_address_input(lambda: address)
        # WHEN: reading from the memory
        # THEN: the data is equal to the initial contents
        self.assertEqual(rom.data, 0x00)
        address = 1
        self.assertEqual(rom.data, 0x01)
        address = 2
        self.assertEqual(rom.data, 0x02)
        address = 3
        self.assertEqual(rom.data, 0x03)
