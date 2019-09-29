import pandas as pd
# Classes
from reader import reader
from interpreter import interpreter
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

class main:

    code = []
    file = 'code.txt'

    it = reader(file, code)

    it.read()

    code = it.get_code()

    print(code)

    # montar array bidimencional para armazenar o lexema encontrado
    # e seu token (keyword, operando ou id)
    # também identificar posição e se contém algum erro 

    #intrp = interpreter(kws, ops, ids, code)


    #keys = intrp.find_keywords()

    #print(keys)

    #operators = intrp.find_operators()

    #print(operators)

    # array de palavras em código montado
    # fazer análise com tokens e retirar palavras chave de usuário