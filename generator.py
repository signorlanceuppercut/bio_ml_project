import numpy as np
import random
import pandas as pd
from feature import Feature

class Generator:

    @staticmethod
    def generate_final_df(global_parameters, structure_features_dict, col_names):

        df = pd.DataFrame(columns=col_names)
        row_feature_dict = {key : -100 for key in col_names}
        weekly_flag = 0
        for key in global_parameters:
            for i in range(0, global_parameters[key].get_num_items()):
                row_feature_list = []
                row_feature_list.append(Feature('age', Generator.rand_age(key), 80, 0))
                gender = Feature('gender', random.randint(0, 1), 1, 0)
                row_feature_list.append(gender)

                not_seen = []
                for feature in structure_features_dict[key].get_discriminant():
                    if 'weekly' not in feature.get_name().lower():
                        if random.randint(0, 100) < global_parameters[key].get_positive():
                            if feature.get_is_for_women() == 1 and gender == 1:
                                feature.set_value(-1)
                            else:
                                if 'Point' in feature.get_name():
                                    feature.set_value(random.randint(100,feature.get_max_random()))
                                else:
                                    feature.set_value(1)
                                # corresponding_feature = next(f for f in structure_features_dict[key].get_discriminant() if 'Weekly ' + feature.get_name() in f.get_name())
                                for f in structure_features_dict[key].get_discriminant():
                                    weekly_flag = 0
                                    if feature.get_name().lower() in f.get_name().lower() and 'weekly' in f.get_name().lower():
                                        corresponding_feature = f
                                        weekly_flag = 1
                                        corresponding_feature.set_value(random.randint(1, corresponding_feature.get_max_random()))
                                        break
                        else:
                            if 'Point' in feature.get_name():
                                feature.set_value(random.randint(100, 350))
                            else:
                                feature.set_value(0)
                        row_feature_list.append(feature)
                        if weekly_flag == 1:
                            row_feature_list.append(corresponding_feature)
                    else:
                        not_seen.append(feature)
                    for obj in not_seen:
                        if obj not in row_feature_list:
                            obj.set_value(0)
                            row_feature_list.append(obj)
                not_seen = []
                for feature in structure_features_dict[key].get_other():
                    if 'weekly' not in feature.get_name().lower():
                        #if key != 'Negative':
                        prob = (100 - global_parameters[key].get_positive()) / 2
                        #else:
                            #prob = (100 - global_parameters[key].get_positive()) / 9
                        if random.randint(0, 100) < prob:
                            if feature.get_is_for_women() == 1 and gender == 1:
                                feature.set_value(-1)
                            else:
                                if 'Point' in feature.get_name():
                                    feature.set_value(random.randint(100, 350))
                                else:
                                    feature.set_value(1)
                                # corresponding_feature = next(f for f in structure_features_dict[key].get_discriminant() if 'Weekly ' + feature.get_name() in f.get_name())
                                for f in structure_features_dict[key].get_other():
                                    weekly_flag = 0
                                    if feature.get_name().lower() in f.get_name().lower() and 'weekly' in f.get_name().lower():
                                        corresponding_feature = f
                                        weekly_flag = 1
                                        corresponding_feature.set_value(random.randint(1,corresponding_feature.get_max_random()))
                                        break
                        else:
                            if 'Point' in feature.get_name():
                                feature.set_value(random.randint(100, 350))
                            else:
                                feature.set_value(0)

                        row_feature_list.append(feature)
                        if weekly_flag == 1:
                            row_feature_list.append(corresponding_feature)
                    else:
                        not_seen.append(feature)
                    for obj in not_seen:
                        if obj not in row_feature_list:
                            obj.set_value(0)
                            row_feature_list.append(obj)

                    if key == 'Gastro-intestinal':
                        encoded_key=0
                    elif key == 'Cardio':
                        encoded_key=1
                    else:
                        encoded_key = 2

                    row_feature_list.append(Feature('class label', encoded_key, -1,-1))
                for obj in row_feature_list:
                    row_feature_dict[obj.get_name()] = obj.get_value()
                #df = df.append(row_feature_dict, ignore_index=True)
                df.loc[len(df)] = row_feature_dict

        return df

    @staticmethod
    def rand_age(key):
        prob_i1=0.50
        prob_i2=0.50

        # definisci l'intervallo di numeri possibili
        lower_bound = 18
        upper_bound = 80


        if key=='Cardio':
            prob_i1 = 0.15
            prob_i2 = 0.85
        if key=='Thyroid':
            prob_i1 = 0.35
            prob_i2 = 0.65

        # definisci la probabilità desiderata
        prob = [prob_i1] * (40 - lower_bound) + [prob_i2] * (upper_bound - 40 + 1)

        # genera un numero casuale con la probabilità desiderata
        rand_num = random.choices(range(lower_bound, upper_bound+1), weights=prob)[0]

        return rand_num
