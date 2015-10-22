from .baseplayer import BasePlayer

class NeuralNetworkPlayer(BasePlayer):
    """ NN-backed player"""
    def __init__(self, net):
        super(NeuralNetworkPlayer, self).__init__()
        self.net = net

    def get_move(self, in_vals):
        results = self.model.activate(in_vals)
        return np.argmax(results)

    def initialize_model(self, params):
        self.net._params = params

    def param_dim(self):
        return self.net.param_dim()
