from asm import SYMTAB, ADDR
from debug.breakpoint import BreakPoint
from util import getFormat, getMnemonicInstr, getopcode, opcodes, F1, getRegister1, registerToString, \
    getRegister2, strformat, F2n, F2rn, F2rr, F2r, flagmap, EXTENDED, isExtendedInstr, F3, IMMIDIATE, isImidiateInstr, \
    INDIRECT, isIndirectInstr, isIndexedInstr, isBaseInstr, isPcInstr, INDEX, BASE, PC, getDisp, F3m, \
    nixbpeToStringInstr, getTargetAddress, INT, isDirectInstr, isSicInstr, bytearrayToInt, bytearrayToFloat, \
    SICXE_SIZE_BIT_EXPONENT, SICXE_SIZE_BIT_MANTISSA,decToInt
from vm import CU, SICXE_NUM_REGISTER_PC, register


class Instruction:
    def __init__(self, cu: CU, loc: int, instr: bytearray, symtab: SYMTAB = None):
        self.cu = cu
        self.loc: int = loc
        self.instr: bytearray = instr
        self.mnemonic = getMnemonicInstr(self.instr)
        self.form = strformat[opcodes[getopcode(self.instr)]['F']]
        self.symtab = symtab

    def getSymbol(self, val, indirect='', immidiate='', index='', toTA=False):
        if self.symtab is not None:
            for sym in self.symtab.table:
                if self.symtab.table[sym].addr == val and \
                        self.symtab.table[sym].group == ADDR:
                    return f'{indirect}{immidiate}{sym}{index}'
        return f'{indirect}{immidiate}0x{val:X}{index}' if toTA else ''

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


class Data(Instruction):
    def __init__(self, cu, loc, instr, length, symtab: SYMTAB):
        super().__init__(cu, loc, instr, symtab)
        self.length = length

    def gethex(self):
        instr = ''
        for i, bytee in enumerate(self.instr):
            if i == 6:
                instr += '... '
            #     continue
            elif i < 6 or i > len(self.instr) - 3:
                instr += f'{bytee:0>2X} '

        # instr = bytearrayToInt(self.instr)

        l = len(self.instr) * 2
        hexcode = '{}'
        hexcode = hexcode.format(instr)
        form = '0x{:0>5X}\t{:<28}   '
        return f'{form.format(self.loc, hexcode):<16}'

    def getDataFormat(self, length):
        if length == 'b':
            return 'BYTE'
        elif length == 'w':
            return 'WORD'
        elif length == 'f':
            return 'FLOA'
        return 'BYTE'

    def getDisas(self):
        return f'{self.getSymbol(self.loc):<15}' + f'{self.getDataFormat(self.length):<9}'


class Word(Data):
    def __init__(self, cu, loc, instr, length, symtab: SYMTAB):
        super().__init__(cu, loc, instr, length, symtab)

    def getDisas(self):
        #f'{hex(bytearrayToInt(self.instr, False)):<15}'
        return super(Word,
                     self).getDisas()  + f'0x{bytearrayToInt(self.instr, False):0>6X}' \
               +f'{"":<7}'+ f'{bytearrayToInt(self.instr, False):<1}' + ' | ' \
               + f'{bytearrayToInt(self.instr, True):<2} '


class Floa(Data):
    def __init__(self, cu, loc, instr, length, symtab: SYMTAB):
        super().__init__(cu, loc, instr, length, symtab)

    def getDisas(self):
        return super(Floa,
                     self).getDisas() + f'0x{bytearrayToInt(self.instr, False):0>12X} ' + f'{bytearrayToFloat(self.instr, SICXE_SIZE_BIT_EXPONENT, SICXE_SIZE_BIT_MANTISSA):<1} '


class Byte(Data):
    def __init__(self, cu, loc, instr, length, symtab: SYMTAB):
        super().__init__(cu, loc, instr, length, symtab)

    def getDisas(self):
        char = "C'"
        for b in self.instr:
            if 0x20 <= b <= 0x7e:
                char += chr(b)
            else:
                char += f'\\x{b:0<2x}'
        char += "'"
        return super().getDisas() + f'{char}'


class InstructionF1(Instruction):
    def __init__(self, cu, loc, instr, symtab: SYMTAB):
        super().__init__(cu, loc, instr, symtab)

    def getDisas(self):
        return f'{"":<6}' + ' ' f'{self.getSymbol(self.loc):<15}' + getMnemonicInstr(self.instr)


class InstructionF2(Instruction):
    def __init__(self, cu, loc, instr, symtab: SYMTAB):
        super().__init__(cu, loc, instr, symtab)
        self.r1 = getRegister1(instr)
        self.r2 = getRegister2(instr)

    def getDisas(self, r1=True, r2=True):
        return f'{"":<6}' + ' ' + self.form.format(self.getSymbol(self.loc), self.mnemonic,
                                                   registerToString(self.r1, r1, False),
                                                   registerToString(self.r2, r2, False))


class InstructionF2n(InstructionF2):
    def __init__(self, cu, loc, instr, symtab: SYMTAB):
        super().__init__(cu, loc, instr, symtab)

    def getDisas(self, r1=True, r2=True):
        return super(InstructionF2n, self).getDisas(False)


class InstructionF2r(InstructionF2):
    def __init__(self, cu, loc, instr, symtab: SYMTAB):
        super().__init__(cu, loc, instr, symtab)

    def getDisas(self, r1=True, r2=True):
        return super(InstructionF2r, self).getDisas(True)


class InstructionF2rn(InstructionF2):
    def __init__(self, cu, loc, instr, symtab: SYMTAB):
        super().__init__(cu, loc, instr, symtab)

    def getDisas(self, r1=True, r2=True):
        return super(InstructionF2rn, self).getDisas(True, False)


class InstructionF2rr(InstructionF2):
    def __init__(self, cu, loc, instr, symtab: SYMTAB):
        super().__init__(cu, loc, instr, symtab)


class InstructionF3(Instruction):
    def __init__(self, cu, loc, instr, symtab: SYMTAB):
        super().__init__(cu, loc, instr, symtab)

    def getDisas(self):
        extended = flagmap[EXTENDED] if isExtendedInstr(self.instr) else ''
        nixpbe = nixbpeToStringInstr(self.instr)
        return nixpbe + ' ' + self.form.format(self.getSymbol(self.loc), extended, self.mnemonic)


class InstructionF3m(InstructionF3):
    def __init__(self, cu, loc, instr, symtab: SYMTAB):
        super().__init__(cu, loc, instr, symtab)

    def getDisas(self):
        extended = flagmap[EXTENDED] if isExtendedInstr(self.instr) else ''
        immidiate = flagmap[IMMIDIATE] if isImidiateInstr(self.instr) else ''
        inDirect = flagmap[INDIRECT] if isIndirectInstr(self.instr) else ''
        index = flagmap[INDEX] if isIndexedInstr(self.instr) else ''
        base = flagmap[BASE] if isBaseInstr(self.instr) else ''
        pc = flagmap[PC] if isPcInstr(self.instr) else ''
        operand = self.signedDisp() #getDisp(self.instr)
        sign = '-' if operand < 0 else ''
        nixpbe = nixbpeToStringInstr(self.instr)
        p = INT(self.loc + len(self.instr), 24, False)
        ta = getTargetAddress(self.instr, p, register.B, register.X, self.cu.mem, isDisas=True)
        out = nixpbe + ' ' + self.form.format(self.getSymbol(self.loc, toTA=False), extended, self.mnemonic,
                                              self.getSymbol(ta.dec, inDirect, immidiate, index, toTA=True), immidiate,
                                              inDirect,
                                              sign,
                                              abs(operand),
                                              pc, base, index)

        f = ' ' * (60 - len(out))
        return out + f + ' = ' + self.ta(ta)

    def signedDisp(self):
        if isExtendedInstr(self.instr):
            return decToInt(getDisp(self.instr),20,signed=True)
        return  decToInt(getDisp(self.instr),12,signed=True)
    
    def ta(self, ta):
        mode = ['', '']
        if isDirectInstr(self.instr) or isSicInstr(self.instr):
            mode = ['(', ')']
        if isIndirectInstr(self.instr):
            mode = ['((', '))']
        if isImidiateInstr(self.instr):
            mode = ['', '']
        return f'{mode[0]}0x{ta.dec:X}{mode[1]}'


def createInstruction(cu: CU, loc: int, instr: bytearray, symtab: SYMTAB = None, datatab=None, isData=False):
    if isData:
        if datatab[loc][1] == 'w':
            return Word(cu, loc, instr, datatab[loc][1], symtab)
        if datatab[loc][1] == 'b':
            return Byte(cu, loc, instr, datatab[loc][1], symtab)
        if datatab[loc][1] == 'f':
            return Floa(cu, loc, instr, datatab[loc][1], symtab)
        return Byte(cu, loc, instr, datatab[loc][1], symtab)
    if opcodes[getopcode(instr)]['F'] == F1:
        return InstructionF1(cu, loc, instr, symtab)
    if opcodes[getopcode(instr)]['F'] == F2r:
        return InstructionF2r(cu, loc, instr, symtab)
    if opcodes[getopcode(instr)]['F'] == F2n:
        return InstructionF2n(cu, loc, instr, symtab)
    if opcodes[getopcode(instr)]['F'] == F2rn:
        return InstructionF2rn(cu, loc, instr, symtab)
    if opcodes[getopcode(instr)]['F'] == F2rr:
        return InstructionF2rr(cu, loc, instr, symtab)
    if opcodes[getopcode(instr)]['F'] == F3:
        return InstructionF3(cu, loc, instr, symtab)
    if opcodes[getopcode(instr)]['F'] == F3m:
        return InstructionF3m(cu, loc, instr, symtab)
    return Instruction(cu, loc, instr, symtab)


def getInstructions(cu: CU, symtab: SYMTAB = None, rang=None, datatab=None):
    instructions = []
    rang = (0, len(cu.mem) / 4) if rang is None else rang
    pc = rang[0]
    while pc < rang[1]:
        i = getInstruction(pc, cu, symtab, datatab=datatab)
        instructions.append(i)
        pc += len(i.instr)
    return instructions


def getInstruction(pc, cu: CU, symtab: SYMTAB = None, datatab=None):
    instr = cu.mem.get(pc, 2, asbytearr=True)
    length = getFormat(instr)

    isData = False
    if datatab is not None:
        if pc in datatab:
            length = datatab[pc][0]
            isData = True
    return createInstruction(cu, pc, cu.mem.get(int(pc), length, asbytearr=True), symtab, datatab, isData)


class Disasembler:
    def __init__(self, cu: CU, br: BreakPoint, symtab: SYMTAB = None, rang=None, datatab=None):
        self.instructions = getInstructions(cu, symtab, rang, datatab)
        self.cu = cu
        self.br = br
        self.symtab = symtab
        self.datatab = datatab

    def disas(self, rang=None):
        self.instructions = getInstructions(self.cu, self.symtab, rang, datatab=self.datatab)

    def __str__(self):
        string = f'{" ":<2}{"ADDR":<7}\t{"HEXCODE":<15} {"OPCODE":<2}\t{"MODE":<7}{"LABEL":<15}{"MNEMON":<9}{"OPERAND":15}{"TA"}\n\n'
        # "{:<1}{:<6} {}{}0x{:x}{}{}{:>2}    \t{}"
        for instr in self.instructions:
            pc = self.cu.registers[SICXE_NUM_REGISTER_PC].get(False)
            string += f"{'>' if pc == instr.loc else '*' if instr.loc in self.br else ' '} {instr}\n"
        return string


def isExpression(token):
    for c in token:
        if not (c == '+' or c == '-' or c == '*' or c == '/' or c == '%' or c == '(' or c == ')' or  c == '[' or c == ']' or c == '.' or c.isalnum()):
            return False
    index = max(token.find('+'), token.find('-'), token.find('*'), token.find('/'), token.find('%'))
    return index != -1 and index != 0
