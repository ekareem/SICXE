from typing import Union, List

from debug.command.command import BinaryCommand, Command, UnaryCommand
from loader import loader
from util import SICXE_SIZE_BIT_BYTE, bytearrayToInt, NUM, BIG, LITTLE
from vm import MEMORY, getRegister, SICXE_NUM_REGISTER_SW, SICXE_NUM_REGISTER_A, CU
from vm.presistance import memoryWrite, MEMORYFILE, readToMemory


class Set(BinaryCommand):
    def __init__(self, left: Command, right: Command):
        super().__init__(left, right)

    def execute(self, inputs=None) -> any:
        if self.left is None:
            raise Exception('no location specified')
        if self.right is None:
            raise Exception('no value specified')

        rm: Union[NUM, List[Union[MEMORY, int, int]]] = self.left.execute(False)
        nbyte = rm[2] if type(rm) == list else 3
        val: bytearray = self.right.execute(True, nbyte)

        return self.set(rm, val)

    def set(self, loc: Union[NUM, List[Union[MEMORY, int]]], val: bytearray):
        raise NotImplementedError


class SetRegister(Set):
    def __init__(self, rm: Command, value: Command):
        super().__init__(rm, value)

    def set(self, rm: Union[NUM, List[Union[MEMORY, int]]], val: bytearray):
        dec = ''
        if issubclass(type(rm), NUM):
            if int(rm.nbits / SICXE_SIZE_BIT_BYTE) != len(val):
                raise Exception('invalid value')
            dec = bytearrayToInt(val, False)
            rm.set(dec, False)
            return dec

        loc = rm[1]
        mem = rm[0]
        for i in range(loc, loc + len(val)):
            mem.setbyte(i, val[i - loc])

        return dec


class SetCC(UnaryCommand):
    def __init__(self, child: Command):
        super().__init__(child)

    def execute(self, inputs=None) -> any:
        value = self.child.execute(False)
        sw = getRegister(SICXE_NUM_REGISTER_SW)
        return self.set(sw, value)

    def set(self, sw: NUM, val: int):
        sw.setbits(val, (6, 8), BIG)
        return val


class SetCH(UnaryCommand):
    def __init__(self, child: Command):
        super().__init__(child)

    def execute(self, inputs=None) -> any:
        value = self.child.execute(False)
        a = getRegister(SICXE_NUM_REGISTER_A)
        return self.set(a, value)

    def set(self, a: NUM, val: int):
        a.setbits(val, (0, 8), LITTLE)
        return val


class Save(Command):
    def __init__(self, cu: CU, file):
        super().__init__()
        self.cu = cu
        self.file = file

    def execute(self, inputs=None) -> any:
        memoryWrite(self.cu, self.file)


class Read(Command):
    def __init__(self, cu: CU, file: str):
        super().__init__()
        self.cu = cu
        self.file = file

    def execute(self, inputs=None) -> any:
        readToMemory(self.cu, self.file)


class Load(Command):
    def __init__(self, cu: CU, file: str):
        super().__init__()
        self.cu = cu
        self.file = file

    def execute(self, inputs=None) -> any:
        return loader.load(self.cu, file=self.file)
