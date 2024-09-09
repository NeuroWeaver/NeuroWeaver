// Generated from /Users/joon/ohai.src/esa/grammar/engine_spec_lang/Esl.g by ANTLR 4.7.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link EslParser}.
 */
public interface EslListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link EslParser#start}.
	 * @param ctx the parse tree
	 */
	void enterStart(EslParser.StartContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#start}.
	 * @param ctx the parse tree
	 */
	void exitStart(EslParser.StartContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#import_stmt_list}.
	 * @param ctx the parse tree
	 */
	void enterImport_stmt_list(EslParser.Import_stmt_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#import_stmt_list}.
	 * @param ctx the parse tree
	 */
	void exitImport_stmt_list(EslParser.Import_stmt_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#import_stmt}.
	 * @param ctx the parse tree
	 */
	void enterImport_stmt(EslParser.Import_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#import_stmt}.
	 * @param ctx the parse tree
	 */
	void exitImport_stmt(EslParser.Import_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#import_stmt_tail}.
	 * @param ctx the parse tree
	 */
	void enterImport_stmt_tail(EslParser.Import_stmt_tailContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#import_stmt_tail}.
	 * @param ctx the parse tree
	 */
	void exitImport_stmt_tail(EslParser.Import_stmt_tailContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#namespace}.
	 * @param ctx the parse tree
	 */
	void enterNamespace(EslParser.NamespaceContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#namespace}.
	 * @param ctx the parse tree
	 */
	void exitNamespace(EslParser.NamespaceContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#namespace_tail}.
	 * @param ctx the parse tree
	 */
	void enterNamespace_tail(EslParser.Namespace_tailContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#namespace_tail}.
	 * @param ctx the parse tree
	 */
	void exitNamespace_tail(EslParser.Namespace_tailContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#id_or_star}.
	 * @param ctx the parse tree
	 */
	void enterId_or_star(EslParser.Id_or_starContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#id_or_star}.
	 * @param ctx the parse tree
	 */
	void exitId_or_star(EslParser.Id_or_starContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#engine_def}.
	 * @param ctx the parse tree
	 */
	void enterEngine_def(EslParser.Engine_defContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#engine_def}.
	 * @param ctx the parse tree
	 */
	void exitEngine_def(EslParser.Engine_defContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#impl}.
	 * @param ctx the parse tree
	 */
	void enterImpl(EslParser.ImplContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#impl}.
	 * @param ctx the parse tree
	 */
	void exitImpl(EslParser.ImplContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#block}.
	 * @param ctx the parse tree
	 */
	void enterBlock(EslParser.BlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#block}.
	 * @param ctx the parse tree
	 */
	void exitBlock(EslParser.BlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#interface_decl_list}.
	 * @param ctx the parse tree
	 */
	void enterInterface_decl_list(EslParser.Interface_decl_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#interface_decl_list}.
	 * @param ctx the parse tree
	 */
	void exitInterface_decl_list(EslParser.Interface_decl_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#interface_decl}.
	 * @param ctx the parse tree
	 */
	void enterInterface_decl(EslParser.Interface_declContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#interface_decl}.
	 * @param ctx the parse tree
	 */
	void exitInterface_decl(EslParser.Interface_declContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#capability_list}.
	 * @param ctx the parse tree
	 */
	void enterCapability_list(EslParser.Capability_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#capability_list}.
	 * @param ctx the parse tree
	 */
	void exitCapability_list(EslParser.Capability_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#capability}.
	 * @param ctx the parse tree
	 */
	void enterCapability(EslParser.CapabilityContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#capability}.
	 * @param ctx the parse tree
	 */
	void exitCapability(EslParser.CapabilityContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#params}.
	 * @param ctx the parse tree
	 */
	void enterParams(EslParser.ParamsContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#params}.
	 * @param ctx the parse tree
	 */
	void exitParams(EslParser.ParamsContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#capability_arg}.
	 * @param ctx the parse tree
	 */
	void enterCapability_arg(EslParser.Capability_argContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#capability_arg}.
	 * @param ctx the parse tree
	 */
	void exitCapability_arg(EslParser.Capability_argContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#capability_arg_list}.
	 * @param ctx the parse tree
	 */
	void enterCapability_arg_list(EslParser.Capability_arg_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#capability_arg_list}.
	 * @param ctx the parse tree
	 */
	void exitCapability_arg_list(EslParser.Capability_arg_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#param_interface}.
	 * @param ctx the parse tree
	 */
	void enterParam_interface(EslParser.Param_interfaceContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#param_interface}.
	 * @param ctx the parse tree
	 */
	void exitParam_interface(EslParser.Param_interfaceContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#literals}.
	 * @param ctx the parse tree
	 */
	void enterLiterals(EslParser.LiteralsContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#literals}.
	 * @param ctx the parse tree
	 */
	void exitLiterals(EslParser.LiteralsContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#literal}.
	 * @param ctx the parse tree
	 */
	void enterLiteral(EslParser.LiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#literal}.
	 * @param ctx the parse tree
	 */
	void exitLiteral(EslParser.LiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#literal_list}.
	 * @param ctx the parse tree
	 */
	void enterLiteral_list(EslParser.Literal_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#literal_list}.
	 * @param ctx the parse tree
	 */
	void exitLiteral_list(EslParser.Literal_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#memory_interface}.
	 * @param ctx the parse tree
	 */
	void enterMemory_interface(EslParser.Memory_interfaceContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#memory_interface}.
	 * @param ctx the parse tree
	 */
	void exitMemory_interface(EslParser.Memory_interfaceContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#data_type}.
	 * @param ctx the parse tree
	 */
	void enterData_type(EslParser.Data_typeContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#data_type}.
	 * @param ctx the parse tree
	 */
	void exitData_type(EslParser.Data_typeContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#data_type_tail}.
	 * @param ctx the parse tree
	 */
	void enterData_type_tail(EslParser.Data_type_tailContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#data_type_tail}.
	 * @param ctx the parse tree
	 */
	void exitData_type_tail(EslParser.Data_type_tailContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#var}.
	 * @param ctx the parse tree
	 */
	void enterVar(EslParser.VarContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#var}.
	 * @param ctx the parse tree
	 */
	void exitVar(EslParser.VarContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#var_id}.
	 * @param ctx the parse tree
	 */
	void enterVar_id(EslParser.Var_idContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#var_id}.
	 * @param ctx the parse tree
	 */
	void exitVar_id(EslParser.Var_idContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#touch}.
	 * @param ctx the parse tree
	 */
	void enterTouch(EslParser.TouchContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#touch}.
	 * @param ctx the parse tree
	 */
	void exitTouch(EslParser.TouchContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#cap_block}.
	 * @param ctx the parse tree
	 */
	void enterCap_block(EslParser.Cap_blockContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#cap_block}.
	 * @param ctx the parse tree
	 */
	void exitCap_block(EslParser.Cap_blockContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#specs}.
	 * @param ctx the parse tree
	 */
	void enterSpecs(EslParser.SpecsContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#specs}.
	 * @param ctx the parse tree
	 */
	void exitSpecs(EslParser.SpecsContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#spec}.
	 * @param ctx the parse tree
	 */
	void enterSpec(EslParser.SpecContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#spec}.
	 * @param ctx the parse tree
	 */
	void exitSpec(EslParser.SpecContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#spec_list}.
	 * @param ctx the parse tree
	 */
	void enterSpec_list(EslParser.Spec_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#spec_list}.
	 * @param ctx the parse tree
	 */
	void exitSpec_list(EslParser.Spec_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#attr}.
	 * @param ctx the parse tree
	 */
	void enterAttr(EslParser.AttrContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#attr}.
	 * @param ctx the parse tree
	 */
	void exitAttr(EslParser.AttrContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#attr_id}.
	 * @param ctx the parse tree
	 */
	void enterAttr_id(EslParser.Attr_idContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#attr_id}.
	 * @param ctx the parse tree
	 */
	void exitAttr_id(EslParser.Attr_idContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#qualifier}.
	 * @param ctx the parse tree
	 */
	void enterQualifier(EslParser.QualifierContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#qualifier}.
	 * @param ctx the parse tree
	 */
	void exitQualifier(EslParser.QualifierContext ctx);
	/**
	 * Enter a parse tree produced by {@link EslParser#attr_val}.
	 * @param ctx the parse tree
	 */
	void enterAttr_val(EslParser.Attr_valContext ctx);
	/**
	 * Exit a parse tree produced by {@link EslParser#attr_val}.
	 * @param ctx the parse tree
	 */
	void exitAttr_val(EslParser.Attr_valContext ctx);
}