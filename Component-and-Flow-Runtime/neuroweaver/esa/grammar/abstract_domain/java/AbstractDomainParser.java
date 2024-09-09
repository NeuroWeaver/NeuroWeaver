// Generated from /Users/joon/ohai.src/esa/grammar/abstract_domain/AbstractDomain.g by ANTLR 4.7.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class AbstractDomainParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.7.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, ABSTRACT=2, DOMAIN=3, CAPABILITY=4, INPUT=5, OUTPUT=6, STATE=7, 
		PARAM=8, IMPORT=9, AS=10, LEFT_CURLY=11, RIGHT_CURLY=12, LEFT_PAREN=13, 
		RIGHT_PAREN=14, COMMA=15, DEFAULT=16, REFERENCE=17, LANGUAGE=18, VERBATIM=19, 
		CODE=20, FILE=21, ID=22, WHITESPACE=23, COMMENT=24, INTLIT=25;
	public static final int
		RULE_start = 0, RULE_import_stmt_list = 1, RULE_import_stmt = 2, RULE_import_stmt_tail = 3, 
		RULE_namespace = 4, RULE_namespace_tail = 5, RULE_domain_def = 6, RULE_block = 7, 
		RULE_default_stmt = 8, RULE_capability_list = 9, RULE_capability = 10, 
		RULE_params = 11, RULE_capability_arg = 12, RULE_capability_arg_list = 13, 
		RULE_memory_interface = 14, RULE_data_type = 15, RULE_var = 16, RULE_var_id = 17;
	public static final String[] ruleNames = {
		"start", "import_stmt_list", "import_stmt", "import_stmt_tail", "namespace", 
		"namespace_tail", "domain_def", "block", "default_stmt", "capability_list", 
		"capability", "params", "capability_arg", "capability_arg_list", "memory_interface", 
		"data_type", "var", "var_id"
	};

	private static final String[] _LITERAL_NAMES = {
		null, "'.'", "'abstract'", "'domain'", "'capability'", "'input'", "'output'", 
		"'state'", "'param'", "'import'", "'as'", "'{'", "'}'", "'('", "')'", 
		"','", "'default'", "'reference'", "'language'", "'verbatim'", "'code'", 
		"'file'"
	};
	private static final String[] _SYMBOLIC_NAMES = {
		null, null, "ABSTRACT", "DOMAIN", "CAPABILITY", "INPUT", "OUTPUT", "STATE", 
		"PARAM", "IMPORT", "AS", "LEFT_CURLY", "RIGHT_CURLY", "LEFT_PAREN", "RIGHT_PAREN", 
		"COMMA", "DEFAULT", "REFERENCE", "LANGUAGE", "VERBATIM", "CODE", "FILE", 
		"ID", "WHITESPACE", "COMMENT", "INTLIT"
	};
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "AbstractDomain.g"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public AbstractDomainParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}
	public static class StartContext extends ParserRuleContext {
		public Import_stmt_listContext import_stmt_list() {
			return getRuleContext(Import_stmt_listContext.class,0);
		}
		public Domain_defContext domain_def() {
			return getRuleContext(Domain_defContext.class,0);
		}
		public StartContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_start; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterStart(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitStart(this);
		}
	}

	public final StartContext start() throws RecognitionException {
		StartContext _localctx = new StartContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_start);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(36);
			import_stmt_list();
			setState(37);
			domain_def();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Import_stmt_listContext extends ParserRuleContext {
		public List<Import_stmtContext> import_stmt() {
			return getRuleContexts(Import_stmtContext.class);
		}
		public Import_stmtContext import_stmt(int i) {
			return getRuleContext(Import_stmtContext.class,i);
		}
		public Import_stmt_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_import_stmt_list; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterImport_stmt_list(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitImport_stmt_list(this);
		}
	}

	public final Import_stmt_listContext import_stmt_list() throws RecognitionException {
		Import_stmt_listContext _localctx = new Import_stmt_listContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_import_stmt_list);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(42);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==IMPORT) {
				{
				{
				setState(39);
				import_stmt();
				}
				}
				setState(44);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Import_stmtContext extends ParserRuleContext {
		public TerminalNode IMPORT() { return getToken(AbstractDomainParser.IMPORT, 0); }
		public NamespaceContext namespace() {
			return getRuleContext(NamespaceContext.class,0);
		}
		public Import_stmt_tailContext import_stmt_tail() {
			return getRuleContext(Import_stmt_tailContext.class,0);
		}
		public Import_stmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_import_stmt; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterImport_stmt(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitImport_stmt(this);
		}
	}

	public final Import_stmtContext import_stmt() throws RecognitionException {
		Import_stmtContext _localctx = new Import_stmtContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_import_stmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(45);
			match(IMPORT);
			setState(46);
			namespace();
			setState(47);
			import_stmt_tail();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Import_stmt_tailContext extends ParserRuleContext {
		public TerminalNode AS() { return getToken(AbstractDomainParser.AS, 0); }
		public TerminalNode ID() { return getToken(AbstractDomainParser.ID, 0); }
		public Import_stmt_tailContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_import_stmt_tail; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterImport_stmt_tail(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitImport_stmt_tail(this);
		}
	}

	public final Import_stmt_tailContext import_stmt_tail() throws RecognitionException {
		Import_stmt_tailContext _localctx = new Import_stmt_tailContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_import_stmt_tail);
		try {
			setState(52);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case AS:
				enterOuterAlt(_localctx, 1);
				{
				setState(49);
				match(AS);
				setState(50);
				match(ID);
				}
				break;
			case EOF:
			case ABSTRACT:
			case IMPORT:
				enterOuterAlt(_localctx, 2);
				{
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class NamespaceContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(AbstractDomainParser.ID, 0); }
		public Namespace_tailContext namespace_tail() {
			return getRuleContext(Namespace_tailContext.class,0);
		}
		public NamespaceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_namespace; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterNamespace(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitNamespace(this);
		}
	}

	public final NamespaceContext namespace() throws RecognitionException {
		NamespaceContext _localctx = new NamespaceContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_namespace);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(54);
			match(ID);
			setState(55);
			namespace_tail();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Namespace_tailContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(AbstractDomainParser.ID, 0); }
		public Namespace_tailContext namespace_tail() {
			return getRuleContext(Namespace_tailContext.class,0);
		}
		public Namespace_tailContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_namespace_tail; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterNamespace_tail(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitNamespace_tail(this);
		}
	}

	public final Namespace_tailContext namespace_tail() throws RecognitionException {
		Namespace_tailContext _localctx = new Namespace_tailContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_namespace_tail);
		try {
			setState(61);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__0:
				enterOuterAlt(_localctx, 1);
				{
				setState(57);
				match(T__0);
				setState(58);
				match(ID);
				setState(59);
				namespace_tail();
				}
				break;
			case EOF:
			case ABSTRACT:
			case IMPORT:
			case AS:
				enterOuterAlt(_localctx, 2);
				{
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Domain_defContext extends ParserRuleContext {
		public TerminalNode ABSTRACT() { return getToken(AbstractDomainParser.ABSTRACT, 0); }
		public TerminalNode DOMAIN() { return getToken(AbstractDomainParser.DOMAIN, 0); }
		public TerminalNode ID() { return getToken(AbstractDomainParser.ID, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public Domain_defContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_domain_def; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterDomain_def(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitDomain_def(this);
		}
	}

	public final Domain_defContext domain_def() throws RecognitionException {
		Domain_defContext _localctx = new Domain_defContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_domain_def);
		try {
			setState(68);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ABSTRACT:
				enterOuterAlt(_localctx, 1);
				{
				setState(63);
				match(ABSTRACT);
				setState(64);
				match(DOMAIN);
				setState(65);
				match(ID);
				setState(66);
				block();
				}
				break;
			case EOF:
				enterOuterAlt(_localctx, 2);
				{
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class BlockContext extends ParserRuleContext {
		public TerminalNode LEFT_CURLY() { return getToken(AbstractDomainParser.LEFT_CURLY, 0); }
		public Default_stmtContext default_stmt() {
			return getRuleContext(Default_stmtContext.class,0);
		}
		public Capability_listContext capability_list() {
			return getRuleContext(Capability_listContext.class,0);
		}
		public TerminalNode RIGHT_CURLY() { return getToken(AbstractDomainParser.RIGHT_CURLY, 0); }
		public BlockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_block; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterBlock(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitBlock(this);
		}
	}

	public final BlockContext block() throws RecognitionException {
		BlockContext _localctx = new BlockContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_block);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(70);
			match(LEFT_CURLY);
			setState(71);
			default_stmt();
			setState(72);
			capability_list();
			setState(73);
			match(RIGHT_CURLY);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Default_stmtContext extends ParserRuleContext {
		public TerminalNode DEFAULT() { return getToken(AbstractDomainParser.DEFAULT, 0); }
		public TerminalNode REFERENCE() { return getToken(AbstractDomainParser.REFERENCE, 0); }
		public TerminalNode ID() { return getToken(AbstractDomainParser.ID, 0); }
		public Default_stmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_default_stmt; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterDefault_stmt(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitDefault_stmt(this);
		}
	}

	public final Default_stmtContext default_stmt() throws RecognitionException {
		Default_stmtContext _localctx = new Default_stmtContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_default_stmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(75);
			match(DEFAULT);
			setState(76);
			match(REFERENCE);
			setState(77);
			match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Capability_listContext extends ParserRuleContext {
		public List<CapabilityContext> capability() {
			return getRuleContexts(CapabilityContext.class);
		}
		public CapabilityContext capability(int i) {
			return getRuleContext(CapabilityContext.class,i);
		}
		public Capability_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_capability_list; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterCapability_list(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitCapability_list(this);
		}
	}

	public final Capability_listContext capability_list() throws RecognitionException {
		Capability_listContext _localctx = new Capability_listContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_capability_list);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(82);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==CAPABILITY) {
				{
				{
				setState(79);
				capability();
				}
				}
				setState(84);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class CapabilityContext extends ParserRuleContext {
		public TerminalNode CAPABILITY() { return getToken(AbstractDomainParser.CAPABILITY, 0); }
		public TerminalNode ID() { return getToken(AbstractDomainParser.ID, 0); }
		public TerminalNode LEFT_PAREN() { return getToken(AbstractDomainParser.LEFT_PAREN, 0); }
		public ParamsContext params() {
			return getRuleContext(ParamsContext.class,0);
		}
		public TerminalNode RIGHT_PAREN() { return getToken(AbstractDomainParser.RIGHT_PAREN, 0); }
		public CapabilityContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_capability; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterCapability(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitCapability(this);
		}
	}

	public final CapabilityContext capability() throws RecognitionException {
		CapabilityContext _localctx = new CapabilityContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_capability);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(85);
			match(CAPABILITY);
			setState(86);
			match(ID);
			setState(87);
			match(LEFT_PAREN);
			setState(88);
			params();
			setState(89);
			match(RIGHT_PAREN);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ParamsContext extends ParserRuleContext {
		public Capability_argContext capability_arg() {
			return getRuleContext(Capability_argContext.class,0);
		}
		public Capability_arg_listContext capability_arg_list() {
			return getRuleContext(Capability_arg_listContext.class,0);
		}
		public ParamsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_params; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterParams(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitParams(this);
		}
	}

	public final ParamsContext params() throws RecognitionException {
		ParamsContext _localctx = new ParamsContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_params);
		try {
			setState(95);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,5,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(91);
				capability_arg();
				setState(92);
				capability_arg_list();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Capability_argContext extends ParserRuleContext {
		public Memory_interfaceContext memory_interface() {
			return getRuleContext(Memory_interfaceContext.class,0);
		}
		public Data_typeContext data_type() {
			return getRuleContext(Data_typeContext.class,0);
		}
		public VarContext var() {
			return getRuleContext(VarContext.class,0);
		}
		public Capability_argContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_capability_arg; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterCapability_arg(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitCapability_arg(this);
		}
	}

	public final Capability_argContext capability_arg() throws RecognitionException {
		Capability_argContext _localctx = new Capability_argContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_capability_arg);
		try {
			setState(102);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case INPUT:
			case OUTPUT:
			case STATE:
			case PARAM:
				enterOuterAlt(_localctx, 1);
				{
				setState(97);
				memory_interface();
				setState(98);
				data_type();
				setState(99);
				var();
				}
				break;
			case RIGHT_PAREN:
			case COMMA:
				enterOuterAlt(_localctx, 2);
				{
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Capability_arg_listContext extends ParserRuleContext {
		public TerminalNode COMMA() { return getToken(AbstractDomainParser.COMMA, 0); }
		public Capability_argContext capability_arg() {
			return getRuleContext(Capability_argContext.class,0);
		}
		public Capability_arg_listContext capability_arg_list() {
			return getRuleContext(Capability_arg_listContext.class,0);
		}
		public Capability_arg_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_capability_arg_list; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterCapability_arg_list(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitCapability_arg_list(this);
		}
	}

	public final Capability_arg_listContext capability_arg_list() throws RecognitionException {
		Capability_arg_listContext _localctx = new Capability_arg_listContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_capability_arg_list);
		try {
			setState(109);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case COMMA:
				enterOuterAlt(_localctx, 1);
				{
				setState(104);
				match(COMMA);
				setState(105);
				capability_arg();
				setState(106);
				capability_arg_list();
				}
				break;
			case RIGHT_PAREN:
				enterOuterAlt(_localctx, 2);
				{
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Memory_interfaceContext extends ParserRuleContext {
		public TerminalNode INPUT() { return getToken(AbstractDomainParser.INPUT, 0); }
		public TerminalNode OUTPUT() { return getToken(AbstractDomainParser.OUTPUT, 0); }
		public TerminalNode STATE() { return getToken(AbstractDomainParser.STATE, 0); }
		public TerminalNode PARAM() { return getToken(AbstractDomainParser.PARAM, 0); }
		public Memory_interfaceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_memory_interface; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterMemory_interface(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitMemory_interface(this);
		}
	}

	public final Memory_interfaceContext memory_interface() throws RecognitionException {
		Memory_interfaceContext _localctx = new Memory_interfaceContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_memory_interface);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(111);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << INPUT) | (1L << OUTPUT) | (1L << STATE) | (1L << PARAM))) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Data_typeContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(AbstractDomainParser.ID, 0); }
		public Data_typeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_data_type; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterData_type(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitData_type(this);
		}
	}

	public final Data_typeContext data_type() throws RecognitionException {
		Data_typeContext _localctx = new Data_typeContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_data_type);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(113);
			match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class VarContext extends ParserRuleContext {
		public Var_idContext var_id() {
			return getRuleContext(Var_idContext.class,0);
		}
		public VarContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_var; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterVar(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitVar(this);
		}
	}

	public final VarContext var() throws RecognitionException {
		VarContext _localctx = new VarContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_var);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(115);
			var_id();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Var_idContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(AbstractDomainParser.ID, 0); }
		public Var_idContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_var_id; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).enterVar_id(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof AbstractDomainListener ) ((AbstractDomainListener)listener).exitVar_id(this);
		}
	}

	public final Var_idContext var_id() throws RecognitionException {
		Var_idContext _localctx = new Var_idContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_var_id);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(117);
			match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\33z\4\2\t\2\4\3\t"+
		"\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4"+
		"\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23"+
		"\t\23\3\2\3\2\3\2\3\3\7\3+\n\3\f\3\16\3.\13\3\3\4\3\4\3\4\3\4\3\5\3\5"+
		"\3\5\5\5\67\n\5\3\6\3\6\3\6\3\7\3\7\3\7\3\7\5\7@\n\7\3\b\3\b\3\b\3\b\3"+
		"\b\5\bG\n\b\3\t\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\13\7\13S\n\13\f\13\16"+
		"\13V\13\13\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\5\rb\n\r\3\16\3\16"+
		"\3\16\3\16\3\16\5\16i\n\16\3\17\3\17\3\17\3\17\3\17\5\17p\n\17\3\20\3"+
		"\20\3\21\3\21\3\22\3\22\3\23\3\23\3\23\2\2\24\2\4\6\b\n\f\16\20\22\24"+
		"\26\30\32\34\36 \"$\2\3\3\2\7\n\2o\2&\3\2\2\2\4,\3\2\2\2\6/\3\2\2\2\b"+
		"\66\3\2\2\2\n8\3\2\2\2\f?\3\2\2\2\16F\3\2\2\2\20H\3\2\2\2\22M\3\2\2\2"+
		"\24T\3\2\2\2\26W\3\2\2\2\30a\3\2\2\2\32h\3\2\2\2\34o\3\2\2\2\36q\3\2\2"+
		"\2 s\3\2\2\2\"u\3\2\2\2$w\3\2\2\2&\'\5\4\3\2\'(\5\16\b\2(\3\3\2\2\2)+"+
		"\5\6\4\2*)\3\2\2\2+.\3\2\2\2,*\3\2\2\2,-\3\2\2\2-\5\3\2\2\2.,\3\2\2\2"+
		"/\60\7\13\2\2\60\61\5\n\6\2\61\62\5\b\5\2\62\7\3\2\2\2\63\64\7\f\2\2\64"+
		"\67\7\30\2\2\65\67\3\2\2\2\66\63\3\2\2\2\66\65\3\2\2\2\67\t\3\2\2\289"+
		"\7\30\2\29:\5\f\7\2:\13\3\2\2\2;<\7\3\2\2<=\7\30\2\2=@\5\f\7\2>@\3\2\2"+
		"\2?;\3\2\2\2?>\3\2\2\2@\r\3\2\2\2AB\7\4\2\2BC\7\5\2\2CD\7\30\2\2DG\5\20"+
		"\t\2EG\3\2\2\2FA\3\2\2\2FE\3\2\2\2G\17\3\2\2\2HI\7\r\2\2IJ\5\22\n\2JK"+
		"\5\24\13\2KL\7\16\2\2L\21\3\2\2\2MN\7\22\2\2NO\7\23\2\2OP\7\30\2\2P\23"+
		"\3\2\2\2QS\5\26\f\2RQ\3\2\2\2SV\3\2\2\2TR\3\2\2\2TU\3\2\2\2U\25\3\2\2"+
		"\2VT\3\2\2\2WX\7\6\2\2XY\7\30\2\2YZ\7\17\2\2Z[\5\30\r\2[\\\7\20\2\2\\"+
		"\27\3\2\2\2]^\5\32\16\2^_\5\34\17\2_b\3\2\2\2`b\3\2\2\2a]\3\2\2\2a`\3"+
		"\2\2\2b\31\3\2\2\2cd\5\36\20\2de\5 \21\2ef\5\"\22\2fi\3\2\2\2gi\3\2\2"+
		"\2hc\3\2\2\2hg\3\2\2\2i\33\3\2\2\2jk\7\21\2\2kl\5\32\16\2lm\5\34\17\2"+
		"mp\3\2\2\2np\3\2\2\2oj\3\2\2\2on\3\2\2\2p\35\3\2\2\2qr\t\2\2\2r\37\3\2"+
		"\2\2st\7\30\2\2t!\3\2\2\2uv\5$\23\2v#\3\2\2\2wx\7\30\2\2x%\3\2\2\2\n,"+
		"\66?FTaho";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}