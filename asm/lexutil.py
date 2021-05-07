import math
from typing import Union

from util import intToBytearray, intToDec, bytearrayToInt, floatToDec, floatToBytearray

LOCAL = 0
GLOBAL = 1


def getHead(cls: Union['Line', 'Block', 'Section']):
    if cls.parent is None:
        return cls
    return getHead(cls.parent)


def getTail(cls: Union['Line', 'Block', 'Section']):
    if cls.child is None:
        return cls
    return getTail(cls.child)


def isExpression(token: str):
    token = token.replace('#', '').replace('@', '')
    for c in token:
        if not (c == '+' or c == '-' or c == '*' or c == '/' or c == '%' or c == '(' or c == ')' or c == '.' or c.isalnum()):
            return False
    index = max(token.find('+'), token.find('-'), token.find('*'), token.find('/'), token.find('%'))
    return index != -1 and index != 0


if __name__ == '__main__':
    print(isExpression("1.5+2.3"))


def isFloat(num: str):
    if num.find('.') == -1:
        return False
    try:
        float(num)
        return True
    except:
        return False


def isdigit(num, base=None):
    try:
        if num.find('0x') == 0 or num.find('-0x') == 0:
            int(num, base if base is not None else 16)
        elif num.find('0o') == 0 or num.find('-0o') == 0:
            int(num, base if base is not None else 8)
        elif num.find('0b') == 0 or num.find('-0b') == 0:
            int(num, base if base is not None else 2)
        else:
            int(num, base if base is not None else 10)
        return True
    except:
        return False


def isNumber(strnum: str):
    if isdigit(strnum):
        return True
    elif strnum.find("C'") == 0 and strnum[-1] == "'":
        return True
    elif strnum.find("X'") == 0 and strnum[-1] == "'":
        return True
    elif strnum.find("O'") == 0 and strnum[-1] == "'":
        return True
    elif strnum.find("B'") == 0 and strnum[-1] == "'":
        return True
    return False


def toNumber(strnum: str, nbits: int, toBytearray=False):
    if isFloat(strnum):
        if toBytearray:
            return floatToBytearray(float(strnum), 11, 36)
        return floatToDec(float(strnum), 11, 36)

    if type(strnum) is int:
        if toBytearray:
            nbyte = math.ceil(nbits / 8)
            return intToBytearray(strnum, nbyte, True)

        return intToDec(strnum, 10, nbits)

    if strnum.find('0x') == 0 or strnum.find('-0x') == 0:
        if toBytearray:
            nbyte = math.ceil(nbits / 8)
            return intToBytearray(int(strnum, 16), nbyte, True)

        return intToDec(int(strnum, 16), nbits)

    elif strnum.find('0o') == 0 or strnum.find('-0o') == 0:
        if toBytearray:
            nbyte = math.ceil(nbits / 8)
            return intToBytearray(int(strnum, 8), nbyte, True)

        return intToDec(int(strnum, 8), nbits)

    elif strnum.find('0b') == 0 or strnum.find('-0b') == 0:
        if toBytearray:
            nbyte = math.ceil(nbits / 8)
            return intToBytearray(int(strnum, 2), nbyte, True)

        return intToDec(int(strnum, 2), nbits)

    elif isdigit(strnum):
        if toBytearray:
            nbyte = math.ceil(nbits / 8)
            return intToBytearray(int(strnum, 10), nbyte, True)

        return intToDec(int(strnum, 10), nbits)

    elif strnum.find("C'") == 0:
        strip = strnum.lstrip("C").replace("'", '')
        if toBytearray:
            return bytearray(strip, encoding='utf-8')

        return bytearrayToInt(bytearray(strip, encoding='utf-8'), False)

    elif strnum.find("X'") == 0:
        strip = strnum.lstrip("X").replace("'", '')
        if toBytearray:
            nbyte = math.ceil(len(strip) / 2)
            return intToBytearray(int(strip, 16), nbyte, True)

        return int(strip, 16)

    elif strnum.find("O'") == 0:
        strip = strnum.lstrip("B").replace("'", '')
        if toBytearray:
            nbyte = math.ceil(nbits / 8)
            return intToBytearray(int(strip, 8), nbyte, True)

        return int(strip, 8)

    elif strnum.find("B'") == 0:
        strip = strnum.lstrip("B").replace("'", '')
        if toBytearray:
            nbyte = math.ceil(nbits / 8)
            return intToBytearray(int(strip, 2), nbyte, True)

        return int(strip, 2)
