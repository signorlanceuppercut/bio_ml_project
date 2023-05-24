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
                print(str(concept.get_id()) + ' ' + concept.get_name() + ' ' + str(concept.get_value()) + ' ' + str(concept.get_level()))
                if concept.get_edge_list() != None:
                    for edge in concept.get_edge_list():
                        print (str(edge.get_id()) + ' ' + str(edge.get_parent()) + ' ' + str(edge.get_child()) + ' ' + str(edge.get_value()))

    def populate_map(self, df_of_concepts, df_of_edges, df_of_weights):
        #step 1: creazione concetti con edges a null e valori a -1
        for key in list(self.concept_dict.keys()):
            concept_list = []
            result_df = df_of_concepts[df_of_concepts['nodes_level'] == key]
            # print(result_df.head())
            i=0
            for concept_name in result_df.iloc[:, 1]:
                concept_list.append(Concept(result_df.iat[i, 0],concept_name, None, -1, result_df.iat[i, 2]))
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
                            list_of_edge.append(Edge(idx, child_concept,weight_dict[row['weight'][j]],row['id'][j]))
                            j=j+1
                        concept.set_edge_list(list_of_edge)
                        concept.set_value(-1)
                        break
        #self.print_map()

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
                concept.set_value(source_values[concept.get_name()]/85)
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
                if 'frequency' in concept.get_name():
                    adj_concept_name = concept.get_name().replace('_frequency','')
                    if 'Weekly Frequency - ' + adj_concept_name in source_values:
                        if adj_concept_name == 'smoke':
                            if source_values['Weekly Frequency - ' + adj_concept_name]/140 > 0.4:
                                concept.set_value(source_values['Weekly Frequency - ' + adj_concept_name]/140)
                            else:
                                concept.set_value(0)
                        elif adj_concept_name == 'coffee/tea':
                            if source_values['Weekly Frequency - ' + adj_concept_name] / 30 > 0.4:
                                concept.set_value(source_values['Weekly Frequency - ' + adj_concept_name] / 30)
                            else:
                                concept.set_value(0)
                        elif adj_concept_name == 'Alcohol intake':
                            if source_values['Weekly Frequency - ' + adj_concept_name] / 35 > 0.4:
                                concept.set_value(source_values['Weekly Frequency - ' + adj_concept_name] / 35)
                            else:
                                concept.set_value(0)
                        else:
                            if source_values['Weekly Frequency - ' + adj_concept_name] /7 > 0.4:
                                concept.set_value(source_values['Weekly Frequency - ' + adj_concept_name] /7)
                            else:
                                concept.set_value(0)
                else:
                    if source_values[concept.get_name().replace('_intensity','')]/5 >0.4:
                        concept.set_value(source_values[concept.get_name().replace('_intensity','')]/5)
                    else:
                        concept.set_value(0)
        alpha=0.4
        beta=0.3
        gamma=0.3

        #step 3: imposto i valori nei livelli successivi
        for key in list(self.concept_dict.keys())[1:]:
            for concept in self.concept_dict[key]:
                if concept.get_edge_list() is not None:
                    value = 0
                    edges_sum = 0
                    active_children = 0
                    #edge_list_len = len(concept.get_edge_list())
                    for edge_node in concept.get_edge_list():
                        edges_sum = edges_sum + abs(edge_node.get_value())
                        if self.__search_value_node(edge_node.get_child()) > 0:
                            active_children = active_children + 1
                    children_count = 0
                    zero_count = 0
                    for edge_node in concept.get_edge_list():
                        if self.__search_value_node(edge_node.get_child()) == 0:
                            zero_count = zero_count +1
                        value = value + self.__search_value_node(edge_node.get_child())*(edge_node.get_value()/edges_sum)
                        children_count = children_count + 1
                    #if zero_count/children_count > 1:
                       #concept.set_value(0)
                    #else:
                    concept.set_value(value)

        #step 4: applico correzione
        max = -1
        concept_name_max = ''
        for key in list(self.concept_dict.keys())[3:]:
            for concept in self.concept_dict[key]:
                if max < concept.get_value():
                    max = concept.get_value()
                    concept_name_max = concept.get_name()
            for concept in self.concept_dict[key]:

                if 'count' not in concept.get_name() and 'max' not in concept.get_name():
                    #if concept.get_name() == concept_name_max:
                    concept.set_value(alpha * concept.get_value() + beta * (self.__count_reachable_nodes(concept, 1) / self.__count_reachable_nodes(concept,0)) + gamma * self.__search_max(concept))

                    reacheble_not_zero = (self.__count_reachable_nodes(concept, 1) / self.__count_reachable_nodes(concept, 0))
                    node_count = self.__search_node_by_name(concept.get_name() + ' count')
                    node_count.set_value(reacheble_not_zero)
                    node_count = self.__search_node_by_name(concept.get_name() + ' max')
                    node_count.set_value(self.__search_max(concept))

    def __search_value_node(self, node_id):
        value = -1
        for key in list(self.concept_dict.keys()):
            for concept in self.concept_dict[key]:
                if concept.get_id() == node_id:
                    value = concept.get_value()
                    break
        return value

    def __search_node(self, node_id):

        for key in list(self.concept_dict.keys()):
            for concept in self.concept_dict[key]:
                if concept.get_id() == node_id:
                    my_node = concept
                    break
        return my_node

    def __search_node_by_name(self, name):

        for key in list(self.concept_dict.keys()):
            for concept in self.concept_dict[key]:
                if concept.get_name() == name:
                    my_node = concept
                    break
        return my_node

    def __count_reachable_nodes(self, start_node, is_value_cheked):
        visited_nodes = set()

        def visit_node(node):
            if is_value_cheked == 1:
                if node.get_value() != 0:
                    visited_nodes.add(node)
            else:
                visited_nodes.add(node)
            if node.get_edge_list() is not None:
                for edge in node.get_edge_list():
                    if edge.get_id() not in range(68,73):
                        visit_node(self.__search_node(edge.get_child()))

        visit_node(start_node)
        return len(visited_nodes)

    def __search_max(self, start_node):
        visited_nodes = set()

        def visit_node(node):
            if node.get_level() == 1:
                visited_nodes.add(node)

            if node.get_edge_list() is not None:
                for edge in node.get_edge_list():
                    if edge.get_id() not in range(68,73):
                        visit_node(self.__search_node(edge.get_child()))

        visit_node(start_node)
        max_value = -1
        for node in visited_nodes:
            if max_value < node.get_value():
                max_value = node.get_value()

        return max_value
