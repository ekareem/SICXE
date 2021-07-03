from typing import Union

from util import INT, BIG, LITTLE, SICXE_CC_GT, SICXE_CC_LT, SICXE_CC_EQ
from util.num import FLOAT
from vm.mem import MEMORY
from vm.register import A, SW, F


def addrm(register: INT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getword(addr, True)
    register.add(operand, setSelf=True)


def subrm(register: INT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getword(addr, True)
    register.sub(operand, setSelf=True)


def mulrm(register: INT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getword(addr, True)
    register.mul(operand, setSelf=True)


def divrm(register: INT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getword(addr, True)
    register.truediv(operand, setSelf=True)


def andrm(register: INT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getword(addr, True)
    register.andd(operand, setSelf=True)


def orrm(register: INT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getword(addr, True)
    register.orr(operand, setSelf=True)


def comprm(register: INT, sw: INT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getword(addr, True)
    cc = SICXE_CC_GT if register > operand else SICXE_CC_LT if register < operand else SICXE_CC_EQ
    sw.setbits(cc, (6, 8), BIG)


def comprr(register1: INT, register2: INT, sw: INT):
    cc = SICXE_CC_GT if register1 > register2 else SICXE_CC_LT if register1 < register2 else SICXE_CC_EQ
    sw.setbits(cc, (6, 8), BIG)


def addfrm(register: FLOAT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getfloat(addr)
    register.add(operand, setSelf=True)


def subfrm(register: FLOAT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getfloat(addr)
    register.sub(operand, setSelf=True)


def mulfrm(register: FLOAT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getfloat(addr)
    register.mul(operand, setSelf=True)


def divfrm(register: FLOAT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getfloat(addr)
    register.truediv(operand, setSelf=True)


def compfrm(register: FLOAT, sw: INT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getfloat(addr)
    cc = SICXE_CC_GT if register > operand else SICXE_CC_LT if register < operand else SICXE_CC_EQ
    sw.setbits(cc, (6, 8), BIG)


def norm(register: FLOAT):
    register.normalize(True, setSelf=True)


def addrr(register1: Union[INT, FLOAT], register2: Union[INT, FLOAT]):
    register2.add(register1, setSelf=True)


def subrr(register1: Union[INT, FLOAT], register2: Union[INT, FLOAT]):
    register2.sub(register1, setSelf=True)


def mulrr(register1: Union[INT, FLOAT], register2: Union[INT, FLOAT]):
    register2.mul(register1, setSelf=True)


def divrr(register1: Union[INT, FLOAT], register2: Union[INT, FLOAT]):
    register2.truediv(register1, setSelf=True)


def shiftl(register1: Union[INT, FLOAT], number: int):
    register1.clshift(number, setSelf=True)


def shiftr(register1: Union[INT, FLOAT], number: int):
    register1.rshift(number, setSelf=True)


def ld(register: INT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getword(addr, False)
    register.set(operand)


def ldf(register: FLOAT, mem: MEMORY, addr, isImmediate=False):
    if isImmediate:
        register.set(addr)
    else:
        register.dec = mem.get(addr, 6)


def ldch(register: INT, mem: MEMORY, addr, isImmediate=False):
    operand = addr if isImmediate else mem.getbyte(addr)
    if operand < 0 or operand > 0xff:
        raise Exception('cannot be longer the a byte')
    register.setbits(operand, (0, 8), LITTLE)


def st(register: INT, mem: MEMORY, addr):
    mem.setword(addr, register)


def stf(register: FLOAT, mem: MEMORY, addr):
    mem.set(addr, register.dec, 6)


def stch(register: INT, mem: MEMORY, addr):
    mem.setbyte(addr, register.getbits((0, 8), False, LITTLE))
