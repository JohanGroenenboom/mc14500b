'''
MC14512B 8-channel data selector
This is a combinatorial device, i.e. it doesn't have any internal state,
and it has no clock.
A query of the output value results in a the device querying the current
state of its inputs, and producing the appropriate output.
Note that this means that connecting an input to the output of the device
will result in an infinite recursion error.

Limitations:
- Disable input not implemented
- Inhibit input not implemented
- Inputs A, B, C are labeled "address", with A=a0, B=a1, C=a2
'''

class MC14512B:
    def __init__(self):
        self._get_input = [None] * 8  # a callable (lambda) for each input
        self._get_address = None      # lambda connection to get the address

    @property
    def data(self) -> bool:
        if not self._get_address:
            raise RuntimeError("MC14512B address input not connected")
        address = self._get_address() & 7
        if not self._get_input[address] or not callable(self._get_input[address]):
            raise RuntimeError(f"MC14512B input {address} not connected")
        return bool(self._get_input[address]())

    def connect_address_input(self, address_input):
        ''' Connect the address input to a callable that returns an integer value '''
        self._get_address = address_input

    def connect_data_input(self, input_adr: int, data_input):
        ''' Connect the data input to a callable that returns a boolean value '''
        if input_adr < 0 or input_adr > 7:
            raise ValueError("Input address must be between 0 and 7")
        self._get_input[input_adr] = data_input

    def connect_data_inputs(self, data_inputs):
        ''' Connect all data inputs to a 8-bit wide source, a lambda that returns an int.
        '''
        for i in range(8):
            self.connect_data_input(i, lambda i=i: bool((data_inputs() >> i) & 1))
    
