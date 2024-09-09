// Generated from /Users/joon/ohai.src/esa/grammar/abstract_domain/AbstractDomain.g by ANTLR 4.7.1
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class AbstractDomainLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.7.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, ABSTRACT=2, DOMAIN=3, CAPABILITY=4, INPUT=5, OUTPUT=6, STATE=7, 
		PARAM=8, IMPORT=9, AS=10, LEFT_CURLY=11, RIGHT_CURLY=12, LEFT_PAREN=13, 
		RIGHT_PAREN=14, COMMA=15, DEFAULT=16, REFERENCE=17, LANGUAGE=18, VERBATIM=19, 
		CODE=20, FILE=21, ID=22, WHITESPACE=23, COMMENT=24, INTLIT=25;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	public static final String[] ruleNames = {
		"T__0", "ABSTRACT", "DOMAIN", "CAPABILITY", "INPUT", "OUTPUT", "STATE", 
		"PARAM", "IMPORT", "AS", "LEFT_CURLY", "RIGHT_CURLY", "LEFT_PAREN", "RIGHT_PAREN", 
		"COMMA", "DEFAULT", "REFERENCE", "LANGUAGE", "VERBATIM", "CODE", "FILE", 
		"ID", "LOWER", "UPPER", "DIGIT", "WHITESPACE", "COMMENT", "INTLIT"
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


	public AbstractDomainLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "AbstractDomain.g"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\33\u00e4\b\1\4\2"+
		"\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4"+
		"\13\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22"+
		"\t\22\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31"+
		"\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\3\2\3\2\3\3\3\3\3\3\3\3"+
		"\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3"+
		"\5\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7"+
		"\3\7\3\b\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3"+
		"\n\3\n\3\n\3\13\3\13\3\13\3\f\3\f\3\r\3\r\3\16\3\16\3\17\3\17\3\20\3\20"+
		"\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\22\3\22\3\22\3\22\3\22\3\22"+
		"\3\22\3\22\3\22\3\22\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\24"+
		"\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\25\3\25\3\25\3\25\3\25\3\26"+
		"\3\26\3\26\3\26\3\26\3\27\3\27\5\27\u00b6\n\27\3\27\3\27\3\27\3\27\7\27"+
		"\u00bc\n\27\f\27\16\27\u00bf\13\27\3\30\3\30\3\31\3\31\3\32\3\32\3\33"+
		"\6\33\u00c8\n\33\r\33\16\33\u00c9\3\33\3\33\3\34\3\34\3\34\3\34\6\34\u00d2"+
		"\n\34\r\34\16\34\u00d3\3\34\5\34\u00d7\n\34\3\34\3\34\3\35\3\35\3\35\7"+
		"\35\u00de\n\35\f\35\16\35\u00e1\13\35\5\35\u00e3\n\35\3\u00d3\2\36\3\3"+
		"\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21"+
		"!\22#\23%\24\'\25)\26+\27-\30/\2\61\2\63\2\65\31\67\329\33\3\2\4\5\2\13"+
		"\f\17\17\"\"\3\3\f\f\2\u00e9\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3"+
		"\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2"+
		"\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37"+
		"\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3"+
		"\2\2\2\2-\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\3;\3\2\2\2\5=\3"+
		"\2\2\2\7F\3\2\2\2\tM\3\2\2\2\13X\3\2\2\2\r^\3\2\2\2\17e\3\2\2\2\21k\3"+
		"\2\2\2\23q\3\2\2\2\25x\3\2\2\2\27{\3\2\2\2\31}\3\2\2\2\33\177\3\2\2\2"+
		"\35\u0081\3\2\2\2\37\u0083\3\2\2\2!\u0085\3\2\2\2#\u008d\3\2\2\2%\u0097"+
		"\3\2\2\2\'\u00a0\3\2\2\2)\u00a9\3\2\2\2+\u00ae\3\2\2\2-\u00b5\3\2\2\2"+
		"/\u00c0\3\2\2\2\61\u00c2\3\2\2\2\63\u00c4\3\2\2\2\65\u00c7\3\2\2\2\67"+
		"\u00cd\3\2\2\29\u00e2\3\2\2\2;<\7\60\2\2<\4\3\2\2\2=>\7c\2\2>?\7d\2\2"+
		"?@\7u\2\2@A\7v\2\2AB\7t\2\2BC\7c\2\2CD\7e\2\2DE\7v\2\2E\6\3\2\2\2FG\7"+
		"f\2\2GH\7q\2\2HI\7o\2\2IJ\7c\2\2JK\7k\2\2KL\7p\2\2L\b\3\2\2\2MN\7e\2\2"+
		"NO\7c\2\2OP\7r\2\2PQ\7c\2\2QR\7d\2\2RS\7k\2\2ST\7n\2\2TU\7k\2\2UV\7v\2"+
		"\2VW\7{\2\2W\n\3\2\2\2XY\7k\2\2YZ\7p\2\2Z[\7r\2\2[\\\7w\2\2\\]\7v\2\2"+
		"]\f\3\2\2\2^_\7q\2\2_`\7w\2\2`a\7v\2\2ab\7r\2\2bc\7w\2\2cd\7v\2\2d\16"+
		"\3\2\2\2ef\7u\2\2fg\7v\2\2gh\7c\2\2hi\7v\2\2ij\7g\2\2j\20\3\2\2\2kl\7"+
		"r\2\2lm\7c\2\2mn\7t\2\2no\7c\2\2op\7o\2\2p\22\3\2\2\2qr\7k\2\2rs\7o\2"+
		"\2st\7r\2\2tu\7q\2\2uv\7t\2\2vw\7v\2\2w\24\3\2\2\2xy\7c\2\2yz\7u\2\2z"+
		"\26\3\2\2\2{|\7}\2\2|\30\3\2\2\2}~\7\177\2\2~\32\3\2\2\2\177\u0080\7*"+
		"\2\2\u0080\34\3\2\2\2\u0081\u0082\7+\2\2\u0082\36\3\2\2\2\u0083\u0084"+
		"\7.\2\2\u0084 \3\2\2\2\u0085\u0086\7f\2\2\u0086\u0087\7g\2\2\u0087\u0088"+
		"\7h\2\2\u0088\u0089\7c\2\2\u0089\u008a\7w\2\2\u008a\u008b\7n\2\2\u008b"+
		"\u008c\7v\2\2\u008c\"\3\2\2\2\u008d\u008e\7t\2\2\u008e\u008f\7g\2\2\u008f"+
		"\u0090\7h\2\2\u0090\u0091\7g\2\2\u0091\u0092\7t\2\2\u0092\u0093\7g\2\2"+
		"\u0093\u0094\7p\2\2\u0094\u0095\7e\2\2\u0095\u0096\7g\2\2\u0096$\3\2\2"+
		"\2\u0097\u0098\7n\2\2\u0098\u0099\7c\2\2\u0099\u009a\7p\2\2\u009a\u009b"+
		"\7i\2\2\u009b\u009c\7w\2\2\u009c\u009d\7c\2\2\u009d\u009e\7i\2\2\u009e"+
		"\u009f\7g\2\2\u009f&\3\2\2\2\u00a0\u00a1\7x\2\2\u00a1\u00a2\7g\2\2\u00a2"+
		"\u00a3\7t\2\2\u00a3\u00a4\7d\2\2\u00a4\u00a5\7c\2\2\u00a5\u00a6\7v\2\2"+
		"\u00a6\u00a7\7k\2\2\u00a7\u00a8\7o\2\2\u00a8(\3\2\2\2\u00a9\u00aa\7e\2"+
		"\2\u00aa\u00ab\7q\2\2\u00ab\u00ac\7f\2\2\u00ac\u00ad\7g\2\2\u00ad*\3\2"+
		"\2\2\u00ae\u00af\7h\2\2\u00af\u00b0\7k\2\2\u00b0\u00b1\7n\2\2\u00b1\u00b2"+
		"\7g\2\2\u00b2,\3\2\2\2\u00b3\u00b6\5/\30\2\u00b4\u00b6\5\61\31\2\u00b5"+
		"\u00b3\3\2\2\2\u00b5\u00b4\3\2\2\2\u00b6\u00bd\3\2\2\2\u00b7\u00bc\5/"+
		"\30\2\u00b8\u00bc\5\61\31\2\u00b9\u00bc\5\63\32\2\u00ba\u00bc\7a\2\2\u00bb"+
		"\u00b7\3\2\2\2\u00bb\u00b8\3\2\2\2\u00bb\u00b9\3\2\2\2\u00bb\u00ba\3\2"+
		"\2\2\u00bc\u00bf\3\2\2\2\u00bd\u00bb\3\2\2\2\u00bd\u00be\3\2\2\2\u00be"+
		".\3\2\2\2\u00bf\u00bd\3\2\2\2\u00c0\u00c1\4c|\2\u00c1\60\3\2\2\2\u00c2"+
		"\u00c3\4C\\\2\u00c3\62\3\2\2\2\u00c4\u00c5\4\62;\2\u00c5\64\3\2\2\2\u00c6"+
		"\u00c8\t\2\2\2\u00c7\u00c6\3\2\2\2\u00c8\u00c9\3\2\2\2\u00c9\u00c7\3\2"+
		"\2\2\u00c9\u00ca\3\2\2\2\u00ca\u00cb\3\2\2\2\u00cb\u00cc\b\33\2\2\u00cc"+
		"\66\3\2\2\2\u00cd\u00ce\7\61\2\2\u00ce\u00cf\7\61\2\2\u00cf\u00d1\3\2"+
		"\2\2\u00d0\u00d2\13\2\2\2\u00d1\u00d0\3\2\2\2\u00d2\u00d3\3\2\2\2\u00d3"+
		"\u00d4\3\2\2\2\u00d3\u00d1\3\2\2\2\u00d4\u00d6\3\2\2\2\u00d5\u00d7\t\3"+
		"\2\2\u00d6\u00d5\3\2\2\2\u00d7\u00d8\3\2\2\2\u00d8\u00d9\b\34\2\2\u00d9"+
		"8\3\2\2\2\u00da\u00e3\7\62\2\2\u00db\u00df\4\63;\2\u00dc\u00de\5\63\32"+
		"\2\u00dd\u00dc\3\2\2\2\u00de\u00e1\3\2\2\2\u00df\u00dd\3\2\2\2\u00df\u00e0"+
		"\3\2\2\2\u00e0\u00e3\3\2\2\2\u00e1\u00df\3\2\2\2\u00e2\u00da\3\2\2\2\u00e2"+
		"\u00db\3\2\2\2\u00e3:\3\2\2\2\13\2\u00b5\u00bb\u00bd\u00c9\u00d3\u00d6"+
		"\u00df\u00e2\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}