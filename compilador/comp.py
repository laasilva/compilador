import pandas as pd
import read_file

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

class main:
    ts = pd.read_csv("tokens.csv", header=[0], sep=',')

    code = []
    file = '../code.txt'
    word = ''

    rf = read_file(file, ts, code)

    rf.read()

    # with open(file) as fp:
    #     w = fp.read()
    #     for c in w:
    #         word += c
    #         # fazer verificação, além de espaços, de tokens seguidos de operadores
    #         if(c == ' ' or c == '/n' or c == ':' or c == ';' or c == '.' or c == '(' or c == ')'):
    #             # antes de fazer o append, verificar de acordo com o array de tokens
    #             # verificar se é uma key, um operador ou um id
    #             for i, row in ts.iterrows():
    #                 if(word[:-1] == row['lexema']):
    #                     code.append(word[:-1])
    #             if(c == ':'):
    #                 code.append(':')
    #             if(c == ';'):
    #                 code.append(';')
    #             if(c == '.'):
    #                 code.append('.')
    #             if(c == '('):
    #                 code.append('(')
    #             if(c == ')'):
    #                 code.append(')')
    #             word = ''
    code = [x for x in code if x not in ['\n', '\t', '', ' ']]
    print(code)
        #line = fp.readline()
        #while line:
        #    print(line.split())
        #    code.append(line.split())
        #    line = fp.readline()

    for c in code:
        for i, row in ts.iterrows():
            if(c == row['lexema']):
                print('<', row['token'], ',', row['lexema'], '>')