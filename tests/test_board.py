import unittest
from memory import Memory
from counter import Counter
from board import Board

ROM = [
    0b0001,  # Instruction 1
    0b0010,  # Instruction 2
    0b0011,  # Instruction 3
    0b0100,  # Instruction 4
]

class TestBoard(unittest.TestCase):
    def setUp(self):
        # Create a board with a 4-bit counter and memory using the
        # counter as its address.
        self.board = Board()
        self.memory = Memory(bits=4, size=8, contents=ROM)
        self.counter = Counter(bits=4)
        self.memory.connect_address_bus(lambda: self.counter.count)
        self.memory.output_enable = True
        # Add the devices to the board so they will be clocked
        self.board.add_device(self.counter)
        self.board.add_device(self.memory)


    def test(self):
        for i in range(4):
            self.board.run(1)
            self.assertEqual(self.memory.data, ROM[i])
            self.assertEqual(self.counter.count, i+1)
            print(f"After {i+1} cycles: Counter = {self.counter.count}, Memory Data: {self.memory.data}")
