from debug.command import Command
from debug.command import BinaryCommand


class ExprCommand(BinaryCommand):
    def __init__(self, token: str, num1: Command, num2: Command):
        super().__init__(num1, num2)
        self.token = token

    def execute(self, inputs=None) -> any:
        if self.token == '+':
            return self.right.execute() + self.left.execute()
        if self.token == '-':
            return self.right.execute() - self.left.execute()
        if self.token == '%':
            return self.right.execute() % self.left.execute()
        if self.token == '/':
            return self.right.execute() / self.left.execute()
        if self.token == '*':
            return self.right.execute() * self.left.execute()
