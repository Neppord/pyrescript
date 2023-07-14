import sys

from corefn.parsing import load_module
from interpreter import Interpreter


def entry_point(argv):
    module_name_argument, = argv[1:1] or ["Main"]
    Interpreter(load_module).run_main(load_module(module_name_argument.split(".")))
    return 0


def target(*args):
    return entry_point, None


if __name__ == "__main__":
    entry_point(sys.argv)
