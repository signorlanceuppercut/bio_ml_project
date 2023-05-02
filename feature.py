class Feature:
    def __init__(self, name, value, max_random, is_for_women):
        self._name = name
        self._value = value
        self._max_random = max_random
        self._is_for_women = is_for_women

    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name

    def get_value(self):
        return self._value
    def set_value(self, value):
        self._value = value

    def get_max_random(self):
        return self._max_random
    def set_max_random(self, max_random):
        self._max_random = max_random

    def get_is_for_women(self):
        return self._is_for_women
    def set_is_for_women(self, is_for_women):
        self._is_for_women = is_for_women
