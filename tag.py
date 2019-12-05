#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 20:17:53 2019

@author: cmdrlias
"""

from enum import Enum

class tag(Enum):
   # Fim de arquivo
   EOF = -1

   # Palavras-chave
   KW_CLASS = 1
   KW_END = 2
   KW_DEF = 3
   KW_RETURN = 4
   KW_STATIC = 5 
   KW_VOID = 6
   KW_MAIN = 7
   KW_BOOL = 8
   KW_INT = 9
   KW_STRING = 10
   KW_DOUBLE = 11
   KW_IF = 12
   KW_ELSE = 13
   KW_WHILE = 14
   KW_WRITE = 15
   
   # Operadores 
   OP_DOT = 16
   OP_SCOL = 17
   OP_COL = 18
   OP_OPAR = 19
   OP_CPAR = 20
   OP_COMMA = 21
   OP_ATR = 22
   OP_OR = 23
   OP_AND = 24
   OP_GRTR = 25
   OP_LESS = 26
   OP_EQL = 27
   OP_SLSH = 28
   OP_MULT = 29
   OP_SUB = 30
   OP_PLUS = 31
   OP_EXCL = 32
   OP_TRUE = 33
   OP_FALSE = 34
   OP_GRTEQ = 35
   OP_LESEQ = 36
   OP_DIF = 37
   OP_OBRACK = 38
   OP_CBRACK = 39
   OP_QUOTE = 40
   OP_COMMENT = 41
   OP_NEG = 42

   # Identificador
   ID = 43

   # Numeros
   NUM = 44
   NUM_INTEIRO = 47
   NUM_DOUBLE = 48

   # String
   STRING = 45
   COMMENT = 46

   LIT = 49

   TIPO_VAZIO = 50