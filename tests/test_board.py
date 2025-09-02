import unittest
from rom import Rom
from counter import Counter
from board import Board
from mc14500b import MC14500B, OPCODE
from mc14599b import MC14599B  # Output latch
from mc14512b import MC14512B  # Data selector / multiplexer


class TestBoard(unittest.TestCase):

    def test_counter_as_memory_address(self):
        ROM = [ 10, 11, 12, 13 ]

        # Create a board with a 4-bit counter and memory using the
        # counter as its address.
        self.board = Board()
        self.rom = Rom(data_bits=4, address_bits=2, contents=ROM)
        self.counter = Counter(bits=4)
        self.rom.connect_address_input(lambda: self.counter.count)
        # Add the devices to the board so they will be clocked
        self.board.add_device(self.counter)
        self.board.add_device(self.rom)
        # Run the board for a few cycles
        for i in range(4):
            self.assertEqual(self.rom.data, ROM[i])
            self.assertEqual(self.counter.count, i)
            self.board.run(1)
            print(f"After {i+1} cycles: Counter = {self.counter.count}, Memory Data = {self.rom.data}")

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
                - 1 bit UNUSED, 
                - 3 bits i/o address 
            '''
            return ((int(opcode) & 15) << 4) | ((data & 1) << 3) | (io_adr & 7)
        
        ROM = [
            rom_entry(OPCODE.LD,   0, 7),  # Load from input 7
            rom_entry(OPCODE.OR,   1, 0),  # or with 1, store the result = 1 @ latch pos. 0
            rom_entry(OPCODE.AND,  0, 1),  # and with 0, store the result = 0 @ latch pos. 1
            rom_entry(OPCODE.XNOR, 1, 2),  # xnor with 1, store the result = 1 @ latch pos. 2
        ]

        program_counter = Counter(bits=4)
        rom = Rom(data_bits=8, address_bits=3, contents=ROM)
        mc14500 = MC14500B()
        latch = MC14599B()
        input_selector = MC14512B()

        # Connect the devices
        rom.connect_address_input(lambda: program_counter.count)
        # Connect the instruction bus of the MC14500B to bits 4..7 of the ROM data output
        mc14500.connect_instruction_input(lambda: (rom.data >> 4 if rom.data is not None else 0) & 0x0F)
        # Connect the data bus of the MC14500B to bit 3 of the ROM data output
        # mc14500.connect_data_input(lambda: (rom.data >> 3 if rom.data is not None else 0) & 0x01)
        # Connect the data input of the MC14500B to the output of the input_selector
        mc14500.connect_data_input(lambda: input_selector.data)
        latch.connect_data_input(lambda: mc14500.data)
        # Connect the latch address to bits 0..2 of the ROM data output
        latch.connect_address_input(lambda: (rom.data if rom.data is not None else 0) & 0x07)
        latch.connect_chip_enable(lambda: True)  # pull-up, always enabled
        latch.connect_write_input(lambda: True)  # always write
        input_selector.connect_address_input(lambda: (rom.data if rom.data is not None else 0) & 0x07)
        input_selector.connect_data_inputs(0xFF)  # All inputs are always high

        # Create the board that runs the simulation
        board = Board()
        board.add_device(mc14500)
        board.add_device(rom)
        board.add_device(program_counter)
        board.add_device(latch)
        board.add_device(input_selector)  # doesn't do anything, not a clocked device

        # Run the simulation
        print()
        print(f'Initial status: MC14500B Output = {mc14500.data}, Latch Output = {latch.q}', end=' ')
        print(f'Counter Output = {program_counter.count}, ROM output = {rom.data}')

        for i in range(4):
            board.run()
            print(f"After {i+1} cycles: MC14500B Output = {mc14500.data}, Latch Output = {latch.q},",
                  f" Counter Output = {program_counter.count}, ROM output = {hex(rom.data if rom.data is not None else 0)}")

