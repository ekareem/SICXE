import time
from typing import List

from debug.disas import createInstruction
from debug.breakpoint import BreakPoint
from debug.command.command import Command, UnaryCommand
from util import SICXE_SIZE_MEMORY, JSUB, getopcode, RSUB
from vm import CU, SICXE_NUM_REGISTER_PC


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
            i = self.cu.getInstruction()
            if self.show:
                print(createInstruction(self.cu, int(pc), i, self.symtab, self.datatab))
            pc = self.cu.registers[SICXE_NUM_REGISTER_PC].get(False)
            self.bp.remove(pc)
            # self.cu.ontick()
            # self.cu.execute()
            self.cu.run()

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

    def step(self, inSub=False):
        instr = self.cu.getInstruction()

        if getopcode(instr) == JSUB:
            inSub = True

        if getopcode(instr) == RSUB:
            inSub = False

        pc = self.cu.registers[SICXE_NUM_REGISTER_PC].get(False)
        if self.show:
            print(createInstruction(self.cu, int(pc), instr, self.symtab, self.datatab))
        self.bp.remove(pc)
        self.cu.run()

        if inSub:
            self.step(inSub)


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
        # count = int(SICXE_SIZE_MEMORY/3)

        while pc.get() not in self.bp and not self.cu.halted:
            i = self.cu.getInstruction()
            if self.show:
                print(createInstruction(self.cu, int(pc), i, self.symtab, self.datatab))
            self.cu.run(ms)
            # self.cu.ontick()
            # self.cu.execute()
        self.cu.halted = False
        self.bp.remove(pc.get())

        return None
