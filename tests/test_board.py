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
        # The program will invert the input byte and store it in the output.

        def rom_entry(opcode, write_enable: bool, io_adr) -> int:
            ''' each ROM entry is 8 bits: 
                - 4 bits opcode
                - 1 bit write enable for output latch
                - 3 bits i/o address 
            '''
            return ((int(opcode) & 15) << 4) | ((int(write_enable) & 1) << 3) | (io_adr & 7)
        
        ROM = [
            rom_entry(OPCODE.LD,   False, 7),  # Load from input 7
            rom_entry(OPCODE.STOC, True,  7),  # store the complement @ latch pos. 7
            rom_entry(OPCODE.LD,   False, 6),  # Load from input 6
            rom_entry(OPCODE.STOC, True,  6),  # store the complement @ latch pos. 6
            rom_entry(OPCODE.LD,   False, 5),  # Load from input 5
            rom_entry(OPCODE.STOC, True,  5),  # store the complement @ latch pos. 5
            rom_entry(OPCODE.LD,   False, 4),  # Load from input 4
            rom_entry(OPCODE.STOC, True,  4),  # store the complement @ latch pos. 4
            rom_entry(OPCODE.LD,   False, 3),  # Load from input 3
            rom_entry(OPCODE.STOC, True,  3),  # store the complement @ latch pos. 3
            rom_entry(OPCODE.LD,   False, 2),  # Load from input 2
            rom_entry(OPCODE.STOC, True,  2),  # store the complement @ latch pos. 2
            rom_entry(OPCODE.LD,   False, 1),  # Load from input 1
            rom_entry(OPCODE.STOC, True,  1),  # store the complement @ latch pos. 1
            rom_entry(OPCODE.LD,   False, 0),  # Load from input 0
            rom_entry(OPCODE.STOC, True,  0),  # store the complement @ latch pos. 0
        ]

        program_counter = Counter(bits=4)
        rom = Rom(data_bits=8, address_bits=4, contents=ROM)
        icu = MC14500B()
        output_latch = MC14599B()
        input_selector = MC14512B()

        input_data = 0b11110000  # Example input data

        # Connect the devices
        rom.connect_address_input(lambda: program_counter.count)
        # Connect the instruction bus of the MC14500B to bits 4..7 of the ROM data output
        icu.connect_instruction_input(lambda: (rom.data >> 4) & 0x0F)
        # Connect the data input of the MC14500B to the output of the input_selector
        icu.connect_data_input(lambda: input_selector.data)
        output_latch.connect_data_input(lambda: icu.data)
        # Connect the latch address to bits 0..2 of the ROM data output
        output_latch.connect_address_input(lambda: rom.data & 0x07)
        output_latch.connect_chip_enable(lambda: True)  # pull-up, always enabled
        # Connect the write input of the output latch to the write_enable signal from the ROM
        output_latch.connect_write_input(lambda: (rom.data >> 3) & 1)
        # Connect the input selector address to bits 0..2 of the ROM data output
        input_selector.connect_address_input(lambda: rom.data & 0x07)
        # Connect the data inputs of the input selector to the input data variable
        input_selector.connect_data_inputs(lambda: input_data)

        # Create the board that runs the simulation
        board = Board()
        board.add_device(icu)
        board.add_device(rom)
        board.add_device(program_counter)
        board.add_device(output_latch)
        board.add_device(input_selector)  # doesn't do anything, not a clocked device

        # Run the simulation
        input_data = 0b11110000  # Example input data
        print()
        # print(f'Initial status: MC14500B = {icu.data}, Latch = {output_latch.q}', end=' ')
        # print(f'Counter = {program_counter.count}, ROM = {rom.data}')
        print(f'Input data = {bin(input_data)}')
        board.run(16)
        # for i in range(16):
        #     board.run()
        #     print(f"After {i+1} cycles: MC14500B = {icu.data}, Latch = {output_latch.q},",
        #           f" Counter = {program_counter.count}, ROM = {hex(rom.data)}")

        # Expect the latch to hold the inverted input data
        self.assertEqual(output_latch.q, ~input_data & 0xFF)
        print(f'Output data = {output_latch.q:#010b}')
