from HitlerBoard import HitlerBoard, HitlerState
from HitlerPlayer import DumbPlayer
from random import randint


class HitlerGame(object):
    def __init__(self, playernum=0):
        """Stuff"""
        self.playernum = playernum
        self.hitler = None
        self.board = None
        self.state = HitlerState()

    def play(self):
        """Main game loop"""
        self.assign_players()
        self.inform_fascists()
        self.choose_first_president()

        loop_game = True

        while loop_game:
            loop_game = not self.turn()

        #print("Game's over!")
        return self.finish_game()

    def turn(self):
        """
        Take a turn.
        """
        # First, pass on the presidency
        self.set_next_president()

        # Ask the president to nominate a chancellor
        self.state.chancellor = self.nominate_chancellor()

        # Ask the players to vote whether they want this pairing
        voted = self.voting()

        if not voted:
            #print("Vote failed!")
            action_enacted = self.vote_failed()
        else:
            # Possibility to win if Hitler is chancellor and more than 2 fascist policies enacted.
            if self.hitler_chancellor_win():
                return True

            action_enacted = self.vote_passed()

        if action_enacted:
            self.perform_vote_action()

        if self.policy_win():
            return True

        if self.hitler.is_dead:
            return True

        return False

    def assign_players(self):
        if self.playernum == 0:
            self.playernum = int(raw_input("How many players?\n"))

        self.board = HitlerBoard(self.state, self.playernum)
        roles = self.board.shuffle_roles()

        for num in range(self.playernum):
            # name = raw_input("Player #%d's name?\n" % num)
            name = "Bot %d" % num
            player = DumbPlayer(num,
                                name,
                                roles.pop(0),
                                self.state)

            if player.is_hitler:
                # Keep track of Hitler
                self.hitler = player

            self.state.players.append(player)

    def inform_fascists(self):
        """
        Inform the fascists who the other fascists are.
        If there are 5 players, Hitler knows who the other fascist is.
        """
        fascists = [player for player in self.state.players if player.is_fascist]

        for fascist in fascists:
            # Every fascist knows who Hitler is
            fascist.hitler = self.hitler
            if self.playernum in [5, 6]:
                # Hitler knows about the other fascist
                fascist.fascists = fascists
            elif not fascist.is_hitler:
                # Hitler doesn't know about the other fascists
                fascist.fascists = fascists

    def choose_first_president(self):
        """
        Choose a random player to be the 'zeroth' president, the first president will
        be the next person after them.
        """
        self.state.president = self.state.players[randint(0, len(self.state.players) - 1)]

    def set_next_president(self):
        self.state.president = self.state.players[(self.state.president.id + 1) % len(self.state.players)]
        if self.state.president.is_dead:
            self.set_next_president()

    def nominate_chancellor(self):
        chancellor = self.state.chancellor
        while (chancellor == self.state.chancellor or
               chancellor == self.state.president or
               (self.playernum in [5, 6] and
                chancellor == self.state.ex_president) or
               chancellor.is_dead):
            chancellor = self.state.president.nominate_chancellor()

        return chancellor

    def voting(self):
        """
        Get votes for the current pairing from all players.
        :returns: Whether the vote succeeded
        """
        self.state.last_votes = []
        for player in self.state.players:
            if not player.is_dead:
                self.state.last_votes.append(player.vote())

        positivity = 0

        for vote in self.state.last_votes:
            if vote:
                positivity += 1
            else:
                positivity -= 1

        return positivity > 0

    def vote_failed(self):
        #print("Vote failed!")
        self.state.failed_votes += 1

        if self.state.failed_votes == 3:
            self.state.failed_votes = 0

            #print("Too many failed votes! Citizens are taking action into their own hands")
            return self.board.enact_policy(self.board.draw_policy(1)[0])

        else:
            # Not enacting a vote, take another turn
            return False

    def vote_passed(self):
        """
        The vote has passed! Get the president and chancellor to do their thang.
        """
        #print("Vote passed!")

        (take, discard) = self.state.president.filter_policies(self.board.draw_policy(3))
        self.board.discards.append(discard)

        if (self.state.veto and
                self.state.chancellor.chancellor_veto(take) and
                self.state.president.president_veto()):
            #print("Vote vetoed!")
            return self.vote_failed()

        (enact, discard) = self.state.chancellor.enact_policy(take)
        self.board.discards.append(discard)
        return self.board.enact_policy(enact)

    def hitler_chancellor_win(self):
        return (self.state.fascist_track >= 3 and
                self.state.chancellor == self.hitler)

    def policy_win(self):
        return self.state.liberal_track == 5 or self.state.fascist_track == 6

    def perform_vote_action(self):
        action = self.board.fascist_track_actions[self.state.fascist_track - 1]
        if action is None:
            #print("No action")
            return

        #print("Performing vote action: %s" % action)

        if action == "policy":
            top_three = self.board.draw_policy(3)
            self.state.president.view_policies(top_three)
            self.board.return_policy(top_three)

        elif action == "kill":
            killed_player = self.state.president.kill()
            while killed_player.is_dead or killed_player == self.state.president:
                killed_player = self.state.president.kill()
            killed_player.is_dead = True

        elif action == "inspect":
            inspect = self.state.president.inspect_player()
            while inspect.is_dead or inspect == self.state.president:
                self.state.president.inspected_players[inspect] = inspect.role.party_membership

        elif action == "choose":
            chosen = self.state.president
            while chosen == self.state.president or chosen.is_dead:
                chosen = self.state.president.choose_next()

            self.state.president = chosen

        else:
            assert False, "Unrecognised action!"

    def finish_game(self):
        if self.hitler_chancellor_win():
            #print("Fascists win by electing Hitler!")
            return -2

        elif self.policy_win():
            if self.state.liberal_track == 5:
                #print("Liberals win by policy!")
                return 1
            else:
                #print("Fascists win by policy!")
                return -1

        elif self.hitler.is_dead:
            #print("Liberals win by shooting Hitler!")
            return 2


def newgame():
    game = HitlerGame(10)
    return game.play()


if __name__ == "__main__":
    games = {"Liberal_policy": 0, "Liberal_kill_Hitler": 0, "Fascist_policy": 0, "Fascist_elect_Hitler": 0}
    for ii in range(100000):
        r = newgame()
        if r == -2:
            games["Fascist_elect_Hitler"] += 1
        elif r == -1:
            games["Fascist_policy"] += 1
        elif r == 1:
            games["Liberal_policy"] += 1
        elif r == 2:
            games["Liberal_kill_Hitler"] += 1

    print(games)
    print(str(games["Liberal_policy"] + games["Liberal_kill_Hitler"]) + ":" +
          str(games["Fascist_policy"] + games["Fascist_elect_Hitler"]))
