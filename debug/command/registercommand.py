from debug.command.command import UnaryCommand, Command, BinaryCommand
from vm import CU


class getRegisterVal(UnaryCommand):
    def __init__(self, cu: CU, num: Command):
        super().__init__(num)
        self.cu = cu

    def execute(self, toDec=True) -> any:
        if self.child is None:
            raise Exception('no register specified')
        num = self.child
        if issubclass(type(self.child), Command):
            num = self.child.execute()
            # maybe lve this as .dec not ,get()
        return self.cu.registers[num].get() if toDec else self.cu.registers[num]


class getMemoryVal(BinaryCommand):
    def __init__(self, cu: CU, loc: Command, nbyte: Command = None):
        super().__init__(loc, nbyte)
        self.cu = cu

    def execute(self, toDec=True) -> any:
        if self.left is None:
            raise Exception('no location specified')
        loc = self.left.execute()
        nbyte = self.right.execute() if self.right is not None else 1

        return self.cu.mem.get(loc, nbyte) if toDec else [self.cu.mem, loc, nbyte]
