from typing import List

from asm import SYMTAB
from debug.command.exprcommand import ExprCommand
from debug.utildubug import stringToReg, stringToInt
from debug.breakpoint import BreakPoint
from debug.command.breakcommand import Break
from debug.command.castcommand import DecToBase, DecToChar, DecToSignedWord, DecToUnsignedWord, DecToFloat, DecToInstr, \
    AddrToCharPoint, AddrToWordPoint, AddrToFloatPoint
from debug.command.command import Command
from debug.command.disascommand import Disas
from debug.command.nextcommand import Run, Nexti, Step
from debug.command.numbercommand import Number, StringToNum
from debug.command.printcommand import PrintCommand, PrintRegisters, PrintMemory, PrintHelp
from debug.command.registercommand import getRegisterVal, getMemoryVal
from debug.command.setcommand import SetRegister, SetCC, SetCH, Save, Read, Load
from debug.disas import Disasembler
from util import infixToPostfix, infixToPostfixx
from vm import CU


class Builder:
    def __init__(self):
        self.stack: List[Command] = []

    def buildNumber(self, num):
        n = Number(num)
        self.stack.append(n)

    def buildStringToNum(self, string):
        sn = StringToNum(string)
        self.stack.append(sn)

    def buildRun(self, cu: CU, bp: BreakPoint, show=False, symtab=None, datatab=None):
        ms = self.stack.pop() if len(self.stack) > 0 else None
        r = Run(cu, bp, ms, show,symtab,datatab)
        self.stack.append(r)

    def buildNexti(self, cu: CU, bp: BreakPoint, show=False, symtab=None, datatab=None):
        num = self.stack.pop() if len(self.stack) > 0 else None
        n = Nexti(cu, bp, num, show, symtab, datatab)
        self.stack.append(n)

    def buildStep(self, cu: CU, bp: BreakPoint, show=False, symtab=None, datatab=None):
        num = self.stack.pop() if len(self.stack) > 0 else None
        n = Step(cu, bp, num, show, symtab, datatab)
        self.stack.append(n)

    def buildBreak(self, bp: BreakPoint):
        addr = self.stack.pop() if len(self.stack) > 0 else None
        b = Break(bp, addr)
        self.stack.append(b)

    def buildDisas(self, dis: Disasembler):
        start = self.stack.pop() if len(self.stack) > 0 else None
        end = self.stack.pop() if len(self.stack) > 0 else None
        d = Disas(dis, start, end)
        self.stack.append(d)

    def buildPrint(self):
        if len(self.stack) == 0:
            raise Exception('no value specified')
        string = self.stack.pop()
        p = PrintCommand(string)
        self.stack.append(p)

    def buildPrintRegisters(self, cu: CU):
        pr = PrintRegisters(cu)
        self.stack.append(pr)

    def buildPrintMemorys(self, cu: CU):
        start = self.stack.pop() if len(self.stack) > 0 else None
        end = self.stack.pop() if len(self.stack) > 0 else None
        pm = PrintMemory(cu, start, end)
        self.stack.append(pm)

    def buildRegisterVal(self, cu: CU, num=None):
        if num is None:
            num = self.stack.pop() if len(self.stack) > 0 else None
        gr = getRegisterVal(cu, num)
        self.stack.append(gr)

    def buildMemoryVal(self, cu: CU):
        loc = self.stack.pop() if len(self.stack) > 0 else None
        nbyte = self.stack.pop() if len(self.stack) > 0 else None
        mv = getMemoryVal(cu, loc, nbyte)
        self.stack.append(mv)

    def buildDecToBase(self, mode='hex'):
        num = self.stack.pop() if len(self.stack) > 0 else None
        tb = DecToBase(num, mode)
        self.stack.append(tb)

    def buildDecToChar(self):
        num = self.stack.pop() if len(self.stack) > 0 else None
        d = DecToChar(num)
        self.stack.append(d)

    def buildDecToCharPoint(self, cu: CU):
        num = self.stack.pop() if len(self.stack) > 0 else None
        d = AddrToCharPoint(cu, num)
        self.stack.append(d)

    def buildSignedWord(self):
        num = self.stack.pop() if len(self.stack) > 0 else None
        d = DecToSignedWord(num)
        self.stack.append(d)

    def buildWordPoint(self, cu: CU, signed):
        addr = self.stack.pop() if len(self.stack) > 0 else None
        length = self.stack.pop() if len(self.stack) > 0 else None
        d = AddrToWordPoint(cu, signed, addr, length)
        self.stack.append(d)

    def buildFloatPoint(self, cu: CU):
        addr = self.stack.pop() if len(self.stack) > 0 else None
        length = self.stack.pop() if len(self.stack) > 0 else None
        d = AddrToFloatPoint(cu, addr, length)
        self.stack.append(d)

    def buildUnSignedWord(self):
        num = self.stack.pop() if len(self.stack) > 0 else None
        d = DecToUnsignedWord(num)
        self.stack.append(d)

    def buildDecToFloat(self):
        num = self.stack.pop() if len(self.stack) > 0 else None
        d = DecToFloat(num)
        self.stack.append(d)

    def buildToInstr(self, cu: CU, symtab=None, datatab=None):
        num = self.stack.pop() if len(self.stack) > 0 else None
        d = DecToInstr(cu, num, symtab, datatab)
        self.stack.append(d)

    def buildSet(self):
        rm = self.stack.pop() if len(self.stack) > 0 else None
        val = self.stack.pop() if len(self.stack) > 0 else None
        s = SetRegister(rm, val)
        self.stack.append(s)

    def buildSetCC(self):
        val = self.stack.pop() if len(self.stack) > 0 else None
        cc = SetCC(val)
        self.stack.append(cc)

    def buildSetCH(self):
        val = self.stack.pop() if len(self.stack) > 0 else None
        ch = SetCH(val)
        self.stack.append(ch)

    def buildSum(self, token):
        num1 = self.stack.pop()
        num2 = self.stack.pop()
        c = ExprCommand(token, num1, num2)
        self.stack.append(c)

    def buildHelp(self, command):
        self.stack.append(PrintHelp(command))

    def getCommand(self):
        if len(self.stack) != 1:
            raise Exception('bad statement')
        self.buildPrint()
        return self.stack[0]

    def buildExpr(self, cu: CU, token, symtab: SYMTAB):
        postfix = infixToPostfixx(token)
        for token in postfix:
            if token.lower() in stringToReg:
                self.buildRegisterVal(cu, stringToReg[token.lower()])
            elif token in ('-', '+', '*', '/', '%'):
                self.buildSum(token)
            elif token.lower() in stringToReg:
                self.buildRegisterVal(cu, stringToReg[token.lower()])
            else:
                num = stringToInt(token, symtab)
                self.buildNumber(num) if num is not None \
                    else self.buildStringToNum(token)

    def buildSave(self, cu: CU, file):
        s = Save(cu, file)
        self.stack.append(s)

    def buildRead(self, cu, file):
        r = Read(cu, file)
        self.stack.append(r)

    def buildLoad(self, cu, file):
        r = Load(cu, file)
        self.stack.append(r)
