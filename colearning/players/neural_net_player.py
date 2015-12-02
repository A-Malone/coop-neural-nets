import numpy as np
from . import BasePlayer

from pybrain.structure import LinearLayer, SigmoidLayer, FeedForwardNetwork, FullConnection

class NeuralNetworkPlayer(BasePlayer):
    """ NN-backed player"""
    def __init__(self):
        super(NeuralNetworkPlayer, self).__init__()

        # Create the network
        self.net = FeedForwardNetwork()

        # Internal Layers
        inLayer = LinearLayer(5)
        hiddenLayer1 = SigmoidLayer(6)
        hiddenLayer2 = SigmoidLayer(6)
        outLayer = LinearLayer(7)

        self.net.addInputModule(inLayer)
        self.net.addModule(hiddenLayer1)
        self.net.addModule(hiddenLayer2)
        self.net.addOutputModule(outLayer)

        self.net.addConnection(FullConnection(inLayer, hiddenLayer1))
        self.net.addConnection(FullConnection(hiddenLayer1, hiddenLayer2))
        self.net.addConnection(FullConnection(hiddenLayer2, outLayer))

        self.net.sortModules()

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
    def reset(self): pass
    def learn(self): pass
