#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 20:32:56 2019

@author: cmdrlias
"""
from colors import colors as clr
from tag import tag

class token_model:
    def __init__(self, nome, lexema, linha, coluna):
        self.nome = nome
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna
        self.tipo = tag.VAZIO

    def getNome(self):
        return self.nome

    def getLexema(self):
        return self.lexema

    def getLinha(self):
        return self.linha

    def setLinha(self, linha):
        self.linha = linha

    def getColuna(self):
        return self.coluna

    def setColuna(self, coluna):
        self.coluna = coluna
    
    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
      self.tipo = tipo

    def toString(self):
        return "<" + clr.BOLD + str(self.nome.name) + clr.ENDC + ", \"" + str(self.lexema) + "\">"
