import sys

from purescript.corefn import interpret_foreign, load_python_foreign
from purescript.corefn.parsing import load_module
from interpreter import Interpreter
from rpython.rlib.objectmodel import not_rpython


def entry_point(argv):
    module_name_argument, = argv[1:2] or ["Main"]
    Interpreter(interpret_foreign, load_module).run_main(load_module(module_name_argument))
    return 0


def target(*args):
    return entry_point, None

@not_rpython
def interpret(argv):
    module_name_argument, = argv[1:2] or ["Main"]
    Interpreter(load_python_foreign, load_module).run_main(load_module(module_name_argument))
    return 0


if __name__ == "__main__":
    interpret(sys.argv)
