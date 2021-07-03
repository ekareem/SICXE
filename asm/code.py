from util import intToDec, intToBytearray


def codeF1(opcode: int, toInt=False):
    if opcode < 0 or opcode > 0xff:
        raise Exception('out of range')
    if toInt is None:
        return intToBytearray(opcode, 1)
    return opcode if toInt else f'{opcode:0>2X}'


def codeF2(opcode: int, r1: int, r2: int = 0, toInt=False):
    if r1 < 0 or r1 > 0xf or r2 < 0 or r2 > 0xf:
        raise Exception('out of range')
    if r1 is None: r1 = 0
    if r2 is None: r2 = 0
    hexstr = f'{opcode:0>2X}{r1:X}{r2:X}'
    if toInt is None:
        return intToBytearray(int(hexstr, 16), 2)
    return int(hexstr, 16) if toInt else hexstr


def codeF3(pc: int,
           base: int,
           ta: int,
           opcode: int,
           mode: int = 0b11,
           x: int = 0,
           b: int = 0,
           p: int = 1,
           e: int = 0,
           toInt: bool = False):
    disp = ta
    if ta is None:
        disp = 0
    elif mode == 0b01 or mode == 00:
        disp = ta
    elif b == 0 and e == 0:
        disp = ta - pc
        if -2048 <= disp <= 2048:
            p = 1
            disp = intToDec(disp, 12)
        else:
            disp = ta - base
            if 0 <= disp <= 4095:
                p = 0
                b = 1
                disp = intToDec(disp, 12)
        disp = intToDec(disp, 12)

    elif b == 1 and p == 0 and e == 0:
        disp = ta - base
        if 0 <= disp <= 4095:
            disp = intToDec(disp, 12)
        disp = intToDec(disp, 12)

    if e == 1:
        b = 0
        p = 0

    opni = f'{opcode:0>8b}'[:6] + f'{mode:0>2b}'

    nbits = 15 if mode == 0b00 else 12 if e == 0 else 20
    disprofm = "{:0>" + str(nbits) + "b}"

    dispstr = disprofm.format(disp)

    if len(dispstr) > nbits:
        dispstr = dispstr[len(dispstr) - nbits:len(dispstr)]

    binary = f'{opni}{x:0>1b}{dispstr}' if mode == 0b00 else f'{opni}{x:0>1b}{b:0>1b}{p:0>1b}{e:0>1b}{dispstr}'
    nbyte = 3 if mode == 0b00 else 3 if e == 0 else 4
    hexform = "{:0>" + str(nbyte * 2) + "X}"

    if toInt is None:
        return intToBytearray(int(binary, 2), nbyte)
    return int(binary, 2) if toInt else hexform.format(int(binary, 2))
