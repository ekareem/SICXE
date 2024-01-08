import math
from typing import Union, List


def isDigit(numstr, base: int):
    try:
        int(numstr, base)
        return True
    except:
        return False


class attribute:
    def __init__(self, length, value=''):
        self.length: int = length
        self.value = value

    def toBytes(self):
        b = bytearray()
        if not isDigit(self.value, 16):
            return b

        value = self.value
        if len(self.value) % 2 == 1:
            value = '0' + value

        for i in range(0, len(value), 2):
            numstr = value[i:i + 2]
            b.append(int(numstr, 16))

        return b

    def roomleft(self):
        return self.length - len(self.value)

    def toInt(self):
        if not isDigit(self.value, 16):
            raise Exception('not a number')

        return int(self.value, 16)

    def set(self, value, cut=False):
        self.reset()
        self.add(value, cut)

    def reset(self):
        self.value = ''

    def canFit(self, value: Union[str, int, bytearray], nhbyte=6):
        straddr = value
        form = "{:0>" + str(nhbyte) + "X}"
        if type(value) == int:
            straddr = form.format(value)
        if type(value) == bytearray:
            a = int.from_bytes(value, 'big', signed=False)
            straddr = form.format(a)

        return len(self.value + straddr) <= self.length

    def add(self, value, cut=False):
        if self.canFit(value) and cut is False:
            self.value += value
        if cut is True:
            self.value += value
        self.value = self.value[:self.length] if len(self.value) > self.length else self.value

        return self.value[:min(self.length, self.length)]

    def __str__(self):
        return self.value + ' ' * (self.length - len(self.value))

    def __repr__(self):
        return self.__str__()


class Record:
    def __init__(self, lengths=()):
        self.columns: List[attribute] = []
        for length in lengths:
            self.columns.append(attribute(length))

    def setHex(self, index: int, data: Union[int, str, bytearray], nhbyte, cut=False):
        straddr = data
        form = "{:0>" + str(nhbyte) + "X}"
        if type(data) == int:
            straddr = form.format(data)
        if type(data) == bytearray:
            a = int.from_bytes(data, 'big', signed=False)
            straddr = form.format(a)
        self.set(index, straddr, cut)

    def addHex(self, index: int, data: Union[int, str, bytearray], nhbyte, cut=False):
        straddr = data
        form = "{:0>" + str(nhbyte) + "X}"
        if type(data) == int:
            straddr = form.format(data)
        if type(data) == bytearray:
            a = int.from_bytes(data, 'big', signed=False)
            straddr = form.format(a)
        self.add(index, straddr, cut)

    def set(self, index, value, cut=False):
        self.columns[index].set(value, cut)

    def add(self, index, value, cut=False):
        self.columns[index].add(value, cut)

    def __str__(self):
        string = ''
        for column in self.columns:
            string += str(column)
        return string

    def __repr__(self):
        return self.__str__()


class HeaderRecord(Record):
    def __init__(self, lengths=(1, 6, 6, 6)):
        super().__init__(lengths)
        self.set(0, 'H')

    def setName(self, name):
        self.set(1, name, True)

    def setStart(self, addr):
        self.setHex(2, addr, nhbyte=6)

    def setLength(self, length):
        self.setHex(3, length, nhbyte=6)


class TextRecord(Record):
    def __init__(self, lengths=(1, 6, 2, 60)):
        super().__init__(lengths)
        self.set(0, 'T')

    def setStart(self, addr):
        self.setHex(1, addr, nhbyte=6)

    def setLength(self):
        length = math.ceil(len(self.columns[3].value) / 2)
        self.setHex(2, length, nhbyte=2)

    def setProgram(self, data, nhbyte=6, addr=0):
        newnhbyte = nhbyte
        if nhbyte > self.columns[3].length - len(self.columns[3].value):
            newnhbyte -= self.columns[3].length - len(self.columns[3].value)
        insertnhbyte = min(self.columns[3].length - len(self.columns[3].value), nhbyte)
        form = "{:0>" + str(nhbyte) + "x}"
        ndata = str(form.format(data))[:insertnhbyte]
        ndata = int(ndata, 16) if type(data) == int else data
        self.addHex(3, ndata, nhbyte=insertnhbyte)
        self.setLength()

        return [addr + math.ceil(insertnhbyte / 2), str(form.format(data))[insertnhbyte:], newnhbyte]


class DefRecord(Record):
    def __init__(self, lengths=(6, 6)):
        super().__init__(lengths)

    def internal(self, name: str):
        self.set(0, name, True)

    def addr(self, addr):
        self.setHex(1, addr, 6)


class DefRecords:
    def __init__(self):
        self.count = 0
        self.Defs: List[List[DefRecord]] = []

    def add(self, internal, addr):
        if self.count == 0:
            self.Defs.append([])
        if self.count <= 6:
            d = DefRecord()
            d.internal(internal)
            d.addr(addr)
            self.Defs[len(self.Defs) - 1].append(d)
            self.count = (self.count + 1) % 6

    def __str__(self):
        string = ''
        for recs in self.Defs:
            string += 'D'
            for i in recs:
                string += str(i)
            string += '\n'
        return string


class RefRecord(Record):
    def __init__(self, lengths=[6]):
        super().__init__(lengths)

    def external(self, name: str):
        self.set(0, name, True)


class RefRecords:
    def __init__(self):
        self.count = 0
        self.Refs: List[List[RefRecord]] = []

    def add(self, external):
        if self.count == 0:
            self.Refs.append([])
        if self.count <= 12:
            d = RefRecord()
            d.external(external)
            self.Refs[len(self.Refs) - 1].append(d)
            self.count = (self.count + 1) % 12

    def __str__(self):
        string = ''
        for recs in self.Refs:
            string += 'R'
            for i in recs:
                string += str(i)
            string += '\n'
        return string


class ModRecord(Record):
    def __init__(self, lengths=(1, 6, 2, 1, 6)):
        super().__init__(lengths)
        self.set(0, 'M')

    def start(self, addr):
        self.setHex(1, addr, 6)

    def length(self, length=0x3):
        self.setHex(2, length, 2)

    def flag(self, f='+'):
        self.set(3, f)

    def external(self, name):
        self.set(4, name, True)


class ModRecords():
    def __init__(self):
        self.mods: List[ModRecord] = []

    def setmod(self, external: str, addr: int, length=3, f='+'):
        m = ModRecord()
        m.start(addr)
        m.length(length)
        m.flag(f)
        m.external(external)
        self.mods.append(m)

    def __str__(self):
        string = ''
        for m in self.mods:
            string += str(m) + '\n'
        return string


class EndRecord(Record):
    def __init__(self, lengths=(1, 6)):
        super().__init__(lengths)
        self.set(0, 'E')

    def first(self, addr):
        self.setHex(1, addr, nhbyte=6)


class TextRecords:
    def __init__(self):
        self.textRecords: List[TextRecord] = []
        self.addr = -1

    def length(self):
        l = 0
        for textRecord in self.textRecords:
            l += math.ceil(len(textRecord.columns[3].value) / 2)
        return l

    def add(self, addr, data, nhbyte):
        if type(addr) == str:
            addr = int(addr, 16)

        t = TextRecord()

        if self.addr != addr:
            self.addr = addr
            t.setStart(self.addr)
            self.textRecords.append(t)
        else:
            t = self.textRecords[len(self.textRecords) - 1]

        if not t.columns[3].canFit(data, nhbyte):
            t = TextRecord()
            t.setStart(self.addr)
            self.textRecords.append(t)

        s = t.setProgram(data, nhbyte, addr)
        self.addr += math.ceil(nhbyte / 2)
        return s

    def __str__(self):
        string = ''
        for textRecord in self.textRecords:
            string += f'{textRecord}\n'
        return string


class ObjectCode:
    def __init__(self):
        self.r = RefRecords()
        self.d = DefRecords()
        self.m = ModRecords()
        self.h = HeaderRecord()
        self.t = TextRecords()
        self.e = EndRecord()

    def setRef(self, external: str):
        self.r.add(external)

    def setdef(self, internal: str, addr: int):
        self.d.add(internal, addr)

    def setmod(self, external: str, addr: int, length=3, f='+'):
        self.m.setmod(external, addr, length, f)

    def setHeaderName(self, name: str):
        self.h.setName(name)

    def setStart(self, addr):
        self.h.setStart(addr)
        self.e.first(addr)

    def addText(self, addr, data, nhbyte: int):
        if self.t.length() == 0:
            self.setStart(addr)
        a = self.t.add(addr, data, nhbyte)
        self.h.setLength(self.t.length())
        if len(a[1]) != 0:
            self.addText(a[0], int(a[1], 16), a[2])
        return a

    def addTextFromByteArray(self, addr, bytes: bytearray):
        for i in bytes:
            self.addText(addr, i, 2)
            addr += 1

    def __str__(self):
        return f'{self.h}\n{self.d}{self.r}{self.t}{self.m}{self.e}'


def parseObjectFile(file):
    o = ObjectCode()
    for line in open(file):
        if len(line) > 0 and line[0:1].upper() == 'H':
            identify = line[0:1]
            name = line[1:7] if len(line) >= 7 else ''
            start = line[7:13] if len(line) >= 13 else ''
            length = line[13:19] if len(line) >= 19 else ''
            o.h.columns[0].value = identify
            o.h.columns[1].value = name
            o.h.columns[2].value = start
            o.h.columns[3].value = length

        elif len(line) > 0 and line[0:1].upper() == 'T':
            identify = line[0:1]
            start = line[1:7] if len(line) >= 7 else ''
            length = line[7:9] if len(line) >= 9 else ''
            code = line[9:].strip() if len(line) >= 1 else ''
            t = TextRecord()
            t.columns[0].value = identify
            t.columns[1].value = start
            t.columns[2].value = length
            t.columns[3].value = code
            o.t.textRecords.append(t)

        elif len(line) > 0 and line[0:1].upper() == 'E':
            identify = line[0:1]
            first = line[1:7] if len(line) >= 7 else ''
            o.e.columns[0].value = identify
            o.e.columns[1].value = first

    return o


if __name__ == '__main__':
    # print(parseObjectFile('mid.obj'))
    o = ObjectCode()
    o.setHeaderName('COPY')
    o.addTextFromByteArray(4096, bytearray(b''))
    o.addTextFromByteArray(4096,bytearray(b'K \x0c'))
    o.addTextFromByteArray(4099,bytearray(b'\x16 9'))
    o.addTextFromByteArray(4102,bytearray(b'K \x0f'))
    o.addTextFromByteArray(4105,bytearray(b'K \x1e'))
    o.addTextFromByteArray(4108,bytearray(b'\x06 0'))
    o.addTextFromByteArray(4111,bytearray(b'\x01\x10\x10B'))
    o.addTextFromByteArray(4114,bytearray(b'\x0f *'))
    #o.addTextFromByteArray()
    print(o)
