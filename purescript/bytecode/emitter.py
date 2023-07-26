from purescript import corefn
from purescript.corefn import ModuleInterface
from purescript.corefn.abs import Abs, NativeX
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
                elif isinstance(binder, ConstructorBinder):
                    # TODO check Identifier
                    for member in binder.binders:
                        if isinstance(member, NullBinder):
                            self.bytecode.emit_pop()
                        elif isinstance(member, VarBinder):
                            self.bytecode.emit_store(member.name)
                        elif isinstance(member, NewtypeBinder):
                            newtype_binder, = member.binders
                            if isinstance(newtype_binder, VarBinder):
                                self.bytecode.emit_store(newtype_binder.name)
                            if isinstance(newtype_binder, ArrayLiteralBinder):
                                value, = newtype_binder.value
                                if isinstance(value, ConstructorBinder):
                                    value_member, = value.binders
                                    if isinstance(value_member, VarBinder):
                                        self.bytecode.emit_store(value_member.name)
                                    else:
                                        raise NotImplementedError()
                                else:
                                    raise NotImplementedError()
                            else:
                                raise NotImplementedError()
                        else:
                            raise NotImplementedError()
                    self.emit(alternative.expression)
                    go_to_ends.append(self.bytecode.emit_jump())
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
        else:
            raise NotImplementedError("%r: %r" % (type(ast), ast))
