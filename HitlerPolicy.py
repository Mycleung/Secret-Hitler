class Policy(object):
    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return self.type.title()


class Liberal(Policy):
    def __init__(self):
        super(Liberal, self).__init__("liberal")


class Fascist(Policy):
    def __init__(self):
        super(Fascist, self).__init__("fascist")