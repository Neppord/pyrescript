from purescript.corefn import load_python_foreign
from purescript.corefn.abs import NativeX
from purescript.corefn.literals import Record, Int, Data
from purescript.corefn.parsing import load_module
from purescript.bytecode import LoadConstant, LoadExternal, Bytecode, Apply, NativeCall, StoreLocal, Declaration, \
    LoadLocal, JumpAbsoluteIfNotEqual, AccessField, AssignField, Duplicate, Pop, JumpAbsolute, MakeData, \
    GuardConstructor
from purescript.bytecode.emitter import Emitter
from purescript.prim import prim


class BytecodeInterpreter(object):

    def __init__(self):
        self.__loaded_modules = {}

    def load_module(self, module_name):
        if module_name in prim:
            return prim[module_name]
        if module_name not in self.__loaded_modules:
            self.__loaded_modules[module_name] = {}
            error = None

            try:
                foreign = load_python_foreign(module_name)
                self.__loaded_modules[module_name] = foreign
            except NotImplementedError as e:
                error = e
                foreign = {}

            try:
                loaded_module = load_module(module_name)
                module_bytecode = Bytecode(module_name)
                Emitter(module_bytecode).emit(loaded_module)
                namespace = {}
                namespace.update(foreign)
                self.__loaded_modules[module_name] = namespace
                self.interpret(module_bytecode, namespace)
            except IOError:
                if error:
                    raise error
        return self.__loaded_modules[module_name]

    def interpret(self, bytecode, frame=None):
        pc = 0
        value_stack = []
        call_stack = []
        if frame is None:
            frame = {}
        while 1:
            while len(bytecode.opcodes) <= pc:
                if call_stack:
                    bytecode, pc = call_stack.pop()
                elif value_stack:
                    return value_stack.pop()
                else:
                    return None
            opcode = bytecode.opcodes[pc]
            if isinstance(opcode, LoadConstant):
                value_stack.append(bytecode.constants[opcode.index])
            elif isinstance(opcode, LoadExternal):
                if (
                        opcode.module in [b.name for b, _ in call_stack] or
                        opcode.module == bytecode.name
                ) and opcode.name in frame:
                    value_stack.append(frame[opcode.name])
                else:
                    module_frame = self.load_module(opcode.module)
                    if opcode.name not in module_frame:
                        raise ValueError(opcode)
                    decl = module_frame[opcode.name]
                    value_stack.append(decl)
            elif isinstance(opcode, Apply):
                func = value_stack.pop()
                if isinstance(func, Bytecode):
                    call_stack.append((bytecode, pc + 1))
                    bytecode = func
                    pc = 0
                    continue
                elif isinstance(func, Data):
                    arg = value_stack.pop()
                    value_stack.append(Data(func.name, func.length, func.members + [arg]))
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
                new_record = {k: v for k, v in record.obj.items()}
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
            elif isinstance(opcode, MakeData):
                value_stack.append(Data(opcode.name, opcode.length, []))
            elif isinstance(opcode, GuardConstructor):
                data = value_stack.pop()
                if data.name == opcode.name:
                    for m in data.members[::-1]:
                        value_stack.append(m)
                else:
                    value_stack.append(data)
                    pc = opcode.address
                    continue
            else:
                raise NotImplementedError(opcode)
            pc += 1
