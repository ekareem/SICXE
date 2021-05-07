from util.num import INT
from util.common import *
from util.opcodee import opcodes

SIC = 0b00000000
DIRECT = 0b11000000
INDIRECT = 0b10000000
IMMIDIATE = 0b01000000
INDEX = 0b00100000
BASE = 0b00010000
PC = 0b00001000
EXTENDED = 0b00000100

flagmap = {
    DIRECT: '',
    INDIRECT: '@',
    IMMIDIATE: '#',
    INDEX: '+(X)',
    BASE: '+(B)',
    PC: '+(PC)',
    EXTENDED: '+',
}


def isSic(flag: int):
    return flag & DIRECT == SIC


def isDirect(flag: int):
    return flag & DIRECT == DIRECT


def isIndirect(flag: int):
    return flag >> 6 == INDIRECT >> 6


def isImidiate(flag: int):
    return flag >> 6 == IMMIDIATE >> 6


def isIndexed(flag: int):
    return flag & INDEX == INDEX


def isBase(flag: int):
    return flag & BASE == BASE


def isPc(flag: int):
    return flag & PC == PC


def isExtended(flag: int):
    return False if isSic(flag) else flag & EXTENDED == EXTENDED


def setSic(flag: int):
    return flag | SIC


def setDirect(flag: int):
    return flag | DIRECT


def setIndirect(flag: int):
    return flag | INDIRECT


def setImidiate(flag: int):
    return flag | IMMIDIATE


def setIndexed(flag: int):
    return flag | INDEX


def setBase(flag: int):
    return flag | BASE


def setPc(flag: int):
    return flag | PC == PC


def setExtended(flag: int):
    return flag | EXTENDED


def toString(instr: bytearray):
    nixbpe = getnixbpe(instr)
    opcode = getopcode(instr)
    operand = getDisp(instr)
    type = 'hex'
    opcode = f'0x{opcode:>02x}' if type == 'hex' else opcodes[opcode]['mnemonic']
    operand = f'0x{operand:>05x}'
    extended = flagmap[EXTENDED] if isExtendedInstr(instr) else ''
    immidiate = flagmap[IMMIDIATE] if isImidiateInstr(instr) else ''
    inDirect = flagmap[INDIRECT] if isIndirectInstr(instr) else ''
    index = flagmap[INDEX] if isIndexed(nixbpe) else ''
    base = flagmap[BASE] if isBase(nixbpe) else ''
    pc = flagmap[PC] if isPc(nixbpe) else ''
    return f"{extended}{opcode}{immidiate}{inDirect}{operand}{index}{base}{pc}"


def nixbpeToStringInstr(instr: bytearray):
    n = 'n' if isIndirectInstr(instr) or isDirectInstr(instr) else '-'
    i = 'i' if isImidiateInstr(instr) or isDirectInstr(instr) else '-'
    x = 'x' if isIndexedInstr(instr) else '-'
    b = 'b' if isBaseInstr(instr) else '-'
    p = 'p' if isPcInstr(instr) else '-'
    e = 'e' if isExtendedInstr(instr) else '-'
    return f'{n}{i}{x}{b}{p}{e}'


def getopcode(instr: bytearray):
    instr = bytearrayToInt(instr[0:1], False)
    return instr & 0xfc


def getnixbpe(instr: bytearray):
    instr = bytearrayToInt(instr[0:2], False)
    return instr >> 2 & 0xfc


def getMnemonicInstr(instr: bytearray):
    return opcodes[getopcode(instr)]['mnemonic']


def isSicInstr(instr: bytearray):
    return isSic(getnixbpe(instr))


def isDirectInstr(instr: bytearray):
    return isDirect(getnixbpe(instr))


def isIndirectInstr(instr: bytearray):
    return isIndirect(getnixbpe(instr))


def isImidiateInstr(instr: bytearray):
    return isImidiate(getnixbpe(instr))


def isIndexedInstr(instr: bytearray):
    return isIndexed(getnixbpe(instr))


def isBaseInstr(instr: bytearray):
    return isBase(getnixbpe(instr))


def isPcInstr(instr: bytearray):
    return isPc(getnixbpe(instr))


def registerToString(num: int, asStr=True, paran=True):
    r = ["(A)", "(X)", "(L)", "(B)", "(S)", "(T)", "(F)", "(?)", "(P)", "(SW)"] \
        if paran else ["A", "X", "L", "B", "S", "T", "F", "?", "P", "SW"]
    if num in [0, 1, 2, 3, 4, 5, 6, 8, 9] and asStr:
        return r[num]
    return str(num)


def isExtendedInstr(instr: bytearray):
    return isExtended(getnixbpe(instr))


def getFormat(instr: bytearray):
    opcode = getopcode(instr)

    if opcode not in opcodes:
        raise Exception('invalid opcode')

    form = opcodes[opcode]['format']
    if form > 2:
        if isExtendedInstr(instr):
            return 4
    return form


def getRegister1(instr: bytearray):
    if getFormat(instr) != 2:
        raise Exception('instruction must be of format 2 to get register 2')
    instr = bytearrayToInt(instr[1:2], False)
    return (instr >> 4) & 0xf


def getRegister2(instr: bytearray):
    if getFormat(instr) != 2:
        raise Exception('instruction must be of format 2 to get register 2')
    instr = bytearrayToInt(instr[1:2], False)
    return instr & 0xf


def getDisp(instr: bytearray):
    if getFormat(instr) < 3:
        print(hex(getopcode(instr)))
        raise Exception('instruction must be of format 3 or greater to have a displacement')

    if isSicInstr(instr):
        xbpedisp = bytearrayToInt(instr[1:3], False)
        return xbpedisp & 0x7fff

    if isExtendedInstr(instr):
        xbpeaddr = bytearrayToInt(instr[1:4], False)
        return xbpeaddr & 0xfffff

    xbpedisp = bytearrayToInt(instr[1:3], False)
    return xbpedisp & 0xfff


def getTargetAddress(instr: bytearray, pc, b, x, mem):
    if getFormat(instr) < 3:
        raise Exception('instruction must be of format 3 or greater to have a target address')

    disp = getDisp(instr)
    dispbitlen = 15 if isSicInstr(instr) else 20 if isExtendedInstr(instr) else 12
    ta = INT(disp, dispbitlen, False, False)

    if not isSicInstr(instr):
        if isBaseInstr(instr):
            ta = ta + b
        if isPcInstr(instr):
            ta = pc + ta.get(True)

    if isIndirectInstr(instr):
        ta = mem.getword(int(ta), False, 'SICWORD')

    if isIndexedInstr(instr):
        ta = ta + x

    return ta
