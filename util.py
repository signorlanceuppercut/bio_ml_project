import pandas as pd


class Util:

    @staticmethod
    def estract_fcm_features():
        train_path = "resources//dataset//our_fuzzy_data_set_train_NODMA.xlsx"
        test_path = "resources//dataset//our_fuzzy_data_set_test_NODMA.xlsx"

        train_data = pd.read_excel(train_path)
        test_data = pd.read_excel(test_path)

        X_train = train_data.iloc[:, :-1]
        y_train = train_data.iloc[:, -1]
        X_test = test_data.iloc[:, :-1]
        y_test = test_data.iloc[:, -1]

        return X_train, y_train, X_test, y_test