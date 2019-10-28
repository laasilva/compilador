#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 20:16:00 2019

@author: cmdrlias
"""
import sys

from ts import ts
from token_model import token_model as tkm
from tag import tag
from colors import colors as clr

class lexer:
    def __init__(self, file):
        try:
            self._file = open(file, 'rb')
            self._lookahead = 0
            self._lookbehind = 0
            self._nline = 1
            self._ncolumn = 1
            self._ts = ts()
            self._sts = True
            self._erros = 0
            
            self._anterior = 0
            
            self._comment = False
            self._string_tag = False
            self._par = False
            self._brack = False
            self._dash = False
        except IOError:
            print(clr.FAIL + 'FATAL! Erro ao ler arquivo de código.')
            sys.exit(0)
        
    def closeFile(self):
        try:
            self._file.close()
        except IOError:
            print(clr.FAIL + 'FATAL! Erro ao fechar arquivo de código.')
            sys.exit(0)
    
    def erroLexico(self, msg):
        print(clr.FAIL + '[Erro lexico]: ' + msg + '\n' + clr.ENDC)
        self._sts = False
        self._erros += 1

    def printTabelaDeSimbolos(self):
        self._ts.printTS()
    
    def contarLinha(self):
        self._ncolumn = 1
        self._nline += 1
        
    def contarColuna(self):
        self._ncolumn += 1
    
    def proximoToken(self):
        state = 0
        word = ""
        char = '\u0000' 
        lookahead = True
    
        while(True):
            if(lookahead):
                self._lookahead = self._file.read(1)
                char = self._lookahead.decode('ascii')
            lookahead = True
            if(self._lookahead == b'\n'):
                self.contarLinha()
            elif(self._lookahead == b' '):
                self.contarColuna()

            if(char == '#'):
                self._comment = True
                return tkm(tag.OP_COMMENT, '#', self._nline, self._ncolumn)

            if(self._comment):
                state = 25

            if(self._string_tag):
                state = 24

            if(state == 0):
                #verificação de caracteres não iseridas
                if(self._string_tag):
                    self.erroLexico('Caractere [ \" ] esperado em (' + str(self._nline) + ',' + str(self._ncolumn) + ')')
                    self._string_tag = False

                if(char == ''):
                    return tkm(tag.EOF, "EOF", self._nline, self._ncolumn)
                elif(char == ' ' or char == '\t' or char == '\n' or char == '\r'):
                    state = 0
                elif(char.isalpha()):
                    word += char
                    state = 2
                elif(char.isdigit()):
                    word += char
                    state = 3
                elif(char == '='):
                    state = 4
                elif(char == '+'):
                    state = 5
                elif(char == '-'):
                    state = 6
                elif(char == '*'):
                    state = 7
                elif(char == '/'):
                    state = 8
                elif(char == '['):
                    lookahead = False
                    state = 9
                elif(char == ']'):
                    state = 10
                elif(char == '('):
                    lookahead = False
                    state = 11
                elif(char == ')'):
                    state = 12
                elif(char == '.'):
                    state = 13
                elif(char == ','):
                    state = 14
                elif(char == ':'):
                    state = 15
                elif(char == ';'):
                    state = 16
                elif(char == '<'):
                    state = 17
                elif(char == '>'):
                    state = 18
                elif(char == '!'):
                    state = 19
                elif(char == 'and'):
                    state = 20
                elif(char == 'or'):
                    state = 21
                elif(char == 'true'):
                    state = 22
                elif(char == 'false'):
                    state = 23
                elif(char == '\"'):
                    state = 24
                elif(char == "#"):
                    state = 25
                    self._comment = True
                else:
                    self.erroLexico('Caractere [' + char + '] inválido. (' + str(self._nline) + 
                                    ',' + str(self._ncolumn) + ')')
            elif(state == 2):
                if(char.isalnum() or char == '_'):
                    word += char
                else:
                    self.voltaPonteiro()
                    tk = self._ts.getToken(word)
                    self._anterior = tk
                    if(tk is None):
                        tk = tkm(tag.ID, word, self._nline, self._ncolumn)
                        self._anterior = tk
                        self._ts.addToken(word, tk)
                    else:
                        self._ts.getToken(word).setLinha(self._nline)
                        self._ts.getToken(word).setColuna(self._ncolumn)
                    return tk
            elif(state == 3):
                if(char.isdigit()):
                    word += char          
                else:
                    self.voltaPonteiro()
                    tk = self._ts.getToken(word)
                    self._anterior = tk
                    if(tk is None):
                        tk = tkm(tag.NUM, word, self._nline, self._ncolumn)
                        self._anterior = tk
                        self._ts.addToken(word, tk)
                    else:
                        self._ts.getToken(word).setLinha(self._nline)
                        self._ts.getToken(word).setColuna(self._ncolumn)
                    return tk
            elif(state == 4):
                if(char == '='):
                    self._anterior = tkm(tag.OP_EQL, '==', self._nline, self._ncolumn)
                    return tkm(tag.OP_EQL, '==', self._nline, self._ncolumn)
                elif(char == ' ' or char == '\t' or char == '\n'):
                    self._anterior = tkm(tag.OP_ATR, '=', self._nline, self._ncolumn)
                    return tkm(tag.OP_ATR, '=', self._nline, self._ncolumn)
                else:
                    self.erroLexico('Caractere [' + char + '] inesperado em (' + str(self._nline) + ',' + str(self._ncolumn) + ')')
                    return None
                self._anterior = tkm(tag.OP_EQL, '=', self._nline, self._ncolumn)
                return tkm(tag.OP_EQL, '=', self._nline, self._ncolumn)
            elif(state == 5):
                self._anterior = tkm(tag.OP_PLUS, '+', self._nline, self._ncolumn)
                return tkm(tag.OP_PLUS, '+', self._nline, self._ncolumn)
            elif(state == 6):
                if(self._anterior is not None and self._anterior.getNome() == tag.NUM):
                    self._anterior = tkm(tag.OP_SUB, '-', self._nline, self._ncolumn)
                    return tkm(tag.OP_SUB, '-', self._nline, self._ncolumn)
                else:
                    self._anterior = tkm(tag.OP_NEG, '-', self._nline, self._ncolumn)
                    return tkm(tag.OP_NEG, '-', self._nline, self._ncolumn)
            elif(state == 7):
                self._anterior = tkm(tag.OP_MULT, '*', self._nline, self._ncolumn)
                return tkm(tag.OP_MULT, '*', self._nline, self._ncolumn)
            elif(state == 8):
                self._anterior = tkm(tag.OP_SLSH, '/', self._nline, self._ncolumn)
                return tkm(tag.OP_SLSH, '/', self._nline, self._ncolumn)
            elif(state == 9):
                self._brack = True
                self._anterior = tkm(tag.OP_OBRACK, '[', self._nline, self._ncolumn)
                return tkm(tag.OP_OBRACK, '[', self._nline, self._ncolumn)
            elif(state == 10):
                self._anterior = tkm(tag.OP_CBRACK, ']', self._nline, self._ncolumn)
                return tkm(tag.OP_CBRACK, ']', self._nline, self._ncolumn)
            elif(state == 11):
                self._par = True
                self._anterior = tkm(tag.OP_OPAR, '(', self._nline, self._ncolumn)
                return tkm(tag.OP_OPAR, '(', self._nline, self._ncolumn)
            elif(state == 12):
                self._par = False
                self._anterior = tkm(tag.OP_CPAR, ')', self._nline, self._ncolumn)
                return tkm(tag.OP_CPAR, ')', self._nline, self._ncolumn)
            elif(state == 13):
                if(char == '' or char == ' '):
                    self._anterior = tkm(tag.OP_DOT, '.', self._nline, self._ncolumn)
                    return tkm(tag.OP_DOT, '.', self._nline, self._ncolumn)
                else:
                    self.erroLexico('Caractere [' + char + '] inesperado em (' + str(self._nline) + ',' + str(self._ncolumn) + ')')
                    return None
            elif(state == 14):
                if(char == '' or char == ' '):
                    self._anterior = tkm(tag.OP_COMMA, ',', self._nline, self._ncolumn)
                    return tkm(tag.OP_COMMA, ',', self._nline, self._ncolumn)
                else:
                    self.erroLexico('Caractere [' + char + '] inesperado em (' + str(self._nline) + ',' + str(self._ncolumn) + ')')
                    return None
            elif(state == 15):
                self._anterior = tkm(tag.OP_COL, ':', self._nline, self._ncolumn)
                return tkm(tag.OP_COL, ':', self._nline, self._ncolumn)
            elif(state == 16):
                self._anterior = tkm(tag.OP_SCOL, ';', self._nline, self._ncolumn)
                return tkm(tag.OP_SCOL, ';', self._nline, self._ncolumn)
            elif(state == 17):
                if(char == '='):
                    self._anterior = tkm(tag.OP_EQL, '<=', self._nline, self._ncolumn)
                    return tkm(tag.OP_EQL, '<=', self._nline, self._ncolumn)
                elif(char == ' ' or char == '\t' or char == '\n' or char == '\r'):
                    self._anterior = tkm(tag.OP_LESS, '<', self._nline, self._ncolumn)
                    return tkm(tag.OP_LESS, '<', self._nline, self._ncolumn)
                else:
                    self.erroLexico('Caractere [' + char + '] inesperado em (' + str(self._nline) + ',' + str(self._ncolumn) + ')')
                    return None
            elif(state == 18):
                if(char == '='):
                    self._anterior = tkm(tag.OP_GRTEQ, '>=', self._nline, self._ncolumn)
                    return tkm(tag.OP_GRTEQ, '>=', self._nline, self._ncolumn)
                elif(char == ' ' or char == '\t' or char == '\n' or char == '\r'):
                    self._anterior = tkm(tag.OP_GRTR, '>', self._nline, self._ncolumn)
                    return tkm(tag.OP_GRTR, '>', self._nline, self._ncolumn)
                else:
                    self.erroLexico('Caractere [' + char + '] inesperado em (' + str(self._nline) + ',' + str(self._ncolumn) + ')')
                    return None
            elif(state == 19):
                if(char == '='):
                    self._anterior = tkm(tag.OP_DIF, '!=', self._nline, self._ncolumn)
                    return tkm(tag.OP_DIF, '!=', self._nline, self._ncolumn)
                elif(char == ' ' or char == '\t' or char == '\n' or char == '\r'):
                    self._anterior = tkm(tag.OP_GRTR, '!', self._nline, self._ncolumn)
                    return tkm(tag.OP_GRTR, '!', self._nline, self._ncolumn)
                else:
                    self.erroLexico('Caractere [' + char + '] inesperado em (' + str(self._nline) + ',' + str(self._ncolumn) + ')')
                    return None
            elif(state == 20):
                self._anterior = tkm(tag.OP_AND, 'and', self._nline, self._ncolumn)
                return tkm(tag.OP_AND, 'and', self._nline, self._ncolumn)
            elif(state == 21):
                self._anterior = tkm(tag.OP_OR, 'or', self._nline, self._ncolumn)
                return tkm(tag.OP_OR, 'or', self._nline, self._ncolumn)
            elif(state == 22):
                self._anterior = tkm(tag.OP_TRUE, 'true', self._nline, self._ncolumn)
                return tkm(tag.OP_TRUE, 'true', self._nline, self._ncolumn)
            elif(state == 23):
                self._anterior = tkm(tag.OP_FALSE, 'false', self._nline, self._ncolumn)
                return tkm(tag.OP_FALSE, 'false', self._nline, self._ncolumn)
            elif(state == 24):
                word += char
                self._string_tag = True
                if(char == '\"'):
                    if(word == '\"'):
                        tk = tkm(tag.STRING, "null", self._nline, self._ncolumn)
                        self._anterior = tk
                        self._ts.addToken("null", tk)    
                    else:
                        tk = tkm(tag.STRING, word[:-1], self._nline, self._ncolumn)
                        self._anterior = tk
                        self._ts.addToken(word[:-1], tk)
                    self._string_tag = False
                    return tk
            elif(state == 25):
                word += char
                self._comment = True
                if(self._lookahead == b'\n'):
                    tk = tkm(tag.COMMENT, word[:-1], self._nline, self._ncolumn)
                    self._ts.addToken(word[:-1], tk)
                    self._comment = False
                    return tk
                
            # elif(state == 4):
            #     if(char == '='):
            #         return tkm(tag.OP_EQL, '==', self._nline, self._ncolumn)
            #     else:
            #         self.erroLexico('Caractere [' + char + '] inválido em (' + str(self._nline) + ',' + str(self._ncolumn) + ')')
            #         return None
        

    def voltaPonteiro(self):
        if(self._lookahead.decode('ascii') != ''):
            self._file.seek(self._file.tell()-1)
    
    def status(self):
        return self._sts
    
    def numErros(self):
        return self._erros
            
    