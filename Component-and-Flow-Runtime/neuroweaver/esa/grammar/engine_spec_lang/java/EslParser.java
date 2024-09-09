// Generated from /Users/joon/ohai.src/esa/grammar/engine_spec_lang/Esl.g by ANTLR 4.7.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class EslParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.7.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, ENGINE=2, CAPABILITY=3, IMPORT=4, AS=5, LEFT_CURLY=6, RIGHT_CURLY=7, 
		LEFT_PAREN=8, RIGHT_PAREN=9, COMMA=10, DEFAULT=11, LANGUAGE=12, RUNTIME_COST=13, 
		VERBATIM=14, CODE=15, FILE=16, TOUCHES=17, IMPLEMENTS=18, INTERFACE=19, 
		ASSIGN=20, KLEENE_STAR=21, COLON=22, LEFT_BRACK=23, RIGHT_BRACK=24, ID=25, 
		WHITESPACE=26, COMMENT=27, INTLIT=28, STRING=29, STRING_LITERAL=30, BYTES_LITERAL=31, 
		NEWLINE=32;
	public static final int
		RULE_start = 0, RULE_import_stmt_list = 1, RULE_import_stmt = 2, RULE_import_stmt_tail = 3, 
		RULE_namespace = 4, RULE_namespace_tail = 5, RULE_id_or_star = 6, RULE_engine_def = 7, 
		RULE_impl = 8, RULE_block = 9, RULE_interface_decl_list = 10, RULE_interface_decl = 11, 
		RULE_capability_list = 12, RULE_capability = 13, RULE_params = 14, RULE_capability_arg = 15, 
		RULE_capability_arg_list = 16, RULE_param_interface = 17, RULE_literals = 18, 
		RULE_literal = 19, RULE_literal_list = 20, RULE_memory_interface = 21, 
		RULE_data_type = 22, RULE_data_type_tail = 23, RULE_var = 24, RULE_var_id = 25, 
		RULE_touch = 26, RULE_cap_block = 27, RULE_specs = 28, RULE_spec = 29, 
		RULE_spec_list = 30, RULE_attr = 31, RULE_attr_id = 32, RULE_qualifier = 33, 
		RULE_attr_val = 34;
	public static final String[] ruleNames = {
		"start", "import_stmt_list", "import_stmt", "import_stmt_tail", "namespace", 
		"namespace_tail", "id_or_star", "engine_def", "impl", "block", "interface_decl_list", 
		"interface_decl", "capability_list", "capability", "params", "capability_arg", 
		"capability_arg_list", "param_interface", "literals", "literal", "literal_list", 
		"memory_interface", "data_type", "data_type_tail", "var", "var_id", "touch", 
		"cap_block", "specs", "spec", "spec_list", "attr", "attr_id", "qualifier", 
		"attr_val"
	};

	private static final String[] _LITERAL_NAMES = {
		null, "'.'", "'engine'", "'capability'", "'import'", "'as'", "'{'", "'}'", 
		"'('", "')'", "','", "'default'", "'language'", "'runtime_cost'", "'verbatim'", 
		"'code'", "'file'", "'touches'", "'implements'", "'interface'", "'='", 
		"'*'", "':'", "'['", "']'"
	};
	private static final String[] _SYMBOLIC_NAMES = {
		null, null, "ENGINE", "CAPABILITY", "IMPORT", "AS", "LEFT_CURLY", "RIGHT_CURLY", 
		"LEFT_PAREN", "RIGHT_PAREN", "COMMA", "DEFAULT", "LANGUAGE", "RUNTIME_COST", 
		"VERBATIM", "CODE", "FILE", "TOUCHES", "IMPLEMENTS", "INTERFACE", "ASSIGN", 
		"KLEENE_STAR", "COLON", "LEFT_BRACK", "RIGHT_BRACK", "ID", "WHITESPACE", 
		"COMMENT", "INTLIT", "STRING", "STRING_LITERAL", "BYTES_LITERAL", "NEWLINE"
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
	public String getGrammarFileName() { return "Esl.g"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public EslParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}
	public static class StartContext extends ParserRuleContext {
		public Import_stmt_listContext import_stmt_list() {
			return getRuleContext(Import_stmt_listContext.class,0);
		}
		public Engine_defContext engine_def() {
			return getRuleContext(Engine_defContext.class,0);
		}
		public StartContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_start; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterStart(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitStart(this);
		}
	}

	public final StartContext start() throws RecognitionException {
		StartContext _localctx = new StartContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_start);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(70);
			import_stmt_list();
			setState(71);
			engine_def();
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
			if ( listener instanceof EslListener ) ((EslListener)listener).enterImport_stmt_list(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitImport_stmt_list(this);
		}
	}

	public final Import_stmt_listContext import_stmt_list() throws RecognitionException {
		Import_stmt_listContext _localctx = new Import_stmt_listContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_import_stmt_list);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(76);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==IMPORT) {
				{
				{
				setState(73);
				import_stmt();
				}
				}
				setState(78);
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
		public TerminalNode IMPORT() { return getToken(EslParser.IMPORT, 0); }
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
			if ( listener instanceof EslListener ) ((EslListener)listener).enterImport_stmt(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitImport_stmt(this);
		}
	}

	public final Import_stmtContext import_stmt() throws RecognitionException {
		Import_stmtContext _localctx = new Import_stmtContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_import_stmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(79);
			match(IMPORT);
			setState(80);
			namespace();
			setState(81);
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
		public TerminalNode AS() { return getToken(EslParser.AS, 0); }
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public Import_stmt_tailContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_import_stmt_tail; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterImport_stmt_tail(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitImport_stmt_tail(this);
		}
	}

	public final Import_stmt_tailContext import_stmt_tail() throws RecognitionException {
		Import_stmt_tailContext _localctx = new Import_stmt_tailContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_import_stmt_tail);
		try {
			setState(86);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case AS:
				enterOuterAlt(_localctx, 1);
				{
				setState(83);
				match(AS);
				setState(84);
				match(ID);
				}
				break;
			case EOF:
			case ENGINE:
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
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public Namespace_tailContext namespace_tail() {
			return getRuleContext(Namespace_tailContext.class,0);
		}
		public NamespaceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_namespace; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterNamespace(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitNamespace(this);
		}
	}

	public final NamespaceContext namespace() throws RecognitionException {
		NamespaceContext _localctx = new NamespaceContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_namespace);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(88);
			match(ID);
			setState(89);
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
		public Id_or_starContext id_or_star() {
			return getRuleContext(Id_or_starContext.class,0);
		}
		public Namespace_tailContext namespace_tail() {
			return getRuleContext(Namespace_tailContext.class,0);
		}
		public Namespace_tailContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_namespace_tail; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterNamespace_tail(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitNamespace_tail(this);
		}
	}

	public final Namespace_tailContext namespace_tail() throws RecognitionException {
		Namespace_tailContext _localctx = new Namespace_tailContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_namespace_tail);
		try {
			setState(96);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__0:
				enterOuterAlt(_localctx, 1);
				{
				setState(91);
				match(T__0);
				setState(92);
				id_or_star();
				setState(93);
				namespace_tail();
				}
				break;
			case EOF:
			case ENGINE:
			case CAPABILITY:
			case IMPORT:
			case AS:
			case RIGHT_CURLY:
			case INTERFACE:
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

	public static class Id_or_starContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public TerminalNode KLEENE_STAR() { return getToken(EslParser.KLEENE_STAR, 0); }
		public Id_or_starContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_id_or_star; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterId_or_star(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitId_or_star(this);
		}
	}

	public final Id_or_starContext id_or_star() throws RecognitionException {
		Id_or_starContext _localctx = new Id_or_starContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_id_or_star);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(98);
			_la = _input.LA(1);
			if ( !(_la==KLEENE_STAR || _la==ID) ) {
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

	public static class Engine_defContext extends ParserRuleContext {
		public TerminalNode ENGINE() { return getToken(EslParser.ENGINE, 0); }
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public ImplContext impl() {
			return getRuleContext(ImplContext.class,0);
		}
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public Engine_defContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_engine_def; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterEngine_def(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitEngine_def(this);
		}
	}

	public final Engine_defContext engine_def() throws RecognitionException {
		Engine_defContext _localctx = new Engine_defContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_engine_def);
		try {
			setState(106);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ENGINE:
				enterOuterAlt(_localctx, 1);
				{
				setState(100);
				match(ENGINE);
				setState(101);
				match(ID);
				setState(102);
				impl();
				setState(103);
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

	public static class ImplContext extends ParserRuleContext {
		public TerminalNode IMPLEMENTS() { return getToken(EslParser.IMPLEMENTS, 0); }
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public ImplContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_impl; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterImpl(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitImpl(this);
		}
	}

	public final ImplContext impl() throws RecognitionException {
		ImplContext _localctx = new ImplContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_impl);
		try {
			setState(111);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case IMPLEMENTS:
				enterOuterAlt(_localctx, 1);
				{
				setState(108);
				match(IMPLEMENTS);
				setState(109);
				match(ID);
				}
				break;
			case LEFT_CURLY:
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
		public TerminalNode LEFT_CURLY() { return getToken(EslParser.LEFT_CURLY, 0); }
		public Interface_decl_listContext interface_decl_list() {
			return getRuleContext(Interface_decl_listContext.class,0);
		}
		public Capability_listContext capability_list() {
			return getRuleContext(Capability_listContext.class,0);
		}
		public TerminalNode RIGHT_CURLY() { return getToken(EslParser.RIGHT_CURLY, 0); }
		public BlockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_block; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterBlock(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitBlock(this);
		}
	}

	public final BlockContext block() throws RecognitionException {
		BlockContext _localctx = new BlockContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_block);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(113);
			match(LEFT_CURLY);
			setState(114);
			interface_decl_list();
			setState(115);
			capability_list();
			setState(116);
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

	public static class Interface_decl_listContext extends ParserRuleContext {
		public List<Interface_declContext> interface_decl() {
			return getRuleContexts(Interface_declContext.class);
		}
		public Interface_declContext interface_decl(int i) {
			return getRuleContext(Interface_declContext.class,i);
		}
		public Interface_decl_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_interface_decl_list; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterInterface_decl_list(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitInterface_decl_list(this);
		}
	}

	public final Interface_decl_listContext interface_decl_list() throws RecognitionException {
		Interface_decl_listContext _localctx = new Interface_decl_listContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_interface_decl_list);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(121);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==INTERFACE) {
				{
				{
				setState(118);
				interface_decl();
				}
				}
				setState(123);
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

	public static class Interface_declContext extends ParserRuleContext {
		public TerminalNode INTERFACE() { return getToken(EslParser.INTERFACE, 0); }
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public TerminalNode ASSIGN() { return getToken(EslParser.ASSIGN, 0); }
		public NamespaceContext namespace() {
			return getRuleContext(NamespaceContext.class,0);
		}
		public Interface_declContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_interface_decl; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterInterface_decl(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitInterface_decl(this);
		}
	}

	public final Interface_declContext interface_decl() throws RecognitionException {
		Interface_declContext _localctx = new Interface_declContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_interface_decl);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(124);
			match(INTERFACE);
			setState(125);
			match(ID);
			setState(126);
			match(ASSIGN);
			setState(127);
			namespace();
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
			if ( listener instanceof EslListener ) ((EslListener)listener).enterCapability_list(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitCapability_list(this);
		}
	}

	public final Capability_listContext capability_list() throws RecognitionException {
		Capability_listContext _localctx = new Capability_listContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_capability_list);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(132);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==CAPABILITY) {
				{
				{
				setState(129);
				capability();
				}
				}
				setState(134);
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
		public TerminalNode CAPABILITY() { return getToken(EslParser.CAPABILITY, 0); }
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public TerminalNode LEFT_PAREN() { return getToken(EslParser.LEFT_PAREN, 0); }
		public ParamsContext params() {
			return getRuleContext(ParamsContext.class,0);
		}
		public TerminalNode RIGHT_PAREN() { return getToken(EslParser.RIGHT_PAREN, 0); }
		public TouchContext touch() {
			return getRuleContext(TouchContext.class,0);
		}
		public Cap_blockContext cap_block() {
			return getRuleContext(Cap_blockContext.class,0);
		}
		public CapabilityContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_capability; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterCapability(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitCapability(this);
		}
	}

	public final CapabilityContext capability() throws RecognitionException {
		CapabilityContext _localctx = new CapabilityContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_capability);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(135);
			match(CAPABILITY);
			setState(136);
			match(ID);
			setState(137);
			match(LEFT_PAREN);
			setState(138);
			params();
			setState(139);
			match(RIGHT_PAREN);
			setState(140);
			touch();
			setState(141);
			cap_block();
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
			if ( listener instanceof EslListener ) ((EslListener)listener).enterParams(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitParams(this);
		}
	}

	public final ParamsContext params() throws RecognitionException {
		ParamsContext _localctx = new ParamsContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_params);
		try {
			setState(147);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,7,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(143);
				capability_arg();
				setState(144);
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
		public Param_interfaceContext param_interface() {
			return getRuleContext(Param_interfaceContext.class,0);
		}
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public TerminalNode ASSIGN() { return getToken(EslParser.ASSIGN, 0); }
		public TerminalNode LEFT_BRACK() { return getToken(EslParser.LEFT_BRACK, 0); }
		public LiteralsContext literals() {
			return getRuleContext(LiteralsContext.class,0);
		}
		public TerminalNode RIGHT_BRACK() { return getToken(EslParser.RIGHT_BRACK, 0); }
		public Capability_argContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_capability_arg; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterCapability_arg(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitCapability_arg(this);
		}
	}

	public final Capability_argContext capability_arg() throws RecognitionException {
		Capability_argContext _localctx = new Capability_argContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_capability_arg);
		try {
			setState(161);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,8,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(149);
				memory_interface();
				setState(150);
				data_type();
				setState(151);
				var();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(153);
				param_interface();
				setState(154);
				match(ID);
				setState(155);
				match(ASSIGN);
				setState(156);
				match(LEFT_BRACK);
				setState(157);
				literals();
				setState(158);
				match(RIGHT_BRACK);
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
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

	public static class Capability_arg_listContext extends ParserRuleContext {
		public TerminalNode COMMA() { return getToken(EslParser.COMMA, 0); }
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
			if ( listener instanceof EslListener ) ((EslListener)listener).enterCapability_arg_list(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitCapability_arg_list(this);
		}
	}

	public final Capability_arg_listContext capability_arg_list() throws RecognitionException {
		Capability_arg_listContext _localctx = new Capability_arg_listContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_capability_arg_list);
		try {
			setState(168);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case COMMA:
				enterOuterAlt(_localctx, 1);
				{
				setState(163);
				match(COMMA);
				setState(164);
				capability_arg();
				setState(165);
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

	public static class Param_interfaceContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public Param_interfaceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_param_interface; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterParam_interface(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitParam_interface(this);
		}
	}

	public final Param_interfaceContext param_interface() throws RecognitionException {
		Param_interfaceContext _localctx = new Param_interfaceContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_param_interface);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(170);
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

	public static class LiteralsContext extends ParserRuleContext {
		public LiteralContext literal() {
			return getRuleContext(LiteralContext.class,0);
		}
		public Literal_listContext literal_list() {
			return getRuleContext(Literal_listContext.class,0);
		}
		public LiteralsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_literals; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterLiterals(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitLiterals(this);
		}
	}

	public final LiteralsContext literals() throws RecognitionException {
		LiteralsContext _localctx = new LiteralsContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_literals);
		try {
			setState(176);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case INTLIT:
			case STRING:
				enterOuterAlt(_localctx, 1);
				{
				setState(172);
				literal();
				setState(173);
				literal_list();
				}
				break;
			case RIGHT_BRACK:
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

	public static class LiteralContext extends ParserRuleContext {
		public TerminalNode INTLIT() { return getToken(EslParser.INTLIT, 0); }
		public TerminalNode STRING() { return getToken(EslParser.STRING, 0); }
		public LiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_literal; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitLiteral(this);
		}
	}

	public final LiteralContext literal() throws RecognitionException {
		LiteralContext _localctx = new LiteralContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_literal);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(178);
			_la = _input.LA(1);
			if ( !(_la==INTLIT || _la==STRING) ) {
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

	public static class Literal_listContext extends ParserRuleContext {
		public TerminalNode COMMA() { return getToken(EslParser.COMMA, 0); }
		public LiteralContext literal() {
			return getRuleContext(LiteralContext.class,0);
		}
		public Literal_listContext literal_list() {
			return getRuleContext(Literal_listContext.class,0);
		}
		public Literal_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_literal_list; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterLiteral_list(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitLiteral_list(this);
		}
	}

	public final Literal_listContext literal_list() throws RecognitionException {
		Literal_listContext _localctx = new Literal_listContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_literal_list);
		try {
			setState(185);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case COMMA:
				enterOuterAlt(_localctx, 1);
				{
				setState(180);
				match(COMMA);
				setState(181);
				literal();
				setState(182);
				literal_list();
				}
				break;
			case RIGHT_BRACK:
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
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public Memory_interfaceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_memory_interface; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterMemory_interface(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitMemory_interface(this);
		}
	}

	public final Memory_interfaceContext memory_interface() throws RecognitionException {
		Memory_interfaceContext _localctx = new Memory_interfaceContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_memory_interface);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(187);
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

	public static class Data_typeContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public Data_type_tailContext data_type_tail() {
			return getRuleContext(Data_type_tailContext.class,0);
		}
		public Data_typeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_data_type; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterData_type(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitData_type(this);
		}
	}

	public final Data_typeContext data_type() throws RecognitionException {
		Data_typeContext _localctx = new Data_typeContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_data_type);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(189);
			match(ID);
			setState(190);
			data_type_tail();
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

	public static class Data_type_tailContext extends ParserRuleContext {
		public TerminalNode LEFT_BRACK() { return getToken(EslParser.LEFT_BRACK, 0); }
		public TerminalNode RIGHT_BRACK() { return getToken(EslParser.RIGHT_BRACK, 0); }
		public Data_type_tailContext data_type_tail() {
			return getRuleContext(Data_type_tailContext.class,0);
		}
		public Data_type_tailContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_data_type_tail; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterData_type_tail(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitData_type_tail(this);
		}
	}

	public final Data_type_tailContext data_type_tail() throws RecognitionException {
		Data_type_tailContext _localctx = new Data_type_tailContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_data_type_tail);
		try {
			setState(196);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case LEFT_BRACK:
				enterOuterAlt(_localctx, 1);
				{
				setState(192);
				match(LEFT_BRACK);
				setState(193);
				match(RIGHT_BRACK);
				setState(194);
				data_type_tail();
				}
				break;
			case ID:
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
			if ( listener instanceof EslListener ) ((EslListener)listener).enterVar(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitVar(this);
		}
	}

	public final VarContext var() throws RecognitionException {
		VarContext _localctx = new VarContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_var);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(198);
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
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public Var_idContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_var_id; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterVar_id(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitVar_id(this);
		}
	}

	public final Var_idContext var_id() throws RecognitionException {
		Var_idContext _localctx = new Var_idContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_var_id);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(200);
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

	public static class TouchContext extends ParserRuleContext {
		public TerminalNode TOUCHES() { return getToken(EslParser.TOUCHES, 0); }
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public TouchContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_touch; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterTouch(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitTouch(this);
		}
	}

	public final TouchContext touch() throws RecognitionException {
		TouchContext _localctx = new TouchContext(_ctx, getState());
		enterRule(_localctx, 52, RULE_touch);
		try {
			setState(205);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case TOUCHES:
				enterOuterAlt(_localctx, 1);
				{
				setState(202);
				match(TOUCHES);
				setState(203);
				match(ID);
				}
				break;
			case LEFT_CURLY:
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

	public static class Cap_blockContext extends ParserRuleContext {
		public TerminalNode LEFT_CURLY() { return getToken(EslParser.LEFT_CURLY, 0); }
		public SpecsContext specs() {
			return getRuleContext(SpecsContext.class,0);
		}
		public TerminalNode RIGHT_CURLY() { return getToken(EslParser.RIGHT_CURLY, 0); }
		public Cap_blockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cap_block; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterCap_block(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitCap_block(this);
		}
	}

	public final Cap_blockContext cap_block() throws RecognitionException {
		Cap_blockContext _localctx = new Cap_blockContext(_ctx, getState());
		enterRule(_localctx, 54, RULE_cap_block);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(207);
			match(LEFT_CURLY);
			setState(208);
			specs();
			setState(209);
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

	public static class SpecsContext extends ParserRuleContext {
		public SpecContext spec() {
			return getRuleContext(SpecContext.class,0);
		}
		public Spec_listContext spec_list() {
			return getRuleContext(Spec_listContext.class,0);
		}
		public SpecsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_specs; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterSpecs(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitSpecs(this);
		}
	}

	public final SpecsContext specs() throws RecognitionException {
		SpecsContext _localctx = new SpecsContext(_ctx, getState());
		enterRule(_localctx, 56, RULE_specs);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(211);
			spec();
			setState(212);
			spec_list();
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

	public static class SpecContext extends ParserRuleContext {
		public AttrContext attr() {
			return getRuleContext(AttrContext.class,0);
		}
		public TerminalNode COLON() { return getToken(EslParser.COLON, 0); }
		public Attr_valContext attr_val() {
			return getRuleContext(Attr_valContext.class,0);
		}
		public SpecContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_spec; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterSpec(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitSpec(this);
		}
	}

	public final SpecContext spec() throws RecognitionException {
		SpecContext _localctx = new SpecContext(_ctx, getState());
		enterRule(_localctx, 58, RULE_spec);
		try {
			setState(219);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case LANGUAGE:
			case RUNTIME_COST:
			case VERBATIM:
			case CODE:
			case FILE:
			case COLON:
				enterOuterAlt(_localctx, 1);
				{
				setState(214);
				attr();
				setState(215);
				match(COLON);
				setState(216);
				attr_val();
				}
				break;
			case RIGHT_CURLY:
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

	public static class Spec_listContext extends ParserRuleContext {
		public TerminalNode COMMA() { return getToken(EslParser.COMMA, 0); }
		public SpecContext spec() {
			return getRuleContext(SpecContext.class,0);
		}
		public Spec_listContext spec_list() {
			return getRuleContext(Spec_listContext.class,0);
		}
		public Spec_listContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_spec_list; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterSpec_list(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitSpec_list(this);
		}
	}

	public final Spec_listContext spec_list() throws RecognitionException {
		Spec_listContext _localctx = new Spec_listContext(_ctx, getState());
		enterRule(_localctx, 60, RULE_spec_list);
		try {
			setState(226);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case COMMA:
				enterOuterAlt(_localctx, 1);
				{
				setState(221);
				match(COMMA);
				setState(222);
				spec();
				setState(223);
				spec_list();
				}
				break;
			case RIGHT_CURLY:
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

	public static class AttrContext extends ParserRuleContext {
		public QualifierContext qualifier() {
			return getRuleContext(QualifierContext.class,0);
		}
		public Attr_idContext attr_id() {
			return getRuleContext(Attr_idContext.class,0);
		}
		public AttrContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_attr; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterAttr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitAttr(this);
		}
	}

	public final AttrContext attr() throws RecognitionException {
		AttrContext _localctx = new AttrContext(_ctx, getState());
		enterRule(_localctx, 62, RULE_attr);
		try {
			setState(232);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case LANGUAGE:
			case RUNTIME_COST:
			case VERBATIM:
			case CODE:
			case FILE:
				enterOuterAlt(_localctx, 1);
				{
				setState(228);
				qualifier();
				setState(229);
				attr_id();
				}
				break;
			case COLON:
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

	public static class Attr_idContext extends ParserRuleContext {
		public TerminalNode LANGUAGE() { return getToken(EslParser.LANGUAGE, 0); }
		public TerminalNode CODE() { return getToken(EslParser.CODE, 0); }
		public TerminalNode FILE() { return getToken(EslParser.FILE, 0); }
		public TerminalNode RUNTIME_COST() { return getToken(EslParser.RUNTIME_COST, 0); }
		public Attr_idContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_attr_id; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterAttr_id(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitAttr_id(this);
		}
	}

	public final Attr_idContext attr_id() throws RecognitionException {
		Attr_idContext _localctx = new Attr_idContext(_ctx, getState());
		enterRule(_localctx, 64, RULE_attr_id);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(234);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << LANGUAGE) | (1L << RUNTIME_COST) | (1L << CODE) | (1L << FILE))) != 0)) ) {
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

	public static class QualifierContext extends ParserRuleContext {
		public TerminalNode VERBATIM() { return getToken(EslParser.VERBATIM, 0); }
		public QualifierContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_qualifier; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterQualifier(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitQualifier(this);
		}
	}

	public final QualifierContext qualifier() throws RecognitionException {
		QualifierContext _localctx = new QualifierContext(_ctx, getState());
		enterRule(_localctx, 66, RULE_qualifier);
		try {
			setState(238);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case VERBATIM:
				enterOuterAlt(_localctx, 1);
				{
				setState(236);
				match(VERBATIM);
				}
				break;
			case LANGUAGE:
			case RUNTIME_COST:
			case CODE:
			case FILE:
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

	public static class Attr_valContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(EslParser.ID, 0); }
		public TerminalNode STRING() { return getToken(EslParser.STRING, 0); }
		public TerminalNode INTLIT() { return getToken(EslParser.INTLIT, 0); }
		public Attr_valContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_attr_val; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).enterAttr_val(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof EslListener ) ((EslListener)listener).exitAttr_val(this);
		}
	}

	public final Attr_valContext attr_val() throws RecognitionException {
		Attr_valContext _localctx = new Attr_valContext(_ctx, getState());
		enterRule(_localctx, 68, RULE_attr_val);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(240);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << ID) | (1L << INTLIT) | (1L << STRING))) != 0)) ) {
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

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\"\u00f5\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\4#\t#\4$\t$\3\2\3\2\3\2\3\3\7\3M\n\3\f\3\16\3P\13\3\3\4\3"+
		"\4\3\4\3\4\3\5\3\5\3\5\5\5Y\n\5\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\5\7c\n"+
		"\7\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\t\5\tm\n\t\3\n\3\n\3\n\5\nr\n\n\3\13"+
		"\3\13\3\13\3\13\3\13\3\f\7\fz\n\f\f\f\16\f}\13\f\3\r\3\r\3\r\3\r\3\r\3"+
		"\16\7\16\u0085\n\16\f\16\16\16\u0088\13\16\3\17\3\17\3\17\3\17\3\17\3"+
		"\17\3\17\3\17\3\20\3\20\3\20\3\20\5\20\u0096\n\20\3\21\3\21\3\21\3\21"+
		"\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\5\21\u00a4\n\21\3\22\3\22\3\22"+
		"\3\22\3\22\5\22\u00ab\n\22\3\23\3\23\3\24\3\24\3\24\3\24\5\24\u00b3\n"+
		"\24\3\25\3\25\3\26\3\26\3\26\3\26\3\26\5\26\u00bc\n\26\3\27\3\27\3\30"+
		"\3\30\3\30\3\31\3\31\3\31\3\31\5\31\u00c7\n\31\3\32\3\32\3\33\3\33\3\34"+
		"\3\34\3\34\5\34\u00d0\n\34\3\35\3\35\3\35\3\35\3\36\3\36\3\36\3\37\3\37"+
		"\3\37\3\37\3\37\5\37\u00de\n\37\3 \3 \3 \3 \3 \5 \u00e5\n \3!\3!\3!\3"+
		"!\5!\u00eb\n!\3\"\3\"\3#\3#\5#\u00f1\n#\3$\3$\3$\2\2%\2\4\6\b\n\f\16\20"+
		"\22\24\26\30\32\34\36 \"$&(*,.\60\62\64\668:<>@BDF\2\6\4\2\27\27\33\33"+
		"\3\2\36\37\4\2\16\17\21\22\4\2\33\33\36\37\2\u00e4\2H\3\2\2\2\4N\3\2\2"+
		"\2\6Q\3\2\2\2\bX\3\2\2\2\nZ\3\2\2\2\fb\3\2\2\2\16d\3\2\2\2\20l\3\2\2\2"+
		"\22q\3\2\2\2\24s\3\2\2\2\26{\3\2\2\2\30~\3\2\2\2\32\u0086\3\2\2\2\34\u0089"+
		"\3\2\2\2\36\u0095\3\2\2\2 \u00a3\3\2\2\2\"\u00aa\3\2\2\2$\u00ac\3\2\2"+
		"\2&\u00b2\3\2\2\2(\u00b4\3\2\2\2*\u00bb\3\2\2\2,\u00bd\3\2\2\2.\u00bf"+
		"\3\2\2\2\60\u00c6\3\2\2\2\62\u00c8\3\2\2\2\64\u00ca\3\2\2\2\66\u00cf\3"+
		"\2\2\28\u00d1\3\2\2\2:\u00d5\3\2\2\2<\u00dd\3\2\2\2>\u00e4\3\2\2\2@\u00ea"+
		"\3\2\2\2B\u00ec\3\2\2\2D\u00f0\3\2\2\2F\u00f2\3\2\2\2HI\5\4\3\2IJ\5\20"+
		"\t\2J\3\3\2\2\2KM\5\6\4\2LK\3\2\2\2MP\3\2\2\2NL\3\2\2\2NO\3\2\2\2O\5\3"+
		"\2\2\2PN\3\2\2\2QR\7\6\2\2RS\5\n\6\2ST\5\b\5\2T\7\3\2\2\2UV\7\7\2\2VY"+
		"\7\33\2\2WY\3\2\2\2XU\3\2\2\2XW\3\2\2\2Y\t\3\2\2\2Z[\7\33\2\2[\\\5\f\7"+
		"\2\\\13\3\2\2\2]^\7\3\2\2^_\5\16\b\2_`\5\f\7\2`c\3\2\2\2ac\3\2\2\2b]\3"+
		"\2\2\2ba\3\2\2\2c\r\3\2\2\2de\t\2\2\2e\17\3\2\2\2fg\7\4\2\2gh\7\33\2\2"+
		"hi\5\22\n\2ij\5\24\13\2jm\3\2\2\2km\3\2\2\2lf\3\2\2\2lk\3\2\2\2m\21\3"+
		"\2\2\2no\7\24\2\2or\7\33\2\2pr\3\2\2\2qn\3\2\2\2qp\3\2\2\2r\23\3\2\2\2"+
		"st\7\b\2\2tu\5\26\f\2uv\5\32\16\2vw\7\t\2\2w\25\3\2\2\2xz\5\30\r\2yx\3"+
		"\2\2\2z}\3\2\2\2{y\3\2\2\2{|\3\2\2\2|\27\3\2\2\2}{\3\2\2\2~\177\7\25\2"+
		"\2\177\u0080\7\33\2\2\u0080\u0081\7\26\2\2\u0081\u0082\5\n\6\2\u0082\31"+
		"\3\2\2\2\u0083\u0085\5\34\17\2\u0084\u0083\3\2\2\2\u0085\u0088\3\2\2\2"+
		"\u0086\u0084\3\2\2\2\u0086\u0087\3\2\2\2\u0087\33\3\2\2\2\u0088\u0086"+
		"\3\2\2\2\u0089\u008a\7\5\2\2\u008a\u008b\7\33\2\2\u008b\u008c\7\n\2\2"+
		"\u008c\u008d\5\36\20\2\u008d\u008e\7\13\2\2\u008e\u008f\5\66\34\2\u008f"+
		"\u0090\58\35\2\u0090\35\3\2\2\2\u0091\u0092\5 \21\2\u0092\u0093\5\"\22"+
		"\2\u0093\u0096\3\2\2\2\u0094\u0096\3\2\2\2\u0095\u0091\3\2\2\2\u0095\u0094"+
		"\3\2\2\2\u0096\37\3\2\2\2\u0097\u0098\5,\27\2\u0098\u0099\5.\30\2\u0099"+
		"\u009a\5\62\32\2\u009a\u00a4\3\2\2\2\u009b\u009c\5$\23\2\u009c\u009d\7"+
		"\33\2\2\u009d\u009e\7\26\2\2\u009e\u009f\7\31\2\2\u009f\u00a0\5&\24\2"+
		"\u00a0\u00a1\7\32\2\2\u00a1\u00a4\3\2\2\2\u00a2\u00a4\3\2\2\2\u00a3\u0097"+
		"\3\2\2\2\u00a3\u009b\3\2\2\2\u00a3\u00a2\3\2\2\2\u00a4!\3\2\2\2\u00a5"+
		"\u00a6\7\f\2\2\u00a6\u00a7\5 \21\2\u00a7\u00a8\5\"\22\2\u00a8\u00ab\3"+
		"\2\2\2\u00a9\u00ab\3\2\2\2\u00aa\u00a5\3\2\2\2\u00aa\u00a9\3\2\2\2\u00ab"+
		"#\3\2\2\2\u00ac\u00ad\7\33\2\2\u00ad%\3\2\2\2\u00ae\u00af\5(\25\2\u00af"+
		"\u00b0\5*\26\2\u00b0\u00b3\3\2\2\2\u00b1\u00b3\3\2\2\2\u00b2\u00ae\3\2"+
		"\2\2\u00b2\u00b1\3\2\2\2\u00b3\'\3\2\2\2\u00b4\u00b5\t\3\2\2\u00b5)\3"+
		"\2\2\2\u00b6\u00b7\7\f\2\2\u00b7\u00b8\5(\25\2\u00b8\u00b9\5*\26\2\u00b9"+
		"\u00bc\3\2\2\2\u00ba\u00bc\3\2\2\2\u00bb\u00b6\3\2\2\2\u00bb\u00ba\3\2"+
		"\2\2\u00bc+\3\2\2\2\u00bd\u00be\7\33\2\2\u00be-\3\2\2\2\u00bf\u00c0\7"+
		"\33\2\2\u00c0\u00c1\5\60\31\2\u00c1/\3\2\2\2\u00c2\u00c3\7\31\2\2\u00c3"+
		"\u00c4\7\32\2\2\u00c4\u00c7\5\60\31\2\u00c5\u00c7\3\2\2\2\u00c6\u00c2"+
		"\3\2\2\2\u00c6\u00c5\3\2\2\2\u00c7\61\3\2\2\2\u00c8\u00c9\5\64\33\2\u00c9"+
		"\63\3\2\2\2\u00ca\u00cb\7\33\2\2\u00cb\65\3\2\2\2\u00cc\u00cd\7\23\2\2"+
		"\u00cd\u00d0\7\33\2\2\u00ce\u00d0\3\2\2\2\u00cf\u00cc\3\2\2\2\u00cf\u00ce"+
		"\3\2\2\2\u00d0\67\3\2\2\2\u00d1\u00d2\7\b\2\2\u00d2\u00d3\5:\36\2\u00d3"+
		"\u00d4\7\t\2\2\u00d49\3\2\2\2\u00d5\u00d6\5<\37\2\u00d6\u00d7\5> \2\u00d7"+
		";\3\2\2\2\u00d8\u00d9\5@!\2\u00d9\u00da\7\30\2\2\u00da\u00db\5F$\2\u00db"+
		"\u00de\3\2\2\2\u00dc\u00de\3\2\2\2\u00dd\u00d8\3\2\2\2\u00dd\u00dc\3\2"+
		"\2\2\u00de=\3\2\2\2\u00df\u00e0\7\f\2\2\u00e0\u00e1\5<\37\2\u00e1\u00e2"+
		"\5> \2\u00e2\u00e5\3\2\2\2\u00e3\u00e5\3\2\2\2\u00e4\u00df\3\2\2\2\u00e4"+
		"\u00e3\3\2\2\2\u00e5?\3\2\2\2\u00e6\u00e7\5D#\2\u00e7\u00e8\5B\"\2\u00e8"+
		"\u00eb\3\2\2\2\u00e9\u00eb\3\2\2\2\u00ea\u00e6\3\2\2\2\u00ea\u00e9\3\2"+
		"\2\2\u00ebA\3\2\2\2\u00ec\u00ed\t\4\2\2\u00edC\3\2\2\2\u00ee\u00f1\7\20"+
		"\2\2\u00ef\u00f1\3\2\2\2\u00f0\u00ee\3\2\2\2\u00f0\u00ef\3\2\2\2\u00f1"+
		"E\3\2\2\2\u00f2\u00f3\t\5\2\2\u00f3G\3\2\2\2\24NXblq{\u0086\u0095\u00a3"+
		"\u00aa\u00b2\u00bb\u00c6\u00cf\u00dd\u00e4\u00ea\u00f0";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}