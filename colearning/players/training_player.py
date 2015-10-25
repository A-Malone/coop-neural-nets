import numpy as np
from . import BasePlayer

from colearning.game import Move

class TurretPlayer(BasePlayer):
    """ Simple AI to train against """
    def __init__(self):
        super(TurretPlayer, self).__init__()

    def get_move(self, in_vals):
        if(in_vals[1] > 0 and in_vals[1] >= in_vals[2]):
            return Move.SHOOT
        return Move.TURN_LEFT

    def set_params(self, params): pass
    def get_params(self): pass
    def param_dim(self): pass
    def reward(self, amount): pass
    def reset(self): pass
    def learn(self): pass
