from typing import Union

from asm.lexutil import toNumber

CONST = 1
ADDR = 2


class Storage:
    def __init__(self, id: str, addr: int = None, value: Union[int, str] = None, group: int = ADDR):
        self.id = id
        self.addr = addr
        self.group = group
        if self.id.find('=') == 0:
            self.value = id.replace('=', '')
        else:
            self.value = str(value)

    def addrIsSet(self):
        return self.addr is None

    def valueIsSet(self):
        return self.value is None

    def getAddr(self):
        if self.addr is not None:
            return self.addr
        return None

    def getValue(self, nbit, asByte=True):
        if self.value is not None:
            return toNumber(self.value, nbit, asByte)
        return toNumber("0", nbit, asByte)

    def __str__(self):
        return f'{self.addr} {self.value} {"address" if self.group == ADDR else "const"}'


class Symbol(Storage):
    def __init__(self, scope: int, id: str, addr: int = None, value: Union[int, bytearray] = None, group: int = ADDR):
        super().__init__(id, addr, value,group)
        self.scope = scope


class Literal(Storage):
    def __init__(self, id: str, addr: int = None, value: Union[int, bytearray] = None, group: int = ADDR):
        super().__init__(id, addr, value,group)
