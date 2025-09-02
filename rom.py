
# Rom class emulates hardware memory device.
# Connect an address source, then read the output data.
# To write to memory, set the address and data properties, then set the write enable and
# clock the device by calling execute().
# Address and data values are truncated to their proper sizes
# The address can be provided either by setting it externally, or by
# connecting the device to an address source by the connect_address_input() method.
# Limitations:
# - output enable (float data bus) not implemented, data_in and data_out are separated

 

class Rom:
    def __init__(self, data_bits: int, address_bits: int, contents: list[int] | None = None):
        self._size = 1 << address_bits
        self._mem_array = [0] * self._size
        self._address = 0
        self._data_out: int = 0
        self._max_data = (1 << data_bits) - 1
        self._max_address = self._size - 1
        self._get_address_input = None  # lambda for getting the address input
        self._get_data_input = None     # lambda for getting the data input
        if contents:
            for i in range(min(self._size, len(contents))):
                self._mem_array[i] = contents[i] & self._max_data

    @property
    def address(self) -> int:
        raise AttributeError("Can't read address")

    @address.setter
    def address(self, value: int):
        ''' set address on the device's address bus '''
        self._address = value & self._max_address

    @property
    def data(self) -> int:
        ''' Returning None is like having the databus in high-Z.
            To get data out, the output enable must be set.
        '''
        
        if not self._get_address_input:
            raise RuntimeError("Memory: address input not connected")
        address = self._get_address_input() & self._max_address
        return self._mem_array[address]

    def connect_address_input(self, address_input):
        ''' Connect the memory's address address_input to an external bus. 
            The address_input should be a lambda that returns the current address.
        '''
        self._get_address_input = address_input
