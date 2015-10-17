from pybrain.utilities import abstractMethod
from pybrain.rl.environments import Environment

#POSSIBLE MOVES
class Move(object):
    FORWARD = 1
    TURN_LEFT = 2
    TURN_RIGHT = 3
    SHOOT = 4
    PING = 5
    NARROW_FOV = 6
    WIDEN_FOV = 7


class MultiAgentGame(Environment):
    """ 
    Base class to represent a game with some finite number of agents
    """
   
    #----OVERRIDES
    def performAction(self, actions):
        """ perform an action on the world that changes it's internal state (maybe
            stochastically).
            :key action: an action that should be executed in the Environment.
            :type action: by default, this is assumed to be a numpy array of doubles
            :note: This function is abstract and has to be implemented.
        """
        self.doMove(*actions)

    def doMove(self, agent, action):
        abstractMethod()
    
class TeamBattleEnvironment(MultiAgentGame):
    """ 
    Implements the rules on which tasks are run
    """

    #Constants
    TIMESTEP = 0.25    

    #Fields
    players = []
    bullets = []

    def __init__(self, players):
        self.players = players

    def num_teams(self):
        return len(Set([x.team for x in players]))

    def team_sizes(self):
        teams = {}
        for player in players:
            teams.setDefault(player.team, 0) += 1
        return teams
        
    #----OVERRIDES
    def getSensors(self):
        """ the currently visible state of the world (the observation may be
            stochastic - repeated calls returning different values)
            :rtype: by default, this is assumed to be a numpy array of doubles
            :note: This function is abstract and has to be implemented.
        """
        pass

    def reset(self):
        """ Most environments will implement this optional method that allows for
            reinitialization.
        """
        current_turn = 0
        pass

    def doMove(self, agent, action):
        pass

    def playGame(self, players, max_turns=100):
        while current_turn <  max_turns:
            for player in players:
                self.performAction(player.getAction())