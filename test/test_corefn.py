import glob
import os
import sys
from subprocess import check_call

import pytest

from interpreter import Interpreter
from purescript.corefn import load_python_foreign
from purescript.corefn.parsing import load_module

dirname = os.path.dirname(__file__)
glob_expression = os.path.join(dirname, "e2e", "*", "expected.txt")
test_directories = [
    os.path.dirname(os.path.relpath(path))
    for path in glob.glob(glob_expression)
]

sys.setrecursionlimit(2**11)
@pytest.mark.parametrize("test_directory", test_directories)
def test_e2e(test_directory, monkeypatch, capsys):
    monkeypatch.chdir(test_directory)
    check_call(
        ["spago", "build", "--purs-args", "--codegen corefn"],
        shell=True
    )
    capsys.readouterr()
    interpreter = Interpreter(load_python_foreign, load_module)
    main = load_module("Main")
    main.preload_imports(interpreter)
    interpreter.run_main(main)
    with open("expected.txt") as f:
        expected = f.read()
    assert capsys.readouterr().out == expected
