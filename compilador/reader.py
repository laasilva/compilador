import pandas as pd
from interpreter import interpreter as inter
from colors import colors

class reader:
    def __init__(self, file, code):
        self.__file = file
        self.__code = code
    
    # Lê o arquivo de código e monta array com as palavras, números e simbolos encontrados
    def read(self):
        word = ''
        oper = ''
        # contador de linha e coluna
        with open(self.__file) as fp:
            #w = fp.read()
            intp = inter()

            w = fp.readline()
            cnt = 0
            code = []
            line = []
            # lê codigo em linhas
            while w:
                line.append(w.strip())
                w = fp.readline()
                
                code.append(line)
                cnt += 1
                line = []
            # divide palavras nas linhas transforma
            # em objeto de array, fazendo um array bi-dimencional
            code_split = []
            for c in code:
                code_split.append(c[0].split(' '))
            # itera no array de linhas
            for c in code_split:
                # itera nas linhas
                for d in c:
                    # itera nas palavras
                    for i, e in enumerate(list(d)):
                        word += e
                        #verifica com tabela de simbolos e concatena valores encontrados
                        keyword = intp.get_keyword(word)
                        operator = intp.get_operator(e)
                        if(keyword):
                            print(colors.HEADER + word)
                            self.__code.append(word)
                        elif(operator):
                            print(colors.WARNING + e)
                            if(e == ':'):
                                word = word[:-1]
                                self.__code.append(e)
                            if(e == ';'):
                                word = word[:-1]
                                self.__code.append(e)
                            if(e == '.'):
                                word = word[:-1]
                                self.__code.append(e)
                            if(e == ','):
                                word = word[:-1]
                                self.__code.append(e)
                            if(e == '('):
                                word = word[:-1]
                                self.__code.append(e)
                            if(e == ')'):
                                word = word[:-1]
                                self.__code.append(e)
                            if(e == '='):
                                word = word[:-1]
                                self.__code.append(e)
                            if(e == '<'):
                                word = word[:-1]
                                self.__code.append(e)
                            if(e == '>'):
                                word = word[:-1]
                                self.__code.append(e)
                            if(e == '/'):
                                word = word[:-1]
                                self.__code.append(e)
                            if(e == '*'):
                                word = word[:-1]
                                self.__code.append(e)
                            if(e == '-'):
                                word = word[:-1]
                                self.__code.append(e)
                            if(e == '+'):
                                word = word[:-1]
                                self.__code.append(e)
                        elif(word == ' ' and keyword != True and operator != True):
                            intp.set_id(word)
                            self.__code.append(e)
                    word = ''
        self.__code = [x for x in self.__code if x not in ['\n', '\t', '', ' ']]
        intp.get_id_csv
    # Retorna o array do código
    def get_code(self):
        return self.__code
