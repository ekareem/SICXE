from typing import List


class Block:
    def __init__(self, name, start=0, parent=None, child=None, section: 'Section' = None):
        self.name = name
        self.start = start
        self.lines: List['Line'] = []
        self.parent = parent
        self.child = child
        self.section = section

    def getLineIndex(self, line: 'Line'):
        for i in range(len(self.lines)):
            if self.lines[i] == line:
                return i
        return -1

    def getLineAddr(self, line: 'Line'):
        index = self.getLineIndex(line)
        length = self.startAddr()
        for i in range(0, index):
            length += self.lines[i].length()
        return length

    def startAddr(self):
        if self.parent is None:
            return self.start

        return self.parent.endAddr()

    def endAddr(self):
        return self.startAddr() + self.blocklength()

    def blocklength(self):
        length = 0
        for line in self.lines:
            length += line.length()
        return length

    def print(self):
        for i in self.lines:
            print(i)

    def __str__(self):
        return f'{self.name:>8} {str(self.startAddr()):>4} {self.endAddr():>4}'
