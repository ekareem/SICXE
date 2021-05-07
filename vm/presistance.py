import math

from vm import CU, BUS, SICXE_NUM_REGISTER_A, SICXE_NUM_REGISTER_X, SICXE_NUM_REGISTER_L, SICXE_NUM_REGISTER_B, \
    SICXE_NUM_REGISTER_S, SICXE_NUM_REGISTER_T, SICXE_NUM_REGISTER_F, SICXE_NUM_REGISTER_PC, SICXE_NUM_REGISTER_SW

MEMORYFILE = 'memory.txt'


def memoryWrite(cu: CU, f):
    string = ''
    for reg in cu.registers:
        form = "{:0>" + str(math.ceil(cu.registers[reg].nbits / 4)) + "x}"
        id = "AXLBSTF?PW"[reg]
        hexx = form.format(cu.registers[reg].dec)
        val = cu.registers[reg].get()
        string += f'{id} {hexx} {val}\n'

    string += str(cu.mem)
    file = open(f, 'w', encoding='UTF-8')
    file.write(string)
    # return string


regnum = {
    'A': SICXE_NUM_REGISTER_A,
    'X': SICXE_NUM_REGISTER_X,
    'L': SICXE_NUM_REGISTER_L,
    'B': SICXE_NUM_REGISTER_B,
    'S': SICXE_NUM_REGISTER_S,
    'T': SICXE_NUM_REGISTER_T,
    'F': SICXE_NUM_REGISTER_F,
    'P': SICXE_NUM_REGISTER_PC,
    'W': SICXE_NUM_REGISTER_SW,
}


def readToMemory(cu: CU, f):
    file = open(f, 'r')
    for line in file:
        line = line.split()
        if line[0] in regnum:
            pass
            cu.registers[regnum[line[0]]].dec = int(line[1], 16)
        else:
            addr = int(line[0], 16)
            arr = line[1:17]
            mem = bytearray()
            for byte in arr:
                mem.append(int(byte, 16))
                cu.mem.setBytearray(addr, mem)