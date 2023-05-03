from data_set_creation import DatasetCreation
from KNN import KNN
from random_forest_classifier import RandomForest
from SVM import SVM
from decision_tree import DecisionTree
from map import Map
import pandas as pd

def main():
    scelta = None
    while scelta != 0:
        print_menu()
        scelta = int(input("Inserisci il numero dell'opzione desiderata: "))

        if scelta == 1:
            DatasetCreation.create_dataset()
            print('\n\n *************Dataset Creati Correttamente*************\n\n')
        elif scelta == 2:
            df_n = pd.read_excel('resources//fuzzy_rules//nodes.xlsx')
            df_n = df_n.iloc[:, :-1]
            key_list = []
            for key in df_n.iloc[:, 2]:
                if (key in key_list) is False:
                    key_list.append(key)
            my_map = Map(key_list)
            my_map.populate_map(df_n, pd.read_excel('resources//fuzzy_rules//archs.xlsx'), pd.read_excel('resources//fuzzy_rules//fuzzy_conf.xlsx'))
            my_map.print_map()
        elif scelta == 3:
            report, confusion_matrix, accuracy, balanced_accuracy, f1 = KNN.use_KNN("resources//dataset//our_data_set_train_NODMA.xlsx", "resources//dataset//our_data_set_test_NODMA.xlsx", ask_for_feature_reduction())
            print_results(report, confusion_matrix, accuracy, balanced_accuracy, f1)
        elif scelta == 4:
            report, confusion_matrix, accuracy, balanced_accuracy, f1 = SVM.use_SVM("resources//dataset//our_data_set_train_NODMA.xlsx", "resources//dataset//our_data_set_test_NODMA.xlsx",ask_for_feature_reduction())
            print_results(report, confusion_matrix, accuracy, balanced_accuracy, f1)
        elif scelta == 5:
            report, confusion_matrix, accuracy, balanced_accuracy, f1 = DecisionTree.use_decision_tree("resources//dataset//our_data_set_train_NODMA.xlsx", "resources//dataset//our_data_set_test_NODMA.xlsx",ask_for_feature_reduction())
            print_results(report, confusion_matrix, accuracy, balanced_accuracy, f1)
        elif scelta == 6:
            report, confusion_matrix, accuracy, balanced_accuracy, f1 = RandomForest.use_random_forest("resources//dataset//our_data_set_train_NODMA.xlsx", "resources//dataset//our_data_set_test_NODMA.xlsx",ask_for_feature_reduction())
            print_results(report, confusion_matrix, accuracy, balanced_accuracy, f1)
        elif scelta == 0:
            print("Programma terminato.")
        else:
            print("Scelta non valida. Riprova.")

def print_menu():
    print("Benvenuto nel menu di selezione.")
    print("1. Crea i dataset")
    print("2. Crea mappe fuzzy")
    print("2. Usa classificatore KNN")
    print("3. Usa classificatore SVM")
    print("4. Usa classificarore DT")
    print("5. Usa classificatore RF")
    print("0. Esci dal programma")

def print_results(report, confusion_matrix, accuracy, balanced_accuracy, f1):
    print('\n**************************************\n')
    print("\nClassification Report:\n", report)
    print("Confusion Matrix:\n", confusion_matrix)
    print("Accuracy Score:", accuracy)
    print("Balanced Accuracy Score:", balanced_accuracy)
    print("F1 Score:", f1)
    print('**************************************\n\n')

def ask_for_feature_reduction():
    scelta = input("Desideri usare una tecnica di feature reduction? [S,N]: ")
    scelta_int = 0
    if scelta.lower()=='s':
        scelta_int = 1
    return scelta_int

if __name__ == "__main__":
    main()