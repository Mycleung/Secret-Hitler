class Role(object):
    """
    Parent role. Inherited by three subclasses: Liberal, Fascist, Hitler.
    """
    def __init__(self):
        self.party_membership = ""
        self.role = ""

    def __repr__(self):
        return self.role.title()


class Liberal(Role):
    def __init__(self):
        super(Liberal, self).__init__()
        self.party_membership = "liberal"
        self.role = "liberal"


class Fascist(Role):
    def __init__(self):
        super(Fascist, self).__init__()
        self.party_membership = "fascist"
        self.role = "fascist"


class Hitler(Role):
    def __init__(self):
        super(Hitler, self).__init__()
        self.party_membership = "fascist"
        self.role = "hitler"
