import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import RandomizedSearchCV

# carica il set di dati di addestramento e di test utilizzando pandas
train_data = pd.read_excel("resources//dataset//our_data_set_train_NODMA.xlsx")
test_data = pd.read_excel("resources//dataset//our_data_set_test_NODMA.xlsx")

del train_data['Unnamed: 0']
del test_data['Unnamed: 0']

pca = PCA()
pca.fit(train_data)
variance = np.cumsum(pca.explained_variance_ratio_)
d= np.argmax(variance>=0.95)+1

# traccia il grafico della varianza spiegata cumulativa
plt.plot(variance)
plt.xlabel('Numero di componenti principali')
plt.ylabel('Varianza spiegata cumulativa')
plt.show()