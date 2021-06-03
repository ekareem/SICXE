from typing import List

from asm import Program
from debug import Debugger
import sys

from loader import load
from vm import BUS
from vm.presistance import memoryWrite, MEMORYFILE, readToMemory


def assemble(file: str, obj=None, tab=None, cod=None, asClass=False):
    try:
        f = file
        if file.find('.') != -1:
            f = file[:file.find('.')]

        p = Program()

        p.parse(file)
        p.execute()

        if asClass:
            return p.sections[0].objectCode, p.sections[0].symtab, p.sections[0].datum

        obj = f + '.obj' if obj is None else obj
        p.writeObj(obj)
        tab = f + '.tab' if tab is None else tab
        p.writeTab(tab)
        cod = f + '.cod' if cod is None else cod
        p.writeCode(cod)

        return [obj, tab, cod]


    except BaseException as e:
        print(e)


def debug(file: str, isAsm=False, memoryFile=None):
    b = BUS()
    if memoryFile is not None:
        readToMemory(b.cu, memoryFile)
    symtab = None
    datatab = None
    if file is not None:
        if isAsm:
            obj, symtab, datatab = assemble(file, asClass=True)
            load(b.cu, None, objectCode=obj)
        else:
            load(b.cu, file)

    d = Debugger(b.cu, symtab, datatab=datatab)
    n = ''
    while n.strip() != 'exit':
        try:
            n = input(':>')
            if n.strip() != 'exit':
                c = d.evaluate(n)
                c.execute()
        except BaseException as e:
          print(e)


def run(file: str, isAsm=False, memfile=None, loadFile=None):
    try:
        b = BUS()

        if loadFile is not None:
            readToMemory(b.cu, loadFile)

        if isAsm:
            obj = assemble(file, asClass=True)[0]
            load(b.cu, None, objectCode=obj)
        else:
            load(b.cu, file)

        b.cu.runall()
        if memfile is not None:
            memoryWrite(b.cu, memfile)
    except BaseException as e:
        if memfile is not None:
            memoryWrite(b.cu, memfile)
        print(e)


commands = {
    ('asm', 'a', '-asm', '-a'): {
        '-asm': 'required flag creates object code and object program from assembly file',
        '\t<asm file>': 'assembles file to object code of .obj'
    },
    ('bug', 'b', '-bug', '-b'): {
        '-bug': 'required flag debugs assembly or object file',
        '\t-o <obj file>': 'debug program from object file',
        '\t-a <asm file>': 'debug program from assembly file',
        '\t-l <memory file>': 'loads to memory file to machine memory'
    },
    ('run', 'r', '-run', '-r'): {
        '-run': 'required flag runs an object file or assembly file',
        '\t-a <asm file>': 'run program from assmble file',
        '\t-o <obj file>': 'run program from object file',
        '\t-w <optional memory file>': 'writes to memory file',
        '\t-l <optional memory file>': 'loads to memory file to machine memory',
    }
}


def help(com=None):
    for command in commands:
        if com is not None and com in command:
            for helps in commands[command]:
                print(f'{helps} : {commands[command][helps]}')
        elif com is None:
            for helps in commands[command]:
                print(f'{helps} : {commands[command][helps]}')
        if com is None:
            print()


def commandDebug(args: List[str]):
    asAsm = False
    script = None
    memoryFile = None

    for i, arg in enumerate(args):
        if arg.strip().lower() in ('-o', '-obj', '-a', '-asm'):
            if script is not None:
                raise Exception("script file already set")
            if len(args) < i + 2:
                raise Exception(f"{arg} requires an assembly file")
            if arg.strip().lower() in ('-a', '-asm'):
                asAsm = True
            elif arg.strip().lower() in ('-o', '-obj'):
                asAsm = False
            script = args[i + 1]
        if arg.strip().lower() in ('-l', '-load'):
            if len(args) < i + 2:
                raise Exception(f"{arg} requires an memory file")
            memoryFile = args[i + 1]

    debug(script, asAsm, memoryFile)


def commandAsm(args: List[str]):
    file = None
    for i, arg in enumerate(args):
        if file is not None:
            raise Exception("too many arguments only one assembly file required")
        file = arg
    if file is None:
        raise Exception("no filename argument found")
    assemble(file)


def commandRun(args: List[str]):
    asAsm = False
    script = None
    loadFile = None
    memoryFile = None

    for i, arg in enumerate(args):
        if arg.strip().lower() in ('-o', '-obj', '-a', '-asm'):
            if script is not None:
                raise Exception("script file already set")
            if len(args) < i + 2:
                raise Exception(f"{arg} requires an assembly file")
            if arg.strip().lower() in ('-a', '-asm'):
                asAsm = True
            elif arg.strip().lower() in ('-o', '-obj'):
                asAsm = False
            script = args[i + 1]
        if arg.strip().lower() in ('-w', '-write'):
            if len(args) < i + 2:
                raise Exception(f"{arg} requires an memory file try memory.txt")
            memoryFile = args[i + 1]
        if arg.strip().lower() in ('-l', '-load'):
            if len(args) < i + 2:
                raise Exception(f"{arg} requires an memory file")
            loadFile = args[i + 1]

    run(script, asAsm, memoryFile, loadFile)


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2 or args[1] in ('-h', '-help', 'help', 'h'):
        help(None if len(args) < 3 else args[2] if args[2] in (
            '-b', 'b', '-bug', 'bug', 'run', 'r', '-run', '-r', 'asm', 'a', '-asm', '-a', 'run', 'r', '-run',
            '-r') else None)
    elif args[1] in ('-asm', '-a', 'asm', '-a'):
        commandAsm(args[2:])
    elif args[1] in ('-b', '-bug', 'b', 'bug'):
        commandDebug(args[2:])
    elif args[1] in ('-r', '-run', 'r', 'run'):
        asAsm = False if args[2] in ('-o', '-obj') else True if args[2] in ('-a', '-asm') else None
        file = args[3]
        i = 4
        mem = None
        if len(args) > i and args[i] == '-w':
            i += 1
            mem = args[i] if len(args) > i else MEMORYFILE

        run(file, asAsm, mem)
    else:
        help(None)
