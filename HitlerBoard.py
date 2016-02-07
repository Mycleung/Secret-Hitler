from HitlerConstants import players, board
from random import shuffle
import HitlerPolicy
import HitlerRole


class HitlerBoard(object):
    def __init__(self, state, playercount):
        self.state = state
        self.num_players = playercount
        self.num_liberals = players[self.num_players]["liberal"]
        self.num_fascists = players[self.num_players]["fascist"]
        self.fascist_track_actions = players[self.num_players]["track"]

        self.policies = ([HitlerPolicy.Liberal()] * board["policy"]["liberal"] +
                         [HitlerPolicy.Fascist()] * board["policy"]["fascist"])
        shuffle(self.policies)
        self.discards = []
        self.previous = []

    def shuffle_roles(self):
        all_roles = ([HitlerRole.Liberal()] * self.num_liberals +
                     [HitlerRole.Fascist()] * self.num_fascists +
                     [HitlerRole.Hitler()])
        shuffle(all_roles)

        return all_roles

    def draw_policy(self, num):
        """
        Draw cards from the policy pile
        :param num: Number to draw
        :return: HitlerPolicy objects
        """
        if len(self.policies) >= num:
            drawn = self.policies[:num]
            self.policies = self.policies[num:]
            return drawn
        else:
            # Shuffle the discard and add them to the policies pile again
            #print("Draw pile is empty! Shuffling discards and putting into draw pile")
            shuffle(self.discards)
            #print("Discards: %s" % self.discards)
            self.policies = self.policies + self.discards
            self.discards = []
            #print ("New policy pile: %s" % self.policies)
            assert len(self.policies) > num
            return self.draw_policy(num)

    def discard(self, cards):
        """
        Discard the card we've been given, assert that they're Policy cards!
        :param cards: Policy or list of Policies
        """
        if not isinstance(cards, list):
            cards = [cards]

        for card in cards:
            assert isinstance(card, HitlerPolicy.Policy)
            self.discards.append(card)

    def return_policy(self, policies):
        """
        Return the card we've been given to the policy pile, assert that they're Policy cards!
        :param cards: Policy or list of Policies
        """
        if not isinstance(policies, list):
            policies = [policies]

        for policy in policies:
            assert isinstance(policy, HitlerPolicy.Policy)

        self.policies = policies + self.policies

    def enact_policy(self, policy):
        if policy.type == "liberal":
            self.state.liberal_track += 1
        else:
            self.state.fascist_track += 1
            if self.fascist_track_actions[self.state.fascist_track - 1] is not None:
                return True

        return False


class HitlerState(object):
    """Storage object for game state"""
    def __init__(self):
        self.liberal_track = 0
        self.fascist_track = 0
        self.failed_votes = 0
        self.president = None
        self.ex_president = None
        self.chosen_president = None
        self.chancellor = None
        self.most_recent_policy = None
        self.last_votes = []
        self.players = []
        self.veto = False

if __name__ == "__main__":
    h = HitlerBoard(5)
    #print(h.shuffle_roles())
    #print(h.policies)
    #print(h.state.fascist_track)

    #print("Drawing three cards")
    #print(h.draw_policy(3))
    #print(h.policies)