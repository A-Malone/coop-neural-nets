import numpy as np

class CoopPlayer(LearningAgent):
    """docstring for CoopPlayer"""

    #Declare the variables such that they are apparent
    team = None
    position = None
    heading = None
    fov_angle = None

    ping = False

    def __init__(self, module, learner):
        """
        Module is the actual neural net, learner modifies the module
        """
        super(CoopPlayer, self).__init__(module, learner)

    def set_team(self, team): self.team = team

    def init_state(position, heading, fov_angle):
        self.position = position
        self.heading  = heading
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