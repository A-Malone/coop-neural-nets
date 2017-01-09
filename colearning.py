import atexit
import pickle
import argparse

from colearning.genetic_optimizer import Optimizer
from colearning.players import NeuralNetworkPlayer

parser = argparse.ArgumentParser(description='Genetically evolve the best player for a 2D game')
parser.add_argument('--file', dest="file", help='Load player data from the path specified')

args = parser.parse_args()

teams = (2,1)
if(args.file):
    with open(file, "w") as f:
        players = pickle.load(f)
else:
    players = [NeuralNetworkPlayer() for x in range(teams[0]*teams[1])]

def save_players():
    print("Saving players to players.cln...")
    with open("players.cln", "w") as f:
        pickle.dump(players, f)
atexit.register(save_players)


opt = Optimizer()
opt.run(players, teams, 25, 1000)
