'''
MC14599B 8-bit addressable latches
See the data sheet for details
The latches are addressed by 3 address bits
A "write" signal selects between reading and writing
Enable signal must be active to be able to write.
The latch outputs are always available.
'''

NUM_LATCHES = 8

class MC14599B:
    def __init__(self):
        self._latches = [False] * NUM_LATCHES
        self._address = 0
        self._input_data = False
        self._enable = False
        self._write = False


    @property
    def address(self):
        raise RuntimeError("Can't read address")

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
        self._input_data = value & 0x01

    @property
    def enable(self):
        return self._enable

    @enable.setter
    def enable(self, value):
        self._enable = value

    @property
    def write(self):
        raise RuntimeError("Can't read the read/write input")

    @write.setter
    def write(self, value: bool):
        ''' Set the read/write input to write (True) or read (False) '''
        if self._enable and self._write != value:
            self._write = value
            if self._write:
                self._latches[self._address] = self._input_data

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