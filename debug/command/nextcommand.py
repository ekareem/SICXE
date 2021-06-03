import time
from typing import List

from debug.disas import createInstruction
from debug.breakpoint import BreakPoint
from debug.command.command import Command, UnaryCommand
from util import SICXE_SIZE_MEMORY, JSUB, getopcode, RSUB, getFormat
from vm import CU, SICXE_NUM_REGISTER_PC, SICXE_NUM_REGISTER_L


class Nexti(UnaryCommand):
    def __init__(self, cu: CU, bp: BreakPoint, child: Command, show=False, symtab=None, datatab=None):
        super().__init__(child)
        self.cu = cu
        self.bp = bp
        self.show = show
        self.symtab = symtab
        self.datatab = datatab

    def execute(self, inputs=None):
        num = self.child.execute() if self.child is not None else 1

        pc = self.cu.registers[SICXE_NUM_REGISTER_PC].get(False)
        for i in range(num):
            try:
                i = self.cu.getInstruction()
                if self.show:
                    print('  ' + str(createInstruction(self.cu, int(pc), i, self.symtab, self.datatab)))
                pc = self.cu.registers[SICXE_NUM_REGISTER_PC].get(False)
                self.bp.remove(pc)
                self.cu.run()
            except BaseException as e:
                print(e)

        return None


class Step(UnaryCommand):
    def __init__(self, cu: CU, bp: BreakPoint, child: Command, show=False, symtab=None, datatab=None):
        super().__init__(child)
        self.cu = cu
        self.bp = bp
        self.show = show
        self.symtab = symtab
        self.datatab = datatab

    def execute(self, inputs=None):
        num = self.child.execute() if self.child is not None else 1

        for i in range(num):
            self.step()

        return None

    def step(self):
        inSub = False
        First = True
        retaddr = 0
        while First or inSub:
            instr = self.cu.getInstruction()

            if getopcode(instr) == JSUB and First:
                inSub = True
                retaddr = self.cu.registers[SICXE_NUM_REGISTER_PC].get(False) + getFormat(self.cu.getInstruction())

            if getopcode(instr) == RSUB and self.cu.registers[SICXE_NUM_REGISTER_L].get(False) == retaddr:
                inSub = False

            pc = self.cu.registers[SICXE_NUM_REGISTER_PC].get(False)
            if self.show:
                print('  ' + str(createInstruction(self.cu, int(pc), instr, self.symtab, self.datatab)))
            self.bp.remove(pc)
            try:
                self.cu.run()
            except BaseException as e:
                print(e)
            First = False


class Run(UnaryCommand):
    def __init__(self, cu: CU, bp: BreakPoint, child: Command, show=False, symtab=None, datatab=None):
        super().__init__(child)
        self.cu = cu
        self.bp = bp
        self.show = show
        self.symtab = symtab
        self.datatab = datatab

    def execute(self, inputs=None):
        ms = self.child.execute() if self.child is not None else 0
        pc = self.cu.registers[SICXE_NUM_REGISTER_PC]

        while pc.get() not in self.bp and not self.cu.halted:
            try:
                i = self.cu.getInstruction()
                if self.show:
                    print('  ' + str(createInstruction(self.cu, int(pc), i, self.symtab, self.datatab)))
                self.cu.run(ms)
            except BaseException as e:
                print(e)

        self.cu.halted = False
        self.bp.remove(pc.get())

        return None
