import pandas as pd
# Classes
from reader import reader
from interpreter import interpreter
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

class main:

    ts = pd.read_csv("tokens.csv", header=[0], sep=',')

    code = []
    file = 'code.txt'

    it = reader(file, ts, code)

    it.read()

    code = it.get_code()

    print(code)

    # array de palavras em código montado
    # fazer análise com tokens e retirar palavras chave de usuário

    for c in code:
        for i, row in ts.iterrows():
            if(c == row['lexema']):
                print('<' + row['token'] + ', "' + row['lexema'] + '">')