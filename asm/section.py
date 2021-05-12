from typing import Dict

from asm.storage import Symbol, CONST

from asm.Line import Line
from asm.block import Block
from asm.table import SYMTAB, LITTAB, BLOCTAB
from asm.lexutil import getTail, LOCAL, isdigit, isFloat, isExpression
from loader.objectCode import ObjectCode


class Section:
    def __init__(self, name):
        self.name = name
        self.objectCode = ObjectCode()
        self.objectCode.setHeaderName(name)
        self.start = 0
        self.firstExeAddr = 0
        self.base = 0
        self.symtab = SYMTAB()
        self.littab = LITTAB()
        self.bloctab = BLOCTAB()
        self.block: Block = None
        self.line: Line = None
        self.currentBlock: Block = None
        self.currentLine: Line = None
        self.datum: Dict[int, str] = {}
        self.onCreate()

    def programLength(self):
        return self.line.lengthAll()

    def onCreate(self):
        self.symtab['A'] = Symbol(LOCAL, 'A', 0, 0, CONST)
        self.symtab['X'] = Symbol(LOCAL, 'X', 1, 1, CONST)
        self.symtab['L'] = Symbol(LOCAL, 'L', 2, 2, CONST)
        self.symtab['P'] = Symbol(LOCAL, 'P', 8, 8, CONST)
        self.symtab['SW'] = Symbol(LOCAL, 'SW', 9, 9, CONST)
        self.symtab['B'] = Symbol(LOCAL, 'B', 3, 3, CONST)
        self.symtab['S'] = Symbol(LOCAL, 'S', 4, 4, CONST)
        self.symtab['T'] = Symbol(LOCAL, 'T', 5, 5, CONST)
        self.symtab['F'] = Symbol(LOCAL, 'F', 6, 6, CONST)

    def setblock(self, id: str):
        if id not in self.bloctab.table:
            b = Block(id, section=self)
            if self.block is None:
                self.block = b
            else:
                tail: Block = getTail(self.block)
                tail.child = b
                b.parent = tail

            self.currentBlock = b
            self.bloctab[id] = b
        else:
            self.currentBlock = self.bloctab[id]
        return self.currentBlock

    def createLine(self, label: str, operator: str, operand: str):
        l = Line(label, operator, operand, self.currentBlock)
        if self.line is None:
            self.line = l
        else:
            tail: Line = getTail(self.line)
            tail.child = l
            l.parent = tail
        l.onCreate()
        return l

    def createLineFromLittab(self):
        littab = self.littab.table
        for lit in littab:
            if isFloat(littab[lit].value):
                self.createLine(lit, 'FLOA', littab[lit].value)
            elif isdigit(littab[lit].value) or isExpression(littab[lit].value) or littab[lit].value.isalnum():
                self.createLine(lit, 'WORD', littab[lit].value)
            else:
                self.createLine(lit, 'BYTE', littab[lit].value)
        littab.clear()

    def passOneExecute(self):
        l = self.line
        while l is not None:
            l.passOneExecute()
            l = l.child

    def passTwoExecute(self):
        l = self.line
        while l is not None:
            l.passTwoExecute()
            l = l.child

    def passThreeExecute(self):
        l = self.line
        while l is not None:
            l.passThreeExecute()
            l = l.child

    def createObjectCode(self):
        l = self.line
        self.objectCode.setHeaderName(self.name)
        while l is not None:
            self.objectCode.addTextFromByteArray(l.addr, l.code)
            l = l.child
        self.objectCode.e.first(self.firstExeAddr)

    def __str__(self):
        return f"""symtab
{self.symtab.toString()}
littab
{str(self.littab)}
bloctab
{str(self.bloctab)}
{str(self.line.toStr())}
"""
