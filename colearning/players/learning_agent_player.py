import numpy as np
from colearning.game.baseplayer import BasePlayer

class LearningAgentPlayer(BasePlayer):
    """ LearningAgent-backed player"""
    def __init__(self, agent):
        super(LearningAgentPlayer, self).__init__()
        self.agent = agent

    def get_move(self, in_vals):
        self.agent.integrateObservation(in_vals)
        return self.agent.getAction()

    def set_params(self, params):
        self.agent.reset()
        self.agent.learner.module._params = params

    def get_params(self):
        return self.agent.learner.module._params

    def param_dim(self):
        return self.agent.learner.module.paramdim

    def reward(self, amount):
        self.agent.giveReward(amount)

    def on_game_start(self):
        self.agent.newEpisode()

    def on_game_end(self):
        self.agent.learn()
