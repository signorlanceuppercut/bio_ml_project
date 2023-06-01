import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, balanced_accuracy_score
from feature_reduction import FeatureReduction
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import mean_squared_error

class DecisionTree:

    @staticmethod
    def use_decision_tree(train_file, test_file, use_feature_reduction):
        data = pd.read_excel(train_file)
        data2 = pd.read_excel(test_file)

        #del data['Unnamed: 0']
        #del data2['Unnamed: 0']

        idx = np.random.permutation(len(data))
        data = data.iloc[idx]

        idx = np.random.permutation(len(data2))
        data2 = data2.iloc[idx]

        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]
        X_test_definitivo = data2.iloc[:, :-1]
        y_test_definitivo = data2.iloc[:, -1]

        if (use_feature_reduction == 1):
            X, X_test_definitivo = FeatureReduction.implement_feature_reduction(X, X_test_definitivo, y)

        # Standardizzazione dei dati
        sc = StandardScaler()
        X_train = sc.fit_transform(X)
        X_test = sc.transform(X_test_definitivo)

        # Definizione del modello Decision Tree
        tree = DecisionTreeClassifier()

        # Definizione della griglia dei parametri da testare con la cross-validation
        param_grid = {
            'criterion': ['gini', 'entropy'],
            'max_depth': [None, 5, 10, 15, 20],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }

        # Ricerca dei parametri ottimali con la cross-validation
        grid_search = GridSearchCV(tree, param_grid, cv=5)
        grid_search.fit(X_train, y)

        # Calcolo della precisione sul set di test
        y_pred = grid_search.predict(X_test)

        return classification_report(y_test_definitivo, y_pred), confusion_matrix(y_test_definitivo, y_pred),  accuracy_score(y_test_definitivo, y_pred), balanced_accuracy_score(y_test_definitivo, y_pred), f1_score(y_test_definitivo, y_pred, average='weighted'), cohen_kappa_score(y_test_definitivo, y_pred), mean_squared_error(y_test_definitivo, y_pred, squared=False)
