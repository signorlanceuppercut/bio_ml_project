import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np


class FeatureImportance:

    @staticmethod
    def compute_importance(path):
        data = pd.read_excel(path)

        X = data.drop('class label', axis=1)
        y = data['class label']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        rf = RandomForestClassifier(n_estimators=100, random_state=42)

        rf.fit(X_train, y_train)

        y_pred = rf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}')

        feature_importances = rf.feature_importances_

        importances_df = pd.DataFrame({'feature': X.columns, 'importance': feature_importances})

        importances_df = importances_df.sort_values(by='importance', ascending=False)

        print(importances_df)

        indices = np.argsort(feature_importances)[::-1]

        # Grafico dell'importanza delle feature
        plt.figure()
        plt.title("Importanza delle feature")
        plt.bar(range(X.shape[1]), feature_importances[indices])
        plt.xticks(range(X.shape[1]), X.columns[indices], rotation=90)
        plt.show()