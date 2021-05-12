from asm import SYMTAB
from vm import SICXE_NUM_REGISTER_A, SICXE_NUM_REGISTER_X, SICXE_NUM_REGISTER_L, SICXE_NUM_REGISTER_B, \
    SICXE_NUM_REGISTER_T, SICXE_NUM_REGISTER_S, SICXE_NUM_REGISTER_F, SICXE_NUM_REGISTER_PC, SICXE_NUM_REGISTER_SW

registerToInt = {
    'a': SICXE_NUM_REGISTER_A,
    'x': SICXE_NUM_REGISTER_X,
    'l': SICXE_NUM_REGISTER_L,
    'b': SICXE_NUM_REGISTER_B,
    's': SICXE_NUM_REGISTER_S,
    't': SICXE_NUM_REGISTER_T,
    'f': SICXE_NUM_REGISTER_F,
    'pc': SICXE_NUM_REGISTER_PC,
    'p': SICXE_NUM_REGISTER_PC,
    'w': SICXE_NUM_REGISTER_SW,
    'sw': SICXE_NUM_REGISTER_SW,
}

stringToReg = {
    '(a)': SICXE_NUM_REGISTER_A,
    '(x)': SICXE_NUM_REGISTER_X,
    '(l)': SICXE_NUM_REGISTER_L,
    '(b)': SICXE_NUM_REGISTER_B,
    '(s)': SICXE_NUM_REGISTER_S,
    '(t)': SICXE_NUM_REGISTER_T,
    '(f)': SICXE_NUM_REGISTER_F,
    '(pc)': SICXE_NUM_REGISTER_PC,
    '(p)': SICXE_NUM_REGISTER_PC,
    '(w)': SICXE_NUM_REGISTER_SW,
    '(sw)': SICXE_NUM_REGISTER_SW,
}


def stringToInt(token, symtab: SYMTAB = None):
    toke = token.strip()

    if toke.lower() in registerToInt:
        return registerToInt[toke.lower()]

    if symtab is not None and toke in symtab.table:
        return symtab[toke].addr

    if toke.find('0x') != -1:
        return int(token, 16)
    if toke.find('0o') != -1:
        return int(token, 8)
    if toke.find('0b') != -1:
        return int(token, 2)

    if is_integer(toke):
        return int(token, 10)


def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False
