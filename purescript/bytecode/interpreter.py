from purescript.corefn import load_python_foreign
from purescript.corefn.value import Record, Data, Closure, NativeX, Array
from purescript.corefn.parsing import load_module
from purescript.bytecode import LoadConstant, LoadExternal, Bytecode, Apply, NativeCall, StoreLocal, Declaration, \
    LoadLocal, JumpAbsoluteIfNotEqual, AccessField, AssignField, Duplicate, Pop, JumpAbsolute, MakeData, \
    GuardConstructor, GuardValue, Stash, RestoreStash, DropStash, Lambda, GuardArray
from purescript.bytecode.emitter import Emitter
from purescript.prim import prim


def print_trace(trace):
    ret = []
    for b, p in trace:
        if len(b.opcodes) <= p:
            continue
        code = b.opcodes[p]
        if isinstance(code, LoadConstant):
            ret.append(b.constants[code.index])
        else:
            ret.append(code)
    return ret


class BaseFrame(object):
    def __init__(self, bytecode, pc, vars_):
        assert isinstance(bytecode, Bytecode)
        self.bytecode = bytecode
        assert isinstance(pc, int)
        self.pc = pc
        assert isinstance(vars_, dict)
        self.vars = vars_

    def get_opcode(self):
        return self.bytecode.opcodes[self.pc]

    def get_constant(self):
        op = self.bytecode.opcodes[self.pc]
        assert isinstance(op, LoadConstant)
        return self.bytecode.constants[op.index]

    def is_done(self):
        return len(self.bytecode.opcodes) <= self.pc

    def get_var(self, name):
        return self.vars[name]

    def has_var(self, name):
        return name in self.vars

    def set_var(self, name, value):
        self.vars[name] = value

    def get_module_name(self):
        return self.bytecode.name

    def get_module_frame(self):
        return self

    def get_closure(self):
        closure = {}
        closure.update(self.vars)
        return closure


class CallFrame(BaseFrame):
    def __init__(self, parent, bytecode, pc, vars_):
        super(CallFrame, self).__init__(bytecode, pc, vars_)
        assert isinstance(parent, BaseFrame)
        self.parent = parent

    def get_var(self, name):
        if name in self.vars:
            return self.vars[name]
        else:
            return self.parent.get_var(name)

    def has_var(self, name):
        return name in self.vars or self.parent.has_var(name)

    def get_module_name(self):
        return self.parent.get_module_name()

    def get_module_frame(self):
        return self.parent

    def get_closure(self):
        closure = self.parent.get_closure()
        closure.update(self.vars)
        return closure


class ClosureFrame(object):

    def __int__(self, closure, parent):
        pass


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
                module_frame = BaseFrame(module_bytecode, 0, namespace)
                self.__loaded_modules[module_name] = namespace
                self.interpret(module_bytecode, module_frame)
            except IOError:
                if error:
                    raise error
        return self.__loaded_modules[module_name]

    def interpret(self, bytecode, frame=None):
        value_stack = []
        stash = []
        if frame is None:
            frame = BaseFrame(bytecode, 0, {})
        else:
            assert isinstance(frame, BaseFrame)
            assert bytecode == frame.bytecode
        trace = []
        while 1:
            trace.append((frame.bytecode, frame.pc))
            while frame.is_done():
                if isinstance(frame, CallFrame):
                    frame = frame.parent
                elif value_stack:
                    return value_stack.pop()
                else:
                    return None
            opcode = frame.get_opcode()
            if isinstance(opcode, LoadConstant):
                value_stack.append(frame.get_constant())
            elif isinstance(opcode, Lambda):
                value_stack.append(Closure(frame.get_closure(), opcode.bytecode))
            elif isinstance(opcode, LoadExternal):
                if opcode.module == frame.get_module_name():
                    if frame.get_module_frame().has_var(opcode.name):
                        value_stack.append(frame.get_module_frame().get_var(opcode.name))
                    else:
                        module_name = opcode.module
                        name = opcode.name
                        loaded_module = load_module(module_name)
                        # TODO, or should the name be module name only
                        declaration_bytecode = Bytecode(module_name + "." + name)
                        found = None
                        for declaration in loaded_module.declarations():
                            if declaration.name == name:
                                found = declaration
                                break
                        if found is None:
                            raise ValueError("could not find declaration %s in %s" % (name, module_name))
                        Emitter(declaration_bytecode).emit(found)
                        get_module_frame = BaseFrame(declaration_bytecode, 0, frame.get_module_frame().vars)
                        value = self.interpret(declaration_bytecode, get_module_frame)
                        frame.set_var(name, value)
                        value_stack.append(value)
                else:
                    module_frame = self.load_module(opcode.module)
                    if opcode.name not in module_frame:
                        raise ValueError(opcode)
                    decl = module_frame[opcode.name]
                    value_stack.append(decl)
            elif isinstance(opcode, Apply):
                func = value_stack.pop()
                if isinstance(func, Closure):
                    frame.pc += 1
                    frame = CallFrame(frame, func.bytecode, 0, func.vars)
                    continue
                elif isinstance(func, Data):
                    arg = value_stack.pop()
                    value_stack.append(Data(func.name, func.length, func.members + [arg]))
                elif isinstance(func, NativeX):
                    if func.x <= func.arguments:
                        arg = value_stack.pop()
                        args = func.arguments + [arg]
                        if len(args) == func.x:
                            value_stack.append(func.native(*args))
                        else:
                            value_stack.append(NativeX(func.native, func.x, args))
                    else:
                        value_stack.append(func.native(*func.arguments))
                else:
                    raise NotImplementedError("cant call %s" % func.__repr__())
            elif isinstance(opcode, NativeCall):
                value_stack.append(NativeX(opcode.native, opcode.number_of_args, []))
            elif isinstance(opcode, StoreLocal):
                frame.set_var(opcode.name, value_stack.pop())
            elif isinstance(opcode, Declaration):
                value_stack.append(opcode.bytecode)
            elif isinstance(opcode, Duplicate):
                value = value_stack.pop()
                value_stack.append(value)
                value_stack.append(value)
            elif isinstance(opcode, Pop):
                if value_stack:
                    value_stack.pop()
                else:
                    raise ValueError("Stack was empty")
            elif isinstance(opcode, LoadLocal):
                value = frame.get_var(opcode.name)
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
                    frame.pc = opcode.address
                    continue
                else:
                    pass
            elif isinstance(opcode, JumpAbsolute):
                frame.pc = opcode.address
                continue
            elif isinstance(opcode, MakeData):
                value_stack.append(Data(opcode.name, opcode.length, []))
            elif isinstance(opcode, GuardConstructor):
                data = value_stack.pop()
                if data.name == opcode.name:
                    for a in data.members[::-1]:
                        value_stack.append(a)
                else:
                    value_stack.append(data)
                    frame.pc = opcode.address
                    continue
            elif isinstance(opcode, GuardArray):
                data = value_stack.pop()
                if isinstance(data, Array) and len(data.array) == opcode.lenght:
                    for a in data.array[::-1]:
                        value_stack.append(a)
                else:
                    value_stack.append(data)
                    frame.pc = opcode.address
                    continue
            elif isinstance(opcode, GuardValue):
                value = value_stack.pop()
                if not value == opcode.value:
                    frame.pc = opcode.address
                    continue
            elif isinstance(opcode, Stash):
                stash.append([v for v in value_stack])
            elif isinstance(opcode, RestoreStash):
                value_stack = [v for v in stash[-1]]
            elif isinstance(opcode, DropStash):
                stash.pop()
            else:
                raise NotImplementedError(opcode)
            frame.pc += 1
