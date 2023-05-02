import pandas as pd

class GlobalSettings:

    # costruttore
    def __init__(self, num_items, positive_items):
        self._num = num_items
        self._positive = positive_items

    def get_positive(self):
        return self._positive

    def set_positive(self, positive_items):
        self._positive = positive_items

    def get_num_items(self):
        return self._num

    def set_num_items(self, num_items):
        self._num = num_items

    def read_glob_parameter(filename):
        dict ={}
        df=pd.read_excel(filename)

        for j in range(1,df.shape[1]):
            if df.columns[j] != 'no':
                dict[df.columns[j]] = GlobalSettings(df.iloc[0,j],df.iloc[1,j])
        print(dict)
        return dict