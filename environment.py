import numpy as np
from pybrain.tools.shortcuts import buildNetwork
import pygame

from coopplayer import CoopPlayer

class CoopGame(object):
    """docstring for CoopGame"""

    window = None

    DIM = (600, 600)

    # In seconds
    DT = 0.25

    game_objects = []

    def __init__(self, render=False, max_moves=200):
        super(CoopGame, self).__init__()
        self.render = render
        self.max_moves = max_moves

        if(self.render):
            pygame.init()
            self.window = pygame.display.set_mode(self.DIM)
            self.play = self._render_and_play

    def setup(self, nets):
        #Setup
        for team_num, team in enumerate(nets):
            for net in team:
                player = CoopPlayer(net, team_num)
                #Asign random positions within the bounds
                player.setup(np.random.rand(2) * self.DIM, 0, np.pi/3)

                self.game_objects.append(player)

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

    def play(self, nets):
        #Main loop
        current_turn = 0
        while current_turn < self.max_moves:
            self._turn()
            current_turn+=1

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
            render_clock.tick(1 / self.DT)

def main():
    game = CoopGame(
        render=True,
        max_moves=50
    )
    num_teams = 4
    team_size = 1

    nets = []
    for team in range(num_teams):
        nets.append([buildNetwork(5, 8, 7) for x in range(team_size)])

    game.play(nets)

if __name__ == '__main__':
    main()
