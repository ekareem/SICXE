from asm.Token import Use, Operator, Label, Directive, Operands, Opcode, Start, Res, Word, Byte, Float, Ltorg, Equ, \
    Base, NoBase, Format2r, Format2rr, Format3, Format3m, End, Extdef, Extref, Operand
from asm.mnemonics import OPCODE, DIRECTIVE
import util


def createLabel(token: str, line: 'Line'):
    label = Label(token, line)
    return label


###########################################
def createOperator(token: str, line: 'Line'):
    operator = None
    if token.strip().find('RES') == 0:
        operator = createRes(token, line)
    elif token.strip() == 'USE':
        operator = Use(token, line)
    elif token.strip() == 'START':
        operator = Start(token, line)
    elif token.strip() == 'BYTE':
        operator = Byte(token, line)
    elif token.strip() == 'WORD':
        operator = Word(token, line)
    elif token.strip() == 'FLOA':
        operator = Float(token, line)
    elif token.strip() == 'LTORG':
        operator = Ltorg(token, line)
    elif token.strip() == 'EQU':
        operator = Equ(token, line)
    elif token.strip() == 'BASE':
        operator = Base(token, line)
    elif token.strip() == 'NOBASE':
        operator = NoBase(token, line)
    elif token.strip() == 'END':
        operator = End(token, line)
    elif token.strip() == 'EXTDEF':
        operator = Extdef(token, line)
    elif token.strip() == 'EXTREF':
        operator = Extref(token, line)
    elif token.strip().replace('+', '') in OPCODE:
        operator = createOpcode(token, line)
    elif token.strip() in DIRECTIVE:
        operator = Directive(token, line)
    else:
        operator = Operator(token, line)
    return operator


def createRes(token: str, line: 'Line'):
    if token.strip() == 'RESW':
        return Res(token, line, 3)
    if token.strip() == 'RESB':
        return Res(token, line, 1)
    if token.strip() == 'RESF':
        return Res(token, line, 6)


def createOpcode(token: str, line: 'Line'):
    stoken = token.replace('+', '')
    F = util.opcodes[util.stringToOpcode(stoken)]['F']
    if F == util.F2n or F == util.F2r:
        return Format2r(token, line)
    if F == util.F2rn or F == util.F2rr:
        return Format2rr(token, line)
    if F == util.F3:
        return Format3(token, line)
    if F == util.F3m:
        return Format3m(token, line)
    return Opcode(token, line)


############################################
def createOperands(token: str, line: 'Line'):
    operands = Operands(token, line)
    return operands


def createOperand(token: str, line: 'Line'):
    operand = Operand(token, line)
    return operand
