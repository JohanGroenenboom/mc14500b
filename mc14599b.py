'''
MC14599B 8-bit addressable latches
See the data sheet for details. 
The latches are addressed by 3 address bits
A "write" signal selects between reading and writing
Enable signal must be active to be able to write.
The latch outputs are always available.
The device has no clock input, but the WD (write disable) falling edge
clocks in the address, and the rising edge clocks in the data.
So effectively it can be regarded as a clock signal, and the application
diagram indeed shows it connected to the clock of the MC14500B.
Therefore, the behavior or the clock_fall and clock_rise methods is based
on the falling and rising edges of the WD signal.
To avoid writing on every clock cycle, the CE (chip enable) signal can be
used - write takes place only if it CE input is active.
'''

NUM_LATCHES = 8

class MC14599B:
    def __init__(self):
        self._latches = [False] * NUM_LATCHES
        self._address: int = 0
        self._input_data: bool = False
        self._output_data: bool = False
        self._chip_enable: bool = False
        self._write: bool = False
        self._get_chip_enable = None
        self._get_address = None
        self._get_write = None
        self._get_data = None


    @property
    def address(self):
        raise RuntimeError("Can't read address of MC14599B")

    @address.setter
    def address(self, value):
        self._address = value & (NUM_LATCHES - 1)

    @property
    def data(self) -> bool | None:
        ''' None means data bus is in write mode '''
        if self._write:
            return None
        return self._latches[self._address]

    @data.setter
    def data(self, value: bool):
        self._input_data = value

    @property
    def chip_enable(self):
        raise RuntimeError("Can't read chip enable of MC14599B")

    @chip_enable.setter
    def chip_enable(self, value):
        self._chip_enable = value

    def clock_fall(self):
        ''' Handle the falling edge of the clock signal by latching the inputs
        '''
        if self._get_chip_enable:
            self.chip_enable = bool(self._get_chip_enable())
        if self._get_address:
            self.address = self._get_address()
        if self._get_write:
            self._write = bool(self._get_write())
        if self._get_data:
            self._input_data = bool(self._get_data())

    def clock_rise(self):
        ''' On the rising edge of the clock signal, update the output
        '''
        if self._chip_enable and self._write:
            self._latches[self._address] = self._input_data

    def execute(self):
        ''' Convenience function, mostly for testing
        '''
        self.clock_fall()
        self.clock_rise()

    def connect_chip_enable(self, chip_enable):
        ''' Connect the chip enable input to a callable that returns a boolean value '''
        self._get_chip_enable = chip_enable

    def connect_write_input(self, write_input):
        ''' Connect the write input to a callable that returns a boolean value '''
        self._get_write = write_input

    def connect_address_input(self, address_input):
        ''' Connect the address input to a callable that returns an integer value '''
        self._get_address = address_input

    def connect_data_input(self, data_input):
        ''' Connect the data input to a callable that returns a boolean value '''
        self._get_data = data_input

    @property
    def q0(self) -> bool:
        return self._latches[0]

    @property
    def q1(self) -> bool:
        return self._latches[1]

    @property
    def q2(self) -> bool:
        return self._latches[2]

    @property
    def q3(self) -> bool:
        return self._latches[3]

    @property
    def q4(self) -> bool:
        return self._latches[4]

    @property
    def q5(self) -> bool:
        return self._latches[5]

    @property
    def q6(self) -> bool:
        return self._latches[6]

    @property
    def q7(self) -> bool:
        return self._latches[7]
    
    @property
    def q(self) -> int:
        ''' Return the latched values as an integer '''
        value = 0
        for i in range(NUM_LATCHES):
            if self._latches[i]:
                value |= (1 << i)
        return value