from random import getrandbits, choice

class HitlerPlayer(object):
    def __init__(self, id, name, role, state):
        self.id = id
        self.name = name
        self.role = role
        self.state = state
        self.hitler = None
        self.fascists = None
        self.is_dead = False
        self.inspected_players = {}

    @property
    def is_fascist(self):
        return self.role.party_membership == "fascist"

    @property
    def is_hitler(self):
        return self.role.role == "hitler"

    @property
    def knows_hitler(self):
        return self.hitler is not None

    def __repr__(self):
        return ("HitlerPlayer id:%d, name:%s, role:%s" %
                (self.id, self.name, self.role))

    def nominate_chancellor(self):
        """
        Choose who you want to be chancellor!
        :return: HitlerPlayer
        """
        raise NotImplementedError("Player must be able to choose a chancellor")

    def filter_policies(self, policies):
        """
        As president, choose 2 of three policies to play
        :return: Tuple of (List[choice1, choice2], discarded)
        """
        raise NotImplementedError("Player must be able to filter policies as president")

    def veto(self):
        """
        Decide whether to veto an action or not
        :return: Boolean
        """
        raise NotImplementedError("Player must be able to veto a policy")

    def enact_policy(self, policies):
        """
        Decide which of two policies to enact
        :param policies: policies
        :return: Tuple of (chosen, discarded)
        """
        raise NotImplementedError("Player must be able to enact a policy as chancellor")

    def vote(self):
        """
        Vote for the current president + chancellor combination
        :return: Vote
        """
        raise NotImplementedError("Player must be able to vote!")

    def view_policies(self, policies):
        """
        What to do if you perform the presidential action to view the top three policies
        :return:
        """
        raise NotImplementedError("Player must react to view policies action")

    def kill(self):
        """
        Choose a person to kill
        :return:
        """
        raise NotImplementedError("Player must choose someone to kill")

    def inspect_player(self):
        """
        Choose a person's party membership to inspect
        :return:
        """
        raise NotImplementedError("Player must choose someone to inspect")

    def choose_next(self):
        """
        Choose the next president
        :return:
        """
        raise NotImplementedError("Player must choose next president")


class DumbPlayer(HitlerPlayer):
    def __init__(self, id, name, role, state):
        super(DumbPlayer, self).__init__(id, name, role, state)

    def vote(self):
        """
        Just do it randomly :D
        :return: Random Ja or Nein
        """
        if bool(getrandbits(1)):
            #print("Player #%d voting Ja" % self.id)
            return Ja()
        else:
            #print("Player #%d voting Nein" % self.id)
            return Nein()

    def nominate_chancellor(self):
        """
        More random!
        :return: HitlerPlayer
        """
        assert len(self.state.players) > 0
        chancellor = self
        while chancellor == self:
            chancellor = choice(self.state.players)
        #print("Player #%d choosing chancellor: %s" % (self.id, chancellor.id))
        return chancellor

    def view_policies(self, policies):
        """
        What to do if you perform the presidential action to view the top three policies
        :return:
        """
        pass

    def kill(self):
        """
        Choose a person to kill
        :return:
        """
        kill = self
        while kill == self or kill.is_dead:
            kill = choice(self.state.players)
        #print("Player #%d killing: %s" % (self.id, kill.id))
        return kill

    def inspect_player(self):
        """
        Choose a person's party membership to inspect
        :return:
        """
        inspect = self
        while inspect == self or inspect.is_dead:
            inspect = choice(self.state.players)
        #print("Player #%d inspecting: %s" % (self.id, inspect.id))
        return inspect

    def choose_next(self):
        """
        Choose the next president
        :return:
        """
        choose = self
        while choose == self or choose.is_dead:
            choose = choice(self.state.players)
        #print("Player #%d choosing: %s" % (self.id, choose.id))
        return choose

    def enact_policy(self, policies):
        #print("Player #%d enacting: %s, discarding: %s" % (self.id, policies[0], policies[1]))
        return (policies[0], policies[1])

    def filter_policies(self, policies):
        #print("Player #%d allowing: (%s,%s), discarding: %s" % (self.id, policies[0], policies[1], policies[2]))
        return ([policies[0], policies[1]], policies[2])

    def veto(self):
        veto = bool(getrandbits(1))
        #print("Player #%d choosing to veto: %s" % (self.id, veto))
        return veto



class Vote(object):
    def __init__(self, type):
        self.type = type

    def __nonzero__(self):
        return self.type

    def __bool__(self):
        return self.type


class Ja(Vote):
    def __init__(self):
        super(Ja, self).__init__(True)


class Nein(Vote):
    def __init__(self):
        super(Nein, self).__init__(False)
