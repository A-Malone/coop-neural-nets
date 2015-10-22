import itertools
import numpy as np

from colearning.game.coopgame import CoopGame


class TeamTournament(object):
    """
    Takes a set of populations of neural nets and has them compete in a
    tournament to determine fitness
    """

    def __init__(self, game_format):
        self.results = np.zeros((game_format[0]*game_format[1], 2))
        self.format = game_format

        self.game = CoopGame(
            render=False,
            max_moves=1000
        )

    def setup(self, populations, players):
        self.rounds = 0
        self.numGames = 0
        self.results.fill(0)
        self.players = players
        self.populations = populations

    def _generateMatchups(self, min_matches=1):
        """
        Generate a list of matchups, ensures all players get at least min_match
        matches
        """
        shape = self.populations.shape

        teams = np.zeros((shape[0], self.format[1]))
        for t_index in range(shape[0]):
            for p_index in range(shape[1]):

                for match in range(min_matches):
                    #Assemble teams for each player
                    for t in range(shape[0]):
                        teams[t, :] = np.random.choice(range(shape[1]), num_players, replace=False)

                    #Ensure that player is in the game!
                    if(p_index not in teams[t_index,:]):
                        teams[t_index, 0] = p_index

                    yield teams


    def _oneGame(self):
        """ play one game between teams of agents"""
        self.numGames += 1
        return self.game.play(players, self.results)

    def play_tournament(self, populations, players, repeat=1):
        """ Play agents against one another """
        self.setup(populations, players)

        for dummy in range(repeat):
            self.rounds += 1

            for teams in self._generateMatchups():

                # Prepare the players
                for t in range(teams.shape[0]):
                    for p in range(teams.shape[1]):
                        self.players[t*teams.shape[1] + p].initialize_player(t,p)
                        self.players[t*teams.shape[1] + p].initialize_model(self.populations[t,teams[t][p],:])

                self._oneGame()

                #Increment the game count
                for p in self.players:
                    self.results[p.team, p.individual_id, 1] += 1

        self.results[:,:,0] /= self.results[:,:,1]
        return self.results[:,:,0]

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
