import numpy as np

#POSSIBLE MOVES
class Move(object):
    FORWARD = 1
    TURN_LEFT = 2
    TURN_RIGHT = 3
    SHOOT = 4
    PING = 5
    NARROW_FOV = 6
    WIDEN_FOV = 7

class CoopPlayer(object):
    """docstring for CoopPlayer"""

    team = None
    position = None
    heading = None
    fov_angle = None

    ping = False

    def __init__(self, net, team):
        super(CoopPlayer, self).__init__()
        self.nn = net
        self.team = team

    def setup(self, pos, heading, fov_angle):
        self.position = pos
        self.heading = heading
        self.fov_angle = fov_angle

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
        output[0] = fov_angle
        
        for p in players:
            if(self.is_in_fov(p.position)):
                if(p.team != self.team):
                    output[1] += 1
                else:
                    output[2] += 1
                    if(p.ping):
                        output[3] += 1

        for b in bullets:
            if(self.is_in_fov(bullets)):
                output[4] += 1

        return output

    def is_in_fov(self, pos):
        angle = np.atan2(*list(pos - self.position))
        return abs((heading - angle)%(2*numpy.pi)) < self.fov_angle/2

    def get_action(self, in_vals):
        results = self.nn.activate(in_vals)
        return results.index(max(results))

    def update(self, move, timestep):
        pass

class CoopGame(object):
    """docstring for CoopGame"""
    WIDTH = 600
    HEIGHT = 600

    players = None

    def __init__(self, max_moves=100):
        super(CoopGame, self).__init__()
        self.max_moves = max_moves        

    def playGame(self, nets):

        #Setup
        self.players = [None for x in nets]
        for index, net in enumerate(nets):
            self.players[index] = Player(net, int(index <= len(nets)//2))            

            self.players[index].setup(
                np.multiply(np.rand(2), (self.WIDTH, self.HEIGHT)),
                0,
                np.pi/3
                )


        #Main loop
        current_move = 0
        while current_move < self.max_moves:
            for i in self.players:
                inputs = player.get_view(self.players)