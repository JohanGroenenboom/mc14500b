
# Memory class emulates hardware memory device.
# To read from memory, set the output enable, then "clock" the device by calling execute().
# Next, get the data property.
# To write to memory, set the address and data properties, then set the write enable and
# clock the device by calling execute().
# Address and data values are truncated to their proper sizes
 

class Memory:
    def __init__(self, bits: int, size: int, read_only: bool):
        self._data = [0] * size
        self._address = 0
        self._data_out: int | None = 0  # None means high-Z output
        self._data_in = 0
        self._write_enable = False
        self._output_enable = False
        self._max_data = (1 << bits) - 1
        self._max_address = size - 1

    @property
    def address(self) -> int:
        raise AttributeError("Can't read address")

    @address.setter
    def address(self, value: int):
        ''' set address on the device's address bus '''
        self._address = value & self._max_address

    @property
    def data(self) -> int | None:
        ''' Returning None is like having the databus in high-Z
            To get data out, the output enable must be set.
        '''
        if self._output_enable:
            return self._data_out
        return None

    @data.setter
    def data(self, value: int):
        ''' set data on the device's data bus '''
        if self._output_enable:
            raise RuntimeError("Bus conflict: can't read and write at the same time")
        self._data_in = value & self._max_data

    @property
    def output_enable(self) -> bool:
        raise AttributeError("Can't read output_enable")

    @output_enable.setter
    def output_enable(self, value: bool):
        self._output_enable = value
        if value:
            self._data_out = self._data[self._address]
        else:
            self._data_out = None

    @property
    def write_enable(self) -> bool:
        raise AttributeError("Can't read write_enable")

    @write_enable.setter
    def write_enable(self, value: bool):
        self._write_enable = value

    def execute(self):
        ''' Execute a memory operation based on the output_enable and 
            write_enable signals (they cannot be active at the same time).
        '''
        if self._write_enable and self._output_enable:
            raise RuntimeError("Bus conflict: can't read and write at the same time")
        if self._write_enable:
            self._data[self._address] = self._data_in
            return
        if self._output_enable:
            self._data_out = self._data[self._address]
