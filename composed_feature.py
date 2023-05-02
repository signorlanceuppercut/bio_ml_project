class ComposedFeature:

    #costruttore
    def __init__(self, discriminant_features, other_features):
        self._discriminant = discriminant_features
        self._other = other_features

    def get_discriminant(self):
        return self._discriminant

    def set_name(self, discriminant_features):
        self._discriminant = discriminant_features

    def get_other(self):
        return self._other

    def set_name(self, other_features):
        self._other = other_features

