#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 20:21:32 2019

@author: cmdrlias
"""

from tag import tag
from token_model import token_model as tkm

from colors import colors as clr

class ts:
   def __init__(self):
      self.ts = {}

      self.ts['class'] = tkm(tag.KW_CLASS, 'class', 0, 0)
      self.ts['end'] = tkm(tag.KW_END, 'end', 0, 0)
      self.ts['def'] = tkm(tag.KW_DEF, 'def', 0, 0)
      self.ts['return'] = tkm(tag.KW_RETURN, 'return', 0, 0)
      self.ts['defstatic'] = tkm(tag.KW_STATIC, 'defstatic', 0, 0)
      self.ts['void'] = tkm(tag.KW_VOID, 'void', 0, 0)
      self.ts['main'] = tkm(tag.KW_MAIN, 'main', 0, 0)
      self.ts['bool'] = tkm(tag.KW_BOOL, 'bool', 0, 0)
      self.ts['String'] = tkm(tag.KW_STRING, 'String', 0, 0)
      self.ts['int'] = tkm(tag.KW_INT, 'int', 0, 0)
      self.ts['double'] = tkm(tag.KW_DOUBLE, 'double', 0, 0)
      self.ts['if'] = tkm(tag.KW_IF, 'if', 0, 0)
      self.ts['else'] = tkm(tag.KW_ELSE, 'else', 0, 0)
      self.ts['while'] = tkm(tag.KW_WHILE, 'while', 0, 0)
      self.ts['write'] = tkm(tag.KW_WRITE, 'write', 0, 0)
      self.ts['return'] = tkm(tag.KW_RETURN, 'return', 0, 0)
      
   def getToken(self, lexema):
      tk = self.ts.get(lexema)
      return tk

   def addToken(self, lexema, tk):
      self.ts[lexema] = tk

   def removeToken(self, lexema):
      self.ts.pop(lexema)

   def printTS(self):
      for k, t in (self.ts.items()):
         print(clr.OKBLUE + k + ":" + clr.ENDC, t.toString())
