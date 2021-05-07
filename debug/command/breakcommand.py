from debug.breakpoint import BreakPoint
from debug.command.command import UnaryCommand, Command


class Break(UnaryCommand):
    def __init__(self, bp: BreakPoint, child: Command):
        super().__init__(child)
        self.bp = bp

    def execute(self, inputs=None) -> str:
        if self.child is None:
            raise Exception('no breakpoint specified')

        point = self.child.execute()
        self.bp.set(point)

        return str(point)
