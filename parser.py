import sys
import copy

from ts import ts
from token_model import token_model as tkm
from tag import tag
from colors import colors as clr
from no import no

class parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.proximoToken()
        self._errosSemanticos = 0
        self._errosSintaticos = 0
        if(self.token is None):
            sys.exit(0)

    def erroSemantico(self, msg):
        print(clr.FAIL + '[Erro semântico]: ' + msg + '\n' + clr.ENDC)
        self._sts = False
        self._errosSemanticos += 1

    def erroSintatico(self, msg):
        print(clr.FAIL + '[Erro sintático]: ' + msg + '\n' + clr.ENDC)
        self._sts = False
        self._errosSintaticos += 1

    def advance(self):
        self.token = self.lexer.proximoToken()

        if self.token is None:
            sys.exit(0)

    def skip(self, message):
        self.erroSintatico(message)
        self.advance()

    # verifica token esperado t
    def eat(self, t):
        if(self.token.getNome() == t):
            self.advance()
            return True
        else:
            return False
    
    def programa(self):
        self.classe()
        if(not self.eat(tag.EOF)):
            self.erroSintatico('"EOF" esperado - Encontrado: ' + self.token.getLexema())
            sys.exit(0)
    
    def classe(self):
        tmp = copy.copy(self.token)

        if(self.eat(tag.KW_CLASS)):
            if(not self.eat(tag.ID)):
                self.erroSintatico('"id" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            else:
                self.lexer._ts.removeToken(tmp.getLexema())
                tmp.setTipo(tag.VAZIO)
                self.lexer._ts.addToken(tmp.getLexema(), tmp)

            if(not self.eat(tag.OP_COL)):
                self.erroSintatico('":" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

            self.listaFuncao()
            self.main()

            if(not self.eat(tag.KW_END)):
                self.erroSintatico('"end" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_DOT)):
                self.erroSintatico('"." esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
        else:
            self.erroSintatico('"class" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
    
    def declaraID(self):
        tmp = copy.copy(self.token)

        if(self.eat(tag.KW_BOOL) or self.eat(tag.KW_INT) \
                or self.eat(tag.KW_STRING) or self.eat(tag.KW_DOUBLE) \
                or self.eat(tag.KW_VOID)):
            self.lexer._ts.removeToken(tmp.getLexema());
            tmp.setTipo(self.tipoPrimitivo().tipo)
            self.lexer._ts.addToken(tmp.getLexema(), tmp)
            if(not self.eat(tag.ID)):
                self.erroSintatico('"id" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_SCOL)):
                self.erroSintatico('";" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
        else:
            self.skip('Declaração de variável esperada em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.EOF)): 
                self.declaraID()

    def listaFuncao(self):
        if(self.eat(tag.KW_DEF)):
            self.listaFuncaoLinha()
        else:
            self.skip('"def" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if not self.eat(tag.EOF): self.listaFuncao()

    def listaFuncaoLinha(self):
        if(self.eat(tag.KW_DEF)):
            self.funcao()
            self.listaFuncao()

    def funcao(self):
        tmp = copy.copy(self.token)
        if(self.eat(tag.KW_DEF)):
            self.tipoPrimitivo()
            if(not self.eat(tag.ID)):
                self.erroSintatico('"id" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            else:
                self.lexer._ts.removeToken(tmp.getLexema())
                tmp.setTipo(tag.VAZIO)
                self.lexer._ts.addToken(tmp.getLexema(), tmp)

            if(not self.eat(tag.OP_OPAR)):
                self.erroSintatico('"(" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            
            self.listaArg()

            if(not self.eat(tag.OP_CPAR)):
                self.erroSintatico('")" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_COL)):
                self.erroSintatico('":" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

            self.regexDeclaraId()
            self.listaCmd()
            self.retorno()

            if(not self.eat(tag.KW_END)):
                self.erroSintatico('"end" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_SCOL)):
                self.erroSintatico('";" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
        else:
            self.erroSintatico('"def" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

    def regexDeclaraId(self):
        if(self.eat(tag.KW_VOID) or self.eat(tag.KW_STRING) \
                or self.eat(tag.KW_BOOL) or self.eat(tag.KW_INT) \
                or self.eat(tag.KW_DOUBLE)):
            self.declaraID()
            self.regexDeclaraId()
            return
        if(not self.eat(tag.ID) or not self.eat(tag.KW_END) \
                or not self.eat(tag.KW_RETURN) \
                or not self.eat(tag.KW_IF) or not self.eat(tag.KW_WRITE) \
                or not self.eat(tag.KW_WHILE)):
            self.skip('Declaração de variável esperada em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.EOF)): 
                self.regexDeclaraId()

    def listaArg(self):
        if(self.eat(tag.KW_VOID) or self.eat(tag.KW_STRING) \
                or self.eat(tag.KW_BOOL) or self.eat(tag.KW_INT) \
                or self.eat(tag.KW_DOUBLE)):
            self.arg()
            self.listaArgLinha()
        else:
            self.skip('Declaração de variável esperada em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.EOF)): 
                self.listaArg()

    def listaArgLinha(self):
        if(self.eat(tag.OP_COMMA)):
            self.listaArg()
            return
        if(not self.eat(tag.OP_CPAR)):
            self.skip('"," esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if not self.eat(tag.EOF): self.listaArgLinha()

    def arg(self):
        tmp = copy.copy(self.token)
        self.tipoPrimitivo()            
        if(not self.eat(tag.ID)):
            self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            self.lexer._ts.removeToken(tmp.getLexema())
            tmp.setTipo(tag.VAZIO)
            self.lexer._ts.addToken(tmp.getLexema(), tmp)

    def retorno(self):
        if(self.eat(tag.KW_RETURN)):
            self.expressao()
            if(not self.eat(tag.OP_SCOL)):
                self.erroSintatico('";" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            return
        if(not self.eat(tag.KW_END)):
            self.skip('Declaração de variável esperada em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.EOF)): 
                self.retorno()

    def main(self):
        tmp = copy.copy(self.token)
        if(self.eat(tag.KW_STATIC)):
            if(not self.eat(tag.KW_VOID)):
                self.erroSintatico('"void" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.KW_MAIN)):
                self.erroSintatico('"main" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_OPAR)):
                self.erroSintatico('"(" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            
            if(not self.eat(tag.KW_STRING)):
                self.erroSintatico('"string" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_OBRACK)):
                self.erroSintatico('"[" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_CBRACK)):
                self.erroSintatico('"]" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.ID)):
                self.erroSintatico('"id" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            
            
            self.lexer._ts.removeToken(tmp.getLexema())
            tmp.setTipo(tag.STRING)
            self.lexer._ts.addToken(tmp.getLexema(), tmp)

            if(not self.eat(tag.OP_CPAR)):
                self.erroSintatico('")" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_SCOL)):
                self.erroSintatico('":" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

            self.regexDeclaraId()
            self.listaCmd()

            if(not self.eat(tag.KW_END)):
                self.erroSintatico('"end" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_SCOL)):
                self.erroSintatico('";" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
        else:
            self.skip('"defstatic" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.EOF)): 
                self.main()

    def tipoPrimitivo(self):
        if(not self.eat(tag.KW_BOOL) and not self.eat(tag.KW_INT) \
                and not self.eat(tag.KW_STRING) \
                and not self.eat(tag.KW_DOUBLE) \
                and not self.eat(tag.KW_VOID)):
            self.erroSintatico('"end" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            return

    def listaCmd(self):
        if(self.eat(tag.ID) or self.eat(tag.KW_IF) \
                or self.eat(tag.KW_WHILE) \
                or self.eat(tag.KW_WRITE) \
                or self.eat(tag.KW_RETURN)):
            self.listaCmdLinha()
        else:
            self.skip('Declaração de variável esperada em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.EOF)): 
                self.listaCmd()

    def listaCmdLinha(self):
        if(self.eat(tag.ID) \
            or self.eat(tag.KW_IF) \
            or self.eat(tag.KW_WHILE) \
            or self.eat(tag.KW_WRITE)):
            self.cmd()
            self.listaCmdLinha()
            return
        if(self.eat(tag.KW_RETURN) \
            or self.eat(tag.KW_END) \
            or self.eat(tag.KW_ELSE)):
            self.skip('Declaração de variável esperada em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.EOF)): 
                self.listaCmdLinha()

    def cmd(self):
        tmp = copy.copy(self.token)

        if(self.eat(tag.ID)):
            if (tmp.getTipo() == None):
                self.erroSemantico('ID esperada em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
                #sys.exit(0)

            noCmdAtribFunc = self.CmdAtribFunc()

            if (noCmdAtribFunc.tipo != tag.VAZIO and tmp.getTipo() != noCmdAtribFunc.tipo):
                self.erroSemantico('Tipos incompatíveis em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
                #sys.exit(0)
        elif(self.eat(tag.KW_IF)):
            self.cmdIf()
        elif(self.eat(tag.KW_WHILE)):
            self.cmdWhile()
        elif(self.eat(tag.KW_WRITE)):
            self.cmdWrite()
        else:
            self.erroSintatico('Declaração de variável esperada em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            return

    def cmdAtribFunc(self):
        if(self.eat(tag.OP_OPAR)):
            self.cmdFuncao()
            return
        elif(self.eat(tag.OP_EQL)):
            self.cmdAtribFunc()
        else:
            self.erroSintatico('"end" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.EOF)): 
                self.cmdAtribFunc()

    def cmdIf(self):
        if(self.eat(tag.KW_IF)):
            if(not self.eat(tag.OP_OPAR)):
                self.erroSintatico('"(" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

            self.expressao()

            if(not self.eat(tag.OP_CPAR)):
                self.erroSintatico('")" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_COL)):
                self.erroSintatico('":" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

            self.listaCmd()
            self.cmdIfLinha()
        else:
            self.erroSintatico('"if" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

    def cmdIfLinha(self):
        if(self.eat(tag.KW_END)):
            if(not self.eat(tag.OP_SCOL)):
                self.erroSintatico('";" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            return
        elif(self.eat(tag.KW_ELSE)):
            if(not self.eat(tag.OP_COL)):
                self.erroSintatico('":" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

            self.listaCmd()

            if not self.eat(tag.KW_END):
                self.erroSintatico('"end" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if not self.eat(tag.OP_SCOL):
                self.erroSintatico('";" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
        else:
            self.erroSintatico('"end/else" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

    def cmdWhile(self):
        if self.eat(tag.KW_WHILE):
            if(not self.eat(tag.OP_OPAR)):
                self.erroSintatico('"(" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

            self.expressao()

            if(not self.eat(tag.OP_CPAR)):
                self.erroSintatico('")" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_COL)):
                self.erroSintatico('":" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

            self.listaCmd()

            if(not self.eat(tag.KW_END)):
                self.erroSintatico('"end" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_SCOL)):
                self.erroSintatico('";" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
        else:
            self.erroSintatico('"while" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

    def cmdWrite(self):
        if self.eat(tag.KW_WRITE):
            if not self.eat(tag.OP_OPAR):
                self.erroSintatico('"(" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

            self.expressao()

            if(not self.eat(tag.OP_CPAR)):
                self.erroSintatico('")" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if not self.eat(tag.OP_SCOL):
                if(not self.eat(tag.OP_CPAR)):
                    self.erroSintatico('";" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                    + ' - Encontrado: ' + self.token.getLexema())
        else:
            if(not self.eat(tag.OP_CPAR)):
                self.erroSintatico('"write" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

    def cmdAtribui(self):
        if self.eat(tag.OP_ATR):
            self.expressao()
            if(not self.eat(tag.OP_SCOL)):
                self.erroSintatico('";" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
        else:
            self.erroSintatico('"=" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

    def cmdFuncao(self):
        if(self.eat(tag.OP_OPAR)):
            self.regexExp()
            if(not self.eat(tag.OP_CPAR)):
                self.erroSintatico('")" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.OP_SCOL)):
                self.erroSintatico('";" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
        else:
            self.erroSintatico('"(" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

    def regexExp(self):
        if(self.eat(tag.ID) or self.eat(tag.OP_OPAR) \
                or self.eat(tag.NUM_INTEIRO) or self.eat(tag.NUM_DOUBLE) \
                or self.eat(tag.LIT) or self.eat(tag.KW_TRUE) or self.eat(tag.KW_FALSE) or self.eat(tag.OP_NEG)\
                or self.eat(tag.OP_NEG)):
            self.expressao()
            self.regexExpLinha()
            return
        elif(not self.eat(tag.OP_CPAR)):
            self.skip('Declaração de variável esperada em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.EOF)): 
                self.regexExp()

    def regexExpLinha(self):
        if self.eat(tag.OP_COMMA):
            self.expressao()
            self.regexExpLinha()
            return
        elif not self.eat(tag.OP_CPAR):
            self.sinalizaErroSintatico('")" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

    def expressao(self):
        if self.eat(tag.ID) or self.eat(tag.NUM_INTEIRO) \
                or self.eat(tag.NUM_DOUBLE) or self.eat(tag.LIT) \
                or self.eat(tag.KW_TRUE) or self.eat(tag.KW_FALSE) \
                or self.eat(tag.OP_OPAR) or self.eat(tag.OP_NEG)\
                or self.eat(tag.OP_DIF):
            self.exp1()
            self.expLinha()
        else:
            self.skip('Declaração de variável esperada em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if not self.eat(tag.EOF): self.expressao()

    def expLinha(self):
        if(self.eat(tag.KW_OR) or self.eat(tag.KW_AND)):
            self.exp1()
            self.expLinha()
            return
        elif(self.eat(tag.OP_FPA) or self.eat(tag.OP_SCOL) \
                or self.eat(tag.OP_COMMA)):
            self.skip('"or, and, ;, ), ," esperados em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if (not self.eat(tag.EOF)): 
                self.expLinha()

    def exp1(self):
        if(self.eat(tag.OP_ID) or self.eat(tag.OP_APA) \
                or self.eat(tag.NUM_INTEIRO) or self.eat(tag.NUM_DOUBLE) \
                or self.eat(tag.LIT) or self.eat(tag.KW_TRUE) \
                or self.eat(tag.KW_FALSE) \
                or self.eat(tag.OP_EQL) \
                or self.eat(tag.OP_EXCL)):
            self.exp2()
            self.exp1Linha()
        else:
            self.skip('Declaração de variável esperada em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if not self.eat(tag.EOF): self.exp1()

    def exp1Linha(self):
        if(self.eat(tag.OP_MENOR) or self.eat(tag.OP_MENOR_IGUAL) \
                or self.eat(tag.OP_GRTR) \
                or self.eat(tag.OP_GRTEQ) \
                or self.eat(tag.OP_EQL) \
                or self.eat(tag.OP_DIF)):
            self.exp2()
            self.exp1Linha()
            return

        elif(not self.eat(tag.KW_OR) or not self.eat(tag.KW_AND) \
                or not self.eat(tag.OP_OPAR) \
                or not self.eat(tag.OP_SCOL) \
                or not self.eat(tag.OP_COMMA)):
            self.sinalizaErroSintatico('Operador esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            
    def exp2(self):
        if self.eat(tag.ID) or self.eat(tag.OP_OPAR) \
            or self.eat(tag.NUM_INTEIRO) \
                or self.eat(tag.NUM_DOUBLE) \
                or self.eat(tag.LIT) \
                or self.eat(tag.KW_TRUE) \
                or self.eat(tag.KW_FALSE) \
                or self.eat(tag.OP_DIF) \
                or self.eat(tag.OP_NEG):
            self.exp3()
            self.exp2Linha()
        else:
            self.skip('Declaração de variável esperada em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if not self.eat(tag.EOF): self.exp2()

    def exp2Linha(self):
        if self.eat(tag.OP_PLUS) or self.eat(tag.OP_SUB):
            self.exp3()
            self.exp2Linha()
            return
        elif self.eat(tag.OP_GRTR) or self.eat(tag.OP_GRTEQ) or self.eat(tag.OP_LESS) or \
                self.eat(tag.OP_LESEQ) or self.eat(tag.OP_EQL) or self.eat(tag.OP_DIF) \
                or self.eat(tag.KW_OR) or self.eat(tag.KW_AND) or self.eat(tag.OP_CPAR) or self.eat(tag.OP_SCOL)\
                or self.eat(tag.OP_COMMA):
            self.skip('Operador ou variável esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if not self.eat(tag.EOF): self.exp2Linha()

    def exp3(self):
        if self.eat(tag.ID) or self.eat(tag.OP_OPAR) \
                or self.eat(tag.NUM_INTEIRO) \
                or self.eat(tag.NUM_DOUBLE) \
                or self.eat(tag.LIT) \
                or self.eat(tag.KW_TRUE) \
                or self.eat(tag.KW_FALSE) \
                or self.eat(tag.OP_DIF) \
                or self.eat(tag.OP_NEG):
            self.exp4()
            self.exp3Linha()
        else:
            self.skip('Operador ou variável esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if not self.eat(tag.EOF): self.exp3()

    def exp3Linha(self):
        if (self.eat(tag.OP_MULT) or self.eat(tag.OP_SLSH)):
            self.exp4()
            self.exp3Linha()
            return
        elif(self.eat(tag.OP_SUB) or self.eat(tag.OP_PLUS) \
                    or self.eat(tag.OP_GRTR) \
                    or self.eat(tag.OP_GRTEQ)\
                    or self.eat(tag.OP_LESS) \
                    or self.eat(tag.OP_LESEQ) \
                    or self.eat(tag.OP_IGUAL_IGUAL) \
                    or self.eat(tag.OP_DIFERENTE) \
                    or self.eat(tag.KW_OR) \
                    or self.eat(tag.KW_AND) \
                    or self.eat(tag.OP_FPA)\
                    or self.eat(tag.OP_PONTO_VIRGULA) \
                    or self.eat(tag.OP_VIRGULA)):
            self.skip('Operador esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if(not self.eat(tag.EOF)): 
                self.exp3Linha()

    def exp4(self):
        tmp = copy.copy(self.token)
        noExp4 = no()
        if(self.eat(tag.ID)):
            self.exp4Linha()
            noExp4.tipo = tmp.getTipo()
            if (noExp4.tipo == None ):
                noExp4.tipo = tag.TIPO_ERRO
                self.sinalizaErroSemantico("Erro, ID nao declado")
                sys.exit(0)
            
            return noExp4
        elif(self.eat(tag.OP_NEGACAO) or self.eat(tag.OP_DIFERENTE)):
            self.exp4()
            return
        elif(self.eat(tag.OP_APA)):
            self.expressao()
            if(not self.eat(tag.OP_CPAR)):
                self.sinalizaErroSintatico('")" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
                return
        elif(not self.eat(tag.NUM_INTEIRO) and not self.eat(tag.LIT) and not self.eat(tag.NUM_DOUBLE)  and not self.eat(tag.KW_TRUE)  and not self.eat(tag.KW_FALSE)):
            self.sinalizaErroSintatico('Operando ou variável esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())

    def exp4Linha(self):
        if(self.eat(tag.OP_APA)):
            self.regexExp()
            if(not self.eat(tag.OP_CPAR)):
                self.sinalizaErroSintatico('")" esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
        elif (self.eat(tag.OP_MULT) \
                or self.eat(tag.OP_DIV) \
                or self.eat(tag.OP_SUB)\
                or self.eat(tag.OP_PLUS) \
                or self.eat(tag.OP_GRTR) \
                or self.eat(tag.OP_GRTEQ)\
                or self.eat(tag.OP_LESS) \
                or self.eat(tag.OP_LESEQ) \
                or self.eat(tag.OP_EQL)\
                or self.eat(tag.OP_DIF) \
                or self.eat(tag.KW_OR) \
                or self.eat(tag.KW_AND) \
                or self.eat(tag.OP_CPAR)\
                or self.eat(tag.OP_SCOL) \
                or self.eat(tag.OP_COMMA)):
            self.skip('Operador esperado em '+ str(self.token.getLinha()) + ', ' + str(self.token.getColuna()) 
                + ' - Encontrado: ' + self.token.getLexema())
            if not self.eat(tag.EOF): self.exp4Linha()

    def opUnario(self):
        if not self.eat(tag.OP_NEG) and not self.eat(tag.OP_DIF):
            self.skip("Esperado \"-n, !\", encontrado " + "\"" + self.token.getLexema() + "\"")
            if not self.eat(tag.EOF): self.opUnario()

            