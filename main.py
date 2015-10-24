from colearning.genetic_optimizer import Optimizer
from colearning.players.neural_net_player import NeuralNetworkPlayer
from colearning.players.learning_agent_player import ActionQLearningPlayer
from pybrain.tools.shortcuts import buildNetwork

opt = Optimizer()
teams = (2, 2)
problem = (5,7)

players = [ActionQLearningPlayer(problem) for x in range(teams[0]*teams[1])]

opt.run(
    players,
    teams,
    10,
    200
)
