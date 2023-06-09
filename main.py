from data_set_creation import DatasetCreation
from KNN import KNN
from random_forest_classifier import RandomForest
from SVM import SVM
from decision_tree import DecisionTree
from paths_configuration import PathsConfiguration
from feature_importance import FeatureImportance
from deep_learning import DeepLearning
from bnc import BayesianNetworkClassifier

def main():
    scelta = None
    paths_configuration = PathsConfiguration(0)
    while scelta != 0:
        print_menu()
        scelta = int(input("Inserisci il numero dell'opzione desiderata: "))

        if scelta == 1:
            DatasetCreation.create_dataset()
            print('\n\n *************Dataset Creati Correttamente*************\n\n')
        elif scelta == 2:
            DatasetCreation.create_fuzzy_dataset()
            print('\n\n *************Dataset Fuzzy Creati Correttamente*************\n\n')
        elif scelta == 3:
            report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse = KNN.use_KNN(paths_configuration.get_train_path(), paths_configuration.get_test_path(), ask_for_feature_reduction())
            print_results(report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse)
        elif scelta == 4:
            report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse = SVM.use_SVM(paths_configuration.get_train_path(), paths_configuration.get_test_path(),ask_for_feature_reduction())
            print_results(report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse)
        elif scelta == 5:
            report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse = DecisionTree.use_decision_tree(paths_configuration.get_train_path(), paths_configuration.get_test_path(),ask_for_feature_reduction())
            print_results(report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse)
        elif scelta == 6:
            report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse = RandomForest.use_random_forest(paths_configuration.get_train_path(), paths_configuration.get_test_path(),ask_for_feature_reduction())
            print_results(report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse)
        elif scelta == 7:
            report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse = DeepLearning.use_DL(paths_configuration.get_train_path(), paths_configuration.get_test_path(),ask_for_feature_reduction())
            print_results(report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse)
        elif scelta == 8:
            report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse = BayesianNetworkClassifier.use_BayesianNetworkClassifier(paths_configuration.get_train_path(), paths_configuration.get_test_path(), ask_for_feature_reduction())
            print_results(report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse)
        elif scelta == 9:
            paths_configuration = PathsConfiguration(1)
        elif scelta == 10:
            paths_configuration = PathsConfiguration(0)
        elif scelta == 11:
            FeatureImportance.compute_importance(paths_configuration.get_train_path())
        elif scelta == 0:
            print("Programma terminato.")
        else:
            print("Scelta non valida. Riprova.")

def print_menu():
    print("Benvenuto nel menu di selezione.")
    print("1. Crea i dataset")
    print("2. Crea mappe fuzzy")
    print("3. Usa classificatore KNN")
    print("4. Usa classificatore SVM")
    print("5. Usa classificarore DT")
    print("6. Usa classificatore RF")
    print("7. Usa classificatore ANN")
    print("8. Usa classificatore BNC")
    print("9. Imposta i path di train e test per la fuzzy")
    print("10. Reset i path di train e test")
    print("11. Calcola importanza")
    print("0. Esci dal programma")

def print_results(report, confusion_matrix, accuracy, balanced_accuracy, f1, kappa, rmse):
    print('\n**************************************\n')
    print("\nClassification Report:\n", report)
    print("Confusion Matrix:\n", confusion_matrix)
    print("Accuracy Score:", accuracy)
    print("Balanced Accuracy Score:", balanced_accuracy)
    print("F1 Score:", f1)
    print("Kappa:", kappa)
    print("RMSE:", rmse)
    print('**************************************\n\n')

def ask_for_feature_reduction():
    scelta = input("Desideri usare una tecnica di feature reduction? [S,N]: ")
    scelta_int = 0
    if scelta.lower()=='s':
        scelta_int = 1
    return scelta_int

if __name__ == "__main__":
    main()