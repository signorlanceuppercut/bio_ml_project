
class Map:

    def __init__(self, key_list):
        self.concept_dict={key_list}

    def get_concept_dict(self):
        return self.concept_dict

    def set_concept_dict(self, concept_dict):
        self.concept_dict = concept_dict
