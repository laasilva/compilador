class interpreter:
    def __init__(self, kws, ops, ids, code):
        self.__kws = kws
        self.__ops = ops
        self.__ids = ids
        self.__code = code

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
