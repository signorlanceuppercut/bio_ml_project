import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, balanced_accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from feature_reduction import FeatureReduction
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import mean_squared_error

class RandomForest:
    @staticmethod
    def use_random_forest(train_file, test_file, use_feature_reduction):
        # carica il set di dati di addestramento e di test utilizzando pandas
        train_data = pd.read_excel(train_file)
        test_data = pd.read_excel(test_file)

        #del train_data['Unnamed: 0']
        #del test_data['Unnamed: 0']

        idx = np.random.permutation(len(train_data))
        train_data = train_data.iloc[idx]

        idx = np.random.permutation(len(test_data))
        test_data = test_data.iloc[idx]

        # separa le feature dalle etichette di classe
        X_train = train_data.iloc[:, :-1]
        y_train = train_data.iloc[:, -1]
        X_test = test_data.iloc[:, :-1]
        y_test = test_data.iloc[:, -1]

        if (use_feature_reduction == 1):
            X_train, X_test = FeatureReduction.implement_feature_reduction(X_train, X_test, y_train)

        # definisci i parametri da testare
        param_grid = {
            'n_estimators': [50, 100, 200, 500],
            'max_depth': [5, 10, 15, 18],
            'min_samples_split': [2, 5, 10, 18],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2']
        }
        '''
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2],
            'max_features': ['sqrt', 'log2']
        }
        param_grid = {
            'n_estimators': [50, 100],
            'max_depth': [10, 15],
            'min_samples_split': [2, 3],
            'min_samples_leaf': [1],
            'max_features': ['sqrt']}'''

        # crea un modello Random Forest con i parametri predefiniti
        rfc = RandomForestClassifier()

        # esegui la ricerca casuale dei parametri
        rfc_random = RandomizedSearchCV(estimator=rfc, param_distributions=param_grid,
                                        n_iter=200, cv=3, verbose=2, random_state=100, n_jobs=-1)

        # addestra il modello con i parametri ottimizzati
        rfc_random.fit(X_train, y_train)

        # fai previsioni sul set di test
        y_pred = rfc_random.predict(X_test)

        return classification_report(y_test, y_pred), confusion_matrix(y_test,y_pred), accuracy_score(y_test, y_pred), balanced_accuracy_score(y_test, y_pred), f1_score(y_test,y_pred,average='weighted'), cohen_kappa_score(y_test, y_pred), mean_squared_error(y_test, y_pred, squared=False)
