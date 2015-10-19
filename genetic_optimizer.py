import random
import time

import numpy as np
from pybrain.tools.shortcuts import buildNetwork

from tournament import TeamTournament

class Optimizer(object):
    """docstring for Optimizer"""

    #Population stats
    pop_size  = 60
    runs = 1
    elitism = True

    #The mutation rate, in percent
    mutation_rate = 3

    def __init__(self):
        super(Optimizer, self).__init__()

    def fitness(self, individual):
        """

        A simple fitness function that simply sums up the values of the traits,
        producing a value to map that individual's chance of reproduction.
        """
        #TODO: Make this work
        return sum(individual)


    def mutate_population(self, population):
        """
        A mutation funtion that mutates the individuals.
        """

        for individual in population:
            for position,trait in enumerate(individual):
                if random.randint(0,100) < self.mutation_rate:
                    individual[position] += np.random.normal()

    def reproduce(self, scores, population, elitism=False):
        """
        Reproduces a population
        """

        if elitism:
            scores[np.argmax(scores)] *= 2

        #Normalize scores
        scores /= sum(scores)

        new_pop = np.zeros(population.shape)

        choices = np.random.choice(
            range(population.shape[0]),
            (len(population), 2),
            p=scores
        )
        for index, parents in enumerate(choices):
            new_pop[index, :] = self.cross_over(map(lambda x:population[x], parents))
        return new_pop

    def cross_over(self, parents):
        """
        Crosses over parents to produce a child
        """
        assert(len(parents[0]) == len(parents[0]))
        num_traits = len(parents[0])

        index = random.randint(int(num_traits/5),int(4*num_traits/5))

        child = np.zeros(parents[0].shape)
        child[:index] = (parents[0])[:index]
        child[index:] = (parents[1])[index:]
        return child

    def run(self, new_individual, teams, pop_size, gen_max, **kwargs):

        num_features = len(new_individual()._params)

        # Create the populations
        populations = np.zeros((teams[0], pop_size, num_features))

        for run in range(self.runs):
            #get the start time
            start_time = time.time()

            #Reset the population
            for t in range(teams[0]):
                for i in range(pop_size):
                    populations[t,i,:] = new_individual()._params

            for gen_count in range(gen_max):
                tourney = TeamTournament(populations)

                scores = tourney.organize(teams[1])
                print("\n{}".format(gen_count))
                print(scores)

                for team, population in enumerate(populations):
                    new_population = self.reproduce(scores[team,:], population)
                    self.mutate_population(new_population)
                    populations[team,:,:] = new_population

def main():
    opt = Optimizer()
    num_teams = 2
    team_size = 2
    def ind() : return buildNetwork(5, 8, 7)
    opt.run(
        ind,
        (num_teams, team_size),
        10,
        200
    )


if __name__ == '__main__':
    main()
