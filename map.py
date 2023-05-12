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
            print('******* Livello ' + str(key) + '*******')
            for concept in self.concept_dict[key]:
                print(str(concept.get_id()) + ' ' + concept.get_name() + ' ' + str(concept.get_value()))
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
        #print (source_values)
        #step 1:mi assicuro di che i valori di inizializzazione siano a -1
        for key in list(self.concept_dict.keys()):
            for concept in self.concept_dict[key]:
                concept.set_value(-1)

        #step 2: imposto i valori delle foglie
        for concept in self.concept_dict[0]:
            #for value in source_values:
            if concept.get_name() == 'age':
                concept.set_value(source_values[concept.get_name()]/100)
            elif concept.get_name() == 'gender_m':
                if source_values['gender'] == 0:
                    concept.set_value(1)
                else:
                    concept.set_value(0)
            elif concept.get_name() == 'gender_f':
                if source_values['gender'] == 0:
                    concept.set_value(0)
                else:
                    concept.set_value(1)
            else:
                if 'Weekly Frequency - ' + concept.get_name() in source_values:
                    if concept.get_name() == 'smoke':
                        concept.set_value(source_values['Weekly Frequency - ' + concept.get_name()]/140)
                    elif concept.get_name() == 'coffee/tea':
                        concept.set_value(source_values['Weekly Frequency - ' + concept.get_name()] / 30)
                    elif concept.get_name() == 'Alcohol intake':
                        concept.set_value(source_values['Weekly Frequency - ' + concept.get_name()] / 35)
                    else:
                        concept.set_value(source_values['Weekly Frequency - ' + concept.get_name()] /7)
                else:
                    concept.set_value(source_values[concept.get_name()])
        alpha=0.7
        beta=0.3
        #step 3: imposto i valori nei livelli successivi
        for key in list(self.concept_dict.keys())[1:]:
            for concept in self.concept_dict[key]:
                value = 0
                edges_sum = 0
                active_children = 0
                edge_list_len = len(concept.get_edge_list())
                for edge_node in concept.get_edge_list():
                    edges_sum = edges_sum + abs(edge_node.get_value())
                    if self.__search_value_node(edge_node.get_child()) > 0:
                        active_children = active_children + 1
                for edge_node in concept.get_edge_list():
                    value = value + alpha*self.__search_value_node(edge_node.get_child())*(edge_node.get_value()/edges_sum) + beta*(active_children)
                concept.set_value(value)


    def __search_value_node(self, node_id):
        value = -1
        for key in list(self.concept_dict.keys()):
            for concept in self.concept_dict[key]:
                if concept.get_id() == node_id:
                    value = concept.get_value()
                    break
        return value




