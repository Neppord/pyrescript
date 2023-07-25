import corefn
from corefn import ModuleInterface
from corefn.abs import Abs, Native1, Native2
from corefn.binders import NullBinder, BoolBinder, NewtypeBinder, VarBinder
from corefn.case import Case, Alternative
from corefn.expression import App, Let, Accessor
from corefn.literals import Box, RecordLiteral, Record, Boolean
from corefn.var import LocalVar, ExternalVar
from purescript.bytecode import Bytecode


class Emitter(object):
    def __init__(self, bytecode):
        self.bytecode = bytecode

    def emit(self, ast):
        if isinstance(ast, Box):
            self.bytecode.emit_load_constant(ast)
        elif isinstance(ast, App):
            self.emit(ast.argument)
            self.emit(ast.abstraction)
            self.bytecode.emit_apply()
        elif isinstance(ast, ExternalVar):
            self.bytecode.emit_load_external(ast.module_name, ast.name)
        elif isinstance(ast, Abs):
            name = "\\%s -> " % ast.argument
            bytecode = Bytecode(name)
            emitter = Emitter(bytecode)
            emitter.bytecode.emit_store(ast.argument)
            emitter.emit(ast.body)
            self.bytecode.emit_declaration(name, emitter.bytecode)
        elif isinstance(ast, Case):
            assert len(ast.expressions) == 1
            go_to_ends = []
            for expression in ast.expressions:
                self.emit(expression)
            for alternative in ast.alternatives:
                binder, = alternative.binders
                if isinstance(binder, NullBinder):
                    self.bytecode.emit_pop()
                    self.emit(alternative.expression)
                    go_to_ends.append(self.bytecode.emit_jump())
                elif isinstance(binder, VarBinder):
                    self.bytecode.emit_store(binder.name)
                    self.emit(alternative.expression)
                    go_to_ends.append(self.bytecode.emit_jump())
                elif isinstance(binder, NewtypeBinder):
                    binder, = binder.binders
                    if isinstance(binder, VarBinder):
                        self.bytecode.emit_store(binder.name)
                        self.emit(alternative.expression)
                        go_to_ends.append(self.bytecode.emit_jump())
                    else:
                        raise NotImplementedError()
                elif isinstance(binder, BoolBinder):
                    self.bytecode.emit_duplicate()
                    self.bytecode.emit_load_constant(Boolean(binder.value))
                    jump = self.bytecode.emit_jump_if_not_equal()
                    self.bytecode.emit_pop()
                    self.emit(alternative.expression)
                    go_to_ends.append(self.bytecode.emit_jump())
                    jump.address = len(self.bytecode.opcodes)
                else:
                    raise NotImplementedError()
            for go_to_end in go_to_ends:
                go_to_end.address = len(self.bytecode.opcodes)
        elif isinstance(ast, Alternative):
            for binder in ast.binders:
                self.emit(binder)
            self.emit(ast.expression)
        elif isinstance(ast, Let):
            for name, _ast in ast.binds.items():
                self.emit(_ast)
                self.bytecode.emit_store(name)
            self.emit(ast.expression)
        elif isinstance(ast, LocalVar):
            self.bytecode.emit_load_declaration(ast.name)
        elif isinstance(ast, Accessor):
            self.emit(ast.expression)
            self.bytecode.emit_access_field(ast.field_name)
        elif isinstance(ast, ModuleInterface):
            for name, _ast in ast.declarations().items():
                bytecode = Bytecode(name)
                emitter = Emitter(bytecode)
                emitter.emit(_ast)
                self.bytecode.emit_declaration(name, emitter.bytecode)
        elif isinstance(ast, corefn.Declaration):
            self.emit(ast.expression)
        elif isinstance(ast, Native1):
            self.bytecode.emit_native_call(ast.native, 1)
        elif isinstance(ast, Native2):
            self.bytecode.emit_native_call(ast.native, 2)
        elif isinstance(ast, RecordLiteral):
            self.bytecode.emit_load_constant(Record({}))
            for key, value in ast.obj.items():
                self.emit(value)
                self.bytecode.emit_assign_field(key)
        else:
            raise NotImplementedError("%r: %r" % (type(ast), ast))
