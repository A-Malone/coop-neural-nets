import random, sys, time
import numpy as np

from .tournament import TeamTournament

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

        #Clip the scores to 0
        np.clip(scores, 0, sys.maxint, scores)
        print(scores)

        #Normalize scores
        total_score = sum(scores)
        scores /= total_score

        choices = np.random.choice(
            range(population.shape[0]),
            (len(population), 2),
            p=scores
        )

        new_pop = np.zeros(population.shape)

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

    def run(self, players, teams, pop_size, gen_max, **kwargs):
        assert(len(players) > 0)
        assert(len(players) == teams[0] * teams[1])

        num_features = players[0].param_dim()

        #Create the tournament object
        tourney = TeamTournament(teams)

        # Create the populations
        populations = np.zeros((teams[0], pop_size, num_features))
        for t in range(teams[0]):
            for p in range(teams[1]):
                populations[t,p,:] = players[t*teams[1] + p].get_params()

        for run in range(self.runs):
            #get the start time
            start_time = time.time()

            for gen_count in range(gen_max):
                scores = tourney.play_tournament(populations, players)
                print("\nGen: {}".format(gen_count))

                for t in range(teams[0]):
                    print(np.average(scores[t,:]))

                for team, population in enumerate(populations):
                    new_population = self.reproduce(scores[team,:], population)
                    self.mutate_population(new_population)
                    populations[team,:,:] = new_population
