import pandas as pd
from composed_feature import ComposedFeature
from feature import Feature
import random

class DiscriminantOther:
    @staticmethod
    def process_file(feature_name_file,feature_condition_file):
        dict={}
        discriminant_features=[]
        other_features=[]
        col_names = []

        df1 = pd.read_excel(feature_name_file)
        df2 = pd.read_excel(feature_condition_file)
        for index, row in df1.iterrows():
            discriminant_features = []
            other_features = []
            col_names = []
            col_names.append('age')
            col_names.append('gender')

            for col, val in row.items():

                col_names.append(col)

                if val == 1:
                    for index2, row2 in df2.iterrows():
                        if index2==0:
                            for col2,val2 in row2.items():
                                if col2==col:
                                    max_random = val2
                        else:
                            for col2,val2 in row2.items():
                                if col2==col:
                                    is_for_woman = val2
                    discriminant_features.append(Feature(col,-1,max_random, is_for_woman))
                else:
                    for index2, row2 in df2.iterrows():
                        if index2 == 0:
                            for col2, val2 in row2.items():
                                if col2 == col:
                                    max_random = val2
                        else:
                            for col2, val2 in row2.items():
                                if col2 == col:
                                    is_for_woman = val2
                    other_features.append(Feature(col,-1,max_random, is_for_woman))

            dict[df1.iat[index,0]]=ComposedFeature(discriminant_features,other_features[1:])
        col_names.remove('Unnamed: 0')
        return dict, col_names


