import glob
import importlib
import os
import sys

import pytest

from corefn import interpret_foreign, load_python_foreign
from corefn.parsing import load_module
from interpreter import Interpreter
from subprocess import check_call

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
