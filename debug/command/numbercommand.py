from debug.command.command import Command
from util import SICXE_SIZE_BIT_EXPONENT, SICXE_SIZE_BIT_MANTISSA, floatToBytearray, \
    intToBytearray, SICXE_SIZE_BYTE_WORD, bytearrayToInt, bytearrayToFloat


class Number(Command):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def execute(self, asBytes=False, nbyte=SICXE_SIZE_BYTE_WORD) -> str:
        return self.num if not asBytes else intToBytearray(self.num, nbyte, True)


class StringToNum(Command):
    def __init__(self, string: str):
        super().__init__()
        self.string = string

    def execute(self, asBytes=False):
        if asBytes is None:
            return self.string

        ret = self.string
        if self.string.find("'") != -1 and asBytes is not None:
            ret = bytearray(self.string.strip("'"), 'utf-8')

        if self.string.find('"') != -1 and asBytes is not None:
            ret = bytearray(self.string.strip('"'), 'utf-8')

        if self.string.find('.') != -1 and asBytes is not None:
            ret = floatToBytearray(float(self.string), SICXE_SIZE_BIT_EXPONENT, SICXE_SIZE_BIT_MANTISSA)
            if not asBytes:
                return bytearrayToFloat(ret, SICXE_SIZE_BIT_EXPONENT, SICXE_SIZE_BIT_MANTISSA)

        if not asBytes:
            return bytearrayToInt(ret)

        return ret
