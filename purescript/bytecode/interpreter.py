from corefn import load_python_foreign
from corefn.abs import NativeX
from corefn.literals import Record
from corefn.parsing import load_module
from purescript.bytecode import LoadConstant, LoadExternal, Bytecode, Apply, NativeCall, StoreLocal, Declaration, \
    LoadLocal, JumpAbsoluteIfNotEqual, AccessField, AssignField, Duplicate, Pop, JumpAbsolute
from purescript.bytecode.emitter import Emitter


class BytecodeInterpreter(object):

    def __init__(self, loaded_modules, loaded_foreign_modules):
        self.__loaded_modules = loaded_modules
        self.__loaded_foreign_modules = loaded_foreign_modules

    def load_module(self, module_name):
        if module_name not in self.__loaded_modules:
            loaded_module = load_module(module_name)
            module_bytecode = Bytecode(module_name)
            Emitter(module_bytecode).emit(loaded_module)
            self.__loaded_modules[module_name] = module_bytecode
        return self.__loaded_modules[module_name]

    def load_foreign_module(self, module_name):
        if module_name not in self.__loaded_foreign_modules:
            loaded_module = load_python_foreign(module_name)
            module_bytecode = Bytecode(module_name)
            Emitter(module_bytecode).emit(loaded_module)
            self.__loaded_foreign_modules[module_name] = module_bytecode
        return self.__loaded_foreign_modules[module_name]

    def interpret(self, bytecode, value_stack=None, call_stack=None):
        pc = 0
        if not value_stack:
            value_stack = []
        if not call_stack:
            call_stack = []
        frame = {}
        while 1:
            while len(bytecode.opcodes) <= pc:
                if call_stack:
                    bytecode, pc = call_stack.pop()
                else:
                    return value_stack.pop()
            opcode = bytecode.opcodes[pc]
            if isinstance(opcode, LoadConstant):
                value_stack.append(bytecode.constants[opcode.index])
            elif isinstance(opcode, LoadExternal):
                try:
                    module_bytecode = self.load_module(opcode.module)
                    decl = module_bytecode.decl(opcode.name)
                except (IOError, KeyError):
                    module_bytecode = self.load_foreign_module(opcode.module)
                    decl = module_bytecode.decl(opcode.name)
                call_stack.append((bytecode, pc + 1))
                bytecode = decl
                pc = 0
                continue
            elif isinstance(opcode, Apply):
                func = value_stack.pop()
                if isinstance(func, Bytecode):
                    call_stack.append((bytecode, pc + 1))
                    bytecode = func
                    pc = 0
                    continue
                elif isinstance(func, NativeX):
                    arg = value_stack.pop()
                    args = func.arguments + [arg]
                    if len(args) == func.x:
                        value_stack.append(func.native(None, *args))
                    else:
                        value_stack.append(NativeX(
                            func.native,
                            func.x,
                            args
                        ))
                else:
                    raise NotImplementedError("cant call %s" % func.__repr__())
            elif isinstance(opcode, NativeCall):
                value_stack.append(NativeX(opcode.native, opcode.number_of_args, []))
            elif isinstance(opcode, StoreLocal):
                frame[opcode.name] = value_stack.pop()
            elif isinstance(opcode, Declaration):
                value_stack.append(opcode.bytecode)
            elif isinstance(opcode, Duplicate):
                value = value_stack.pop()
                value_stack.append(value)
                value_stack.append(value)
            elif isinstance(opcode, Pop):
                value_stack.pop()
            elif isinstance(opcode, LoadLocal):
                value = frame[opcode.name]
                value_stack.append(value)
            elif isinstance(opcode, AccessField):
                record = value_stack.pop()
                assert isinstance(record, Record)
                value_stack.append(record.obj[opcode.name])
            elif isinstance(opcode, AssignField):
                value = value_stack.pop()
                record = value_stack.pop()
                assert isinstance(record, Record)
                new_record = {k:v for k,v in record.obj.items()}
                new_record[opcode.name] = value
                value_stack.append(Record(new_record))
            elif isinstance(opcode, JumpAbsoluteIfNotEqual):
                v1 = value_stack.pop()
                v2 = value_stack.pop()
                if v1 != v2:
                    pc = opcode.address
                    continue
                else:
                    pass
            elif isinstance(opcode, JumpAbsolute):
                pc = opcode.address
                continue
            else:
                raise NotImplementedError(opcode)
            pc += 1
