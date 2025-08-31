# MC14500B emulation

## Project description

To analyse the behavior of this one-bit ALU, and learn how it can be used, this project aims to emulate its behavior, together with some harware components around it, using some Python code.  

I have no experience with hardware emulation code. The structure I have in mind is to model each chip as a class, that has methods for setting its inputs, and methods for getting its outputs.
There's also a method for applying a clock cycle, which causes new outputs to be calculated from inputs and internal state.  

## Resources

[A one-bit processor explained: reverse-engineering the vintage MC14500[]](https://www.righto.com/2021/02/a-one-bit-processor-explained-reverse.html)
