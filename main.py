from colearning.genetic_optimizer import Optimizer
from colearning.players.neural_net_player import NeuralNetworkPlayer
from pybrain.tools.shortcuts import buildNetwork

opt = Optimizer()
teams = (2, 2)

players = [NeuralNetworkPlayer(buildNetwork(5, 8, 7)) for x in range(teams[0]*teams[1])]

opt.run(
    players,
    teams,
    10,
    200
)
