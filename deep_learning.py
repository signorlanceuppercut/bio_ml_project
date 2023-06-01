import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, balanced_accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from feature_reduction import FeatureReduction
import random
import tensorflow as tf
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import mean_squared_error

class DeepLearning:
    @staticmethod
    def use_DL(train_file, test_file, use_feature_reduction):

        seed_value = 42
        random.seed(seed_value)
        np.random.seed(seed_value)
        tf.random.set_seed(seed_value)

        # Caricamento dei dati da file Excel
        data = pd.read_excel(train_file)
        data2 = pd.read_excel(test_file)

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

        # Definizione del modello di rete neurale
        model = Sequential()
        model.add(Dense(256, activation='tanh', input_shape=(X_train.shape[1],)))
        model.add(Dropout(0.2))
        model.add(Dense(128, activation='LeakyReLU'))
        model.add(Dropout(0.2))
        model.add(Dense(64, activation='LeakyReLU'))
        model.add(Dropout(0.2))
        model.add(Dense(32, activation='LeakyReLU'))
        model.add(Dense(16, activation='LeakyReLU'))  # Aggiunto un altro strato Dense
        model.add(Dense(8, activation='LeakyReLU'))  # Aggiunto un altro strato Dense
        model.add(Dense(3, activation='softmax'))

        # Compilazione del modello
        model.compile(optimizer=Adam(learning_rate=0.001),
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        # Definizione delle callback
        early_stopping = EarlyStopping(monitor='val_loss', patience=1000, restore_best_weights=True)

        # Addestramento del modello
        model.fit(X_train, y, validation_split=0.2, epochs=10000, batch_size=16, callbacks=[early_stopping])

        # Valutazione del modello
        y_pred = np.argmax(model.predict(X_test), axis=-1)
        accuracy = accuracy_score(y_test_definitivo, y_pred)

        return classification_report(y_test_definitivo, y_pred), confusion_matrix(y_test_definitivo,y_pred), accuracy_score(y_test_definitivo, y_pred), balanced_accuracy_score(y_test_definitivo, y_pred), f1_score(y_test_definitivo,y_pred,average='weighted'), cohen_kappa_score(y_test_definitivo, y_pred), mean_squared_error(y_test_definitivo, y_pred, squared=False)