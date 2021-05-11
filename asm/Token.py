import math
from typing import List

from asm.code import codeF1, codeF2, codeF3
from asm.mnemonics import OPCODE, DIRECTIVE
from asm.storage import Symbol, Literal
from asm.lexutil import LOCAL, getHead, toNumber, isdigit, isExpression, isFloat
from util import intToBytearray, tokenize, isMul, infixToPostfixx, floatToBytearray, SICFLOAT, \
    SICXE_SIZE_BIT_EXPONENT, SICXE_SIZE_BIT_MANTISSA


class Token:
    def __init__(self, token: str, line: 'Line'):
        self.token = token
        self.line = line

    def onCreate(self, create=True):
        pass

    def passOneExecute(self):
        pass

    def passTwoExecute(self):
        pass

    def passThreeExecute(self):
        pass

    def execute(self, nbits, asbyte):
        symtab = self.line.block.section.symtab
        if self.token in symtab:
            return symtab[self.token].getAddr()
        return toNumber(self.token, nbits, asbyte)

    def __str__(self):
        return self.token


class Label(Token):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def onCreate(self, create=True):
        super(Label, self).onCreate()
        if self.token in OPCODE or self.token in DIRECTIVE:
            raise Exception(f'{self.token} is a used key word')
        self.line.block.section.symtab[self.token] = Symbol(LOCAL, self.token)

    def passOneExecute(self):
        super().passOneExecute()
        symbol = self.line.block.section.symtab[self.token]
        symbol.addr = self.line.addr if symbol.addr is None else symbol.addr

    def passTwoExecute(self):
        super().passTwoExecute()


class Operator(Token):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def onCreate(self, create=True):
        if self.line.operands is not None:
            self.line.operands.onCreate(create)

    def length(self):
        return 0

    def base(self):
        pass

    def nobase(self):
        pass

    def passTwoExecute(self):
        self.line.code = self.getObjectCode(None)

    def getObjectCode(self, toInt=False):
        return bytearray() if toInt is None else 0 if toInt else ''


class Opcode(Operator):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)
        self.opcode = OPCODE[self.token.replace('+', '')]['opcode']

    def isExtended(self):
        return OPCODE[self.token.replace('+', '')]['format'] == 3 and self.token.find('+') == 0

    def length(self):
        extend = 1 if self.isExtended() else 0
        # print(self.token, OPCODE[self.token.replace('+', '')]['format'], extend)
        return OPCODE[self.token.replace('+', '')]['format'] + extend

    def getObjectCode(self, toInt=False):
        return codeF1(self.opcode, toInt)


class Format2r(Opcode):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)
        self.r1 = 0
        self.r2 = 0

    def getObjectCode(self, toInt=False):
        operands = self.line.operands.operands
        self.r1 = operands[0].execute(8, False)
        return codeF2(self.opcode, self.r1, self.r2, toInt)


class Format2rr(Opcode):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)
        self.r1 = 0
        self.r2 = 0

    def getObjectCode(self, toInt=False):
        operands = self.line.operands.operands
        self.r1 = operands[0].execute(8, False)
        self.r2 = operands[1].execute(8, False)
        token = operands[0].token

        if self.r1 is None or self.r2 is None:
            objectCode = self.line.block.section.objectCode
            objectCode.setmod(token.replace('#', '').replace('@', ''), self.line.addr + 1, 1)
        return codeF2(self.opcode, self.r1, self.r2, toInt)


class Format3m(Opcode):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)
        self.mode = 0b11
        self.x = 0
        self.b = 0
        self.p = 1
        self.e = 0

    def base(self):
        self.b = 1
        self.p = 0

    def nobase(self):
        self.b = 0
        self.p = 1

    def getObjectCode(self, toInt=False):
        operands = self.line.operands.operands
        pc = self.line.block.getLineAddr(self.line) + self.line.length()
        ta = operands[0].execute(24, False)
        token = operands[0].token

        base = self.line.block.section.base

        mode = self.getmode(token)
        if mode == 0b01: self.p = 0
        if len(operands) == 2:
            x = operands[1].execute(8, False)
            self.x = 1 if x == 1 else self.x

        self.e = 1 if self.token.find('+') == 0 else self.e
        if ta is None:
            objectCode = self.line.block.section.objectCode
            objectCode.setmod(token.replace('#', '').replace('@', ''), self.line.addr + 1, 3 if self.e == 0 else 5)

        return codeF3(pc, base, ta, self.opcode, mode, self.x, self.b, self.p, self.e, toInt)

    def getmode(self, token):
        if token.find("#") == 0:
            return 0b01
        if token.find("@") == 0:
            return 0b10
        return 0b11


class Format3(Opcode):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)
        self.x = 0
        self.b = 0
        self.p = 0
        self.e = 0

    def base(self):
        self.b = 1

    def nobase(self):
        self.b = 0

    def getObjectCode(self, toInt=False):
        pc = self.line.block.getLineAddr(self.line) + self.line.length()
        ta = None
        base = self.line.block.section.base
        self.e = 1 if self.token.find('+') == 0 else self.e
        return codeF3(pc, base, ta, self.opcode, 0b11, self.x, self.b, self.p, self.e, toInt)

    def getmode(self, token):
        if token.find("#") == 0:
            return 0b01
        if token.find("@") == 0:
            return 0b10
        return 0b11


class Directive(Operator):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)


class Operand(Token):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def onCreate(self, create=True):
        super(Operand, self).onCreate()

        if self.token.replace('=', '') in OPCODE or self.token.replace('=', '') in DIRECTIVE:
            raise Exception(f'{self.token} is a used key word')

        if self.token.replace("#", '').replace("@", '').find('=') == 0:
            self.line.block.section.littab[self.token] = Literal(self.token, value=self.token.replace("=", ''))
        elif len(self.token) > 0 and self.token[:1].isalpha() and self.token.isalnum():
            self.line.block.section.symtab[self.token] = Symbol(LOCAL, self.token)

    def execute(self, nbits, asbyte, asFloat=False):

        symtab = self.line.block.section.symtab
        token = self.token.replace("#", '')
        token = token.replace("@", '')
        if token == '*':
            return self.line.addr
        if token in symtab.table:
            if asbyte:
                if asFloat:
                    return floatToBytearray(float(symtab[token].getAddr()), SICXE_SIZE_BIT_EXPONENT,
                                            SICXE_SIZE_BIT_MANTISSA)
                return toNumber(str(symtab[token].getAddr()), nbits, asbyte)
            return symtab[token].getAddr()
        # print(self.line.label.token, self.line.operator.token, self.token)
        # print(token,nbits,asbyte)
        n = token
        if asFloat and isdigit(token):
            n = toNumber(token, nbits, False)
        if asFloat and asbyte:
            return floatToBytearray(float(n), SICXE_SIZE_BIT_EXPONENT, SICXE_SIZE_BIT_MANTISSA)
        if asFloat:
            return float(n)
        return toNumber(token, nbits, asbyte)

    def length(self):
        symtab = self.line.block.section.symtab
        if self.token in symtab:
            symbol = symtab[self.token]
            return symbol.addr if symbol.addr is not None else 0
        return 0


class Operands(Token):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)
        self.operands: List[Operand] = []

    def onCreate(self, create=True):
        super(Operands, self).onCreate()
        for token in tokenize(self.token, (",",)):
            # token = token.replace("#", '')
            # token = token.replace("@", '')
            # index = max(token.find('+'), token.find('-'))
            # if index != -1 and index != 0:
            if isExpression(token):
                o = Expr(token, self.line)
            else:
                o = Operand(token, self.line)
            if create:
                o.onCreate()
            self.operands.append(o)

    def execute(self, nbits, asbyte):
        nums = []
        for operand in self.operands:
            nums.append(operand.execute(nbits, asbyte))
        return nums

    def __getitem__(self, item: int) -> Operand:
        return self.operands[item]

    def __setitem__(self, key: int, value: Operand):
        self.operands[key] = value

    def __len__(self):
        len(self.operands)

    def __str__(self):
        return self.token


class Expr(Operand):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def onCreate(self, create=True):
        postfix = infixToPostfixx(self.token.replace('#', '').replace('@', ''))

        for token in postfix:
            if len(token) > 0 and token.isalnum() and not isdigit(token, None):
                self.line.block.section.symtab[token] = Symbol(LOCAL, self.token)

    def execute(self, nbits, asbyte, asFloat=False):
        postfix = infixToPostfixx(self.token.replace('#', '').replace('@', ''))
        stack = []
        hasNone = False
        for i, token in enumerate(postfix):
            if token == 'NUMaLLLoRRR':
                stack.append((token, toNumber(str(self.line.addr), 24, False)))
            elif token.isalnum() or isFloat(token):
                if isdigit(token, None):
                    stack.append((token, toNumber(token, 24, False)))
                elif isFloat(token):
                    stack.append((token, SICFLOAT(float(token), True)))
                elif token.isalnum():
                    stack.append((token, self.line.block.section.symtab[token].addr))

            if token in ('+', '-', '*', '/', '%'):
                num = stack.pop()
                num1 = num[1] if type(num) == tuple else num

                if num1 is None:
                    objectCode = self.line.block.section.objectCode
                    objectCode.setmod(num[0], self.line.addr, 6, token)
                    hasNone = True

                num = stack.pop()
                num2 = num[1] if type(num) == tuple else num
                if num2 is None:
                    objectCode = self.line.block.section.objectCode
                    objectCode.setmod(num[0], self.line.addr, 6, token)
                    hasNone = True
                if token == '+':
                    sum = 0 if num1 is None or num2 is None else (num2 + num1)
                    stack.append(sum)
                if token == '-':
                    sum = 0 if num1 is None or num2 is None else (num2 - num1)
                    stack.append(sum)
                if token == '*':
                    sum = 0 if num1 is None or num2 is None else (num2 * num1)
                    stack.append(sum)
                if token == '/':
                    sum = 0 if num1 is None or num2 is None else (num2 / num1)
                    stack.append(sum)
                if token == '%':
                    sum = 0 if num1 is None or num2 is None else (num2 % num1)
                    stack.append(sum)
        if asbyte:
            if asFloat:
                return floatToBytearray(float(stack[0]), SICXE_SIZE_BIT_EXPONENT, SICXE_SIZE_BIT_MANTISSA)
            else:
                nbyte = math.ceil(nbits / 8)
                return intToBytearray(int(stack[0]), nbyte) if not hasNone else bytearray(nbyte)
        return int(stack[0]) if not hasNone and not asFloat else float(stack[0]) if asFloat else 0


class Use(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def onCreate(self, create=True):
        super(Use, self).onCreate(False)
        operands = self.line.operands
        operand = ''
        if operands is None or len(operands.operands) == 0:
            operand = 'MAIN'
        else:
            operand = operands.operands[0].token

        self.line.block.section.setblock(operand)


class Start(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def onCreate(self, create=True):
        super().onCreate()
        operands = self.line.operands
        operand = 0

        if operands is None or len(operands.operands) == 0:
            operand = 0
        else:
            operand = operands.operands[0].execute(24, False)

        if self.line.label is not None:
            self.line.block.section.name = self.line.label.token

        self.line.block.section.start = operand
        headblock: 'Block' = getHead(self.line.block)
        self.line.block.section.block.start = operand
        headblock.start = operand


class Res(Directive):
    def __init__(self, token: str, line: 'Line', nbyte: int):
        super().__init__(token, line)
        self.nbyte = nbyte

    def length(self):
        operands = self.line.operands
        operand = 0
        if operands is None or len(operands.operands) == 0:
            operand = 0
        else:
            operand = operands.operands[0].execute(24, False)
        # print(self.line.label.token,self.token,type(operands[0]), operands[0].token)
        return operand * self.nbyte


class Byte(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def length(self):
        operands = self.line.operands
        operand = 0
        if operands is None or len(operands.operands) != 1:
            operand = bytearray()
        else:
            operand = operands.operands[0].execute(8, True)
        return len(operand) * 1

    def getObjectCode(self, toInt=None):
        operands = self.line.operands
        operand = 0
        if operands is None or len(operands.operands) != 1:
            operand = bytearray()
        else:
            operand = operands.operands[0].execute(8, True)
        return operand


class Word(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def length(self):
        operands = self.line.operands
        if operands is None or len(operands.operands) != 1:
            raise Exception('missing operand')
        # operand = operands.operands[0].execute(24, False)
        return 3

    def getObjectCode(self, toInt=None):
        operands = self.line.operands
        if operands is None or len(operands.operands) != 1:
            raise Exception('missing operand')
        byte = operands.operands[0].execute(24, True)
        return byte if byte is not None else bytearray(3)


class Float(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def length(self):
        operands = self.line.operands
        if operands is None or len(operands.operands) != 1:
            raise Exception('missing operand')
        # operand = operands.operands[0].execute(48, True)
        return 6

    def getObjectCode(self, toInt=False):
        operands = self.line.operands
        if operands is None or len(operands.operands) != 1:
            raise Exception('missing operand')
        return operands.operands[0].execute(48, True, asFloat=True)


class Ltorg(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def onCreate(self, create=True):
        super().onCreate()
        self.line.block.section.createLineFromLittab()


class End(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def passTwoExecute(self):
        first = self.line.operands.operands[0].execute(24, False)
        self.line.block.section.firstExeAddr = first if first is not None else 0


class Base(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def passTwoExecute(self):
        baseVal = self.line.operands.operands[0].execute(24, False)
        self.line.block.section.base = baseVal
        if self.line.child is not None:
            self.line.child.operator.base()


class NoBase(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def passTwoExecute(self):
        self.line.block.section.base = 0
        if self.line.child is not None:
            self.line.child.operator.nobase()


class Equ(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def passOneExecute(self):
        super().passOneExecute()
        symbol = self.line.block.section.symtab[self.line.label.token]
        val = self.line.operands.operands[0].execute(24, False)
        symbol.addr = val
        symbol.value = val


class Extdef(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def passThreeExecute(self):
        super(Extdef, self).passOneExecute()
        objectCode = self.line.block.section.objectCode
        operands = self.line.operands.operands
        for operand in operands:
            objectCode.setdef(operand.token, operand.execute(24, False))


class Extref(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)

    def passThreeExecute(self):
        super(Extref, self).passOneExecute()
        objectCode = self.line.block.section.objectCode
        operands = self.line.operands.operands
        for operand in operands:
            objectCode.setRef(operand.token)


class Macro(Directive):
    def __init__(self, token: str, line: 'Line'):
        super().__init__(token, line)
        self.line: 'Line' = None
