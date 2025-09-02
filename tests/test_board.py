import unittest
from memory import Memory
from counter import Counter
from board import Board
from mc14500b import MC14500B, OPCODE
from mc14599b import MC14599B


class TestBoard(unittest.TestCase):

    def test_counter_as_memory_address(self):
        ROM = [ 10, 11, 12, 13 ]

        # Create a board with a 4-bit counter and memory using the
        # counter as its address.
        self.board = Board()
        self.memory = Memory(bits=4, size=4, contents=ROM)
        self.counter = Counter(bits=4)
        self.memory.connect_address_bus(lambda: self.counter.count)
        self.memory.output_enable = True
        # Add the devices to the board so they will be clocked
        self.board.add_device(self.counter)
        self.board.add_device(self.memory)
        # Run the board for a few cycles
        for i in range(4):
            self.board.run(1)
            self.assertEqual(self.memory.data, ROM[i])
            self.assertEqual(self.counter.count, i+1)
            print(f"After {i+1} cycles: Counter = {self.counter.count}, Memory Data = {self.memory.data}")

    def test_execute_14500_from_rom(self):
        # Test the execution of the 14500 instruction set from ROM
        # Create a board that has a program counter, ROM and MC14500
        # and an MC14512B for an input selector.
        # The ROM has 4 bits of instruction and 1 bit of data
        # Fill the rom with instructions: (using 0 and 1 for False and True)
        # OR 1    (result: 1)
        # STO 0   (store the result = 1 @ latch pos. 0)
        # AND 0   (result: 0)
        # STO 1   (store the result = 0 @ latch pos. 1)
        # XNOR 1  (result: 1)
        # STO 2   (store the result = 1 @ latch pos. 2)

        def rom_entry(opcode, data, io_adr) -> int:
            ''' each ROM entry is 8 bits: 
                - 4 bits opcode, 
                - 1 bit data, 
                - 3 bits i/o address 
            '''
            return ((int(opcode) & 15) << 4) | ((data & 1) << 3) | (io_adr & 7)
        
        ROM = [
            rom_entry(OPCODE.OR,   1, 0),  # or with 1, store the result = 1 @ latch pos. 0
            rom_entry(OPCODE.AND,  0, 1),  # and with 0, store the result = 0 @ latch pos. 1
            rom_entry(OPCODE.XNOR, 1, 2),  # xnor with 1, store the result = 1 @ latch pos. 2
        ]

        program_counter = Counter(bits=4)
        rom = Memory(bits=8, size=8, contents=ROM)
        mc14500 = MC14500B()
        latch = MC14599B()

        # Connect the devices
        rom.connect_address_bus(lambda: program_counter.count)
        rom.output_enable = True
        # Connect the instruction bus of the MC14500B to bits 4..7 of the ROM data output
        mc14500.connect_instruction_input(lambda: (rom.data >> 4 if rom.data is not None else 0) & 0x0F)
        # Connect the data bus of the MC14500B to bit 3 of the ROM data output
        mc14500.connect_data_input(lambda: (rom.data >> 3 if rom.data is not None else 0) & 0x01)
        latch.connect_data_input(lambda: mc14500.data)
        # Connect the latch address to bits 0..2 of the ROM data output
        latch.connect_address_input(lambda: (rom.data if rom.data is not None else 0) & 0x07)
        latch.connect_chip_enable(lambda: True)  # pull-up, always enabled
        latch.connect_write_input(lambda: True)  # always write

        # Create the board that runs the simulation
        board = Board()
        board.add_device(mc14500)
        board.add_device(rom)
        board.add_device(program_counter)
        board.add_device(latch)

        # Run the simulation
        print(f'Initial status: MC14500B Output = {mc14500.data}, Latch Output = {latch.q}')
        print(f'Counter Output = {program_counter.count}, ROM output = {rom.data}')
        for i in range(4):
            board.run()
            print(f"After {i+1} cycles: MC14500B Output = {mc14500.data}")
        print(f'latch output = {latch.q}')

