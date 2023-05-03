from edge import Edge

class Concept:

    def __init__(self, id, name, edge_list, value):
        self.id = id
        self.name = name
        self.edge_list = edge_list
        self.value = value

    def get_id(self):
        return self.id

    def set_id(self,id):
        self.id = id
    def get_name(self):
        return self.name

    def set_name(self,name):
        self.name = name

    def get_edge_list(self):
        return self.edge_list

    def set_edge_list(self,edge):
        self.edge_list =edge

    def get_value(self):
        return self.value

    def set_value(self,value):
        self.value = value
