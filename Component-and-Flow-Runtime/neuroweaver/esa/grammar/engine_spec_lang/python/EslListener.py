# Generated from /Users/joon/ohai.src/esa/grammar/engine_spec_lang/Esl.g by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .EslParser import EslParser
else:
    from EslParser import EslParser

# This class defines a complete listener for a parse tree produced by EslParser.
class EslListener(ParseTreeListener):

    # Enter a parse tree produced by EslParser#start.
    def enterStart(self, ctx:EslParser.StartContext):
        pass

    # Exit a parse tree produced by EslParser#start.
    def exitStart(self, ctx:EslParser.StartContext):
        pass


    # Enter a parse tree produced by EslParser#import_stmt_list.
    def enterImport_stmt_list(self, ctx:EslParser.Import_stmt_listContext):
        pass

    # Exit a parse tree produced by EslParser#import_stmt_list.
    def exitImport_stmt_list(self, ctx:EslParser.Import_stmt_listContext):
        pass


    # Enter a parse tree produced by EslParser#import_stmt.
    def enterImport_stmt(self, ctx:EslParser.Import_stmtContext):
        pass

    # Exit a parse tree produced by EslParser#import_stmt.
    def exitImport_stmt(self, ctx:EslParser.Import_stmtContext):
        pass


    # Enter a parse tree produced by EslParser#import_stmt_tail.
    def enterImport_stmt_tail(self, ctx:EslParser.Import_stmt_tailContext):
        pass

    # Exit a parse tree produced by EslParser#import_stmt_tail.
    def exitImport_stmt_tail(self, ctx:EslParser.Import_stmt_tailContext):
        pass


    # Enter a parse tree produced by EslParser#namespace.
    def enterNamespace(self, ctx:EslParser.NamespaceContext):
        pass

    # Exit a parse tree produced by EslParser#namespace.
    def exitNamespace(self, ctx:EslParser.NamespaceContext):
        pass


    # Enter a parse tree produced by EslParser#namespace_tail.
    def enterNamespace_tail(self, ctx:EslParser.Namespace_tailContext):
        pass

    # Exit a parse tree produced by EslParser#namespace_tail.
    def exitNamespace_tail(self, ctx:EslParser.Namespace_tailContext):
        pass


    # Enter a parse tree produced by EslParser#id_or_star.
    def enterId_or_star(self, ctx:EslParser.Id_or_starContext):
        pass

    # Exit a parse tree produced by EslParser#id_or_star.
    def exitId_or_star(self, ctx:EslParser.Id_or_starContext):
        pass


    # Enter a parse tree produced by EslParser#engine_def.
    def enterEngine_def(self, ctx:EslParser.Engine_defContext):
        pass

    # Exit a parse tree produced by EslParser#engine_def.
    def exitEngine_def(self, ctx:EslParser.Engine_defContext):
        pass


    # Enter a parse tree produced by EslParser#impl.
    def enterImpl(self, ctx:EslParser.ImplContext):
        pass

    # Exit a parse tree produced by EslParser#impl.
    def exitImpl(self, ctx:EslParser.ImplContext):
        pass


    # Enter a parse tree produced by EslParser#block.
    def enterBlock(self, ctx:EslParser.BlockContext):
        pass

    # Exit a parse tree produced by EslParser#block.
    def exitBlock(self, ctx:EslParser.BlockContext):
        pass


    # Enter a parse tree produced by EslParser#interface_decl_list.
    def enterInterface_decl_list(self, ctx:EslParser.Interface_decl_listContext):
        pass

    # Exit a parse tree produced by EslParser#interface_decl_list.
    def exitInterface_decl_list(self, ctx:EslParser.Interface_decl_listContext):
        pass


    # Enter a parse tree produced by EslParser#interface_decl.
    def enterInterface_decl(self, ctx:EslParser.Interface_declContext):
        pass

    # Exit a parse tree produced by EslParser#interface_decl.
    def exitInterface_decl(self, ctx:EslParser.Interface_declContext):
        pass


    # Enter a parse tree produced by EslParser#capability_list.
    def enterCapability_list(self, ctx:EslParser.Capability_listContext):
        pass

    # Exit a parse tree produced by EslParser#capability_list.
    def exitCapability_list(self, ctx:EslParser.Capability_listContext):
        pass


    # Enter a parse tree produced by EslParser#capability.
    def enterCapability(self, ctx:EslParser.CapabilityContext):
        pass

    # Exit a parse tree produced by EslParser#capability.
    def exitCapability(self, ctx:EslParser.CapabilityContext):
        pass


    # Enter a parse tree produced by EslParser#params.
    def enterParams(self, ctx:EslParser.ParamsContext):
        pass

    # Exit a parse tree produced by EslParser#params.
    def exitParams(self, ctx:EslParser.ParamsContext):
        pass


    # Enter a parse tree produced by EslParser#capability_arg.
    def enterCapability_arg(self, ctx:EslParser.Capability_argContext):
        pass

    # Exit a parse tree produced by EslParser#capability_arg.
    def exitCapability_arg(self, ctx:EslParser.Capability_argContext):
        pass


    # Enter a parse tree produced by EslParser#capability_arg_list.
    def enterCapability_arg_list(self, ctx:EslParser.Capability_arg_listContext):
        pass

    # Exit a parse tree produced by EslParser#capability_arg_list.
    def exitCapability_arg_list(self, ctx:EslParser.Capability_arg_listContext):
        pass


    # Enter a parse tree produced by EslParser#param_interface.
    def enterParam_interface(self, ctx:EslParser.Param_interfaceContext):
        pass

    # Exit a parse tree produced by EslParser#param_interface.
    def exitParam_interface(self, ctx:EslParser.Param_interfaceContext):
        pass


    # Enter a parse tree produced by EslParser#literals.
    def enterLiterals(self, ctx:EslParser.LiteralsContext):
        pass

    # Exit a parse tree produced by EslParser#literals.
    def exitLiterals(self, ctx:EslParser.LiteralsContext):
        pass


    # Enter a parse tree produced by EslParser#literal.
    def enterLiteral(self, ctx:EslParser.LiteralContext):
        pass

    # Exit a parse tree produced by EslParser#literal.
    def exitLiteral(self, ctx:EslParser.LiteralContext):
        pass


    # Enter a parse tree produced by EslParser#literal_list.
    def enterLiteral_list(self, ctx:EslParser.Literal_listContext):
        pass

    # Exit a parse tree produced by EslParser#literal_list.
    def exitLiteral_list(self, ctx:EslParser.Literal_listContext):
        pass


    # Enter a parse tree produced by EslParser#memory_interface.
    def enterMemory_interface(self, ctx:EslParser.Memory_interfaceContext):
        pass

    # Exit a parse tree produced by EslParser#memory_interface.
    def exitMemory_interface(self, ctx:EslParser.Memory_interfaceContext):
        pass


    # Enter a parse tree produced by EslParser#data_type.
    def enterData_type(self, ctx:EslParser.Data_typeContext):
        pass

    # Exit a parse tree produced by EslParser#data_type.
    def exitData_type(self, ctx:EslParser.Data_typeContext):
        pass


    # Enter a parse tree produced by EslParser#data_type_tail.
    def enterData_type_tail(self, ctx:EslParser.Data_type_tailContext):
        pass

    # Exit a parse tree produced by EslParser#data_type_tail.
    def exitData_type_tail(self, ctx:EslParser.Data_type_tailContext):
        pass


    # Enter a parse tree produced by EslParser#var.
    def enterVar(self, ctx:EslParser.VarContext):
        pass

    # Exit a parse tree produced by EslParser#var.
    def exitVar(self, ctx:EslParser.VarContext):
        pass


    # Enter a parse tree produced by EslParser#var_id.
    def enterVar_id(self, ctx:EslParser.Var_idContext):
        pass

    # Exit a parse tree produced by EslParser#var_id.
    def exitVar_id(self, ctx:EslParser.Var_idContext):
        pass


    # Enter a parse tree produced by EslParser#touch.
    def enterTouch(self, ctx:EslParser.TouchContext):
        pass

    # Exit a parse tree produced by EslParser#touch.
    def exitTouch(self, ctx:EslParser.TouchContext):
        pass


    # Enter a parse tree produced by EslParser#cap_block.
    def enterCap_block(self, ctx:EslParser.Cap_blockContext):
        pass

    # Exit a parse tree produced by EslParser#cap_block.
    def exitCap_block(self, ctx:EslParser.Cap_blockContext):
        pass


    # Enter a parse tree produced by EslParser#specs.
    def enterSpecs(self, ctx:EslParser.SpecsContext):
        pass

    # Exit a parse tree produced by EslParser#specs.
    def exitSpecs(self, ctx:EslParser.SpecsContext):
        pass


    # Enter a parse tree produced by EslParser#spec.
    def enterSpec(self, ctx:EslParser.SpecContext):
        pass

    # Exit a parse tree produced by EslParser#spec.
    def exitSpec(self, ctx:EslParser.SpecContext):
        pass


    # Enter a parse tree produced by EslParser#spec_list.
    def enterSpec_list(self, ctx:EslParser.Spec_listContext):
        pass

    # Exit a parse tree produced by EslParser#spec_list.
    def exitSpec_list(self, ctx:EslParser.Spec_listContext):
        pass


    # Enter a parse tree produced by EslParser#attr.
    def enterAttr(self, ctx:EslParser.AttrContext):
        pass

    # Exit a parse tree produced by EslParser#attr.
    def exitAttr(self, ctx:EslParser.AttrContext):
        pass


    # Enter a parse tree produced by EslParser#attr_id.
    def enterAttr_id(self, ctx:EslParser.Attr_idContext):
        pass

    # Exit a parse tree produced by EslParser#attr_id.
    def exitAttr_id(self, ctx:EslParser.Attr_idContext):
        pass


    # Enter a parse tree produced by EslParser#qualifier.
    def enterQualifier(self, ctx:EslParser.QualifierContext):
        pass

    # Exit a parse tree produced by EslParser#qualifier.
    def exitQualifier(self, ctx:EslParser.QualifierContext):
        pass


    # Enter a parse tree produced by EslParser#attr_val.
    def enterAttr_val(self, ctx:EslParser.Attr_valContext):
        pass

    # Exit a parse tree produced by EslParser#attr_val.
    def exitAttr_val(self, ctx:EslParser.Attr_valContext):
        pass


