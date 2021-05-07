from typing import List, Dict

from asm.mnemonics import DIRECTIVE, OPCODE, SYMBOL_FLAG, OPCODE_FLAG, MACRO
from util import tokenize


def isOperator(operator: str):
    operatorlist = list(operator)
    if len(operatorlist) > 0:
        operatorlist = operatorlist[1:] if operatorlist[0] == '+' else operatorlist
    operator = ''.join(operatorlist)
    return operator in OPCODE or operator in DIRECTIVE or operator in MACRO


def symbolflag(symbol: str):
    if len(symbol) > 0 and symbol[:1] in SYMBOL_FLAG:
        return symbol[:1]
    return ''


def opcodeflag(opcode: str):
    if len(opcode) > 0 and opcode[:1] in OPCODE_FLAG:
        return opcode[:1]
    return ''


class Line:
    def __init__(self, line):
        self.line = line

    def length(self):
        return len(tokenize(self.linewithoutcomment()))

    def asList(self):
        return tokenize(self.linewithoutcomment())

    def hascomment(self):
        return self.line.find(" .") != -1 or self.line.find("\t.") != -1

    def comment(self):
        index = self.line.find(" .")
        if index == -1: index = self.line.find(". ")
        if index == -1: index = self.line.find(".\t")
        if index == -1: index = self.line.find("\t.")
        return self.line[index:] if index != -1 else '\n'

    def linewithoutcomment(self):
        index = self.line.find(" .")
        if index == -1: index = self.line.find(". ")
        if index == -1: index = self.line.find(".\t")
        if index == -1: index = self.line.find("\t.")
        return self.line[:index] if index != -1 else self.line

    def iscommentline(self):
        return self.label() == '' and self.operator() == ''

    def labelindex(self):
        syntaxlist = self.asList()
        if self.length() > 0:
            if not isOperator(syntaxlist[0]):
                return 0
        return -1

    def haslabel(self):
        return self.labelindex() != -1

    def label(self):
        index = self.labelindex()
        if index != -1:
            return self.asList()[index]
        return ''

    def operatorindex(self):
        labelindex = self.labelindex()

        opcodeindex = labelindex + 1
        if opcodeindex < self.length():
            if isOperator(self.asList()[opcodeindex]):
                return opcodeindex
        return -1

    def hasoperator(self):
        return self.operatorindex() != -1

    def operator(self, flag=False):
        index = self.operatorindex()
        if index != -1:
            operatorstr = self.asList()[index]
            if flag and opcodeflag(operatorstr) != '':
                return operatorstr[1:]
            else:
                return operatorstr
        return ''

    def operandindex(self):
        operatorindex = self.operatorindex();
        operandindex = operatorindex + 1
        if operandindex < self.length():
            return operandindex
        return -1

    def hasoperand(self):
        return self.operandindex() != -1

    def isEmpty(self):
        return self.hasoperator() is False

    def operand(self, flag=False):
        index = self.operandindex()
        if index != -1:
            operandstr = self.asList()[index]
            if flag and symbolflag(operandstr) != '':
                return operandstr[1:]
            else:
                return operandstr
        return ''

    def __str__(self):
        return f'{self.label():<10} {self.operator():<10} {self.operand():<10} {self.comment()}\n'

    def __repr__(self):
        return self.__str__()


class Lines:
    def __init__(self, file):
        self.macro = None
        self.file = file
        self.lines: List[Line] = []
        self.mactab: Dict[str, Macro] = {}
        self.unique = []
        self.open()

    def __getitem__(self, index) -> Line:
        return self.lines[index]

    def open(self):
        file = open(self.file, "r")

        for line in file.readlines():
            line = line.replace('\n', '')
            l = Line(line)
            if l.operator() in MACRO:
                self.lines.append(l)
                self.mactab[l.operator()].insertoprands(l.operand(), self)
                continue
            if l.operator() == 'MACRO':
                self.macro = self.mactab[l.label()] = Macro(line, self)
                MACRO.append(l.label())
            elif l.operator() == 'MEND':
                self.macro = None
            elif len(line) > 0 and l.hasoperator():
                if self.macro is not None:
                    self.macro.add(line)
                else:
                    self.lines.append(l)

    def __str__(self):
        string = ''
        for line in self.lines:
            string += str(line)

        return string

    def __repr__(self):
        return self.__str__()


class Macro:
    def __init__(self, header, lines):
        self.header: str = header
        self.body: List[str] = []
        self.args: Dict[str, str] = {}
        self.arguments()
        self.lines: Lines = lines

    def label(self):
        return self.header.split()[1]

    def arguments(self):
        if len(self.header.split()) > 2:
            arguemnt = self.header.split()[2].split(',')

            for arg in arguemnt:
                if arg.find("=") != -1:
                    pair = arg.split("=")
                    self.args[pair[0]] = pair[1]
                else:
                    self.args[arg] = ''

            return self.header.split()[2].split(',')
        return []

    def add(self, line):
        self.body.append(line)

    def insertoprands(self, operands, lines: Lines):
        operands = operands.split(',')
        newunique = []
        for line in self.body:
            copyline = line
            i = 0
            checked = []
            for arg in self.args:
                if getAmper(copyline):
                    for lebel in getAmper(copyline):
                        ul = createuniquelabel(lebel, self.lines.unique)
                        copyline = copyline.replace(lebel, ul)
                        newunique.append(ul)

                if len(operands) > i:
                    if operands[i].find("=") != -1:
                        key = '&' + operands[i].split("=")[0]
                        value = operands[i].split("=")[1]
                        value = self.args[key] if value == '' else value
                        copyline = copyline.replace(key, value)
                        checked.append(key)
                    else:
                        checked.append(arg)
                        copyline = copyline.replace(arg, operands[i])
                i += 1

            for arg in self.args:
                if arg not in checked:
                    copyline = copyline.replace(arg, self.args[arg])

            for i, arg in enumerate(self.arguments()):
                pass
                # copyline = copyline.replace(arg, operands[i])
            lines.lines.append(Line(copyline))
        for u in newunique:
            if u not in self.lines.unique:
                self.lines.unique.append(u)
        newunique.clear()

    def __str__(self):
        # string = self.header
        # for line in self.body:
        #     string += str(line)
        # return string
        return str(self.args)

    def __repr__(self):
        return self.__str__()


def getAmper(lines: str):
    out = []
    for line in tokenize(lines, add=(",", "+", "-", "*", '=')):
        start = line.find("$")
        if start == -1:
            continue
        out.append(line)
    return out


def createuniquelabel(label, uique: List[str]):
    while label in uique:
        label = label.replace('$', '$' + 'A' * 1)
    return label
