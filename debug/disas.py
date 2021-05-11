from debug.breakpoint import BreakPoint
from util import getFormat, getMnemonicInstr, getopcode, opcodes, F1, getRegister1, registerToString, \
    getRegister2, strformat, F2n, F2rn, F2rr, F2r, flagmap, EXTENDED, isExtendedInstr, F3, IMMIDIATE, isImidiateInstr, \
    INDIRECT, isIndirectInstr, isIndexedInstr, isBaseInstr, isPcInstr, INDEX, BASE, PC, getDisp, F3m, \
    nixbpeToStringInstr, getTargetAddress, INT, isDirectInstr, isSicInstr
from vm import CU, SICXE_NUM_REGISTER_PC, register


class Instruction:
    def __init__(self, cu: CU, loc: int, instr: bytearray):
        self.cu = cu
        self.loc: int = loc
        self.instr: bytearray = instr
        self.mnemonic = getMnemonicInstr(self.instr)
        self.form = strformat[opcodes[getopcode(self.instr)]['F']]

    def gethex(self):
        instr = ''
        for bytee in self.instr:
            instr += f'{bytee:0>2X} '

        # instr = bytearrayToInt(self.instr)

        l = len(self.instr) * 2
        hexcode = '{:0>' + str(l) + '}'
        hexcode = hexcode.format(instr)
        form = '0x{:0>5X}\t{:<15} op:{:0>2X}'
        return f'{form.format(self.loc, hexcode, getopcode(self.instr)):<16}\t'

    def getDisas(self):
        return ''

    def __str__(self):
        return self.gethex() + self.getDisas()

    def __repr__(self):
        return str(self)


class InstructionF1(Instruction):
    def __init__(self, cu, loc, instr):
        super().__init__(cu, loc, instr)

    def getDisas(self):
        return f'{"":>8}' + getMnemonicInstr(self.instr)


class InstructionF2(Instruction):
    def __init__(self, cu, loc, instr):
        super().__init__(cu, loc, instr)
        self.r1 = getRegister1(instr)
        self.r2 = getRegister2(instr)

    def getDisas(self, r1=True, r2=True):
        return f'{"":>8}' + self.form.format(self.mnemonic, registerToString(self.r1, r1, False),
                                             registerToString(self.r2, r2, False))


class InstructionF2n(InstructionF2):
    def __init__(self, cu, loc, instr):
        super().__init__(cu, loc, instr)

    def getDisas(self, r1=True, r2=True):
        return super(InstructionF2n, self).getDisas(False)


class InstructionF2r(InstructionF2):
    def __init__(self, cu, loc, instr):
        super().__init__(cu, loc, instr)

    def getDisas(self, r1=True, r2=True):
        return super(InstructionF2r, self).getDisas(True)


class InstructionF2rn(InstructionF2):
    def __init__(self, cu, loc, instr):
        super().__init__(cu, loc, instr)

    def getDisas(self, r1=True, r2=True):
        return super(InstructionF2rn, self).getDisas(True, False)


class InstructionF2rr(InstructionF2):
    def __init__(self, cu, loc, instr):
        super().__init__(cu, loc, instr)


class InstructionF3(Instruction):
    def __init__(self, cu, loc, instr):
        super().__init__(cu, loc, instr)

    def getDisas(self):
        extended = flagmap[EXTENDED] if isExtendedInstr(self.instr) else ''
        nixpbe = nixbpeToStringInstr(self.instr)
        return nixpbe + ' ' + self.form.format(extended, self.mnemonic)


class InstructionF3m(InstructionF3):
    def __init__(self, cu, loc, instr):
        super().__init__(cu, loc, instr)

    def getDisas(self):
        extended = flagmap[EXTENDED] if isExtendedInstr(self.instr) else ''
        immidiate = flagmap[IMMIDIATE] if isImidiateInstr(self.instr) else ''
        inDirect = flagmap[INDIRECT] if isIndirectInstr(self.instr) else ''
        index = flagmap[INDEX] if isIndexedInstr(self.instr) else ''
        base = flagmap[BASE] if isBaseInstr(self.instr) else ''
        pc = flagmap[PC] if isPcInstr(self.instr) else ''
        operand = getDisp(self.instr)
        nixpbe = nixbpeToStringInstr(self.instr)
        p = INT(self.loc + len(self.instr), 24, False)
        ta = getTargetAddress(self.instr, p, register.B, register.X, self.cu.mem, isDisas=True)
        out = nixpbe + ' ' + self.form.format(extended, self.mnemonic, immidiate, inDirect, operand, pc, base, index)

        f = ' ' * (44 - len(out))
        return out + f + self.ta(ta)

    def ta(self, ta):
        mode = ['', '']
        if isDirectInstr(self.instr) or isSicInstr(self.instr):
            mode = ['(', ')']
        if isIndirectInstr(self.instr):
            mode = ['((', '))']
        if isImidiateInstr(self.instr):
            mode = ['', '']
        return f'{mode[0]}0x{ta.dec:X}{mode[1]}'


def createInstruction(cu: CU, loc: int, instr: bytearray):
    if opcodes[getopcode(instr)]['F'] == F1:
        return InstructionF1(cu, loc, instr)
    if opcodes[getopcode(instr)]['F'] == F2r:
        return InstructionF2r(cu, loc, instr)
    if opcodes[getopcode(instr)]['F'] == F2n:
        return InstructionF2n(cu, loc, instr)
    if opcodes[getopcode(instr)]['F'] == F2rn:
        return InstructionF2rn(cu, loc, instr)
    if opcodes[getopcode(instr)]['F'] == F2rr:
        return InstructionF2rr(cu, loc, instr)
    if opcodes[getopcode(instr)]['F'] == F3:
        return InstructionF3(cu, loc, instr)
    if opcodes[getopcode(instr)]['F'] == F3m:
        return InstructionF3m(cu, loc, instr)
    return Instruction(cu, loc, instr)


def getInstructions(cu: CU, rang=None):
    instructions = []
    rang = (0, len(cu.mem) / 4) if rang is None else rang
    pc = rang[0]
    while pc < rang[1]:
        i = getInstruction(pc, cu)
        instructions.append(i)
        pc += len(i.instr)
    return instructions


def getInstruction(pc, cu: CU):
    instr = cu.mem.get(pc, 2, asbytearr=True)
    length = getFormat(instr)
    return createInstruction(cu, pc, cu.mem.get(int(pc), length, asbytearr=True))


class Disasembler:
    def __init__(self, cu: CU, br: BreakPoint, rang=None):
        self.instructions = getInstructions(cu, rang)
        self.cu = cu
        self.br = br

    def disas(self, rang=None):
        self.instructions = getInstructions(self.cu, rang)

    def __str__(self):
        string = f'{" ":<2}{"ADDR":<7}\t{"HEXCODE":<15} {"OPCODE":<2}\t{"MODE":<8}{"MNEMON":<8}{"OPERAND":16}{"TA":>14}\n\n'
        # "{:<1}{:<6} {}{}0x{:x}{}{}{:>2}    \t{}"
        for instr in self.instructions:
            pc = self.cu.registers[SICXE_NUM_REGISTER_PC].get(False)
            string += f"{'>' if pc == instr.loc else '*' if instr.loc in self.br else ' '} {instr}\n"
        return string


def isExpression(token):
    index = max(token.find('+'), token.find('-'))
    return index != -1 and index != 0
