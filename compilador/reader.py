import pandas as pd

class reader:
    def __init__(self, file, ts, code):
        self.__file = file
        self.__ts = ts
        self.__code = code
    
    # Lê o arquivo de código e monta array com as palavras, números e simbolos encontrados
    def read(self):
        word = ''
        with open(self.__file) as fp:
            w = fp.read()
            for c in w:
                word += c
                if(c == ' ' or c == '/n' or c == ':' or c == ';' or c == '.' or c == '(' or c == ')'):
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
        self.__code = [x for x in self.__code if x not in ['\n', '\t', '', ' ']]

    # Retorna o array do código
    def get_code(self):
        return self.__code
