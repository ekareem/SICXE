from util import INT, SICXE_SIZE_BIT_EXPONENT, SICXE_SIZE_BIT_MANTISSA, SICXE_SIZE_BIT_WORD
from util.num import FLOAT

SICXE_NUM_REGISTER_A = 0
SICXE_NUM_REGISTER_X = 1
SICXE_NUM_REGISTER_L = 2
SICXE_NUM_REGISTER_PC = 8
SICXE_NUM_REGISTER_SW = 9
SICXE_NUM_REGISTER_B = 3
SICXE_NUM_REGISTER_S = 4
SICXE_NUM_REGISTER_T = 5
SICXE_NUM_REGISTER_F = 6

A = INT(0, SICXE_SIZE_BIT_WORD, True)
X = INT(0, SICXE_SIZE_BIT_WORD, False)
L = INT(0, SICXE_SIZE_BIT_WORD, False)
PC = INT(0, SICXE_SIZE_BIT_WORD, False)
SW = INT(0, SICXE_SIZE_BIT_WORD, False)
B = INT(0, SICXE_SIZE_BIT_WORD, False)
S = INT(0, SICXE_SIZE_BIT_WORD, False)
T = INT(0, SICXE_SIZE_BIT_WORD, False)
F = FLOAT(0, SICXE_SIZE_BIT_EXPONENT, SICXE_SIZE_BIT_MANTISSA, False)

registers = {0: A, 1: X, 2: L, 3: B, 4: S, 5: T, 6: F, 8: PC, 9: SW}


def registerToString(num: int):
    r = "AXLBSTF?PW"
    if num in registers:
        return r[num]
    return str(num)


def getRegister(num: int):
    if num not in registers:
        raise Exception('invalid register number')
    return registers[num]
