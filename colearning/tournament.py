import itertools
import numpy as np

from colearning.game import CoopGame

class TeamTournament(object):
    """
    Takes a set of populations of neural nets and has them compete in a
    tournament to determine fitness
    """

    results = None

    def __init__(self, game_format):
        self.format = game_format
        self.game = CoopGame(
            render=False,
            max_moves=1000
        )

    def setup(self, populations, players):
        self.rounds = 0
        self.numGames = 0
        self.players = players
        self.populations = populations

        if(self.results == None):
            self.results = np.zeros((populations.shape[0], populations.shape[1], 2), dtype=np.float32)
        else:
            self.results.fill(0.0)

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
                        teams[t, :] = np.random.choice(range(shape[1]), self.format[1], replace=False)

                    #Ensure that player is in the game!
                    if(p_index not in teams[t_index,:]):
                        teams[t_index, 0] = p_index

                    yield teams


    def _oneGame(self):
        """ play one game between teams of agents"""
        self.numGames += 1
        return self.game.play(self.players, self.results)

    def play_tournament(self, populations, players, repeat=1):
        """ Play agents against one another """
        self.setup(populations, players)

        for dummy in range(repeat):
            self.rounds += 1

            for teams in self._generateMatchups():

                # Prepare the players
                for t in range(teams.shape[0]):
                    for p in range(teams.shape[1]):
                        self.players[t*teams.shape[1] + p].initialize_player(t,teams[t][p])
                        self.players[t*teams.shape[1] + p].set_params(self.populations[t,teams[t][p],:])

                self._oneGame()

                # Retrieve the players
                for t in range(teams.shape[0]):
                    for p in range(teams.shape[1]):
                        self.populations[t,teams[t][p],:] = self.players[t*teams.shape[1] + p].get_params()

        self.results[:,:,0] /= self.results[:,:,1]
        return self.results[:,:,0]
