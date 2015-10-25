import pickle
import numpy as np

from colearning.game import CoopGame
from colearning.players import TurretPlayer

print("Loading players from players.cln...")
with open("players.cln", "r") as f:
    players = pickle.load(f)

#players = [TurretPlayer(), TurretPlayer()]
#players[0].initialize_player(0,0)
#players[1].initialize_player(1,0)

for player in players:
    print(type(player))

teams = (2, 1)
results = np.zeros((teams[0], teams[1], 2))

game = CoopGame(
    render=True,
    max_moves=1000
)

print("Playing game...")
game.play(players, results)
