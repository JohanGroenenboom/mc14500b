from enum import Enum

class OPCODE(Enum):
    NOP0 = 0    # No Operation (activates o_flag)
    LD = 1      # Load Data
    LDC = 2     # Load Complement of Data
    AND = 3     # RR AND Data => RR
    ANDC = 4    # RR AND !Data => RR
    OR = 5      # RR OR Data => RR
    ORC = 6     # RR OR !Data => RR
    XNOR = 7    # RR XNOR Data => RR (Equivalence)
    STO = 8     # Store Data
    STOC = 9    # Store Complement of Data
    IEN = 10    # Input Enable
    OEN = 11    # Output Enable
    JMP = 12    # Jump (activates jmp_flag)
    RTN = 13    # Return (activates rtn_flag)
    SKZ = 14    # Skip next instruction if Zero (activates skz_flag)
    NOPF = 15   # No Operation (activates f_flag)


class MC14500B: 
    def __init__(self):
        self._rr: bool = False # result register rr
        self._opcode: OPCODE = OPCODE.NOP0
        self._input_enable: bool = True
        self._output_enable: bool = True
        self._input_data: bool = False
        self.jmp_flag: bool = False
        self.rtn_flag: bool = False
        self.skz_flag: bool = False
        self.o_flag: bool = False
        self.f_flag: bool = False
        self.wr_flag: bool = False


    def execute(self):
        self.jmp_flag = self._opcode == OPCODE.JMP
        self.rtn_flag = self._opcode == OPCODE.RTN
        self.o_flag = self._opcode == OPCODE.NOP0
        self.f_flag = self._opcode == OPCODE.NOPF
        self.wr_flag = self._opcode in {OPCODE.STO, OPCODE.STOC}
        if self.skz_flag and not self._rr:
            self.skz_flag = False
            return
        self.skz_flag = self._opcode == OPCODE.SKZ

        match self._opcode:
            case OPCODE.LD:
                self._rr = self._input_data
            case OPCODE.LDC:
                self._rr = not self._input_data
            case OPCODE.AND:
                self._rr = self._rr and self._input_data
            case OPCODE.ANDC:
                self._rr = self._rr and (not self._input_data)
            case OPCODE.OR:
                self._rr = self._rr or self._input_data
            case OPCODE.ORC:
                self._rr = self._rr or (not self._input_data)
            case OPCODE.XNOR:
                self._rr = self._rr == self._input_data
            case OPCODE.IEN:
                self._input_enable = self._input_data
            case OPCODE.OEN:
                self._output_enable = self._input_data
            case _:
                return
            
    @property
    def data(self) -> bool | None:
        ''' Different from the hardware, where input and output data are 
            multiplexed on a single pin, the MC14500B provides separate
            methods for input and output.
            The function of the WRITE pin of the MC14500B is represented
            by the data being optional: if the WRITE signal would be inactive
            in hardware, the data method returns None.
        '''
        if self._output_enable:
            return self._rr
        return None

    @data.setter
    def data(self, value: bool):
        if self._input_enable:
            self._input_data = value

    @property
    def opcode(self) -> OPCODE:
        return self._opcode

    @opcode.setter
    def opcode(self, value: OPCODE):
        self._opcode = value