import sys
import time
from util import NUM, BIG, SICXE_CC_GT, LITTLE, INT

SICXE_DEVICE_IN = 0xf1
SICXE_DEVICE_OUT = 0x05
SICXE_DEVICE_ER = 0x00


class Device:
    def __init__(self):
        self.id = ''

    def test(self, register: NUM):
        cc = SICXE_CC_GT
        register.setbits(cc, (6, 8), BIG)

    def read(self, register: NUM):
        return

    def write(self, register: NUM):
        pass


class Output(Device):
    def __init__(self):
        super(Output, self).__init__()
        self.id = 'OUT'
        self.stdout = sys.stdout
        self.lastwrite = 0x00

    def read(self, register: NUM):
        register.setbits(self.lastwrite, (0, 8),LITTLE)
        return self.lastwrite

    def write(self, register: NUM):
        byte = register.getbits((0, 8), order=LITTLE)
        self.lastwrite = byte
        self.stdout.write(chr(byte))
        self.stdout.flush()


class Input(Device):
    def __init__(self):
        super(Input, self).__init__()
        self.id = 'IN'
        self.stdin = sys.stdin

    def read(self, register: NUM):
        byte = self.stdin.readline(1)
        register.setbits(ord(byte), (0, 8), LITTLE)
        return


class Error(Device):
    def __init__(self):
        super(Error, self).__init__()
        self.id = 'ER'
        self.stderr = sys.stderr

    def write(self, register: NUM):
        byte = register.getbits((0, 8), order=LITTLE)
        self.stderr.write(chr(byte))
        self.stderr.flush()


class Devices:
    def __init__(self, size):
        self.devices = [Device()] * size
        self.devices[SICXE_DEVICE_OUT] = Output()
        self.devices[SICXE_DEVICE_IN] = Input()
        self.devices[SICXE_DEVICE_ER] = Error()

    def __getitem__(self, addr: int):
        addr %= len(self.devices)
        return self.devices[addr]

    def __setitem__(self, addr: int, device: Device):
        addr %= len(self.devices)
        self.devices[addr] = device
