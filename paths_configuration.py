class PathsConfiguration:

    def __init__(self, is_fuzzy):
        self.train_path = "resources//dataset//our_data_set_train_NODMA.xlsx"
        self.test_path = "resources//dataset//our_data_set_test_NODMA.xlsx"

        if is_fuzzy:
            self.train_path = "resources//dataset//our_fuzzy_data_set_train_NODMA.xlsx"
            self.test_path = "resources//dataset//our_fuzzy_data_set_test_NODMA.xlsx"

    def get_train_path(self):
        return self.train_path

    def get_test_path(self):
        return self.test_path
