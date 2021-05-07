import time
from typing import Dict

from vm.device import Devices
from vm.mem import MEMORY
from util import *
from util.opcodee import FLOAT as FLOA
import vm.register as reg
import vm.alu as alu


class CU:
    def __init__(self, bus: 'BUS'):
        self.mem: MEMORY = bus.mem
        self.devices: Devices = bus.devices
        self.registers: Dict[int, Union[INT, FLOAT]] = bus.registers
        self.instruction = self.getInstruction()
        self.command = self.getCommand()
        self.halted = False
        self.bus = bus

    def setStartingAddress(self, addr):
        reg.getRegister(reg.SICXE_NUM_REGISTER_PC).set(addr)

    def getCommand(self):
        opcode = getopcode(self.instruction)
        if opcode == ADD: return self.add
        if opcode == ADDF: return self.addf
        if opcode == ADDR: return self.addr
        if opcode == AND: return self.andd
        if opcode == CLEAR: return self.clear
        if opcode == COMP: return self.comp
        if opcode == COMPF: return self.compf
        if opcode == COMPR: return self.compr
        if opcode == DIV: return self.div
        if opcode == DIVF: return self.divf
        if opcode == DIVR: return self.divr
        if opcode == FIX: return self.fix
        if opcode == FLOA: return self.float
        if opcode == HIO: return self.hio
        if opcode == J: return self.j
        if opcode == JEQ: return self.jeq
        if opcode == JGT: return self.jgt
        if opcode == JLT: return self.jlt
        if opcode == JSUB: return self.jsub
        if opcode == LDA: return self.lda
        if opcode == LDB: return self.ldb
        if opcode == LDCH: return self.ldch
        if opcode == LDF: return self.ldf
        if opcode == LDL: return self.ldl
        if opcode == LDS: return self.lds
        if opcode == LDT: return self.ldt
        if opcode == LDX: return self.ldx
        if opcode == LPS: return self.lps
        if opcode == MUL: return self.mul
        if opcode == MULF: return self.mulf
        if opcode == MULR: return self.mulr
        if opcode == NORM: return self.norm
        if opcode == OR: return self.orr
        if opcode == RD: return self.rd
        if opcode == RMO: return self.rmo
        if opcode == RSUB: return self.rsub
        if opcode == SHIFTL: return self.shiftl
        if opcode == SHIFTR: return self.shiftr
        if opcode == SIO: return self.sio
        if opcode == SSK: return self.ssk
        if opcode == STA: return self.sta
        if opcode == STB: return self.stb
        if opcode == STCH: return self.stch
        if opcode == STF: return self.stf
        if opcode == STL: return self.stl
        if opcode == STS: return self.sts
        if opcode == STT: return self.stt
        if opcode == STX: return self.stx
        if opcode == SUB: return self.sub
        if opcode == SUBF: return self.subf
        if opcode == SUBR: return self.subr
        if opcode == SVC: return self.svc
        if opcode == TD: return self.td
        if opcode == TIO: return self.tio
        if opcode == TIX: return self.tix
        if opcode == TIXR: return self.tixr
        if opcode == WD: return self.wd
        if opcode == HALT: return self.halt
        return self.xxx

    def ontick(self):
        self.instruction = self.getInstruction()
        pc = reg.getRegister(reg.SICXE_NUM_REGISTER_PC)
        pc.add(len(self.getInstruction()), setSelf=True)

    def execute(self):
        self.command = self.getCommand()
        self.command()

    def runall(self):
        while not self.halted:
            self.run()

    def run(self, s=0):
        self.ontick()
        self.execute()
        time.sleep(s)

    def getInstruction(self):
        pc = reg.getRegister(reg.SICXE_NUM_REGISTER_PC)
        instr = self.mem.get(int(pc), 2, asbytearr=True)
        length = getFormat(instr)
        return self.mem.get(int(pc), length, asbytearr=True)

    def fetch(self):
        pc = reg.getRegister(reg.SICXE_NUM_REGISTER_PC)
        b = reg.getRegister(reg.SICXE_NUM_REGISTER_B)
        x = reg.getRegister(reg.SICXE_NUM_REGISTER_X)

        ta = getTargetAddress(self.instruction, pc, b, x, self.mem)

        return ta.dec

    def xxx(self):
        pass

    def add(self):
        alu.addrm(reg.getRegister(reg.SICXE_NUM_REGISTER_A),
                  self.mem,
                  self.fetch(),
                  isImidiateInstr(self.instruction))

    def addf(self):
        alu.addfrm(reg.getRegister(reg.SICXE_NUM_REGISTER_F),
                   self.mem,
                   self.fetch(),
                   isImidiateInstr(self.instruction))

    def addr(self):
        alu.addrr(reg.getRegister(getRegister1(self.instruction)),
                  reg.getRegister(getRegister2(self.instruction)))

    def andd(self):
        alu.andrm(reg.getRegister(reg.SICXE_NUM_REGISTER_A),
                  self.mem,
                  self.fetch(),
                  isImidiateInstr(self.instruction))

    def clear(self):
        reg.getRegister(getRegister1(self.instruction)).set(0)

    def comp(self):
        alu.comprm(reg.getRegister(reg.SICXE_NUM_REGISTER_A),
                   reg.getRegister(reg.SICXE_NUM_REGISTER_SW),
                   self.mem,
                   self.fetch(),
                   isImidiateInstr(self.instruction))

    def compf(self):
        alu.compfrm(reg.getRegister(reg.SICXE_NUM_REGISTER_F),
                    reg.getRegister(reg.SICXE_NUM_REGISTER_SW),
                    self.mem,
                    self.fetch(),
                    isImidiateInstr(self.instruction))

    def compr(self):
        alu.comprr(getRegister1(self.instruction),
                   getRegister2(self.instruction),
                   reg.getRegister(reg.SICXE_NUM_REGISTER_SW))

    def div(self):
        alu.divrm(reg.getRegister(reg.SICXE_NUM_REGISTER_A),
                  self.mem,
                  self.fetch(),
                  isImidiateInstr(self.instruction))

    def divf(self):
        alu.divfrm(reg.getRegister(reg.SICXE_NUM_REGISTER_F),
                   self.mem,
                   self.fetch(),
                   isImidiateInstr(self.instruction))

    def fix(self):
        reg.getRegister(reg.SICXE_NUM_REGISTER_A).set(reg.getRegister(reg.SICXE_NUM_REGISTER_F))

    def float(self):
        reg.getRegister(reg.SICXE_NUM_REGISTER_F).set(reg.getRegister(reg.SICXE_NUM_REGISTER_A))

    def halt(self):
        self.halted = True

    def hio(self):
        pass

    def j(self):
        reg.getRegister(reg.SICXE_NUM_REGISTER_PC).set(self.fetch())

    def jeq(self):
        cc = reg.getRegister(reg.SICXE_NUM_REGISTER_SW).getbits((6, 8), BIG)
        if cc == alu.SICXE_CC_EQ: self.j()

    def jgt(self):
        cc = reg.getRegister(reg.SICXE_NUM_REGISTER_SW).getbits((6, 8), BIG)
        if cc == alu.SICXE_CC_GT: self.j()

    def jlt(self):
        cc = reg.getRegister(reg.SICXE_NUM_REGISTER_SW).getbits((6, 8), BIG)
        if cc == alu.SICXE_CC_LT: self.j()

    def jsub(self):
        reg.getRegister(reg.SICXE_NUM_REGISTER_L).set(reg.getRegister(reg.SICXE_NUM_REGISTER_PC))
        self.j()

    def lda(self):
        alu.ld(reg.getRegister(reg.SICXE_NUM_REGISTER_A),
               self.mem,
               self.fetch(),
               isImidiateInstr(self.instruction))

    def ldb(self):
        alu.ld(reg.getRegister(reg.SICXE_NUM_REGISTER_B),
               self.mem,
               self.fetch(),
               isImidiateInstr(self.instruction))

    def ldch(self):
        alu.ldch(reg.getRegister(reg.SICXE_NUM_REGISTER_A),
                 self.mem,
                 self.fetch(),
                 isImidiateInstr(self.instruction))

    def ldf(self):
        alu.ldf(reg.getRegister(reg.SICXE_NUM_REGISTER_F),
                self.mem,
                self.fetch(),
                isImidiateInstr(self.instruction))

    def ldl(self):
        alu.ld(reg.getRegister(reg.SICXE_NUM_REGISTER_L),
               self.mem,
               self.fetch(),
               isImidiateInstr(self.instruction))

    def lds(self):
        alu.ld(reg.getRegister(reg.SICXE_NUM_REGISTER_S),
               self.mem,
               self.fetch(),
               isImidiateInstr(self.instruction))

    def ldt(self):
        alu.ld(reg.getRegister(reg.SICXE_NUM_REGISTER_T),
               self.mem,
               self.fetch(),
               isImidiateInstr(self.instruction))

    def ldx(self):
        alu.ld(reg.getRegister(reg.SICXE_NUM_REGISTER_X),
               self.mem,
               self.fetch(),
               isImidiateInstr(self.instruction))

    def lps(self):
        pass

    def mul(self):
        alu.mulrm(reg.getRegister(reg.SICXE_NUM_REGISTER_A),
                  self.mem,
                  self.fetch(),
                  isImidiateInstr(self.instruction))

    def mulf(self):
        alu.mulfrm(reg.getRegister(reg.SICXE_NUM_REGISTER_F),
                   self.mem,
                   self.fetch(),
                   isImidiateInstr(self.instruction))

    def mulr(self):
        alu.mulrr(reg.getRegister(getRegister1(self.instruction)),
                  reg.getRegister(getRegister2(self.instruction)))

    def norm(self):
        reg.getRegister(reg.SICXE_NUM_REGISTER_F).normalize(setSelf=True)

    def orr(self):
        alu.orrm(reg.getRegister(reg.SICXE_NUM_REGISTER_A),
                 self.mem,
                 self.fetch(),
                 isImidiateInstr(self.instruction))

    def rd(self):
        device = self.fetch() if isImidiateInstr(self.instruction) else self.mem.getbyte(self.fetch())
        self.devices[device].read(reg.getRegister(reg.SICXE_NUM_REGISTER_A))

    def rmo(self):
        reg.getRegister(getRegister2(self.instruction)).set(reg.getRegister(getRegister1(self.instruction)))

    def rsub(self):
        reg.getRegister(reg.SICXE_NUM_REGISTER_PC).set(reg.getRegister(reg.SICXE_NUM_REGISTER_L))

    def shiftl(self):
        alu.shiftl(reg.getRegister(getRegister1(self.instruction)),
                   getRegister2(self.instruction))

    def shiftr(self):
        alu.shiftr(reg.getRegister(getRegister1(self.instruction)),
                   getRegister2(self.instruction))

    def sio(self):
        pass

    def ssk(self):
        pass

    def sta(self):
        alu.st(reg.getRegister(reg.SICXE_NUM_REGISTER_A),
               self.mem,
               self.fetch())

    def stb(self):
        alu.st(reg.getRegister(reg.SICXE_NUM_REGISTER_B),
               self.mem,
               self.fetch())

    def stch(self):
        alu.stch(reg.getRegister(reg.SICXE_NUM_REGISTER_A),
                 self.mem,
                 self.fetch())

    def stf(self):
        alu.stf(reg.getRegister(reg.SICXE_NUM_REGISTER_F),
                self.mem,
                self.fetch())

    def stt(self):
        alu.st(reg.getRegister(reg.SICXE_NUM_REGISTER_T),
               self.mem,
               self.fetch())

    def sti(self):
        pass

    def stl(self):
        alu.st(reg.getRegister(reg.SICXE_NUM_REGISTER_L),
               self.mem,
               self.fetch())

    def sts(self):
        alu.st(reg.getRegister(reg.SICXE_NUM_REGISTER_S),
               self.mem,
               self.fetch())

    def stsw(self):
        alu.st(reg.getRegister(reg.SICXE_NUM_REGISTER_SW),
               self.mem,
               self.fetch())

    def stt(self):
        alu.st(reg.getRegister(reg.SICXE_NUM_REGISTER_T),
               self.mem,
               self.fetch())

    def stx(self):
        alu.st(reg.getRegister(reg.SICXE_NUM_REGISTER_X),
               self.mem,
               self.fetch())

    def sub(self):
        alu.subrm(reg.getRegister(reg.SICXE_NUM_REGISTER_A),
                  self.mem,
                  self.fetch(),
                  isImidiateInstr(self.instruction))

    def subf(self):
        alu.subfrm(reg.getRegister(reg.SICXE_NUM_REGISTER_F),
                   self.mem,
                   self.fetch(),
                   isImidiateInstr(self.instruction))

    def subr(self):
        alu.subrr(reg.getRegister(getRegister1(self.instruction)),
                  reg.getRegister(getRegister2(self.instruction)))

    def svc(self):
        pass

    def td(self):
        device = self.mem.getbyte(self.fetch())
        self.devices[device].test(reg.getRegister(reg.SICXE_NUM_REGISTER_SW))

    def tio(self):
        pass

    def tix(self):
        alu.addrm(reg.getRegister(reg.SICXE_NUM_REGISTER_X),
                  self.mem,
                  1,
                  True)
        alu.comprm(reg.getRegister(reg.SICXE_NUM_REGISTER_X),
                   reg.getRegister(reg.SICXE_NUM_REGISTER_SW),
                   self.mem,
                   self.fetch(),
                   isImidiateInstr(self.instruction))

    def tixr(self):
        alu.addrm(reg.getRegister(reg.SICXE_NUM_REGISTER_X),
                  self.mem,
                  1,
                  True)
        alu.comprr(reg.getRegister(reg.SICXE_NUM_REGISTER_X),
                   reg.getRegister(getRegister1(self.instruction)),
                   reg.getRegister(reg.SICXE_NUM_REGISTER_SW))

    def wd(self):
        device = self.fetch() if isImidiateInstr(self.instruction) else self.mem.getbyte(self.fetch())
        self.devices[device].write(reg.getRegister(reg.SICXE_NUM_REGISTER_A))
