# Board class manages the clocking of devices.
# It assumes "duck typed" devices, having clock_fall and/or clock_rise methods.
# Devices can be added to the board and will be clocked in each cycle.


class Board:
    def __init__(self):
        self._devices = []

    def reset(self):
        for device in self._devices:
            if hasattr(device, 'reset') and callable(device.reset):
                device.reset()

    def run(self, clocks: int = 1):
        for _ in range(clocks):
            self.clock_fall()
            self.clock_rise()

    def add_device(self, device):
        self._devices.append(device)

    def clock_fall(self):
        for device in self._devices:
            if hasattr(device, 'clock_fall') and callable(device.clock_fall):
                device.clock_fall()

    def clock_rise(self):
        for device in self._devices:
            if hasattr(device, 'clock_rise') and callable(device.clock_rise):
                device.clock_rise()
