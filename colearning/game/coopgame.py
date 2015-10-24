import numpy as np
from pybrain.tools.shortcuts import buildNetwork
import pygame

from .bullet import Bullet
from .baseplayer import BasePlayer

class CoopGame(object):
    """docstring for CoopGame"""

    window = None

    DIM = (600, 600)

    FPS = 24
    DT = 1.0/FPS

    players = []
    bullets = []

    def __init__(self, render=False, max_moves=200):
        super(CoopGame, self).__init__()
        self.render = render
        self.max_moves = max_moves

        if(self.render):
            pygame.init()
            self.window = pygame.display.set_mode(self.DIM)
            self.play = self._render_and_play

    def setup(self, players):
        self.players = players

        self.results = np.zeros(len(players))
        self.moves = np.zeros(len(players))
        self.rewards = np.zeros((2, len(players)))

        for ind,player in enumerate(players):
            assert(player.object_id == ind)
            player.setup(np.random.rand(2) * self.DIM, 0, np.pi/3)
            player.on_game_start()

        self.bullets = []

    def _turn(self, current_turn):
        self.rewards[0,:].fill(0)

        for i, obj in enumerate(self.players):
            move = obj.pre_update(self.players, self.bullets)
            self.moves[i] = move
            if(move not in obj.past_moves):
                obj.past_moves.add(move)
                self.rewards[0, i] += 3*(len(obj.past_moves)+1)

        for i, obj in enumerate(self.players):
            obj.update(self.moves[i], self.players, self.bullets, self.DIM, self.DT)

        for obj in self.bullets:
            obj.update(self.players, self.bullets, self.DIM, self.DT)

        # Check for collisions
        for player in self.players:
            for bullet in self.bullets:
                if(player.collision(bullet.position)):
                    if(bullet.firer_id == player.object_id):
                        continue
                    firer = filter(lambda x: x.object_id == bullet.firer_id, self.players)[0]
                    self.rewards[0, bullet.firer_id] += 10 if player.team != firer.team else -10
                    self.rewards[0, player.object_id] -= 10

        #Remove innactive objects
        self.bullets = filter(lambda x: x.active, self.bullets)

        #Reward players
        for i, player in enumerate(self.players):
            player.reward(self.rewards[int(current_turn==self.max_moves-1),i])

        #Update scores
        self.rewards[1,:] += self.rewards[0,:]

    def _render(self):
        for obj in self.players:
            obj.render(self.window)

    def play(self, players, results):
        self.setup(players)

        #Main loop
        current_turn = 0
        while current_turn < self.max_moves:
            self._turn(current_turn)
            current_turn+=1

        #Update the results
        for player in self.players:
            results[player.team, player.individual_id, 0] += self.rewards[1,player.object_id]
            results[player.team, player.individual_id, 1] += 1
            player.on_game_end()

    def _render_and_play(self, players, results):
        self.setup(players)

        render_clock = pygame.time.Clock()

        #Main loop
        current_turn = 0
        while current_turn < self.max_moves:

            pygame.display.flip()
            self.window.fill((0, 0, 0))
            self.window.lock()

            self._turn(current_turn)
            self._render()
            current_turn+=1

            self.window.unlock()
            #Tick the clock
            render_clock.tick(self.FPS)

        #Update the results
        for player in self.players:
            results[player.team, player.individual_id, 0] += player.score
            results[player.team, player.individual_id, 1] += 1
            player.on_game_end()

def main():

    num_teams = 4
    team_size = 1

    game = CoopGame(
        render=True,
        max_moves=1000
    )

if __name__ == '__main__':
    main()
