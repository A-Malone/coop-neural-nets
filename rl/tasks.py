from .environment import TeamBattleEnvironment

class TeamBattleTask(EpisodicTask):
    """ Represents the format of the game and decides the final scoring for a team battle task """

    def __init__(self, agents):
        super(TeamBattleTask, self).__init__(TeamBattleEnvironment(agents))    

    def isFinished(self):
        abstractMethod()

    def getReward(self):
        """ Final positive reward for winners, negative for loser. """
        abstractMethod()    

    def f(self, x):
        """ I have no idea what this does"""
        raise ValueError("??????")
