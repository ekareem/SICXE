import math

from vm.cu import CU, registerToString
from vm.device import Devices
from vm.mem import MEMORY, SICXE_SIZE_MEMORY, SICXE_SIZE_DEVICES
import vm.register as reg
import time


class BUS:
    def __init__(self):
        self.mem = MEMORY(SICXE_SIZE_MEMORY)
        self.devices = Devices(SICXE_SIZE_DEVICES)
        self.registers = reg.registers
        self.cu = CU(self)

    def regToStr(self):
        string = ''
        for num in list(self.registers.keys()):
            form = "{} = {:0>" + str(int(self.registers[num].nbits / 4)) + "X} {}\n"
            string += form.format(registerToString(num), self.registers[num].dec, self.registers[num])
        return string

    def __str__(self):
        string = ''
        for reg in self.registers:
            form = "{:0>" + str(math.ceil(self.registers[reg].nbits / 4)) + "x}"
            id = "AXLBSTF?PW"[reg]
            hexx = form.format(self.cu.registers[reg].dec)
            val = self.registers[reg].get()
            string += f'{id} {hexx} {val}\n'

        string += str(self.mem)
        return string
