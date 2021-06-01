import math
from typing import List

from debug.command.command import Command, UnaryCommand, BinaryCommand
from debug.disas import getInstruction
from util import SICXE_SIZE_BIT_WORD, intToDec, decToInt, intToBytearray, SICXE_SIZE_BIT_MANTISSA, \
    SICXE_SIZE_BIT_EXPONENT, decToFloat
from vm import CU, SICXE_NUM_REGISTER_PC


class DecTo(UnaryCommand):
    def __init__(self, child: Command):
        super().__init__(child)

    def execute(self, inputs=None) -> any:
        if self.child is None:
            raise Exception('no number found')

        num = int(self.child.execute())

        return self.cast(num)

    def cast(self, num: int):
        return num


class DecToBase(DecTo):
    def __init__(self, child: Command, mode='hex'):
        super().__init__(child)
        self.mode = mode

    def cast(self, num: int):
        if self.mode == 'hex': return hex(num)
        if self.mode == 'bin': return bin(num)
        if self.mode == 'oct': return oct(num)
        return num


class DecToChar(DecTo):
    def __init__(self, child: Command = None):
        super().__init__(child)

    def cast(self, num: int):
        nbyte = math.ceil(num.bit_length() / 8)
        dec = intToDec(num, nbyte * 8)
        # b = intToBytearray(dec, nbyte)
        # return ord(b[len(b) - 1])
        string = "'"
        for i in intToBytearray(dec, nbyte):
            string += (chr(i))
        string += "'"
        return string


class DecToUnsignedWord(DecTo):
    def __init__(self, child: Command = None):
        super().__init__(child)

    def cast(self, num: int):
        dec = intToDec(num, SICXE_SIZE_BIT_WORD)
        return decToInt(dec, SICXE_SIZE_BIT_WORD, False)


class DecToSignedWord(DecTo):
    def __init__(self, child: Command = None):
        super().__init__(child)

    def cast(self, num: int):
        dec = intToDec(num, SICXE_SIZE_BIT_WORD)
        return decToInt(dec, SICXE_SIZE_BIT_WORD, True)


class DecToFloat(DecTo):
    def __init__(self, child: Command = None):
        super().__init__(child)

    def cast(self, num: float):
        return decToFloat(num, SICXE_SIZE_BIT_EXPONENT, SICXE_SIZE_BIT_MANTISSA)


class DecToInstr(DecTo):
    def __init__(self, cu: CU, child: Command = None, symtab=None, datatab=None,br=[]):
        super().__init__(child)
        self.cu = cu
        self.symtab = symtab
        self.datatab = datatab
        self.br = br

    def cast(self, num: float):
        pc = self.cu.registers[SICXE_NUM_REGISTER_PC].get(False)
        instr = getInstruction(num, self.cu, self.symtab, self.datatab,isDat=False)
        return f"{'>' if pc == instr.loc else '*' if instr.loc in self.br else ' '} {instr}"
        #return string'  ' + str(getInstruction(num, self.cu, self.symtab, self.datatab))


class AddrToCharPoint(DecTo):
    def __init__(self, cu: CU, child: Command = None):
        super().__init__(child)
        self.cu = cu

    def cast(self, num: int):
        addr = num
        byte = self.cu.mem.getbyte(addr)
        string = bytearray()
        while byte != 0:  # 0x20 <= byte <= 0x7f:
            string.append(byte)
            addr += 1
            byte = self.cu.mem.getbyte(addr)

        return f'"{string.decode(encoding="utf-8")}"'


class AddrToWordPoint(BinaryCommand):
    def __init__(self, cu: CU, signed: bool, addr: Command, length: Command):
        super().__init__(addr, length)
        self.cu = cu
        self.signed = signed

    def execute(self, inputs=None) -> any:
        if self.left is None:
            raise Exception()
        addr = self.left.execute()
        length = self.right.execute()
        return self.cast(addr, length)

    def cast(self, addr: int, length: int) -> str:
        index = 0
        arr = []
        while index < length:
            word = self.cu.mem.getword(addr + index * 3, self.signed, 'int')
            arr.append(word)
            index += 1

        return str(arr)


class AddrToFloatPoint(BinaryCommand):
    def __init__(self, cu: CU, addr: Command, length: Command):
        super().__init__(addr, length)
        self.cu = cu

    def execute(self, inputs=None) -> any:
        if self.left is None:
            raise Exception()
        addr = self.left.execute()
        length = self.right.execute()
        return self.cast(addr, length)

    def cast(self, addr: int, length: int) -> str:
        index = 0
        arr = []
        while index < length:
            floa = self.cu.mem.getfloat(addr + index * 6, 'float')
            arr.append(floa)
            index += 1

        return str(arr)
