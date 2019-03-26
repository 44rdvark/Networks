class DeltaMod(object):
    def __init__(self, value, nodes):
        self.__value = value
        self.__nodes = nodes
        self.__positions = [None, None]

    def get_position(self, which):
        return self.__positions[which]

    def set_position(self, which, value):
        self.__positions[which] = value

    def get_nodes(self):
        return self.__nodes

    def set_nodes(self, nodes):
        self.__nodes = nodes

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    def __eq__(self, other):
        return self.__value == other.get_value()

    def __lt__(self, other):
        return self.__value < other.get_value()

    def __str__(self):
        return str(self.__nodes) + " " + str(self.__positions) + " " + str(self.__value)



