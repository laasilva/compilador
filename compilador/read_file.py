import pandas as pd

class read_file:
    def __init__(self, file, ts, code):
        self.__file = file
        self.__ts = ts
        self.__code = code

    def read(self):
        with open(self.__file) as fp:
            w = fp.read()
            for c in w:
                word += c
                # fazer verificação, além de espaços, de tokens seguidos de operadores
                if(c == ' ' or c == '/n' or c == ':' or c == ';' or c == '.' or c == '(' or c == ')'):
                    # antes de fazer o append, verificar de acordo com o array de tokens
                    # verificar se é uma key, um operador ou um id
                    for i, row in self.__ts.iterrows():
                        if(word[:-1] == row['lexema']):
                            self.__code.append(word[:-1])
                    if(c == ':'):
                        self.__code.append(':')
                    if(c == ';'):
                        self.__code.append(';')
                    if(c == '.'):
                        self.__code.append('.')
                    if(c == '('):
                        self.__code.append('(')
                    if(c == ')'):
                        self.__code.append(')')
                    word = ''

