from concept import Concept
from edge import Edge
import pandas as pd

class Map:
    concept_dict={}

    def __init__(self, key_list):
        for key in key_list:
            self.concept_dict[key]=None

    def get_concept_dict(self):
        return self.concept_dict

    def set_concept_dict(self, concept_dict):
        self.concept_dict = concept_dict

    def print_map(self):
        for key in list(self.concept_dict.keys()):
            print('*******Livello ' + str(key) + '*******')
            for concept in self.concept_dict[key]:
                print(str(concept.get_id()) + ' ' + concept.get_name())
                if concept.get_edge_list() != None:
                    for edge in concept.get_edge_list():
                        print (str(edge.get_parent()) + ' ' + str(edge.get_child()) + ' ' + str(edge.get_value()))
    def populate_map(self, df_of_concepts, df_of_edges, df_of_weights):
        #step 1: creazione concetti con edges a null e valori a -1
        for key in list(self.concept_dict.keys()):
            concept_list = []
            result_df = df_of_concepts[df_of_concepts['nodes_level'] == key]
            # print(result_df.head())
            i=0
            for concept_name in result_df.iloc[:, 1]:
                concept_list.append(Concept(result_df.iat[i, 0],concept_name, None, -1))
                i = i+1
            self.concept_dict[key] = concept_list

        #step 2: creazione di pesi degli archi
        weight_dict = {}
        i=0
        for weight_name in df_of_weights.iloc[:, 2]:
            weight_dict[weight_name] = df_of_weights.iat[i, 1]
            i = i+1

        #step 3: creazione degli archi
        df_of_edges = df_of_edges.groupby('arch_node_2').agg(lambda x: list(x))
        for idx, row in df_of_edges.iterrows():
            for key in list(self.concept_dict.keys()):
                for concept in self.concept_dict[key]:
                    if idx == concept.get_id():
                        #crea arco
                        list_of_edge = []
                        j=0
                        for child_concept in row['arch_node_1']:
                            list_of_edge.append(Edge(idx, child_concept,weight_dict[row['weight'][j]]))
                            j=j+1
                        concept.set_edge_list(list_of_edge)
                        concept.set_value(-1)
                        break

    def compute_map_values(self, source_values):
        return 1
