import sys

from purescript.corefn import interpret_foreign, load_python_foreign
from purescript.corefn.literals import Effect
from purescript.corefn.parsing import load_module
from interpreter import Interpreter


def target(*args):
    _, module_names = args
    module_name, = module_names
    interpreter = Interpreter(load_python_foreign, load_module)
    module = load_module(module_name)
    module.preload_imports(interpreter)
    decl = module.decl("main")  # type: Expression
    main = decl.expression.eval(interpreter, {})
    assert isinstance(main, Effect)

    def entry_point(argv):
        main.run_effect(interpreter)
        return 0

    return entry_point, None


if __name__ == '__main__':
    program, _ = target(None, sys.argv[1:2])
    program(sys.argv[2:])
