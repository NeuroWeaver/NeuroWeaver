# Generated from /Users/joon/ohai.src/esa/grammar/abstract_domain/AbstractDomain.g by ANTLR 4.7.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\33")
        buf.write("z\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16\t")
        buf.write("\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\3\2\3\2\3\2\3\3\7\3+\n\3\f\3\16\3.\13\3\3\4\3\4\3\4\3")
        buf.write("\4\3\5\3\5\3\5\5\5\67\n\5\3\6\3\6\3\6\3\7\3\7\3\7\3\7")
        buf.write("\5\7@\n\7\3\b\3\b\3\b\3\b\3\b\5\bG\n\b\3\t\3\t\3\t\3\t")
        buf.write("\3\t\3\n\3\n\3\n\3\n\3\13\7\13S\n\13\f\13\16\13V\13\13")
        buf.write("\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\5\rb\n\r\3\16")
        buf.write("\3\16\3\16\3\16\3\16\5\16i\n\16\3\17\3\17\3\17\3\17\3")
        buf.write("\17\5\17p\n\17\3\20\3\20\3\21\3\21\3\22\3\22\3\23\3\23")
        buf.write("\3\23\2\2\24\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36 \"")
        buf.write("$\2\3\3\2\7\n\2o\2&\3\2\2\2\4,\3\2\2\2\6/\3\2\2\2\b\66")
        buf.write("\3\2\2\2\n8\3\2\2\2\f?\3\2\2\2\16F\3\2\2\2\20H\3\2\2\2")
        buf.write("\22M\3\2\2\2\24T\3\2\2\2\26W\3\2\2\2\30a\3\2\2\2\32h\3")
        buf.write("\2\2\2\34o\3\2\2\2\36q\3\2\2\2 s\3\2\2\2\"u\3\2\2\2$w")
        buf.write("\3\2\2\2&\'\5\4\3\2\'(\5\16\b\2(\3\3\2\2\2)+\5\6\4\2*")
        buf.write(")\3\2\2\2+.\3\2\2\2,*\3\2\2\2,-\3\2\2\2-\5\3\2\2\2.,\3")
        buf.write("\2\2\2/\60\7\13\2\2\60\61\5\n\6\2\61\62\5\b\5\2\62\7\3")
        buf.write("\2\2\2\63\64\7\f\2\2\64\67\7\30\2\2\65\67\3\2\2\2\66\63")
        buf.write("\3\2\2\2\66\65\3\2\2\2\67\t\3\2\2\289\7\30\2\29:\5\f\7")
        buf.write("\2:\13\3\2\2\2;<\7\3\2\2<=\7\30\2\2=@\5\f\7\2>@\3\2\2")
        buf.write("\2?;\3\2\2\2?>\3\2\2\2@\r\3\2\2\2AB\7\4\2\2BC\7\5\2\2")
        buf.write("CD\7\30\2\2DG\5\20\t\2EG\3\2\2\2FA\3\2\2\2FE\3\2\2\2G")
        buf.write("\17\3\2\2\2HI\7\r\2\2IJ\5\22\n\2JK\5\24\13\2KL\7\16\2")
        buf.write("\2L\21\3\2\2\2MN\7\22\2\2NO\7\23\2\2OP\7\30\2\2P\23\3")
        buf.write("\2\2\2QS\5\26\f\2RQ\3\2\2\2SV\3\2\2\2TR\3\2\2\2TU\3\2")
        buf.write("\2\2U\25\3\2\2\2VT\3\2\2\2WX\7\6\2\2XY\7\30\2\2YZ\7\17")
        buf.write("\2\2Z[\5\30\r\2[\\\7\20\2\2\\\27\3\2\2\2]^\5\32\16\2^")
        buf.write("_\5\34\17\2_b\3\2\2\2`b\3\2\2\2a]\3\2\2\2a`\3\2\2\2b\31")
        buf.write("\3\2\2\2cd\5\36\20\2de\5 \21\2ef\5\"\22\2fi\3\2\2\2gi")
        buf.write("\3\2\2\2hc\3\2\2\2hg\3\2\2\2i\33\3\2\2\2jk\7\21\2\2kl")
        buf.write("\5\32\16\2lm\5\34\17\2mp\3\2\2\2np\3\2\2\2oj\3\2\2\2o")
        buf.write("n\3\2\2\2p\35\3\2\2\2qr\t\2\2\2r\37\3\2\2\2st\7\30\2\2")
        buf.write("t!\3\2\2\2uv\5$\23\2v#\3\2\2\2wx\7\30\2\2x%\3\2\2\2\n")
        buf.write(",\66?FTaho")
        return buf.getvalue()


class AbstractDomainParser ( Parser ):

    grammarFileName = "AbstractDomain.g"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'.'", "'abstract'", "'domain'", "'capability'", 
                     "'input'", "'output'", "'state'", "'param'", "'import'", 
                     "'as'", "'{'", "'}'", "'('", "')'", "','", "'default'", 
                     "'reference'", "'language'", "'verbatim'", "'code'", 
                     "'file'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "ABSTRACT", "DOMAIN", "CAPABILITY", 
                      "INPUT", "OUTPUT", "STATE", "PARAM", "IMPORT", "AS", 
                      "LEFT_CURLY", "RIGHT_CURLY", "LEFT_PAREN", "RIGHT_PAREN", 
                      "COMMA", "DEFAULT", "REFERENCE", "LANGUAGE", "VERBATIM", 
                      "CODE", "FILE", "ID", "WHITESPACE", "COMMENT", "INTLIT" ]

    RULE_start = 0
    RULE_import_stmt_list = 1
    RULE_import_stmt = 2
    RULE_import_stmt_tail = 3
    RULE_namespace = 4
    RULE_namespace_tail = 5
    RULE_domain_def = 6
    RULE_block = 7
    RULE_default_stmt = 8
    RULE_capability_list = 9
    RULE_capability = 10
    RULE_params = 11
    RULE_capability_arg = 12
    RULE_capability_arg_list = 13
    RULE_memory_interface = 14
    RULE_data_type = 15
    RULE_var = 16
    RULE_var_id = 17

    ruleNames =  [ "start", "import_stmt_list", "import_stmt", "import_stmt_tail", 
                   "namespace", "namespace_tail", "domain_def", "block", 
                   "default_stmt", "capability_list", "capability", "params", 
                   "capability_arg", "capability_arg_list", "memory_interface", 
                   "data_type", "var", "var_id" ]

    EOF = Token.EOF
    T__0=1
    ABSTRACT=2
    DOMAIN=3
    CAPABILITY=4
    INPUT=5
    OUTPUT=6
    STATE=7
    PARAM=8
    IMPORT=9
    AS=10
    LEFT_CURLY=11
    RIGHT_CURLY=12
    LEFT_PAREN=13
    RIGHT_PAREN=14
    COMMA=15
    DEFAULT=16
    REFERENCE=17
    LANGUAGE=18
    VERBATIM=19
    CODE=20
    FILE=21
    ID=22
    WHITESPACE=23
    COMMENT=24
    INTLIT=25

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class StartContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def import_stmt_list(self):
            return self.getTypedRuleContext(AbstractDomainParser.Import_stmt_listContext,0)


        def domain_def(self):
            return self.getTypedRuleContext(AbstractDomainParser.Domain_defContext,0)


        def getRuleIndex(self):
            return AbstractDomainParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)




    def start(self):

        localctx = AbstractDomainParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.import_stmt_list()
            self.state = 37
            self.domain_def()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_stmt_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def import_stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AbstractDomainParser.Import_stmtContext)
            else:
                return self.getTypedRuleContext(AbstractDomainParser.Import_stmtContext,i)


        def getRuleIndex(self):
            return AbstractDomainParser.RULE_import_stmt_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_stmt_list" ):
                listener.enterImport_stmt_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_stmt_list" ):
                listener.exitImport_stmt_list(self)




    def import_stmt_list(self):

        localctx = AbstractDomainParser.Import_stmt_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_import_stmt_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==AbstractDomainParser.IMPORT:
                self.state = 39
                self.import_stmt()
                self.state = 44
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_stmtContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IMPORT(self):
            return self.getToken(AbstractDomainParser.IMPORT, 0)

        def namespace(self):
            return self.getTypedRuleContext(AbstractDomainParser.NamespaceContext,0)


        def import_stmt_tail(self):
            return self.getTypedRuleContext(AbstractDomainParser.Import_stmt_tailContext,0)


        def getRuleIndex(self):
            return AbstractDomainParser.RULE_import_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_stmt" ):
                listener.enterImport_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_stmt" ):
                listener.exitImport_stmt(self)




    def import_stmt(self):

        localctx = AbstractDomainParser.Import_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_import_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self.match(AbstractDomainParser.IMPORT)
            self.state = 46
            self.namespace()
            self.state = 47
            self.import_stmt_tail()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_stmt_tailContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AS(self):
            return self.getToken(AbstractDomainParser.AS, 0)

        def ID(self):
            return self.getToken(AbstractDomainParser.ID, 0)

        def getRuleIndex(self):
            return AbstractDomainParser.RULE_import_stmt_tail

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImport_stmt_tail" ):
                listener.enterImport_stmt_tail(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImport_stmt_tail" ):
                listener.exitImport_stmt_tail(self)




    def import_stmt_tail(self):

        localctx = AbstractDomainParser.Import_stmt_tailContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_import_stmt_tail)
        try:
            self.state = 52
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [AbstractDomainParser.AS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 49
                self.match(AbstractDomainParser.AS)
                self.state = 50
                self.match(AbstractDomainParser.ID)
                pass
            elif token in [AbstractDomainParser.EOF, AbstractDomainParser.ABSTRACT, AbstractDomainParser.IMPORT]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class NamespaceContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(AbstractDomainParser.ID, 0)

        def namespace_tail(self):
            return self.getTypedRuleContext(AbstractDomainParser.Namespace_tailContext,0)


        def getRuleIndex(self):
            return AbstractDomainParser.RULE_namespace

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamespace" ):
                listener.enterNamespace(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamespace" ):
                listener.exitNamespace(self)




    def namespace(self):

        localctx = AbstractDomainParser.NamespaceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_namespace)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self.match(AbstractDomainParser.ID)
            self.state = 55
            self.namespace_tail()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Namespace_tailContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(AbstractDomainParser.ID, 0)

        def namespace_tail(self):
            return self.getTypedRuleContext(AbstractDomainParser.Namespace_tailContext,0)


        def getRuleIndex(self):
            return AbstractDomainParser.RULE_namespace_tail

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamespace_tail" ):
                listener.enterNamespace_tail(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamespace_tail" ):
                listener.exitNamespace_tail(self)




    def namespace_tail(self):

        localctx = AbstractDomainParser.Namespace_tailContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_namespace_tail)
        try:
            self.state = 61
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [AbstractDomainParser.T__0]:
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self.match(AbstractDomainParser.T__0)
                self.state = 58
                self.match(AbstractDomainParser.ID)
                self.state = 59
                self.namespace_tail()
                pass
            elif token in [AbstractDomainParser.EOF, AbstractDomainParser.ABSTRACT, AbstractDomainParser.IMPORT, AbstractDomainParser.AS]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Domain_defContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ABSTRACT(self):
            return self.getToken(AbstractDomainParser.ABSTRACT, 0)

        def DOMAIN(self):
            return self.getToken(AbstractDomainParser.DOMAIN, 0)

        def ID(self):
            return self.getToken(AbstractDomainParser.ID, 0)

        def block(self):
            return self.getTypedRuleContext(AbstractDomainParser.BlockContext,0)


        def getRuleIndex(self):
            return AbstractDomainParser.RULE_domain_def

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDomain_def" ):
                listener.enterDomain_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDomain_def" ):
                listener.exitDomain_def(self)




    def domain_def(self):

        localctx = AbstractDomainParser.Domain_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_domain_def)
        try:
            self.state = 68
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [AbstractDomainParser.ABSTRACT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 63
                self.match(AbstractDomainParser.ABSTRACT)
                self.state = 64
                self.match(AbstractDomainParser.DOMAIN)
                self.state = 65
                self.match(AbstractDomainParser.ID)
                self.state = 66
                self.block()
                pass
            elif token in [AbstractDomainParser.EOF]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BlockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LEFT_CURLY(self):
            return self.getToken(AbstractDomainParser.LEFT_CURLY, 0)

        def default_stmt(self):
            return self.getTypedRuleContext(AbstractDomainParser.Default_stmtContext,0)


        def capability_list(self):
            return self.getTypedRuleContext(AbstractDomainParser.Capability_listContext,0)


        def RIGHT_CURLY(self):
            return self.getToken(AbstractDomainParser.RIGHT_CURLY, 0)

        def getRuleIndex(self):
            return AbstractDomainParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)




    def block(self):

        localctx = AbstractDomainParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_block)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            self.match(AbstractDomainParser.LEFT_CURLY)
            self.state = 71
            self.default_stmt()
            self.state = 72
            self.capability_list()
            self.state = 73
            self.match(AbstractDomainParser.RIGHT_CURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Default_stmtContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DEFAULT(self):
            return self.getToken(AbstractDomainParser.DEFAULT, 0)

        def REFERENCE(self):
            return self.getToken(AbstractDomainParser.REFERENCE, 0)

        def ID(self):
            return self.getToken(AbstractDomainParser.ID, 0)

        def getRuleIndex(self):
            return AbstractDomainParser.RULE_default_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefault_stmt" ):
                listener.enterDefault_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefault_stmt" ):
                listener.exitDefault_stmt(self)




    def default_stmt(self):

        localctx = AbstractDomainParser.Default_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_default_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.match(AbstractDomainParser.DEFAULT)
            self.state = 76
            self.match(AbstractDomainParser.REFERENCE)
            self.state = 77
            self.match(AbstractDomainParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Capability_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def capability(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(AbstractDomainParser.CapabilityContext)
            else:
                return self.getTypedRuleContext(AbstractDomainParser.CapabilityContext,i)


        def getRuleIndex(self):
            return AbstractDomainParser.RULE_capability_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCapability_list" ):
                listener.enterCapability_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCapability_list" ):
                listener.exitCapability_list(self)




    def capability_list(self):

        localctx = AbstractDomainParser.Capability_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_capability_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==AbstractDomainParser.CAPABILITY:
                self.state = 79
                self.capability()
                self.state = 84
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CapabilityContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CAPABILITY(self):
            return self.getToken(AbstractDomainParser.CAPABILITY, 0)

        def ID(self):
            return self.getToken(AbstractDomainParser.ID, 0)

        def LEFT_PAREN(self):
            return self.getToken(AbstractDomainParser.LEFT_PAREN, 0)

        def params(self):
            return self.getTypedRuleContext(AbstractDomainParser.ParamsContext,0)


        def RIGHT_PAREN(self):
            return self.getToken(AbstractDomainParser.RIGHT_PAREN, 0)

        def getRuleIndex(self):
            return AbstractDomainParser.RULE_capability

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCapability" ):
                listener.enterCapability(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCapability" ):
                listener.exitCapability(self)




    def capability(self):

        localctx = AbstractDomainParser.CapabilityContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_capability)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self.match(AbstractDomainParser.CAPABILITY)
            self.state = 86
            self.match(AbstractDomainParser.ID)
            self.state = 87
            self.match(AbstractDomainParser.LEFT_PAREN)
            self.state = 88
            self.params()
            self.state = 89
            self.match(AbstractDomainParser.RIGHT_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ParamsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def capability_arg(self):
            return self.getTypedRuleContext(AbstractDomainParser.Capability_argContext,0)


        def capability_arg_list(self):
            return self.getTypedRuleContext(AbstractDomainParser.Capability_arg_listContext,0)


        def getRuleIndex(self):
            return AbstractDomainParser.RULE_params

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParams" ):
                listener.enterParams(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParams" ):
                listener.exitParams(self)




    def params(self):

        localctx = AbstractDomainParser.ParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_params)
        try:
            self.state = 95
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 91
                self.capability_arg()
                self.state = 92
                self.capability_arg_list()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Capability_argContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def memory_interface(self):
            return self.getTypedRuleContext(AbstractDomainParser.Memory_interfaceContext,0)


        def data_type(self):
            return self.getTypedRuleContext(AbstractDomainParser.Data_typeContext,0)


        def var(self):
            return self.getTypedRuleContext(AbstractDomainParser.VarContext,0)


        def getRuleIndex(self):
            return AbstractDomainParser.RULE_capability_arg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCapability_arg" ):
                listener.enterCapability_arg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCapability_arg" ):
                listener.exitCapability_arg(self)




    def capability_arg(self):

        localctx = AbstractDomainParser.Capability_argContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_capability_arg)
        try:
            self.state = 102
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [AbstractDomainParser.INPUT, AbstractDomainParser.OUTPUT, AbstractDomainParser.STATE, AbstractDomainParser.PARAM]:
                self.enterOuterAlt(localctx, 1)
                self.state = 97
                self.memory_interface()
                self.state = 98
                self.data_type()
                self.state = 99
                self.var()
                pass
            elif token in [AbstractDomainParser.RIGHT_PAREN, AbstractDomainParser.COMMA]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Capability_arg_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMMA(self):
            return self.getToken(AbstractDomainParser.COMMA, 0)

        def capability_arg(self):
            return self.getTypedRuleContext(AbstractDomainParser.Capability_argContext,0)


        def capability_arg_list(self):
            return self.getTypedRuleContext(AbstractDomainParser.Capability_arg_listContext,0)


        def getRuleIndex(self):
            return AbstractDomainParser.RULE_capability_arg_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCapability_arg_list" ):
                listener.enterCapability_arg_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCapability_arg_list" ):
                listener.exitCapability_arg_list(self)




    def capability_arg_list(self):

        localctx = AbstractDomainParser.Capability_arg_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_capability_arg_list)
        try:
            self.state = 109
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [AbstractDomainParser.COMMA]:
                self.enterOuterAlt(localctx, 1)
                self.state = 104
                self.match(AbstractDomainParser.COMMA)
                self.state = 105
                self.capability_arg()
                self.state = 106
                self.capability_arg_list()
                pass
            elif token in [AbstractDomainParser.RIGHT_PAREN]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Memory_interfaceContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INPUT(self):
            return self.getToken(AbstractDomainParser.INPUT, 0)

        def OUTPUT(self):
            return self.getToken(AbstractDomainParser.OUTPUT, 0)

        def STATE(self):
            return self.getToken(AbstractDomainParser.STATE, 0)

        def PARAM(self):
            return self.getToken(AbstractDomainParser.PARAM, 0)

        def getRuleIndex(self):
            return AbstractDomainParser.RULE_memory_interface

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMemory_interface" ):
                listener.enterMemory_interface(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMemory_interface" ):
                listener.exitMemory_interface(self)




    def memory_interface(self):

        localctx = AbstractDomainParser.Memory_interfaceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_memory_interface)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 111
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << AbstractDomainParser.INPUT) | (1 << AbstractDomainParser.OUTPUT) | (1 << AbstractDomainParser.STATE) | (1 << AbstractDomainParser.PARAM))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Data_typeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(AbstractDomainParser.ID, 0)

        def getRuleIndex(self):
            return AbstractDomainParser.RULE_data_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterData_type" ):
                listener.enterData_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitData_type" ):
                listener.exitData_type(self)




    def data_type(self):

        localctx = AbstractDomainParser.Data_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_data_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            self.match(AbstractDomainParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class VarContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def var_id(self):
            return self.getTypedRuleContext(AbstractDomainParser.Var_idContext,0)


        def getRuleIndex(self):
            return AbstractDomainParser.RULE_var

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVar" ):
                listener.enterVar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVar" ):
                listener.exitVar(self)




    def var(self):

        localctx = AbstractDomainParser.VarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_var)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.var_id()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Var_idContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(AbstractDomainParser.ID, 0)

        def getRuleIndex(self):
            return AbstractDomainParser.RULE_var_id

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVar_id" ):
                listener.enterVar_id(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVar_id" ):
                listener.exitVar_id(self)




    def var_id(self):

        localctx = AbstractDomainParser.Var_idContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_var_id)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 117
            self.match(AbstractDomainParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





