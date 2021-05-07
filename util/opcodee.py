from util.format import *

ADD = 0x18
ADDF = 0x58
ADDR = 0x90
AND = 0x40
CLEAR = 0xB4
COMP = 0x28
COMPF = 0x88
COMPR = 0xA0
DIV = 0x24
DIVF = 0x64
DIVR = 0x9C
FIX = 0xC4
FLOAT = 0xC0
HIO = 0xF4
J = 0x3C
JEQ = 0x30
JGT = 0x34
JLT = 0x38
JSUB = 0x48
LDA = 0x00
LDB = 0x68
LDCH = 0x50
LDF = 0x70
LDL = 0x08
LDS = 0x6C
LDT = 0x74
LDX = 0x04
LPS = 0xD0
MUL = 0x20
MULF = 0x60
MULR = 0x98
NORM = 0xC8
OR = 0x44
RD = 0xD8
RMO = 0xAC
RSUB = 0x4C
SHIFTL = 0xA4
SHIFTR = 0xA8
SIO = 0xF0
SSK = 0xEC
STA = 0x0C
STB = 0x78
STCH = 0x54
STF = 0x80
STI = 0xD4
STL = 0x14
STS = 0x7C
STSW = 0xE8
STT = 0x84
STX = 0x10
SUB = 0x1C
SUBF = 0x5C
SUBR = 0x94
SVC = 0xB0
TD = 0xE0
TIO = 0xF8
TIX = 0x2C
TIXR = 0xB8
WD = 0xDC
HALT = 0xE4
N0x8C = 0x8C
N0xBC = 0xBC
N0xCC = 0xCC
N0xFC = 0xFC

opcodes = {}
opcodes[ADD] = {'op': ADD, 'mnemonic': 'ADD', 'format': 3, 'F': F3m}
opcodes[ADDF] = {'op': ADDF, 'mnemonic': 'ADDF', 'format': 3, 'F': F3m}
opcodes[ADDR] = {'op': ADDR, 'mnemonic': 'ADDR', 'format': 2, 'F': F2rr}
opcodes[AND] = {'op': AND, 'mnemonic': 'AND', 'format': 3, 'F': F3m}
opcodes[CLEAR] = {'op': CLEAR, 'mnemonic': 'CLEAR', 'format': 2, 'F': F2r}
opcodes[COMP] = {'op': COMP, 'mnemonic': 'COMP', 'format': 3, 'F': F3m}
opcodes[COMPF] = {'op': COMPF, 'mnemonic': 'COMPF', 'format': 3, 'F': F3m}
opcodes[COMPR] = {'op': COMPR, 'mnemonic': 'COMPR', 'format': 2, 'F': F2rr}
opcodes[DIV] = {'op': DIV, 'mnemonic': 'DIV', 'format': 3, 'F': F3m}
opcodes[DIVF] = {'op': DIVF, 'mnemonic': 'DIVF', 'format': 3, 'F': F3m}
opcodes[DIVR] = {'op': DIVR, 'mnemonic': 'DIVR', 'format': 2, 'F': F2rr}
opcodes[FIX] = {'op': FIX, 'mnemonic': 'FIX', 'format': 1, 'F': F1}
opcodes[FLOAT] = {'op': FLOAT, 'mnemonic': 'FLOAT', 'format': 1, 'F': F1}
opcodes[HIO] = {'op': HIO, 'mnemonic': 'HIO', 'format': 1, 'F': F1}
opcodes[J] = {'op': J, 'mnemonic': 'J', 'format': 3, 'F': F3m}
opcodes[JEQ] = {'op': JEQ, 'mnemonic': 'JEQ', 'format': 3, 'F': F3m}
opcodes[JGT] = {'op': JGT, 'mnemonic': 'JGT', 'format': 3, 'F': F3m}
opcodes[JLT] = {'op': JLT, 'mnemonic': 'JLT', 'format': 3, 'F': F3m}
opcodes[JSUB] = {'op': JSUB, 'mnemonic': 'JSUB', 'format': 3, 'F': F3m}
opcodes[LDA] = {'op': LDA, 'mnemonic': 'LDA', 'format': 3, 'F': F3m}
opcodes[LDB] = {'op': LDB, 'mnemonic': 'LDB', 'format': 3, 'F': F3m}
opcodes[LDCH] = {'op': LDCH, 'mnemonic': 'LDCH', 'format': 3, 'F': F3m}
opcodes[LDF] = {'op': LDF, 'mnemonic': 'LDF', 'format': 3, 'F': F3m}
opcodes[LDL] = {'op': LDL, 'mnemonic': 'LDL', 'format': 3, 'F': F3m}
opcodes[LDS] = {'op': LDS, 'mnemonic': 'LDS', 'format': 3, 'F': F3m}
opcodes[LDT] = {'op': LDT, 'mnemonic': 'LDT', 'format': 3, 'F': F3m}
opcodes[LDX] = {'op': LDX, 'mnemonic': 'LDX', 'format': 3, 'F': F3m}
opcodes[LPS] = {'op': LPS, 'mnemonic': 'LPS', 'format': 3, 'F': F3m}
opcodes[MUL] = {'op': MUL, 'mnemonic': 'MUL', 'format': 3, 'F': F3m}
opcodes[MULF] = {'op': MULF, 'mnemonic': 'MULF', 'format': 3, 'F': F3m}
opcodes[MULR] = {'op': MULR, 'mnemonic': 'MULR', 'format': 2, 'F': F2rr}
opcodes[NORM] = {'op': NORM, 'mnemonic': 'NORM', 'format': 1, 'F': F1}
opcodes[OR] = {'op': OR, 'mnemonic': 'OR', 'format': 1, 'F': F1}
opcodes[RD] = {'op': RD, 'mnemonic': 'RD', 'format': 3, 'F': F3m}
opcodes[RMO] = {'op': RMO, 'mnemonic': 'RMO', 'format': 2, 'F': F2rr}
opcodes[RSUB] = {'op': RSUB, 'mnemonic': 'RSUB', 'format': 3, 'F': F3}
opcodes[SHIFTL] = {'op': SHIFTL, 'mnemonic': 'SHIFTL', 'format': 2, 'F': F2rn}
opcodes[SHIFTR] = {'op': SHIFTR, 'mnemonic': 'SHIFTR', 'format': 2, 'F': F2rn}
opcodes[SIO] = {'op': SIO, 'mnemonic': 'SIO', 'format': 1, 'F': F1}
opcodes[SSK] = {'op': SSK, 'mnemonic': 'SSK', 'format': 3, 'F': F3m}
opcodes[SSK] = {'op': SSK, 'mnemonic': 'SSK', 'format': 3, 'F': F3m}
opcodes[STA] = {'op': STA, 'mnemonic': 'STA', 'format': 3, 'F': F3m}
opcodes[STB] = {'op': STB, 'mnemonic': 'STB', 'format': 3, 'F': F3m}
opcodes[STCH] = {'op': STCH, 'mnemonic': 'STCH', 'format': 3, 'F': F3m}
opcodes[STF] = {'op': STF, 'mnemonic': 'STF', 'format': 3, 'F': F3m}
opcodes[STI] = {'op': STI, 'mnemonic': 'STI', 'format': 3, 'F': F3m}
opcodes[STL] = {'op': STL, 'mnemonic': 'STL', 'format': 3, 'F': F3m}
opcodes[STS] = {'op': STS, 'mnemonic': 'STS', 'format': 3, 'F': F3m}
opcodes[STSW] = {'op': STSW, 'mnemonic': 'STSW', 'format': 3, 'F': F3m}
opcodes[STT] = {'op': STT, 'mnemonic': 'STT', 'format': 3, 'F': F3m}
opcodes[STX] = {'op': STX, 'mnemonic': 'STX', 'format': 3, 'F': F3m}
opcodes[SUB] = {'op': SUB, 'mnemonic': 'SUB', 'format': 3, 'F': F3m}
opcodes[SUBF] = {'op': SUBF, 'mnemonic': 'SUBF', 'format': 3, 'F': F3m}
opcodes[SUBR] = {'op': SUBR, 'mnemonic': 'SUBR', 'format': 2, 'F': F2rr}
opcodes[SVC] = {'op': SVC, 'mnemonic': 'SVC', 'format': 2, 'F': F2n}
opcodes[TD] = {'op': TD, 'mnemonic': 'TD', 'format': 3, 'F': F3m}
opcodes[TIO] = {'op': TIO, 'mnemonic': 'TIO', 'format': 1, 'F': F1}
opcodes[TIX] = {'op': TIX, 'mnemonic': 'TIX', 'format': 3, 'F': F3m}
opcodes[TIXR] = {'op': TIXR, 'mnemonic': 'TIXR', 'format': 2, 'F': F2r}
opcodes[WD] = {'op': WD, 'mnemonic': 'WD', 'format': 3, 'F': F3m}

opcodes[HALT] = {'op': HALT, 'mnemonic': 'HALT', 'format': 1, 'F': F1}
opcodes[N0x8C] = {'op': N0x8C, 'mnemonic': 'XXX', 'format': 1, 'F': F1}
opcodes[N0xBC] = {'op': N0xBC, 'mnemonic': 'XXX', 'format': 1, 'F': F1}
opcodes[N0xCC] = {'op': N0xCC, 'mnemonic': 'XXX', 'format': 1, 'F': F1}
opcodes[N0xFC] = {'op': N0xFC, 'mnemonic': 'XXX', 'format': 1, 'F': F1}


def stringToOpcode(mnemonic):
    return globals()[mnemonic]


def isOpcode(mnemonic):
    try:
        globals()[mnemonic]
        return True
    except:
        return False