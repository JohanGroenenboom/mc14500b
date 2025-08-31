# Board class manages the clocking of devices.
# It assumes "duck typed" devices, having clock_inputs and/or clock_outputs methods.
# Devices can be added to the board and will be clocked in each cycle.


class Board:
    def __init__(self):
        self._devices = []

    def reset(self):
        for device in self._devices:
            if hasattr(device, 'reset') and callable(device.reset):
                device.reset()

    def run(self):
        self._clock_inputs()
        self._clock_outputs()

    def add_device(self, device):
        self._devices.append(device)

    def _clock_inputs(self):
        for device in self._devices:
            if hasattr(device, 'clock_inputs') and callable(device.clock_inputs):
                device.clock_inputs()

    def _clock_outputs(self):
        for device in self._devices:
            if hasattr(device, 'clock_outputs') and callable(device.clock_outputs):
                device.clock_outputs()
