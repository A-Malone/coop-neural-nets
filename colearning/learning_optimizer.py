from time import time
import numpy as np

from colearning.game import CoopGame

class LearningOptimizer(object):
    """docstring for LearningOptimizer"""
    def __init__(self):
        self.game = CoopGame(
            render=False,
            max_moves=1000
        )


    def run(self, players, teams, learn_max, **kwargs):
        assert(len(players) == teams[0]*teams[1])

        results = np.zeros((teams[0],teams[1],2))

        #Initialize all of the players once
        for t in range(teams[0]):
            for p in range(teams[1]):
                players[t*teams[1] + p].initialize_player(t,p)

        learn_every = 100
        for learning in range(learn_max):
            print("Starting Round {}".format(learning + 1))
            start = time()

            for i in range(learn_every):
                self.game.play(players, results)
            mid = time()
            print("Played {} matches in {}s, learning...".format(learn_every, mid-start))

            for player in players:
                player.learn()
                player.reset()

            end = time()
            print("Finished Round {} in {}s".format(learning + 1, end-start))
            print("-"*20)
