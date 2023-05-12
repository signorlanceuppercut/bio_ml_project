import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, balanced_accuracy_score
from feature_reduction import FeatureReduction

class SVM:
    @staticmethod
    def use_SVM(train_file, test_file, use_feature_reduction):
        # Caricamento dei dati da file Excel
        data = pd.read_excel(train_file)
        data2 = pd.read_excel(test_file)

        #del data['Unnamed: 0']
        #del data2['Unnamed: 0']

        idx = np.random.permutation(len(data))
        data = data.iloc[idx]

        idx = np.random.permutation(len(data2))
        data2 = data2.iloc[idx]

        # Divisione in set di training e di test
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

        # Definizione del modello SVM
        svm = SVC()

        # Definizione della griglia dei parametri da testare con la cross-validation
        param_grid = {
            'C': [0.1, 1, 10],
            'kernel': ['linear', 'rbf', 'sigmoid'],
            'gamma': ['scale', 'auto']
        }

        # Ricerca dei parametri ottimali con la cross-validation
        grid_search = GridSearchCV(svm, param_grid, cv=5)
        grid_search.fit(X_train, y)

        # Calcolo della precisione sul set di test
        y_pred = grid_search.predict(X_test)
        accuracy = accuracy_score(y_test_definitivo, y_pred)

        return classification_report(y_test_definitivo, y_pred), confusion_matrix(y_test_definitivo,y_pred), accuracy_score(y_test_definitivo, y_pred), balanced_accuracy_score(y_test_definitivo, y_pred), f1_score(y_test_definitivo,y_pred,average='weighted')
