from typing import List

from util import SICXE_SIZE_MEMORY


class BreakPoint:
    def __init__(self):
        self.breaks: List[int] = []

    def get(self, loc):
        return loc if loc in self.breaks else -1

    def set(self, loc):
        if loc < 0 or loc >= SICXE_SIZE_MEMORY:
            raise Exception(f' address must be between 0 and {SICXE_SIZE_MEMORY}')

        if loc not in self.breaks:
            self.breaks.append(loc)

    def remove(self, loc):
        if loc in self.breaks:
            self.breaks.remove(loc)

    def atBreakPoint(self,loc):
        return loc in self.breaks

    def clear(self):
        self.breaks.clear()

    def __str__(self):
        string = ''
        for points in self.breaks:
            string += f'0x{points:0>5X}\n'
        return string

    def __iter__(self):
        for i in self.breaks:
            yield i


BREAKPOINTS = BreakPoint()
