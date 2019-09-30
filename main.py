#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 19:57:00 2019

@author: cmdrlias
"""
from token_model import token_model as tkm
from tag import tag
from colors import colors as clr
from interpreter import interpreter as inter

if __name__ == "__main__":
    file = inter('HelloPyscal.pys')
    
    print(clr.HEADER + "\n=>Lista de tokens\n" + clr.ENDC)
    tk = file.proximoToken()
    while (tk is not None and tk.getNome() != tag.EOF):
        print(tk.toString(), clr.UNDERLINE + 'Linha: ' + str(tk.getLinha()), 'Coluna: ' + str(tk.getColuna()) + clr.ENDC)
        tk = file.proximoToken()
        
    print(clr.HEADER + '\n=>Tabela de simbolos\n' + clr.ENDC)
    file.printTabelaDeSimbolos()
    file.closeFile()

    if(file.status()):
        print(clr.OKGREEN + '\n=> Compilado com sucesso\n')
    else:
        if(file.numErros() > 1):
            print(clr.WARNING + '\n=> Compilado com avisos (' + str(file.numErros()) + ' erros léxicos).\n')
        else:
            print(clr.WARNING + '\n=> Compilado com aviso (' + str(file.numErros()) + ' erro léxico).\n')