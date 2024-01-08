from typing import List

from asm.lexer import Lines
from asm.section import Section


class Program:
    def __init__(self):
        pass
        self.sections: List[Section] = []

    def parse(self, file):
        l = Lines(file)
        s = Section('test')
        s.setblock('MAIN')
        self.sections.append(s)
        for line in l.lines:
            if line.operator() == 'CSECT':
                s.createLineFromLittab()
                s = Section(str(line.label()))
                s.setblock('MAIN')
                self.sections.append(s)
            s.createLine(line.label(), line.operator(), line.operand())
        s.createLineFromLittab()

    def execute(self):
        for s in self.sections:
            s.passOneExecute()
            s.passTwoExecute()
            s.passThreeExecute()
            s.createObjectCode()
            # print(s.symtab)
            # print(s)

    def writeObj(self, f):
        file = open(f, "w+")
        file.write(self.getObjectCode())

    def writeTab(self, f):
        string = ''
        for s in self.sections:
            string += s.symtab.toString() + '\n\n'

        file = open(f, "w+")
        file.write(string)

    def writeCode(self, f):
        string = ''
        for s in self.sections:
            if s.line is not None:
                string += s.line.toStr()

        file = open(f, "w+")
        file.write(string)

    def getObjectCode(self):
        string = ''
        for s in self.sections:
            string += str(s.objectCode) + '\n'
        return string


# def assemble(f: str, obj=None, tab=None, cod=None, asClass=False):
#     if f.find('.') != -1:
#         f = f[:f.find('.')]
#
#     p = Program()
#     p.parse(f + '.asm')
#     p.execute()
#     if asClass:
#         return p.sections[0].objectCode
#
#     obj = f + '.obj' if obj is None else obj
#     p.writeObj(obj)
#     tab = f + '.tab' if tab is None else tab
#     p.writeTab(tab)
#     cod = f + '.cod' if cod is None else cod
#     p.writeCode(cod)
#     return [obj, tab, cod]
#
#
