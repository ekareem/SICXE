class Command:
    def __init__(self):
        pass

    def execute(self, inputs=None) -> any:
        raise NotImplementedError


class UnaryCommand(Command):
    def __init__(self, child: Command):
        super().__init__()
        self.child: Command = child


class BinaryCommand(Command):
    def __init__(self, left: Command, right: Command):
        super().__init__()
        self.left = left
        self.right = right
