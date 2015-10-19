import numpy as np
from pybrain.tools.shortcuts import buildNetwork
import pygame

from coopplayer import CoopPlayer

class CoopGame(object):
    """docstring for CoopGame"""

    window = None

    DIM = (600, 600)

    FPS = 24
    DT = 1.0/FPS
    
    game_objects = []

    def __init__(self, render=False, max_moves=200):
        super(CoopGame, self).__init__()
        self.render = render
        self.max_moves = max_moves

        if(self.render):
            pygame.init()
            self.window = pygame.display.set_mode(self.DIM)
            self.play = self._render_and_play

    def setup(self, teams):
        self.game_objects = []

        self.results = np.zeros(teams.shape[:2])

        #Setup
        for t in range(teams.shape[0]):
            for p in range(teams.shape[1]):
                #Create net and the player
                net = buildNetwork(5, 8, 7)
                net._params = teams[t,p,:]
                player = CoopPlayer(net, t, p)

                #Asign random positions within the bounds
                player.setup(np.random.rand(2) * self.DIM, 0, np.pi/3)

                self.game_objects.append(player)

    def get_results(self):
        for player in filter(lambda x : x is CoopPlayer, self.game_objects):
            self.results[player.team, player.individual_id] = player.score
        return self.results

    def _turn(self):
        #print(self.game_objects)
        for obj in self.game_objects:
            obj.pre_update(self.game_objects)

        for obj in self.game_objects:
            obj.update(self.game_objects, self.DIM, self.DT)

        for obj in self.game_objects:
            obj.post_update(self.game_objects)

        self.game_objects = filter(lambda x: x.active, self.game_objects)

    def _render(self):
        for obj in self.game_objects:
            obj.render(self.window)

    def play(self, teams):
        self.setup(teams)

        #Main loop
        current_turn = 0
        while current_turn < self.max_moves:
            self._turn()
            current_turn+=1

        return self.get_results()

    def _render_and_play(self, nets):
        self.setup(nets)

        render_clock = pygame.time.Clock()

        #Main loop
        current_turn = 0
        while current_turn < self.max_moves:

            pygame.display.flip()
            self.window.fill((0, 0, 0))
            self.window.lock()

            self._turn()
            self._render()
            current_turn+=1

            self.window.unlock()
            #Tick the clock
            render_clock.tick(self.FPS)

        return self.get_results()

def main():

    num_teams = 4
    team_size = 1

    game = CoopGame(
        render=True,
        max_moves=1000
    )

    #nets = []
    #for team in range(num_teams):
    #    nets.append([ for x in range(team_size)])

    #game.play(nets)

if __name__ == '__main__':
    main()
