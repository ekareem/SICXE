import math


def tokenizeExpr(string):
    toadd = ''
    output = []
    for x, i in enumerate(string):
        if i in ('+', '-', '*', '/', '%', '(', ')'):
            if i == '*' and not isMul(x, string):
                i = 'NUMaLLLoRRR'
            if toadd != '':
                output.append(toadd)
            output.append(i)
            toadd = ''
        else:
            toadd += i
    if toadd != '':
        output.append(toadd)
    return output


def tokenizeExpr2(string):
    toadd = ''
    output = []
    for x, i in enumerate(string):
        if i in ('+', '-'):
            if toadd != '':
                output.append(toadd)
            output.append(i)
            toadd = ''
        else:
            toadd += i
    if toadd != '':
        output.append(toadd)
    return output


def isMul(i, infix):
    if i == 0:
        return False
    if i == infix[len(infix) - 1]:
        return False
    if infix[i - 1] in ('+', '-', '*', '/', '%') and infix[i + 1] in ('+', '-', '*', '/', '%'):
        return False
    if infix[i - 1] == '(' or infix[i + 1] == ')':
        return False
    return True


def infixToPostfix(string):
    infix = tokenizeExpr2(string)
    stack = []
    postfix = []

    for token in infix:
        if token not in ('+', '-'):
            postfix.append(token)
        else:
            if len(stack) > 0:
                postfix.append(stack.pop())
            stack.append(token)
    for token in reversed(stack):
        postfix.append(token)
    postfix.reverse()
    return postfix


def isFloat(num: str):
    if num.find('.') == -1:
        return False
    try:
        float(num)
        return True
    except:
        return False
        
regs = ['[a]','[x]','[l]','[b]','[s]','[t]','[f]','[pc]','[p]','[w]','[sw]']

def infixToPostfixx(infixexpr):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["%"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = []
    postfixList = []
    tokenList = tokenizeExpr(infixexpr)

    for token in tokenList:
        if token.isalnum() or isFloat(token) or token.lower() in regs:
            postfixList.append(token)
        elif token == '(':
            opStack.append(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not len(opStack) == 0) and \
                    (prec[opStack[len(opStack) - 1]] >= prec[token]):
                postfixList.append(opStack.pop())
            opStack.append(token)

    while not len(opStack) == 0:
        postfixList.append(opStack.pop())
    return postfixList


def tokenize(string, add=()):
    quotes_opened = False
    out = []
    toadd = ''
    for c, char in enumerate(string):
        if c == len(string) - 1:  # is the character the last char
            if char not in ('', ' ', '\t', '\r') + add:
                toadd += char
            if toadd not in ('', ' ', '\t', '\r') + add:
                out.append(toadd)
            break
        elif char in ("'", '"'):  # is the character a quote
            if quotes_opened:
                quotes_opened = False  # if quotes are open then close
            else:
                quotes_opened = True  # if quotes are closed the open
            toadd += char
        elif char not in (' ', '\t', '\r') + add:
            toadd += char  # add the character if it is not a space
        elif char in (' ', '\t', '\r') + add:  # if character is a space
            if not quotes_opened:  # if quotes are not open then add the string to list
                if toadd not in ('', ' ') + add:
                    out.append(toadd)
                toadd = ''
            else:  # if quotes are still open then do not add to list
                toadd += char
    return out


def fit(val: int, nbits: int):
    """
    taktes only the first {nbits} of val
    :param val:
    :param nbits:
    :return:
    """
    binary = '1' * nbits
    return val & int(binary, 2)


def decToInt(dec: int, nbits: int, signed=True):
    """
    dec to int
    :param dec: value to be chenged
    :param nbits: number of bits
    :param signed: signed
    :return:
    """
    return __decToIntReq(dec, nbits, nbits, signed=signed)


def __decToIntReq(dec, nbits, maxbits, summ=0, signed=True):
    """
    dec to int
    :param dec: number to be converted
    :param nbits: current number of bits used for recursion
    :param maxbits: maxmimum number of bits
    :param summ: current sum recursion
    :param signed: signed
    :return:
    """
    if nbits > 0:
        # get value of left most bit
        bit = dec >> nbits - 1 & 0b1
        summ += pow(2, nbits - 1) * bit
        # if multiply left most bit by -1 if signed
        if nbits == maxbits and signed: summ *= -1

        # remove left most bit and recurse add to sum
        return __decToIntReq(dec, nbits - 1, maxbits, summ)

    return summ


def intToDec(intnum: int, nbits: int):
    """
    signed or unsigned nbits interger to bin, oct, dec,or hex

    :param intnum: integer to be conveted
    :param nbits: needed for signed bits
    :return: returns specifed number format
    """
    signed = intnum < 0
    # getting signed binary format for intnum
    result = (intnum + (1 << nbits)) % (1 << nbits) if signed else intnum
    # if intnum < 0 then turnde intnum to twoscomplemnt
    result = decToInt(result, nbits, False)

    return result


def decToFloat(dec, exponentLen, mantissaLen):
    """
    decimal to flaot

    :param dec:
    :return:
    """

    # get sign exponent and mantissa
    sign = 1 if (dec >> (exponentLen + mantissaLen) & 0x1) * -1 == 0 else -1
    exponent = dec >> mantissaLen & int('1' * exponentLen, 2)
    function = dec & int('1' * mantissaLen, 2)
    exponent = exponent - (2 ** (exponentLen - 1))

    # calulate mantisa
    mantisa = calculatemantisa(function, mantissaLen)

    # return float
    return sign * mantisa * pow(2, exponent)


def decToSEM(dec, exponentLen, mantissaLen):
    """
    decimal to flaot

    :param dec:
    :return:
    """

    # get sign exponent and mantissa
    sign = 1 if (dec >> (exponentLen + mantissaLen) & 0x1) * -1 == 0 else -1
    exponent = dec >> mantissaLen & int('1' * exponentLen, 2)
    function = dec & int('1' * mantissaLen, 2)
    exponent = exponent - (2 ** (exponentLen - 1))

    # calulate mantisa
    mantisa = calculatemantisa(function, mantissaLen)

    # return float
    return [sign, mantisa, exponent]


def calculatemantisa(decfunction: int, mantissaLen):
    """
    calulates mantisa

    :param decfunction:
    :return:
    """
    bits = bin(decfunction)
    bits = bits.replace('0b', '')

    # fillup missing bits
    while len(bits) < mantissaLen:
        bits = '0' + bits

    sum = 0

    # calulate mantissa
    for i in range(len(bits), 0, -1):
        unit = len(bits) - i
        sum += (1 / pow(2, unit + 1)) * int(bits[unit])

    return sum


def floatToDec(floatnum, exponentLen, mantissaLen):
    """
    float to decimal
    :param floatnum:
    :return:
    """
    # sign
    signstr = '0' if floatnum >= 0 else '1'
    exp = 0
    # make floatvalue positive
    floatnum = floatnum * -1 if floatnum < 0 else floatnum
    # floatnum to fix point notation wholestr.decimalstr
    wholestr, decimalstr = floatToFixpoint(floatnum, mantissaLen)

    # move deivmal point until higers order 1 is brhind the decimal point
    while len(wholestr) > 0:
        decimalstr = wholestr[len(wholestr) - 1] + decimalstr
        wholestr = wholestr[0:len(wholestr) - 1]
        exp += 1

    exp += 2 ** (exponentLen - 1)  # offest exponenet

    # add missing zeros to exponent to make it 11bits
    expstr = bin(exp).replace('0b', '')
    while len(expstr) < exponentLen:
        expstr = '0' + expstr

    manstr = decimalstr[0:mantissaLen]  # mantissa
    binstr = signstr + expstr + manstr  # put it all to getter to get floating point
    return int(binstr, 2)  # convert to int


def floatToFixpoint(floatnum, mantissaLen):
    """
    flaot to fixed point notation

    :param floatnum:
    :return: whole is number before the decimal point decimal is number after the decimal point
    """
    intnum = int(floatnum)  # extrance the whole number form the float
    point = floatnum - intnum  # extract the decimal point from the float
    whole = bin(intnum).replace('0b', '')
    decimal = decimalPointToBin(point, mantissaLen)
    return whole, decimal


def decimalPointToBin(point: float, depth: int):
    """
    decimal points to binary

    :param point:
    :param depth: bit length
    :return:
    """
    point = point - 1 if point >= 1 else point
    point2 = point * 2
    intpoint = int(point2)
    depth -= 1

    if depth == 0:
        return str(intpoint)

    return str(intpoint) + decimalPointToBin(point2, depth)


def normalize(dec, exponentLen, mantissaLen):
    """
    normalize a floating point number

    :param dec: int
    :return:
    """
    return floatToDec(decToFloat(dec, exponentLen, mantissaLen), exponentLen, mantissaLen)


def int_to(intnum: int, nbits: int, flag: str = 'bin', signed: bool = True):
    """
    signed or unsigned nbits interger to bin, oct, dec,or hex

    :param intnum: integer to be conveted
    :param nbits: needed for signed bits
    :param flag: what number foramt to convert the integer to
    :param signed: check if the conversion should be in twos complement if intnum is negative it will automatically be signed
    :return: returns specifed number format
    """
    # getting signed binary format for intnum
    result = (intnum + (1 << nbits)) % (1 << nbits) if signed else intnum
    # if intnum < 0 then turnde intnum to twoscomplemnt
    result = int_to(intnum, nbits, 'dec', True) if intnum < 0 and not signed else result
    result = decToInt(result, nbits, False)

    if flag.lower() == 'bin': return bin(result)
    if flag.lower() == 'oct': return oct(result)
    if flag.lower() == 'hex': return hex(result)

    return result


def bytearrayToInt(bytearr: bytearray, signed: bool = False):
    """
    converts bytearry to signed ot unsigned integer

    :param bytearr: bytearr
    :param signed: checks if byte arr is signed
    :return:
    """
    return int.from_bytes(bytearr, byteorder="big", signed=signed)


def intToBytearray(intnum, nbytes, signed=False):
    """
    turns integer to byte array

    :param intnum: input
    :param nbytes: bytearray size
    :param signed: if intnum is signed or not is innum < 0 it is signed automatically
    :return:
    """
    # get form hex form of intnum
    hexnum = int_to(intnum, nbytes * 8, 'hex', signed)
    hexnum = hexnum.replace('0x', '')
    if len(hexnum) % 2 == 1: hexnum = '0' + hexnum

    # hex to byte array
    bytearr = bytearray.fromhex(hexnum)
    if len(bytearr) > nbytes:  # throws exception
        return bytearray(nbytes)
    while len(bytearr) < nbytes:
        bytearr = bytearray(1) + bytearr

    return bytearr


def bytearrayToFloat(bytearr: bytearray, exponentLen: int, mantissaLen: int):
    """
    byte array to float

    :param bytearr: byte must be of length 6
    :return:
    """
    size = math.ceil((1 + exponentLen + mantissaLen) / 8)
    if len(bytearr) != size:
        # throw error
        return 0

    dec = bytearrayToInt(bytearr, False)
    return decToFloat(dec, exponentLen, mantissaLen)


def floatToBytearray(floa: float, exponentLen: int, mantissaLen: int):
    """
    float to byte array
    :param floa: floating point number
    :return:
    """
    dec = floatToDec(floa, exponentLen, mantissaLen)
    size = math.ceil((1 + exponentLen + mantissaLen) / 8)
    return intToBytearray(dec, size, False)


def decToFitNbit(dec, nbits, sum=0):
    sum = sum
    if nbits > 0:
        bit = dec >> nbits - 1 & 0b1
        sum += pow(2, nbits - 1) * bit
        return decToFitNbit(dec, nbits - 1, sum)

    return sum


def leftRotate(number, shift, nbits):
    return ((number << shift % nbits) | (number >> (nbits - shift % nbits))) & ((1 << nbits) - 1)


def rightRotate(number, shift, nbits):
    return (number >> shift % nbits) | (number << (nbits - shift % nbits)) & ((1 << nbits) - 1)
