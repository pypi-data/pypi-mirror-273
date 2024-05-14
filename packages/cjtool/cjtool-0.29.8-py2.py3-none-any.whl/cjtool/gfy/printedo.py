import pykd
from cjtool.stl import *
from cjtool.common import *
import pyperclip as pc
import argparse


def getEdoInfo(edoId) -> str:
    stringVar = malloc_wstring("")
    Void = pykd.typeInfo("Void")
    functype = pykd.defineFunction(Void, pykd.callingConvention.NearC)
    functype.append("argret", pykd.baseTypes.VoidPtr)
    functype.append("id", pykd.baseTypes.Int8B)
    printEdoWPtr = pykd.typedVar("GFCCommon!getEdoW")
    pykd.callFunctionByAddr(
        functype, printEdoWPtr.getAddress(), stringVar.getAddress(), edoId)
    value = wstring(stringVar.getAddress())
    return str(value)


def getShape(edoId) -> str:
    stringVar = malloc_string("")
    Void = pykd.typeInfo("Void")
    functype = pykd.defineFunction(Void, pykd.callingConvention.NearC)
    functype.append("argret", pykd.baseTypes.VoidPtr)
    functype.append("id", pykd.baseTypes.Int8B)
    printEdoWPtr = pykd.typedVar("GFCCommon!getShape")
    pykd.callFunctionByAddr(
        functype, printEdoWPtr.getAddress(), stringVar.getAddress(), edoId)
    value = string(stringVar.getAddress())
    return str(value)


def main():
    parser = argparse.ArgumentParser(description="Input the edoid")
    parser.add_argument("edoid", type=int, help="The GFY Edo Id")
    args = parser.parse_args()
    edoid = args.edoid

    ext = pykd.isWindbgExt()
    try:
        if not ext:
            pykd.initialize()
            pid = getProcessByName("gfy4.exe")
            if pid == 0:
                print("The app: {} is not found".format("gfy4.exe"))
                exit()

            pykd.attachProcess(pid)

        # 下行的代码，bp不能省去，否则pykd.go就不返回了
        bp = pykd.setBp(pykd.getOffset(
            'Qt5Core!QEventDispatcherWin32::processEvents'))
        ret = pykd.go()
        if ret == pykd.executionStatus.Break:
            edoInfo = getEdoInfo(edoid)
            print(edoInfo)

        ret = pykd.go()
        if ret == pykd.executionStatus.Break:
            szShape = getShape(edoid)
            print(szShape)
            pc.copy(szShape)

    except Exception as errtxt:
        print(errtxt)
    finally:
        if not ext:
            pykd.detachAllProcesses()


if __name__ == "__main__":
    main()
