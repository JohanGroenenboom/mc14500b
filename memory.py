
# Memory class emulates hardware memory device.
# To read from memory, set the output enable, then "clock" the device by calling execute().
# Next, get the data property.
# To write to memory, set the address and data properties, then set the write enable and
# clock the device by calling execute().
# Address and data values are truncated to their proper sizes
# The address can be provided either by setting it externally, or by
# connecting the device to an address source by the connect_address_bus() method.

 

class Memory:
    def __init__(self, bits: int, size: int, contents: list[int] | None = None):
        self._mem_array = [0] * size
        self._address = 0
        self._data_out: int = 0
        self._data_in = 0
        self._write_enable = False
        self._output_enable = False
        self._max_data = (1 << bits) - 1
        self._max_address = size - 1  # FIXME
        self._address_bus = None
        self._data_bus = None
        if contents:
            for i in range(min(size, len(contents))):
                self._mem_array[i] = contents[i] & self._max_data

    @property
    def address(self) -> int:
        raise AttributeError("Can't read address")

    @address.setter
    def address(self, value: int):
        ''' set address on the device's address bus '''
        self._address = value & self._max_address

    @property
    def data(self) -> int | None:
        ''' Returning None is like having the databus in high-Z.
            To get data out, the output enable must be set.
        '''
        if self._output_enable:
            return self._data_out
        return None

    @data.setter
    def data(self, value: int):
        ''' set data on the device's data bus.
            The preferred way is to connect a data bus
        '''
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
            self._data_out = self._mem_array[self._address]

    @property
    def write_enable(self) -> bool:
        raise AttributeError("Can't read write_enable")

    @write_enable.setter
    def write_enable(self, value: bool):
        self._write_enable = value

    def clock_fall(self):
        ''' Clock the memory inputs (address and data)
        '''
        if self._write_enable and self._output_enable:
            raise RuntimeError("Bus conflict: can't read and write at the same time")
        if self._address_bus:
            self._address = self._address_bus() & self._max_address
        if self._write_enable:
            if self._data_bus:
                self._data_in = self._data_bus() & self._max_data
            self._mem_array[self._address] = self._data_in
            return

    def clock_rise(self):
        ''' Clock the memory outputs (data)
        '''
        self._data_out = self._mem_array[self._address]


    def execute(self):
        ''' Execute a memory operation based on the output_enable and 
            write_enable signals (they cannot be active at the same time).
            Combined operation of clock_fall() and clock_rise()
        '''
        self.clock_fall()
        self.clock_rise()

    def connect_address_bus(self, bus):
        ''' Connect the memory's address bus to an external address bus. 
            The bus should be callable and return the current address.
        '''
        self._address_bus = bus

    def connect_data_bus(self, bus):
        ''' Connect the memory's data bus to an external data bus. 
            The bus should be callable and return the current data.
        '''
        self._data_bus = bus
