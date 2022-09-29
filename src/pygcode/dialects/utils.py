
# Data Classes

class WordType(object):
    def __init__(self, value_class, value_regex, alternate_regex, description, clean_value):
        self.value_class = value_class
        self.value_regex = value_regex
        self.alternate_regex = alternate_regex
        self.description = description
        self.clean_value = clean_value
