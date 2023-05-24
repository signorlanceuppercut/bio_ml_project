class Edge:

    def __init__(self, parent_node, child_node, value, id):
        self.parent_node = parent_node
        self.child_node = child_node
        self.value = value
        self.id = id

    def get_parent(self):
        return self.parent_node

    def set_parent(self, parent_node):
        self.parent_node = parent_node

    def get_child(self):
        return self.child_node

    def set_child(self, child_node):
        self.child_node = child_node

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id
