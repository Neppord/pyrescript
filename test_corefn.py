from corefn.parsing import load_module
from foreign import curry
from interpreter import Interpreter
from subprocess import check_call


def test_curry():
    assert curry(lambda a, b: a - b, 2)(2)(1) == 1

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
