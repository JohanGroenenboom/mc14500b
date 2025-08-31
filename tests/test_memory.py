import unittest

from memory import Memory

class TestMemory(unittest.TestCase):

    def test_memory_write_then_read(self):
        # GIVEN:
        # a value written to address 0x10
        mem = Memory(bits=8, size=256)
        mem.address = 0x10
        mem.data = 0x42
        mem.write_enable = True
        mem.output_enable = False
        mem.execute()
        # WHEN:
        # Reading address 0x10
        mem.write_enable = False
        mem.output_enable = True
        mem.execute()
        # THEN: 
        # Data is equal to the value written earlier
        self.assertEqual(mem.data, 0x42)
        # WHEN: reading the next address
        mem.address = 0x11
        mem.execute()
        # THEN: 
        # Data is equal to the initial startup value (0)
        self.assertEqual(mem.data, 0x00)

    def test_memory_write_out_of_range(self):
        # GIVEN: a memory of 8 bytes
        mem = Memory(bits=8, size=8)
        # WHEN: writing to address 8
        mem.address = 8
        mem.write_enable = True
        mem.output_enable = False
        mem.data = 42
        mem.execute()
        # THEN: the data reads back correctly on that same address
        mem.write_enable = False
        mem.output_enable = True
        self.assertEqual(mem.data, 42)
        # AND: the data reads back correctly on the address modulo the size
        mem.address = 0
        mem.execute()
        self.assertEqual(mem.data, 42)

    def test_memory_with_contents(self):
        # GIVEN: a memory with initial contents
        initial_contents = [0x00, 0x01, 0x02, 0x03]
        mem = Memory(bits=8, size=4, contents=initial_contents)
        # WHEN: reading from the memory
        mem.address = 0
        mem.output_enable = True
        mem.execute()
        # THEN: the data is equal to the initial contents
        self.assertEqual(mem.data, 0x00)
        mem.address = 1
        mem.execute()
        self.assertEqual(mem.data, 0x01)
        mem.address = 2
        mem.execute()
        self.assertEqual(mem.data, 0x02)
        mem.address = 3
        mem.execute()
        self.assertEqual(mem.data, 0x03)
