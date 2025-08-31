# from mc14500b import MC14500B
from memory import Memory
from counter import Counter

# mc = MC14500B()
ROM = [
    0b0001,  # Instruction 1
    0b0010,  # Instruction 2
    0b0011,  # Instruction 3
    0b0100,  # Instruction 4
]
memory = Memory(bits=4, size=16, contents=ROM)
counter = Counter(bits=4)

for i in range(4):
    memory.address = counter.count
    memory.output_enable = True
    memory.execute()
    print(f"Counter: {counter.count}, Memory Data: {memory.data}")
    counter.execute()
