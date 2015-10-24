import numpy as np
from colearning.game.baseplayer import BasePlayer

class NeuralNetworkPlayer(BasePlayer):
    """ NN-backed player"""
    def __init__(self, net):
        super(NeuralNetworkPlayer, self).__init__()
        self.net = net

    def get_move(self, in_vals):
        results = self.net.activate(in_vals)
        return np.argmax(results)

    def set_params(self, params):
        self.net._params = params

    def get_params(self):
        return self.net._params

    def param_dim(self):
        return self.net.paramdim

    def reward(self, amount): pass
    def on_game_start(self): pass
    def on_game_end(self): pass
