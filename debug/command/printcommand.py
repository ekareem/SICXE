from debug.command.token import *
from debug.command.command import UnaryCommand, Command, BinaryCommand
from util import registerToString, LITTLE, BIG, decToSEM, SICXE_SIZE_MEMORY, CC_MAP
from vm import CU, SICXE_NUM_REGISTER_A, SICXE_NUM_REGISTER_SW, SICXE_NUM_REGISTER_F


class PrintCommand(UnaryCommand):
    def __init__(self, child: Command):
        super().__init__(child)

    def execute(self, inputs=None) -> any:
        if self.child is None:
            raise Exception('no noting to print')
        string: str = self.child.execute()
        if string is None:
            return
        string = str(string)
        lines = string.split('\n')
        count = 0
        for line in lines:
            print(line)
            if count > 30:
                n = input('continue y or n')
                if n.lower() in ['n', 'no']:
                    break
                else:
                    count = 0
            count += 1
        return string


class PrintRegisters(Command):
    def __init__(self, cu: CU):
        super().__init__()
        self.cu = cu

    def execute(self, inputs=None) -> any:
        string = ''
        for num in list(self.cu.registers.keys()):
            r = self.cu.registers[num]
            nhb = int(r.nbits / 4)
            form = "{} {:>4} : 0x{:0>" + str(nhb) + "X} {} {}\n"
            s = registerToString(num)
            dec = r.dec
            infl = r.get()
            extra = f"ch = '{chr(r.getbits((0, 8), False, order=LITTLE)) if 0x20 <= r.getbits((0, 8), False, order=LITTLE) <= 0x7f else ''}'" if num == SICXE_NUM_REGISTER_A \
                else f'cc = 0b{r.getbits((6, 8), False, order=BIG):0>2b} {CC_MAP[r.getbits((6, 8), False, order=BIG)]}' if num == SICXE_NUM_REGISTER_SW \
                else ' '
            if num == SICXE_NUM_REGISTER_F:
                SEM = decToSEM(r.dec, r.exponentLen, r.mantissaLen)
                extra = f'sign = 0b{r.sign()} exponent = 0b{r.exponent():0>11b} mantissa = 0b{r.mantissa():0>36b} ' \
                        f'({SEM[0]} * {SEM[1]} * 2^{SEM[2]})'
            string += form.format(num, s, dec, infl, extra)
        return string


class PrintMemory(BinaryCommand):
    def __init__(self, cu: CU, left: Command, right: Command):
        super().__init__(left, right)
        self.cu = cu

    def execute(self, inputs=None) -> any:
        start = self.left.execute() if self.left is not None else 0
        stop = self.right.execute() if self.right is not None else start + int(SICXE_SIZE_MEMORY / 32)
        return self.cu.mem.toString((start, stop))


helps = [
    {'RUN': """
RUN -- Runs all instructions until break point is hit
COMMANDS = run, r
OPTIONAL FLAG -- <number>, wait time between instruction
EX: run
EX: run 5

RUNI -- Runs and prints all instructions until break point is hit
COMMANDS = runi, ri
OPTIONAL FLAG -- <number>, wait time between instruction
EX: runi
EX: runi 5
""", },
    {'NEXT': """
NEXT -- Runs next command 
COMMANDS = next, n
OPTIONAL FLAG -- <number>, how many instructions to run
EX: next
EX: next 5

NEXTI -- Runs and prints next command 
COMMANDS = nexti, ni
OPTIONAL FLAG -- <number>, how many instructions to run
EX: nexti
EX: nexti 5
""", },
    {'BREAK': """
BREAK -- Sets a break point at a memory location 
COMMANDS = break, breakpoint, br
REQUIRED FLAG -- <number>, memory location 
EX: break 0x5

""", },
    {'DISAS': """
DISAS -- Converts machine code to low level symbolic language 
COMMANDS = disassemble, disas, d
OPTIONAL FLAG -- <number>, starting address
OPTIONAL FLAG -- <number>, ending address
EX: disas 
EX: disas 0x5
EX: disas 0x5 0x10
""", },
    {'PRINT': """
PRINT -- Print the value of given command 
COMMANDS = print, pr
REQUIRED FLAG -- <value>, value of command
EX: print 5
EX: print register a
EX: print memory 0x10
""", },
    {'REGISTER': """
REGISTER -- Return the value of given register 
COMMANDS = register, reg, rg
REQUIRED FLAG -- <number> or <letter>, number of register or register letter
EX: register 5
EX: register a

REGISTERVALUES -- Returns all values of given register 
COMMANDS = registers, rgs
EX: registers 

(a) = value of register a
(x) = value of register x
(l) = value of register l
(p) = value of register p
(w) = value of register w
(b) = value of register b
(s) = value of register s
(t) = value of register t
(f) = value of register f
""", },
    {'MEMORY': """
MEMORY -- Gets memory value
COMMANDS = memory, m, mem
REQUIRED FLAG -- <number>, starting address 
OPTIONAL FLAG -- <number>, ending address; if not specified, starting address plus 1
EX: memory 0x5
EX: memory 0x5 0x8

MEMORYVALUES -- Returns all memory values
COMMANDS = memories, mems, ms
OPTIONAL FLAG -- <number>, starting memory location 
OPTIONAL FLAG -- <number>, ending memory location
EX: memories
EX: memories 0x5 
Ex: memories 0x5 0x8
""", },
    {'CAST': """
TOBASE -- Converts number to specified base, and returns that string
COMMANDS = hex(hexadecimal), h(hexadecimal), oct(octal), o(octal), bin(binary)
REQUIRED FLAG -- <number>, the number to be casted  
EX: hex 1
EX: bin 5

TOCHAR -- Converts a number to a string
COMMANDS = char, c
REQUIRED FLAG -- <number>, the number to be converted  
EX: char 0x31323

TOCHARPOINT --returns string at address
COMMANDS = char*, c*
REQUIRE FLAG -- <number>, address of string
EX: char* 0x22

TOSIGNEDWORD -- Converts a number to word or signed word
COMMANDS = word, w, signedword, sword
REQUIRED FLAG -- <number>, the number to be converted
EX: word 0x138571
EX: signedword 0x138571

TOSIGNEDWORDPOINT --returns array of signed word at address
COMMANDS = word*, w*, signedword*, sword*
REQUIRE FLAG -- <number>, stating address of array
REQUIRE FLAG -- <number>, length of array
EX: signedword* 0x22 5

TOUNSIGNEDWORD -- Converts a number to word or unsigned word
COMMANDS = unsignedword, unw, unword
REQUIRED FLAG -- <number>, the number to be converted
EX: unword 0x138571
EX: unsignedword 0x138571

TOUNSIGNEDWORDPOINT --returns array of unsigned word at address
COMMANDS = unsignedword*, unsw*, unsword*
REQUIRE FLAG -- <number>, stating address of array
REQUIRE FLAG -- <number>, length of array
EX: unsignedword* 0x22 5


TOFLOAT -- Converts a number to float
COMMANDS = float, fl
REQUIRED FLAG -- <number>, the number to be converted
EX: float 0x1039582

TOUNSIGNEDWORDPOINT --returns array of floating point numbers at address
COMMANDS = float*, fl*
REQUIRE FLAG -- <number>, stating address of array
REQUIRE FLAG -- <number>, length of array
EX: float* 0x22 5

TOINSTRUCTION -- Gets instruction and memory location 
COMMANDS = instruction, i, in, instr
REQUIRED FLAG -- <number>, the number to be converted
EX: instruction 0x138571
""", },
    {'SET': """
SET -- Sets memory or registor value 
COMMANDS = set
REQUIRED FLAG -- <memory> or <register>,  return memory or registor
    REQUIRED FLAG -- <number>, start memory location
    REQUIRED FLAG -- <number>, end memory location 
REQUIRED FLAG -- <number>, register number
REQUIRED FLAG -- <number>, value to be set
EX: set mem 0x5 0x8 0x138571
EX: set reg 5 0x138571

SETCH -- Sets right most byte of register a
COMMANDS = setch, sch
REQUIRED FLAG -- <number> or <string>, value to be set
EX: setch 5
EX: setch "x"

SETCC -- Sets the sixth to eighth bit of the status word register
COMMANDS = setch, scc
REQUIRED FLAG -- <number>, value to be set
EX: setcc 0b11
""", },
    {'HELP': """
HELP -- prints shortlist of commands
COMMANDS = help
OPTIONAL FLAG -- <string>, different help options
EX: help run
""", },
    {'SAVE': """
SAVE -- Saves memory to memory file 
COMMANDS = save
OPTIONAL FLAG -- <file>, file to save to
EX: save file.txt
""", },
    {'READ': """
READ -- Retrieves memory from memory file 
COMMANDS = read
OPTIONAL FLAG -- <file>, file to read from
EX: read file.txt
"""},
    {'LOAD': """
READ -- load object program to memory
COMMANDS = load
REQUIRED FLAG -- <file>, file to load from
EX: load file.txt
"""},
    {'EXIT': """
EXIT -- stops debugger
COMMANDS = exit
EX: exit
"""}
]


class PrintHelp(Command):
    def __init__(self, command: str):
        super().__init__()
        self.command = command.upper() if command is not None else command

    def execute(self, inputs=None) -> str:
        string = ''
        if self.command is None:
            string = """
type help get these commands 

#type help all to see all commands 
RUN -- Runs all instructions until break point is hit
NEXT -- Runs next command 
BREAK -- Sets a break point at a memory location 
DISAS -- Converts machine code to low level symbolic language 
PRINT -- Print the value of given command 
REGISTER --Gets register value
MEMORY -- Gets memory value
CAST -- Caste value of given command 
SET -- Sets memory or register value 
SAVE -- Saves memory to memory file 
READ -- Retrieves memory from memory file 
LOAD -- loads object program to memory
EXIT -- exits program

a = 0
x = 1
l = 2
b = 3
s = 4
t = 5
f = 6
p = 8
pc = 8
w = 9
sw = 9
"""
        if self.command == "ALL":
            for h in helps:
                for v in h.values():
                    string += v
        else:
            for h in helps:
                for v in h:
                    if self.command == v:
                        string += str(h[v])
        return string
