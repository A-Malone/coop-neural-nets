import itertools
from .environment import MultiPlayerGame

class MultiPlayerTournament(Named):
    """ the tournament class is a specific kind of experiment, that takes a pool of agents
    and has them compete in a multiplayer game. """

    # do all moves need to be checked for legality?
    forcedLegality = False

    def __init__(self, env):
        assert isinstance(env, TeamBattleEnvironment)
        self.env = env
        self.players = env.players
        for a in self.players:
            a.game = self.env
        self.reset()

    def reset(self):
        # a dictionnary attaching a list of outcomes to a player-couple-key
        self.results = {}
        self.rounds = 0
        self.numGames = 0

    def _generateMatchups(self):
        """ produce a list of all possible matchups"""

        team_sizes = self.env.team_sizes
        teams = list(team_sizes)

        curr_teams = {}

        for perm in itertools.permutations(self.players):
            index = 0
            for team in teams:
                curr_teams[team] = perm[index:index+team_sizes[team]]
                index+=team_sizes[team]
            yield curr_teams

    def _oneGame(self, teams):
        """ play one game between two agents p1 and p2."""
        self.numGames += 1
        self.env.reset()

        players = reduce(lambda x,y : teams[x]+teams[y], teams)
        for player in players:
            player.newEpisode()

        self.env.playGame
       
        self.results[players].append(winner)

    def organize(self, repeat=1):
        """ have all agents play all others in all orders, and repeat. """
        for dummy in range(repeat):
            self.rounds += 1
            for teams in self._generateMatchups():
                for team, players in teams.items():
                    for player in players:
                        player.set_team(team)
                self._oneGame(teams)

        return self.results

    def eloScore(self, startingscore=1500, k=32):
        """ compute the elo score of all the agents, given the games played in the tournament.
        Also checking for potentially initial scores among the agents ('elo' variable). """
        # initialize
        elos = {}
        for a in self.players:
            if 'elo' in a.__dict__:
                elos[a] = a.elo
            else:
                elos[a] = startingscore
        # adjust ratings
        for i, a1 in enumerate(self.players[:-1]):
            for a2 in self.players[i + 1:]:
                # compute score (in favor of a1)
                s = 0
                outcomes = self.results[(a1, a2)] + self.results[(a2, a1)]
                for r in outcomes:
                    if r == a1:
                        s += 1.
                    elif r == self.env.DRAW:
                        s += 0.5
                # what score would have been estimated?
                est = len(outcomes) / (1. + 10 ** ((elos[a2] - elos[a1]) / 400.))
                delta = k * (s - est)
                elos[a1] += delta
                elos[a2] -= delta
        for a, e in list(elos.items()):
            a.elo = e
        return elos
