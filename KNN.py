import numpy as np
import pandas as pd
from sklearn.model_selection import  StratifiedKFold, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, balanced_accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from feature_reduction import FeatureReduction
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import mean_squared_error


class KNN:

    @staticmethod
    def use_KNN(train_file, test_file, use_feature_reduction):
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

        if(use_feature_reduction==1):
            X, X_test_definitivo= FeatureReduction.implement_feature_reduction(X,X_test_definitivo,y)

        # Crea un pipeline per normalizzare i dati e addestrare il modello KNN
        knn = make_pipeline(StandardScaler(), KNeighborsClassifier())

        # Definisci i parametri da cercare con la cross-validation
        parameters = {'kneighborsclassifier__n_neighbors': list(range(1, 30)),
                      'kneighborsclassifier__weights': ['uniform', 'distance']}

        # Crea un oggetto GridSearchCV per cercare i migliori parametri
        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
        grid_search = GridSearchCV(knn, parameters, cv=cv, scoring='accuracy')
        grid_search.fit(X, y)

        # Addestra il modello utilizzando i migliori parametri trovati
        best_k = grid_search.best_params_['kneighborsclassifier__n_neighbors']
        best_weights = grid_search.best_params_['kneighborsclassifier__weights']
        knn_best = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=best_k, weights=best_weights))
        knn_best.fit(X, y)

        # Valuta il modello sul set di test
        y_pred = knn_best.predict(X_test_definitivo)

        return classification_report(y_test_definitivo, y_pred), confusion_matrix(y_test_definitivo, y_pred),  accuracy_score(y_test_definitivo, y_pred), balanced_accuracy_score(y_test_definitivo, y_pred), f1_score(y_test_definitivo, y_pred, average='weighted'), cohen_kappa_score(y_test_definitivo, y_pred), mean_squared_error(y_test_definitivo, y_pred, squared=False)
