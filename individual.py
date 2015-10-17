from pybrain.structure.networks.recurrent import RecurrentNetwork

nn = RecurrentNetwork()
print(dir(nn))

class CoopPlayer(object):
    """
    Represents one of the player objects in the game
    """

    #Declare the variables such that they are apparent
    team = None
    position = None
    heading = None
    fov_angle = None

    def __init__(self, nn):
        super(CoopPlayer, self).__init__()
        self.arg = arg

    def init_state(position, heading, fov_angle):
        self.position = position
        self.heading  = heading
        self.fov_angle = fov_angle
        
