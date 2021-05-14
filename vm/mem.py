from typing import Tuple

from util.size import *
from util.num import *
from util.common import *


class MEMORY:
    def __init__(self, size):
        self.mem = bytearray(size)

    def __getitem__(self, addr):
        return self.getbyte(addr)

    def __setitem__(self, addr, value):
        self.setbyte(addr, value)

    def __len__(self):
        return len(self.mem)

    def reset(self):
        for addr in range(len(self.mem)):
            self.mem[addr] = 0x00

    def getbyte(self, addr):
        addr %= len(self.mem)
        return self.mem[addr]

    def setbyte(self, addr, byte):
        addr %= len(self.mem)
        self.mem[addr] = byte

    def get(self, addr, nbyte, dec=0, asbytearr=False):
        nbits = nbyte * SICXE_SIZE_BIT_BYTE

        dec |= self.getbyte(addr) << nbits - SICXE_SIZE_BIT_BYTE

        if nbyte > 1:
            dec |= self.get(addr + 1, nbyte - 1, dec, False)

        return intToBytearray(dec, nbyte) if asbytearr else dec

    def set(self, addr, val, nbyte):
        val = bytearrayToInt(val) if type(val) == bytearray else decToFitNbit(val, nbyte * SICXE_SIZE_BIT_BYTE)
        nbits = nbyte * SICXE_SIZE_BIT_BYTE
        if nbyte > 1:
            self.set(addr + 1, val, nbyte - 1)

        self.setbyte(addr, val >> nbits - SICXE_SIZE_BIT_BYTE & 0xff)

    def setBytearray(self, addr, bytes: bytearray):
        count = 0
        for bytee in bytes:
            self.setbyte(addr + count, bytee)
            count += 1

    def getword(self, addr, signed=False, to='SICWORD'):
        asbytearr = True if to == 'bytearray' else False
        dec = self.get(addr, SICXE_SIZE_BYTE_WORD, asbytearr=asbytearr)
        if to == 'SICWORD':
            return SICWORD(dec, signed, False)

        return decToInt(dec, SICXE_SIZE_BYTE_WORD * SICXE_SIZE_BIT_BYTE, signed=signed)

    def setword(self, addr, val, signed=False):
        dec = val
        if issubclass(type(val), NUM):
            dec = val.dec
        else:
            dec = decToInt(val, SICXE_SIZE_BYTE_WORD * SICXE_SIZE_BIT_BYTE, signed)
        self.set(addr, dec, SICXE_SIZE_BYTE_WORD)

    def getfloat(self, addr, to='SICFLOAT'):
        asbytearr = True if to == 'bytearray' else False
        dec = self.get(addr, SICXE_SIZE_BYTE_FLOAT, asbytearr=asbytearr)
        if to == 'SICFLOAT':
            return SICFLOAT(dec, False)

        return decToFloat(dec, SICXE_SIZE_BIT_EXPONENT, SICXE_SIZE_BIT_MANTISSA)

    def setfloat(self, addr, val):
        dec = val
        if issubclass(type(val), NUM):
            dec = val.dec
        else:
            dec = floatToDec(val, SICXE_SIZE_BIT_FLOAT_EXPONENT, SICXE_SIZE_BIT_FLOAT_MANTISSA)
        self.set(addr, dec, SICXE_SIZE_BYTE_FLOAT)

    def toString(self, rang: Tuple[int, int]):
        string = ''
        for i in range(rang[0], rang[1], 16):
            addr = hex(i).replace('0x', '')
            addr = '0' * (5 - len(addr)) + addr
            string += addr + '\t'
            for j in range(i, i + 16, 1):
                if j % 4 == 0: string += ' '
                val = hex(self.mem[j]).replace('0x', '')
                val = '0' * (2 - len(val)) + val
                string += val + ' '

            for j in range(i, i + 16, 1):
                if j % 4 == 0: string += ' '
                # char = chr()
                val = chr(self.mem[j]) if 0x20 <= self.mem[j] <= 0x7e else '.'
                string += val + ' '
            string += '\n'

        return string

    def __str__(self):
        return self.toString((0, len(self.mem)))


if __name__ == '__main__':
    r = MEMORY(0x20)
    r.set(0x1e, 0x142115, 3)
    r.setfloat(0x8, 1.4)
    print(r.toString((0, 0x20)))
