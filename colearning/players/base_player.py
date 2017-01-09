import numpy as np

from colearning.game import Player

class BasePlayer(Player):
    """docstring for BasePlayer"""

    #----Fields
    team = None
    individual_id = None

    def initialize_player(self, team, individual_id):
        """ Setup the player's external attributes """
        self.team = team
        self.individual_id = individual_id

    def get_view(self, players, bullets):
        """
        Returns what the player is able to see
        Outputs:
            Fov (in rad)
            Num enemy
            Num Ally in view
                Num Ally ping in view
            Enemy bullets in view
        """
        output = np.zeros(5)
        output[0] = self.fov_angle

        for obj in players:
            if(self.is_in_fov(obj.position)):
                if(obj.team != self.team):
                    output[1] += 1
                else:
                    output[2] += 1
                    if(obj.ping):
                        output[3] += 1

        for obj in bullets:
            if(self.is_in_fov(obj.position)):
                output[4] += 1

        return output

    def pre_update(self, players, bullets):
        """ Get a move from the model """
        in_vals = self.get_view(players, bullets)
        return self.get_move(in_vals)

    #----VIRTUAL FUNTIONS
    #----------------------------------------------------
    def reset(self):
        raise NotImplementedError('Player subclasses must reimplement reset')

    def learn(self):
        raise NotImplementedError('Player subclasses must reimplement learn')

    def get_move(self, in_vals):
        raise NotImplementedError('Player subclasses must reimplement get_move')

    def set_params(self, params):
        raise NotImplementedError('Player subclasses must reimplement set_params')

    def get_params(self):
        raise NotImplementedError('Player subclasses must reimplement set_params')

    def param_dim(self):
        raise NotImplementedError('Player subclasses must reimplement param_dim')

    def reward(self, amount):
        raise NotImplementedError('Player subclasses must reimplement reward')
