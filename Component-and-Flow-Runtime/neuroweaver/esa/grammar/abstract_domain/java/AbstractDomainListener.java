// Generated from /Users/joon/ohai.src/esa/grammar/abstract_domain/AbstractDomain.g by ANTLR 4.7.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link AbstractDomainParser}.
 */
public interface AbstractDomainListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#start}.
	 * @param ctx the parse tree
	 */
	void enterStart(AbstractDomainParser.StartContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#start}.
	 * @param ctx the parse tree
	 */
	void exitStart(AbstractDomainParser.StartContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#import_stmt_list}.
	 * @param ctx the parse tree
	 */
	void enterImport_stmt_list(AbstractDomainParser.Import_stmt_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#import_stmt_list}.
	 * @param ctx the parse tree
	 */
	void exitImport_stmt_list(AbstractDomainParser.Import_stmt_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#import_stmt}.
	 * @param ctx the parse tree
	 */
	void enterImport_stmt(AbstractDomainParser.Import_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#import_stmt}.
	 * @param ctx the parse tree
	 */
	void exitImport_stmt(AbstractDomainParser.Import_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#import_stmt_tail}.
	 * @param ctx the parse tree
	 */
	void enterImport_stmt_tail(AbstractDomainParser.Import_stmt_tailContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#import_stmt_tail}.
	 * @param ctx the parse tree
	 */
	void exitImport_stmt_tail(AbstractDomainParser.Import_stmt_tailContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#namespace}.
	 * @param ctx the parse tree
	 */
	void enterNamespace(AbstractDomainParser.NamespaceContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#namespace}.
	 * @param ctx the parse tree
	 */
	void exitNamespace(AbstractDomainParser.NamespaceContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#namespace_tail}.
	 * @param ctx the parse tree
	 */
	void enterNamespace_tail(AbstractDomainParser.Namespace_tailContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#namespace_tail}.
	 * @param ctx the parse tree
	 */
	void exitNamespace_tail(AbstractDomainParser.Namespace_tailContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#domain_def}.
	 * @param ctx the parse tree
	 */
	void enterDomain_def(AbstractDomainParser.Domain_defContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#domain_def}.
	 * @param ctx the parse tree
	 */
	void exitDomain_def(AbstractDomainParser.Domain_defContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#block}.
	 * @param ctx the parse tree
	 */
	void enterBlock(AbstractDomainParser.BlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#block}.
	 * @param ctx the parse tree
	 */
	void exitBlock(AbstractDomainParser.BlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#default_stmt}.
	 * @param ctx the parse tree
	 */
	void enterDefault_stmt(AbstractDomainParser.Default_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#default_stmt}.
	 * @param ctx the parse tree
	 */
	void exitDefault_stmt(AbstractDomainParser.Default_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#capability_list}.
	 * @param ctx the parse tree
	 */
	void enterCapability_list(AbstractDomainParser.Capability_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#capability_list}.
	 * @param ctx the parse tree
	 */
	void exitCapability_list(AbstractDomainParser.Capability_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#capability}.
	 * @param ctx the parse tree
	 */
	void enterCapability(AbstractDomainParser.CapabilityContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#capability}.
	 * @param ctx the parse tree
	 */
	void exitCapability(AbstractDomainParser.CapabilityContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#params}.
	 * @param ctx the parse tree
	 */
	void enterParams(AbstractDomainParser.ParamsContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#params}.
	 * @param ctx the parse tree
	 */
	void exitParams(AbstractDomainParser.ParamsContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#capability_arg}.
	 * @param ctx the parse tree
	 */
	void enterCapability_arg(AbstractDomainParser.Capability_argContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#capability_arg}.
	 * @param ctx the parse tree
	 */
	void exitCapability_arg(AbstractDomainParser.Capability_argContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#capability_arg_list}.
	 * @param ctx the parse tree
	 */
	void enterCapability_arg_list(AbstractDomainParser.Capability_arg_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#capability_arg_list}.
	 * @param ctx the parse tree
	 */
	void exitCapability_arg_list(AbstractDomainParser.Capability_arg_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#memory_interface}.
	 * @param ctx the parse tree
	 */
	void enterMemory_interface(AbstractDomainParser.Memory_interfaceContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#memory_interface}.
	 * @param ctx the parse tree
	 */
	void exitMemory_interface(AbstractDomainParser.Memory_interfaceContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#data_type}.
	 * @param ctx the parse tree
	 */
	void enterData_type(AbstractDomainParser.Data_typeContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#data_type}.
	 * @param ctx the parse tree
	 */
	void exitData_type(AbstractDomainParser.Data_typeContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#var}.
	 * @param ctx the parse tree
	 */
	void enterVar(AbstractDomainParser.VarContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#var}.
	 * @param ctx the parse tree
	 */
	void exitVar(AbstractDomainParser.VarContext ctx);
	/**
	 * Enter a parse tree produced by {@link AbstractDomainParser#var_id}.
	 * @param ctx the parse tree
	 */
	void enterVar_id(AbstractDomainParser.Var_idContext ctx);
	/**
	 * Exit a parse tree produced by {@link AbstractDomainParser#var_id}.
	 * @param ctx the parse tree
	 */
	void exitVar_id(AbstractDomainParser.Var_idContext ctx);
}