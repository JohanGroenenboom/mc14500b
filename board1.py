# from mc14500b import MC14500B
from mc14500b import MC14500B
from rom import Rom
from counter import Counter
from board import Board

# mc = MC14500B()
ROM = [15, 14, 13, 12]
memory = Rom(data_bits=4, address_bits=4, contents=ROM)
counter = Counter(bits=4)

memory.connect_address_input(lambda: counter.count)

board = Board()
board.add_device(counter)
board.add_device(memory)

for i in range(4):
    # memory.address = counter.count
    print(f"Counter: {counter.count}, Memory Data: {memory.data}")
    board.run()
