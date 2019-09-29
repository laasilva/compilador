import pandas as pd

class interpreter:
    def __init__(self):
        self.__code = []

        self.__kws = pd.read_csv("ts_keywords.csv", header=[0], sep=',')
        self.__ops = pd.read_csv("ts_operators.csv", header=[0], sep=',')
        self.__ids = pd.read_csv("ts_ids.csv", header=[0], sep=',')

        self.__kwlist = []
        self.__oplist = []
    
    def find_keywords(self):
        for c in self.__code:
            for i, row in self.__kws.iterrows():
                if(c == row['lexema']):
                    self.__kwlist.append(c)
        return self.__kwlist

    def find_operators(self):
        for o in self.__code:
            for i, row in self.__ops.iterrows():
                if(o == row['lexema']):
                    self.__oplist.append(o)
        return self.__oplist

    def get_keyword(self, word):
        kw = False
        for i, row in self.__kws.iterrows():
                if(word == row['lexema']):
                    kw = True
                    break
                else:
                    kw = False
        return kw

    def get_operator(self, word):
        op = False
        for i, row in self.__ops.iterrows():
                if(word == row['lexema']):
                    op = True
                    break
                else:
                    op = False
        return op

    def set_id(self, word):
        data = {'token': 'ID', 'lexema': word}
        self.__ids.append(data, ignore_index=True)

    def get_id_csv(self):
        return self.__ids