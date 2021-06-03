from typing import Union

from util.common import *
import copy

BIG = 'big'
LITTLE = 'little'


class NUM:
    def __init__(self, dec: int = 0, nbits: int = 8, order=BIG):
        self.dec = fit(dec, nbits)
        self.nbits = nbits
        self.order = order

    def get(self, signed=None):
        raise NotImplementedError

    def set(self, val, iscls):
        raise NotImplementedError

    def getbits(self, rangee=(0, 1), order=BIG) -> Union['INT', int]:
        f = len(list(self)) - rangee[0] if order == LITTLE else rangee[0]
        l = len(list(self)) - rangee[1] if order == LITTLE else rangee[1]
        rangee = [l, f] if order == LITTLE else [f, l]
        form = "{:>0" + str(self.nbits) + "b}"
        lis = list(form.format(self.dec))
        numstr = ''.join(lis[rangee[0]:rangee[1]])
        valint = int(numstr, 2)

        return valint

    def __getitem__(self, key: Union[int, tuple]) -> Union:
        # if item is int turn it to a tuple
        key = (key, key + 1) if type(key) == int else key
        return self.getbits(key, self.order)

    def setbits(self, val: int, rangee=(0, 1), order=BIG):
        f = len(list(self)) - rangee[0] if order == LITTLE else rangee[0]
        l = len(list(self)) - rangee[1] if order == LITTLE else rangee[1]
        rangee = [l, f] if order == LITTLE else [f, l]

        form = "{:>0" + str(self.nbits) + "b}"
        lis = list(form.format(self.dec))
        g = "{:>0" + str(rangee[1] - rangee[0]) + "b}"
        declist = list(g.format(val))
        if len(declist) != rangee[1] - rangee[0]:
            raise Exception('range value out of bounds')

        lis[rangee[0]:rangee[1]] = declist
        self.dec = int(''.join(lis), 2)

    def __setitem__(self, key: Union[int, tuple], value: int):
        # if item is int turn it to a tuple
        key = (key, key + 1) if type(key) == int else key
        self.setbits(value, key, self.order)

    def toBytearray(self):
        return intToBytearray(self.dec, math.ceil(self.nbits / 8), False)

    def output(self, val: int, toCLS=True, setSelf=False, signed=None):
        return NotImplemented

    def toDec(self, val):
        return NotImplemented

    def __copy__(self):
        return self

    def __bytes__(self):
        return int.to_bytes(self.dec, math.ceil(self.nbits / 8), self.order)

    def __iter__(self):
        current = 1
        f = "{:>0" + str(self.nbits) + "b}"
        l = list(f.format(self.dec))
        while current < self.nbits + 1:
            index = self.nbits - current if self.order == LITTLE else current - 1
            yield int(l[index], 2)
            current += 1

    """
    bitwise
    """

    def andd(self, other, toCLS=True, setSelf=False, signed=None):
        operand = other.dec if issubclass(type(other), NUM) else self.toDec(other)
        val = self.dec & operand
        return self.output(val, toCLS, setSelf, signed)

    def __and__(self, other):
        return self.andd(other, True)

    def lshift(self, other, toCLS=True, setSelf=False, signed=None):
        operand = other.dec if issubclass(type(other), NUM) else other
        val = self.dec << operand
        return self.output(val, toCLS, setSelf, signed)

    def clshift(self, other, toCLS=True, setSelf=False, signed=None):
        operand = other.dec if issubclass(type(other), NUM) else other
        val = leftRotate(self.dec, operand, self.nbits)
        return self.output(val, toCLS, setSelf, signed)

    def __lshift__(self, other):
        return self.lshift(other, True)

    def invert(self, toCLS=True, setSelf=False, signed=None):
        val = ~self.dec
        return self.output(val, toCLS, setSelf, signed)

    def __invert__(self) -> int:
        return self.invert(True)

    def orr(self, other, toCLS=True, setSelf=False, signed=None):
        operand = other.dec if issubclass(type(other), NUM) else self.toDec(other)
        val = self.dec | operand
        return self.output(val, toCLS, setSelf, signed)

    def __or__(self, other):
        return self.orr(other, False)

    def rand(self, other, toCLS=True, setSelf=False, signed=None):
        operand = other.dec if issubclass(type(other), NUM) else self.toDec(other)
        val = operand & self.dec
        return self.output(val, toCLS, setSelf, signed)

    def __rand__(self, other):
        return self.rand(other, False)

    def ror(self, other, toCLS=True, setSelf=False, signed=None):
        operand = other.dec if issubclass(type(other), NUM) else self.toDec(other)
        val = operand | self.dec
        return self.output(val, toCLS, setSelf, signed)

    def __ror__(self, other):
        return self.ror(other, False)

    def rrshift(self, other, toCLS=True, setSelf=False, signed=None):
        operand = other.dec if issubclass(type(other), NUM) else other
        val = operand >> self.dec
        return self.output(val, toCLS, setSelf, signed)

    def __rrshift__(self, other):
        return self.rrshift(other, False)

    def rshift(self, other, toCLS=True, setSelf=False, signed=None):
        operand = other.dec if issubclass(type(other), NUM) else other
        val = self.dec >> operand
        return self.output(val, toCLS, setSelf, signed)

    def crshift(self, other, toCLS=True, setSelf=False, signed=None):
        operand = other.dec if issubclass(type(other), NUM) else other
        val = rightRotate(self.dec, operand, self.nbits)
        return self.output(val, toCLS, setSelf, signed)

    def __rshift__(self, other):
        return self.rshift(other, True)

    def rxor(self, other, toCLS=True, setSelf=False, signed=None):
        operand = other.dec if issubclass(type(other), NUM) else self.toDec(other)
        val = operand ^ self.dec
        return self.output(val, toCLS, setSelf, signed)

    def __rxor__(self, other):
        return self.rxor(other, False)

    def xor(self, other, toCLS=True, setSelf=False, signed=None):
        operand = other.dec if issubclass(type(other), NUM) else self.toDec(other)
        val = self.dec ^ operand
        return self.output(val, toCLS, setSelf, signed)

    def __xor__(self, other):
        return self.xor(other, True)

    def __repr__(self):
        return str(self)

    def __bool__(self) -> bool:
        return self.dec != 0

    def __index__(self):
        return self.dec

    def __len__(self):
        return self.nbits


class INT(NUM):
    def __init__(self, val: int = 0, nbits: int = 8, signed=True, isInt=True, order=BIG):
        dec = intToDec(int(val), nbits) if isInt else fit(val, nbits)
        super(INT, self).__init__(dec, nbits, order)
        self.signed: bool = signed

    def set(self, val, isInt=True):
        self.dec = intToDec(int(val), self.nbits) if isInt else fit(val, self.nbits)

    def toUnsignedInt(self):
        """
        makes int unsgned
        :return: INT
        """
        if self.signed:
            self.dec &= int('1' * (self.nbits - 1), 2)
        self.signed = False
        return self

    def get(self, signed=None):
        signed = self.signed if signed is None else signed
        return decToInt(self.dec, self.nbits, signed)

    def toInt(self, val, signed=True):
        val = intToDec(int(val), self.nbits)
        return decToInt(val, self.nbits, signed)

    def output(self, val: int, toCLS=True, setSelf=False, signed=None):
        signed = self.signed if signed is None else signed
        out = INT(val, self.nbits, signed, True, self.order)
        if not toCLS:
            valint = intToDec(val, self.nbits)
            out = decToInt(valint, self.nbits, signed)
        if setSelf:
            self.set(out)
        return out

    def toDec(self, val):
        return intToDec(int(val), self.nbits)

    def getbits(self, rangee=(0, 1), toCLS=True, order=BIG):
        val = super(INT, self).getbits(rangee, order)
        return self.output(val, toCLS)

    def __deepcopy__(self, memodict={}):
        deep = INT()
        deep.dec = copy.deepcopy(self.dec)
        deep.nbits = copy.deepcopy(self.nbits)
        deep.signed = copy.deepcopy(self.signed)
        return deep

    """
    aritmetic
    """

    def add(self, other, toCLS: bool = True, setSelf=False, signed=None):
        val = self.toInt(self, signed) + int(other)
        return self.output(val, toCLS, setSelf, signed)

    def __add__(self, other) -> int:
        return self.add(other, True)

    def mod(self, other, toCLS=True, setSelf=False, signed=None):
        val = self.toInt(self, signed) % int(other)
        return self.output(val, toCLS, setSelf, signed)

    def __mod__(self, other):
        return self.mod(other, True)

    def mul(self, other, toCLS=True, setSelf=False, signed=None):
        val = self.toInt(self, signed) * int(other)
        return self.output(val, toCLS, setSelf, signed)

    def __mul__(self, other):
        return self.mul(other, True)

    def neg(self, toCLS=True, setSelf=False, signed=None):
        val = -self.toInt(self, signed)
        return self.output(val, toCLS, setSelf, signed)

    def __neg__(self):
        return self.neg(True)

    def pos(self, toCLS=True, setSelf=False, signed=None):
        val = +self.toInt(self, signed)
        return self.output(val, toCLS, setSelf, signed)

    def __pos__(self):
        return self.pos(True)

    def pow(self, other, toCLS=True, setSelf=False, signed=None):
        val = self.toInt(self, signed) ** int(other)
        return self.output(val, toCLS, setSelf, signed)

    def __pow__(self, power, modulo=None):
        return self.pow(power, True)

    def radd(self, other, toCLS=True, setSelf=False, signed=None):
        val = int(other) + self.toInt(self, signed)
        return self.output(val, toCLS, setSelf, signed)

    def __radd__(self, other):
        return self.radd(other, False)

    def rmod(self, other, toCLS=True, setSelf=False, signed=None):
        val = int(other) % self.toInt(self, signed)
        return self.output(val, toCLS, setSelf, signed)

    def __rmod__(self, other):
        return self.rmod(other, False)

    def rmul(self, other, toCLS=True, setSelf=False, signed=None):
        val = int(other) * self.toInt(self, signed)
        return self.output(val, toCLS, setSelf, signed)

    def __rmul__(self, other):
        return self.rmul(other, False)

    def rsub(self, other, toCLS=True, setSelf=False, signed=None):
        val = int(other) - self.toInt(self, signed)
        return self.output(val, toCLS, setSelf, signed)

    def __rsub__(self, other):
        return self.rsub(other, False)

    def rtruediv(self, other, toCLS=True, setSelf=False, signed=None):
        val = int(int(other) / self.toInt(self, signed))
        return self.output(val, toCLS, setSelf, signed)

    def __rtruediv__(self, other):
        return self.rtruediv(other, False)

    def sub(self, other, toCLS=True, setSelf=False, signed=None):
        val = self.toInt(self, signed) - int(other)
        return self.output(val, toCLS, setSelf, signed)

    def __sub__(self, other):
        return self.sub(other, True)

    def truediv(self, other, toCLS=True, setSelf=False, signed=None):
        val = int(self.toInt(self, signed) / int(other))
        return self.output(val, toCLS, setSelf, signed)

    def __truediv__(self, other):
        return self.truediv(other, True)

    def abs(self, toCLS=True, setSelf=False, signed=None):
        val = abs(self.toInt(self, signed))
        return self.output(val, toCLS, setSelf, signed)

    def __abs__(self):
        return self.abs(True)

    def __divmod__(self, other):
        return divmod(int(self), int(other))

    def __rdivmod__(self, other):
        return divmod(int(other), int(self))

    """
    compare
    """

    def __eq__(self, other) -> bool:
        return int(self) == int(other)

    def __ge__(self, other) -> bool:
        return int(self) >= int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __le__(self, other) -> bool:
        return int(self) <= int(other)

    def __lt__(self, other) -> bool:
        return int(self) < int(other)

    def __ne__(self, other) -> bool:
        return int(self) != int(other)

    """
    conversion
    """

    def __int__(self) -> int:
        return decToInt(self.dec, self.nbits, self.signed)

    def __str__(self) -> str:
        return str(int(self))

    def __float__(self) -> float:
        return float(int(self))


class FLOAT(NUM):
    def __init__(self, val: float = 0, exponentLen=11, mantissaLen=36, isFloat=True, order=BIG):
        self.nbits = 1 + exponentLen + mantissaLen
        dec = floatToDec(float(val), exponentLen, mantissaLen) if isFloat else fit(val, self.nbits)
        super(FLOAT, self).__init__(dec, self.nbits, order)
        self.exponentLen = exponentLen
        self.mantissaLen = mantissaLen

    def __deepcopy__(self, memodict={}):
        deep = FLOAT()
        deep.dec = copy.deepcopy(self.dec)
        deep.nbits = copy.deepcopy(self.nbits)
        deep.exponentLen = copy.deepcopy(self.exponentLen)
        deep.mantissaLen = copy.deepcopy(self.mantissaLen)
        return deep

    def get(self, signed=None):
        return decToFloat(self.dec, self.exponentLen, self.mantissaLen)

    def set(self, val, isFloat=True):
        self.dec = floatToDec(float(val), self.exponentLen, self.mantissaLen) if isFloat else fit(val, self.nbits)

    def sign(self):
        return self.getbits((0, 1), BIG)

    def exponent(self):
        return self.getbits((1, self.exponentLen + 1), BIG)

    def mantissa(self):
        return self.getbits((0, self.mantissaLen), LITTLE)

    def normalize(self, toCLS=True, setSelf=False):
        val = decToFloat(self.dec, self.exponentLen, self.mantissaLen)
        return self.output(val, toCLS, setSelf)

    def output(self, val: float, toCLS=True, setSelf=False, signed=None):
        out = FLOAT(val, self.exponentLen, self.mantissaLen, True, self.order)
        if not toCLS:
            valint = floatToDec(val, self.exponentLen, self.mantissaLen)
            return decToFloat(valint, self.exponentLen, self.mantissaLen)
        if setSelf:
            self.set(out)
        return out

    def toDec(self, val):
        return floatToDec(float(val), self.exponentLen, self.mantissaLen)

    def add(self, other, toCLS: bool = True, setSelf=False):
        val = float(self) + float(other)
        return self.output(val, toCLS, setSelf)

    def __add__(self, other):
        return self.add(other, True)

    def mod(self, other, toCLS=True, setSelf=False):
        val = float(self) % float(other)
        return self.output(val, toCLS, setSelf)

    def __mod__(self, other):
        return self.mod(other, True)

    def mul(self, other, toCLS=True, setSelf=False):
        val = float(self) * float(other)
        return self.output(val, toCLS, setSelf)

    def __mul__(self, other):
        return self.mul(other, True)

    def neg(self, toCLS=True, setSelf=False):
        val = -float(self)
        return self.output(val, toCLS, setSelf)

    def __neg__(self):
        return self.neg(True)

    def pos(self, toCLS=True, setSelf=False):
        val = +float(self)
        return self.output(val, toCLS, setSelf)

    def __pos__(self):
        return self.pos(True)

    def pow(self, other, toCLS=True, setSelf=False):
        val = float(self) ** float(other)
        return self.output(val, toCLS, setSelf)

    def __pow__(self, power, modulo=None):
        return self.pow(power, True)

    def radd(self, other, toCLS=True, setSelf=False):
        val = float(other) + float(self)
        return self.output(val, toCLS, setSelf)

    def __radd__(self, other):
        return self.radd(other, False)

    def rmod(self, other, toCLS=True, setSelf=False):
        val = float(other) % float(self)
        return self.output(val, toCLS, setSelf)

    def __rmod__(self, other):
        return self.rmod(other, False)

    def rmul(self, other, toCLS=True, setSelf=False):
        val = float(other) * float(self)
        return self.output(val, toCLS, setSelf)

    def __rmul__(self, other):
        return self.rmul(other, False)

    def rsub(self, other, toCLS=True, setSelf=False):
        val = float(other) - float(self)
        return self.output(val, toCLS, setSelf)

    def __rsub__(self, other):
        return self.rsub(other, False)

    def rtruediv(self, other, toCLS=True, setSelf=False):
        val = float(other) / float(self)
        return self.output(val, toCLS, setSelf)

    def __rtruediv__(self, other):
        return self.rtruediv(other, False)

    def sub(self, other, toCLS=True, setSelf=False):
        val = float(self) - float(other)
        return self.output(val, toCLS, setSelf)

    def __sub__(self, other):
        return self.sub(other, True)

    def truediv(self, other, toCLS=True, setSelf=False):
        val = float(self) / float(other)
        return self.output(val, toCLS, setSelf)

    def __truediv__(self, other):
        return self.truediv(other, True)

    def abs(self, toCLS=True, setSelf=False):
        val = abs(float(self))
        return self.output(val, toCLS, setSelf)

    def __abs__(self):
        return self.abs(True)

    def __divmod__(self, other):
        return divmod(float(self), float(other))

    def __rdivmod__(self, other):
        return divmod(float(other), float(self))

    """
    compare
    """

    def __eq__(self, other: Union['FLOAT', float]) -> bool:
        return float(self) == float(other)

    def __ge__(self, other: Union['FLOAT', float]) -> bool:
        return float(self) >= float(other)

    def __gt__(self, other):
        return float(self) > float(other)

    def __le__(self, other: Union['FLOAT', float]) -> bool:
        return float(self) <= float(other)

    def __lt__(self, other: Union['FLOAT', float]) -> bool:
        return float(self) < float(other)

    def __ne__(self, other: Union['FLOAT', float]) -> bool:
        return float(self) != float(other)

    """
    conversion
    """

    def __int__(self) -> int:
        return int(float(self))

    def __str__(self) -> str:
        return str(float(self))

    def __float__(self) -> float:
        return decToFloat(self.dec, self.exponentLen, self.mantissaLen)


class SICWORD(INT):
    def __init__(self, val, signed=True, isInt=False):
        super().__init__(val, 24, signed, isInt, BIG)


class SICFLOAT(FLOAT):
    def __init__(self, val, isFloat=False):
        super().__init__(val, 11, 36, isFloat, BIG)
