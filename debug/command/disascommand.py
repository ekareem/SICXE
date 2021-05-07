from debug.command.command import BinaryCommand, Command
from debug.disas import Disasembler
from util import SICXE_SIZE_MEMORY
from vm import SICXE_NUM_REGISTER_PC


class Disas(BinaryCommand):
    def __init__(self, dis: Disasembler, left: Command, right: Command):
        super().__init__(left, right)
        self.dis = dis

    def execute(self, inputs=None) -> any:
        start = self.left.execute() if self.left is not None else self.dis.cu.registers[SICXE_NUM_REGISTER_PC].get()
        stop = self.right.execute() if self.right is not None else start + int(SICXE_SIZE_MEMORY/64)
        self.dis.disas((start, stop))
        return str(self.dis)
