from pykd import *
from common import *


def main():
    ext = pykd.isWindbgExt()

    try:
        if not ext:
            process_name = sys.argv[1]
            attach_process(process_name)

        allocConsole()
    except Exception as errtxt:
        print(errtxt)
    finally:
        if not ext:
            pykd.detachAllProcesses()


if __name__ == "__main__":
    main()
