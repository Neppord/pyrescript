from corefn import Interpreter, Module, load_module
from examples import hello_world, hello_concat
from foreign import curry
from lib import lib
from subprocess import check_call


def _load_module(module_name):
    return Module(lib[tuple(module_name)])


class ModuleStore(object):

    def __init__(self):
        self.modules = {}

    def add_lib(self, lib):
        for key, value in lib.items():
            self.add_module_dict(key, value)

    def add_module_dict(self, module_name, module):
        self.modules[tuple(module_name)] = Module(module)

    def load_module(self, module_name):
        return self.modules[tuple(module_name)]


def test_curry():
    assert curry(lambda a, b: a - b, 2)(2)(1) == 1


def test_hello_world(capsys):
    store = ModuleStore()
    store.add_lib(lib)
    store.add_module_dict(["Main"], hello_world)
    Interpreter(store.load_module).run_module_by_name(["Main"])
    assert capsys.readouterr().out == "hello world!\n"


def test_hello_concat(capsys):
    store = ModuleStore()
    store.add_lib(lib)
    store.add_module_dict(["Main"], hello_concat)
    Interpreter(store.load_module).run_module_by_name(["Main"])
    assert capsys.readouterr().out == "hello world!\n"


def test_e2e_fizz_buzz(monkeypatch, capsys):
    monkeypatch.chdir("e2e/fizz-buzz")
    check_call(["spago", "build", "--purs-args", "--codegen corefn"], shell=True)
    capsys.readouterr()
    Interpreter(load_module).run_main(load_module(["Main"]))
    assert capsys.readouterr().out == """\
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
"""
