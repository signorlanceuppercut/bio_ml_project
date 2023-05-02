from discriminant_other import DiscriminantOther
from generator import Generator
from global_settings import GlobalSettings


class DatasetCreation:
    @staticmethod
    def create_dataset():
        result, col_names = DiscriminantOther.process_file('resources//conf//Tabella_Booleana_valori_significativi.xlsx','resources//conf//features_max_value.xlsx')
        #print(result)
        #print(col_names)

        global_settings_train = Global_settings.read_glob_parameter('resources//conf//globalSettings - Train.xlsx')
        global_settings_test = Global_settings.read_glob_parameter('resources//conf//globalSettings - Test.xlsx')
        #print(global_settings)

        final_df_train=Generator.generate_final_df(global_settings_train, result,col_names)
        final_df_test=Generator.generate_final_df(global_settings_test, result,col_names)

        final_df_train_noDMA = final_df_train.filter(regex='^(?!.*Point)', axis=1)
        final_df_test_noDMA = final_df_test.filter(regex='^(?!.*Point)', axis=1)

        final_df_train.to_excel('resources//dataset//our_data_set_train.xlsx')
        final_df_test.to_excel('resources//dataset//our_data_set_test.xlsx')

        final_df_train_noDMA.to_excel('resources//dataset//our_data_set_train_NODMA.xlsx')
        final_df_test_noDMA.to_excel('resources//dataset//our_data_set_test_NODMA.xlsx')