# MC14500B emulation

## Project description

To analyse the behavior of this one-bit ALU, and learn how it can be used, this project aims to emulate its behavior, together with some harware components around it, using some Python code.  

I have no experience with hardware emulation code. The structure I have in mind is to model each chip as a class, that has methods for setting its inputs, and methods for getting its outputs.
There's also a method for applying a clock cycle, which causes new outputs to be calculated from inputs and internal state.  

## Clocking

Devices are modeled as classes.  To be able to operate quasi-synchronously, they have a clock.
Typical device behavior is to use the falling edge of the clock to "freeze" the inputs by copying them internally.
On the rising edge of the clock, devices update their outputs. As a result, the state of the network (at the board or device interconnect level) is 
captured on the falling edge, and the new state happens on the rising edge.
This is independent on the order in which devices are clocked, as long as they all get a falling clock edge before all getting a rising edge.
Both the rising edge and falling edge behavior of a device are optional. Each edge is implemented by a method (clock_fall and clock_rise), and device classes are free to not implement either or both of them.

## Reset

Similar to clocking, device classes can optionally have a reset method.

## Boards

The clocking takes place at the Board level. The Board class allows the addition of devices.
It uses "duck typing", checking each device for the presence of clock_fall, clock_rise and reset methods. 
Reset and clocking can be applied at the board level. The run method applies clock pulses to the board.

## Device connections

Devices are connected by providing a callable input object (lambda) for each of its inputs.
On the falling clock edge, the device will call this input object to obtain the current value of that signal or bus.
For example, the Memory class has connect_address_bus and connect_data_bus methods.

## Resources

[A one-bit processor explained: reverse-engineering the vintage MC14500](https://www.righto.com/2021/02/a-one-bit-processor-explained-reverse.html)
[MC14500B Industrial Control Unit Handbook](https://bitsavers.org/components/motorola/14500/MC14500B_Industrial_Control_Unit_Handbook_1977.pdf)
[Nicola Cimmino's PLC-14500 project on github](https://github.com/nicolacimmino/PLC-14500)
