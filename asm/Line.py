from asm.Token import Label, Operator, Operands
from asm.block import Block
from asm.lexutil import getHead
from asm.factory import createLabel, createOperator, createOperands
from util import bytearrayToInt


class Line:
    def __init__(self, label: str,
                 operator: str,
                 operand: str,
                 block: 'Block',
                 addr: int = None,
                 parent: 'Line' = None,
                 child: 'Line' = None):
        self.block: 'Block' = block
        self.label: Label = createLabel(label, self) if label != '' or label is None else None
        self.operands: Operands = createOperands(operand, self) if operand != '' or operand is None else None
        self.operator: Operator = createOperator(operator, self) if operator != '' or operator is None else None
        self.block.lines.append(self)
        self.addr = addr
        self.parent = parent
        self.child = child
        self.code: bytearray = bytearray()

    def length(self):
        return self.operator.length()

    def lengthAll(self):
        length = 0
        l: 'Line' = getHead(self)
        while l is not None:
            length += l.length()
            l = l.child
        return length

    def onCreate(self):
        if self.label is not None:
            self.label.onCreate()
        # if self.operands is not None:
        #     self.operands.onCreate()
        if self.operator is not None:
            self.operator.onCreate()

    def passOneExecute(self):
        # print('pass  ',self)
        self.addr = self.block.getLineAddr(self)
        if self.label is not None:
            self.label.passOneExecute()
        if self.operands is not None:
            self.operands.passOneExecute()
        if self.operator is not None:
            self.operator.passOneExecute()

    def passTwoExecute(self):
        self.addr = self.block.getLineAddr(self)
        if self.label is not None:
            self.label.passTwoExecute()
        if self.operator is not None:
            self.operator.passTwoExecute()
        if self.operands is not None:
            self.operands.passTwoExecute()

    def passThreeExecute(self):
        if self.label is not None:
            self.label.passThreeExecute()
        if self.operands is not None:
            self.operands.passThreeExecute()
        if self.operator is not None:
            self.operator.passThreeExecute()

    def toStr(self, all=True):
        string = f'{"block":<10} {"address":0>6}\t{"code":<6}{"":>14}{"label":<10} {"operator":<8} {"operand":<15}\n\n'
        curr = self
        if all:
            while curr is not None:
                string += curr.toString()+ '\n'
                curr = curr.child
        else:
            string += self.toString() + '\n'
        return string

    def toString(self):
        l = len(self.code) * 2
        c = bytearrayToInt(self.code, False)
        f = '{:0>' + str(l) + 'x}'
        g = '{:>' + str(20 - l) + '}' if 20 - l >=0  else '{:>5}'
        return f'{str(self.block.name):<10} {self.addr:0>6x}\t{f.format(c) if len(self.code) > 0 else ""}{g.format("")}{str(self.label if not self.label is None else ""):<10} {str(self.operator):<8} {str(self.operands if not self.operands is None else ""):<15}'

    def __str__(self):
        # l = len(self.code) * 2
        # c = bytearrayToInt(self.code, False)
        # f = '{:0>'+str(l)+'x}'

        return f'{self.addr:0>6x} {str(self.block):<8} {str(self.label):<8} {str(self.operator):<8} {self.operator.length():<4} {str(self.operands):<8} {""} {self.code} '
