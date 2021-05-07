from loader.objectCode import ObjectCode, parseObjectFile
from vm import CU


def load(cu: CU, file=None, objectCode=None):
    objectCode = parseObjectFile(file) if file is not None else objectCode
    firstExecutable = objectCode.e.columns[1].toInt()
    cu.setStartingAddress(firstExecutable)

    for textRecord in objectCode.t.textRecords:
        startAddr = textRecord.columns[1].toInt()
        bytes = textRecord.columns[3].toBytes()
        cu.mem.setBytearray(startAddr, bytes)
    return objectCode
