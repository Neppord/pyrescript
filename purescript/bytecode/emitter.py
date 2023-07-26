from purescript import corefn
from purescript.corefn import ModuleInterface
from purescript.corefn.abs import Abs, NativeX, Constructor
from purescript.corefn.binders import NullBinder, BoolBinder, NewtypeBinder, VarBinder, ConstructorBinder, \
    ArrayLiteralBinder
from purescript.corefn.case import Case, Alternative
from purescript.corefn.expression import App, Let, Accessor
from purescript.corefn.literals import Box, RecordLiteral, Record, Boolean
from purescript.corefn.var import LocalVar, ExternalVar
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
            self.bytecode.emit_load_constant(emitter.bytecode)
        elif isinstance(ast, Case):
            go_to_ends = []
            for expression in ast.expressions:
                self.emit(expression)
            for alternative in ast.alternatives:
                go_to_ends.extend(alternative.emit_alternative_bytecode(self))
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
                self.bytecode.emit_declaration(emitter.bytecode)
        elif isinstance(ast, corefn.Declaration):
            self.emit(ast.expression)
        elif isinstance(ast, NativeX):
            self.bytecode.emit_native_call(ast.native, ast.x)
        elif isinstance(ast, RecordLiteral):
            self.bytecode.emit_load_constant(Record({}))
            for key, value in ast.obj.items():
                self.emit(value)
                self.bytecode.emit_assign_field(key)
        elif isinstance(ast, Constructor):
            self.bytecode.emit_make_data(ast.name, len(ast.field_names))
        else:
            raise NotImplementedError("%r: %r" % (type(ast), ast))
