from discriminant_other import DiscriminantOther
from generator import Generator
from global_settings import GlobalSettings
from map import Map
import pandas as pd


class DatasetCreation:
    @staticmethod
    def create_dataset():
        result, col_names = DiscriminantOther.process_file('resources//conf//Tabella_Booleana_valori_significativi.xlsx','resources//conf//features_max_value.xlsx')
        #print(result)
        #print(col_names)

        global_settings_train = GlobalSettings.read_glob_parameter('resources//conf//globalSettings - Train.xlsx')
        global_settings_test = GlobalSettings.read_glob_parameter('resources//conf//globalSettings - Test.xlsx')
        #print(global_settings)

        final_df_train=Generator.generate_final_df(global_settings_train, result,col_names)
        final_df_test=Generator.generate_final_df(global_settings_test, result,col_names)

        final_df_train_noDMA = final_df_train.filter(regex='^(?!.*Point)', axis=1)
        final_df_test_noDMA = final_df_test.filter(regex='^(?!.*Point)', axis=1)

        final_df_train.to_excel('resources//dataset//our_data_set_train.xlsx')
        final_df_test.to_excel('resources//dataset//our_data_set_test.xlsx')

        final_df_train_noDMA.to_excel('resources//dataset//our_data_set_train_NODMA.xlsx', index=False)
        final_df_test_noDMA.to_excel('resources//dataset//our_data_set_test_NODMA.xlsx', index=False)

    @staticmethod
    def create_fuzzy_dataset():
        df_n = pd.read_excel('resources//fuzzy_rules//nodes.xlsx')
        df_n = df_n.iloc[:, :-1]
        key_list = []
        for key in df_n.iloc[:, 2]:
            if (key in key_list) is False:
                key_list.append(key)
        my_map = Map(key_list)
        my_map.populate_map(df_n, pd.read_excel('resources//fuzzy_rules//archs.xlsx'),
                            pd.read_excel('resources//fuzzy_rules//fuzzy_conf.xlsx'))

        data = pd.read_excel("resources//dataset//our_data_set_train_NODMA.xlsx")
        df_fuzzy = DatasetCreation.fuzzy_dataframe(data, my_map)
        data.reset_index(inplace=True)
        df_fuzzy.reset_index(inplace=True)
        df_fuzzy_merged = pd.merge(df_fuzzy, data[['index', 'class label']], on='index', how='left')
        df_fuzzy_merged = df_fuzzy_merged.drop('index', axis=1)
        df_fuzzy_merged.to_excel('resources//dataset//our_fuzzy_data_set_train_NODMA.xlsx', index=False)

        data = pd.read_excel("resources//dataset//our_data_set_test_NODMA.xlsx")
        df_fuzzy = DatasetCreation.fuzzy_dataframe(data, my_map)
        data.reset_index(inplace=True)
        df_fuzzy.reset_index(inplace=True)
        df_fuzzy_merged = pd.merge(df_fuzzy, data[['index', 'class label']], on='index', how='left')
        df_fuzzy_merged = df_fuzzy_merged.drop('index', axis=1)
        df_fuzzy_merged.to_excel('resources//dataset//our_fuzzy_data_set_test_NODMA.xlsx', index=False)

    @staticmethod
    def fuzzy_dataframe(data, map):
        initialization_df = 0
        for i in range(0,data.shape[0]):
            map.compute_map_values(data.iloc[i,:])
            #map.print_map()
            col_names = []
            row_feature_dict = {}
            for concept in map.get_concept_dict()[max(map.get_concept_dict().keys())]:
                if initialization_df == 0:
                    col_names.append(concept.get_name())
                row_feature_dict[concept.get_name()] = concept.get_value()
            if initialization_df == 0:
                df_fuzzy = pd.DataFrame(columns=col_names)
            initialization_df = -1
            df_fuzzy.loc[len(df_fuzzy)] = row_feature_dict
        return df_fuzzy
