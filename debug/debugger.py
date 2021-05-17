from typing import List, Dict

from asm import SYMTAB
from debug.breakpoint import BreakPoint
from debug.builder import Builder
import debug.command.token as tk
from debug.disas import Disasembler, isExpression
from debug.utildubug import stringToReg, stringToInt
from util import tokenize
from vm import CU
from vm.presistance import MEMORYFILE


class Debugger:
    def __init__(self, cu: CU, symtab: SYMTAB = None, datatab: Dict[int, List] = None):
        self.builder = Builder()
        self.bp = BreakPoint()
        self.cu = cu
        self.dis = Disasembler(self.cu, self.bp, symtab, datatab=datatab)
        self.symtab = symtab
        self.datatab = datatab

    def evaluate(self, statement: str):

        tokens = tokenize(statement)
        self.parse(tokens)
        return self.builder.getCommand()

    def parse(self, tokens: List[str]):
        self.builder.stack.clear()
        if tokens[0].lower() in tk.READ:
            file = MEMORYFILE if len(tokens) < 2 else tokens[1]
            self.builder.buildRead(self.cu, file)
        elif tokens[0].lower() in tk.SAVE:
            file = MEMORYFILE if len(tokens) < 2 else tokens[1]
            self.builder.buildSave(self.cu, file)
        elif tokens[0].lower() in tk.HELP:
            self.builder.buildHelp(tokens[1] if len(tokens) > 1 else None)
        elif tokens[0].lower() in tk.LOAD:
            if len(tokens) < 2:
                raise Exception('requires object file')
            file = tokens[1]
            self.builder.buildLoad(self.cu, file)
        else:
            for token in reversed(tokens):
                if token.lower() in tk.RUN:
                    self.builder.buildRun(self.cu, self.bp)
                elif token.lower() in tk.RUNI:
                    self.builder.buildRun(self.cu, self.bp, True, self.symtab, self.datatab)
                elif token.lower() in stringToReg:
                    self.builder.buildRegisterVal(self.cu, stringToReg[token.lower()])
                elif token.lower() in tk.NEXT:
                    self.builder.buildNexti(self.cu, self.bp)
                elif token.lower() in tk.NEXTI:
                    self.builder.buildNexti(self.cu, self.bp, True, self.symtab, self.datatab)
                elif token.lower() in tk.STEP:
                    self.builder.buildStep(self.cu, self.bp)
                elif token.lower() in tk.STEPI:
                    self.builder.buildStep(self.cu, self.bp, True, self.symtab, self.datatab)
                elif token.lower() in tk.BREAK:
                    self.builder.buildBreak(self.bp)
                elif token.lower() in tk.BREAK:
                    self.builder.buildBreak(self.bp)
                elif token.lower() in tk.DISAS:
                    self.builder.buildDisas(self.dis)
                elif token.lower() in tk.PRINT:
                    self.builder.buildPrint()
                elif token.lower() in tk.PRINTRRGISTERS:
                    self.builder.buildPrintRegisters(self.cu)
                elif token.lower() in tk.PRINTMEMORYS:
                    self.builder.buildPrintMemorys(self.cu)
                elif token.lower() in tk.REGISTER:
                    self.builder.buildRegisterVal(self.cu)
                elif token.lower() in tk.MEMORY:
                    self.builder.buildMemoryVal(self.cu)
                elif token.lower() in tk.TOBASE:
                    self.builder.buildDecToBase(token.lower())
                elif token.lower() in tk.TOCHAR:
                    self.builder.buildDecToChar()
                elif token.lower() in tk.TOCHARPOINT:
                    self.builder.buildDecToCharPoint(self.cu)
                elif token.lower() in tk.TOSIGNEDWORD:
                    self.builder.buildSignedWord()
                elif token.lower() in tk.TOSIGNEDWORDPOINT:
                    self.builder.buildWordPoint(self.cu, True)
                elif token.lower() in tk.TOUNSIGNEDWORDPOINT:
                    self.builder.buildWordPoint(self.cu, False)
                elif token.lower() in tk.TOFLOATPOINT:
                    self.builder.buildFloatPoint(self.cu)
                elif token.lower() in tk.TOFLOAT:
                    self.builder.buildDecToFloat()
                elif token.lower() in tk.TOINSTRUCTION:
                    self.builder.buildToInstr(self.cu, self.symtab, self.datatab)
                elif token.lower() in tk.SET:
                    self.builder.buildSet()
                elif token.lower() in tk.SETCC:
                    self.builder.buildSetCC()
                elif token.lower() in tk.SETCH:
                    self.builder.buildSetCH()
                elif isExpression(token):
                    self.builder.buildExpr(self.cu, token, self.symtab)
                else:
                    num = stringToInt(token, self.symtab)
                    self.builder.buildNumber(num) if num is not None \
                        else self.builder.buildStringToNum(token)

# def debug(file: str, isAsm=False):
#     b = BUS()
#
#     if isAsm:
#         obj = assemble(file, asClass=True)
#         load(b.cu, None, objectCode=obj)
#     else:
#         load(b.cu, file)
#
#     d = Debugger(b.cu)
#     n = ''
#     while n != 'exit':
#         try:
#             n = input(':>')
#             c = d.evaluate(n)
#             c.execute()
#         except BaseException as e:
#             print(e)
#
#
# def run(file: str, isAsm=False):
#     b = BUS()
#
#     if isAsm:
#         obj = assemble(file, asClass=True)
#         load(b.cu, None, objectCode=obj)
#     else:
#         load(b.cu, file)
#
#     d = Debugger(b.cu)
#     d.evaluate('run').execute()
