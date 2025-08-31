
# Counter class emulates hardware counter device.
 

class Counter:
    def __init__(self, bits: int):
        self._count: int = 0
        self._max_count = (1 << bits) - 1

    @property
    def count(self) -> int:
        return self._count

    def execute(self):
        ''' Increment the counter, modulo its maximum value
        '''
        self._count = (self._count + 1) & self._max_count
