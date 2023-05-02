import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import LocallyLinearEmbedding as LLE


class FeatureReduction:

    @staticmethod
    def implement_feature_reduction(x_train, x_test, y_train):
        method, components = FeatureReduction.__choose_typology()
        if method == 1:
            if components is None:
                components = 'mle'
            pca = PCA(n_components=components)
            x_train_reduced = pca.fit_transform(x_train)
            x_test_reduced = pca.transform(x_test)

        elif method == 2:
            if components is None:
                components = 0.2
            vt = VarianceThreshold(threshold=components)
            x_train_reduced = vt.fit_transform(x_train)
            x_test_reduced = vt.transform(x_test)

        elif method == 3:
            if components is None:
                components = 'all'
            skb = SelectKBest(f_classif, k=components)
            skb.fit(x_train,y_train)
            x_train_reduced = skb.transform(x_train)
            x_test_reduced = skb.transform(x_test)

        elif method == 4:
            if components is None:
                components = x_train.shape[1] // 2
            lle = LLE(n_components=components)
            x_train_reduced = lle.fit_transform(x_train)
            x_test_reduced = lle.transform(x_test)

        elif method == 5:
            if components is None:
                components = min(x_train.shape[1] - 1, len(np.unique(y_train)) - 1)
            lda = LDA(n_components=components)
            lda.fit(x_train, y_train)
            x_train_reduced = lda.transform(x_train)
            x_test_reduced = lda.transform(x_test)

        else:
            raise ValueError(f"Invalid method: {method}")

        return x_train_reduced, x_test_reduced

    @staticmethod
    def __choose_typology():
        scelta_tecnica = None
        while scelta_tecnica not in [1,2,3,4,5]:
            print("Scegli la tipologia di tecnica da utilizzare.")
            print("1. PCA")
            print("2. VarianceThreshold")
            print("3. Select Kbest")
            print("4. LLE")
            print("5. LDA")
            scelta_tecnica = int(input("Scegli la tecnica: "))
        use_custom_components = input("Vuoi specificare il parametro numero di componeti/soglia? (S/N) ").lower() == 's'

        if use_custom_components:
            if scelta_tecnica == 2:
                components = float(input("Inserisci il valore di soglia: "))
            else:
                components = int(input("Inserisci il numero di componenti: "))
        else:
            components = None

        return scelta_tecnica, components
