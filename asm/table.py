from typing import Dict, Union

from asm.block import Block
from asm.storage import Storage, Literal,Symbol


class Table:
    def __init__(self):
        self.table: Dict[str, Union[Storage, Block]] = {}

    def __setitem__(self, id: str, storage: any, cls: type = Storage):
        if id not in self.table and type(storage) == cls:
            self.table[id] = storage

    def __getitem__(self, id):
        if id in self.table:
            return self.table[id]
        return None

    def toString(self):
        string = f'{"name":<10} {"address":<6} {"value":<10}\n'
        for elem in self.table:
            string += f'{elem:<10} {str(hex(self.table[elem].addr).replace("0x","") if not self.table[elem].addr is None else "------"):0>6}' \
                      f' {str(self.table[elem].value if not self.table[elem].value is None else ""):<10}\n'
        return string

    def __str__(self):
        string = ''
        for i in self.table:
            string += f'{i} : {self.table[i]}\n'
        return string


class SYMTAB(Table):
    def __init__(self):
        super().__init__()

    def __setitem__(self, id: str, symbol: Symbol, cls: type = Symbol):
        super().__setitem__(id, symbol, cls)

    def __getitem__(self, id):
        return super().__getitem__(id)


class LITTAB(Table):
    def __init__(self):
        super().__init__()

    def __setitem__(self, id: str, literal: Literal, cls: type = Literal):
        super().__setitem__(id, literal, cls)

    def __getitem__(self, id):
        return super().__getitem__(id)


class BLOCTAB(Table):
    def __init__(self):
        super().__init__()

    def __setitem__(self, id: str, block: Block, cls: type = Block):
        super().__setitem__(id, block, cls)

    def __getitem__(self, id):
        return super().__getitem__(id)
