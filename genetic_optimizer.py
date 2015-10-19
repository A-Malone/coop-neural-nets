import random
import time

class Optimizer(object):
    """docstring for Optimizer"""

    #Population stats
    pop_size  = 60
    runs = 1
    elitism = True

    #The mutation rate, in percent
    mutation_rate = 3

    def __init__(self, arg):
        super(Optimizer, self).__init__()
        self.arg = arg


    def fitness(self, individual):
        """

        A simple fitness function that simply sums up the values of the traits,
        producing a value to map that individual's chance of reproduction.
        """
        #TODO: Make this work
        return sum(individual)


    def mutate_population(self, population, min_val, max_val):
        """
        A mutation funtion that mutates the individuals.
        """

        for individual in population:
            for position,trait in enumerate(individual):
                if random.randint(0,100) < self.mutation_rate:
                    individual[position] = random_trait(min_val, max_val)

    def reproduce(self, population, elitism=False):
        """
        Reproduces a population
        """

        if elitism:
            scores[np.argmax(scores)] *= 2

        #Normalize scores
        scores /= sum(scores)

        new_pop = np.zeros(population.shape)

        choices = np.random.choice(population, (len(population), 2), p=scores)
        for index, parents in enumerate(choices):
            new_pop[index, :] self.cross_over(parents)
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
        self.__dict__.update(kwargs)

        #Create a sample individual
        sample = new_individual()
        num_features = len(sample._params)

        # Create the populations
        populations = np.zeros((teams[0], pop_size, num_features))

        for run in range(self.runs):
            #get the start time
            start_time = time.time()

            #Reset the population
            for t in teams[0]:
                for i in pop_size:
                    populations[t,i,:] = new_individual._params

            for gen_count in range(gen_max):

                #TODO: Implement tournament fitness
                scores = Tournament.play
                for team, population in enumerate(populations):
                    new_population = reproduce(scores[team,:], population)
                    mutate_population(new_population, min_val, max_val)
                    populations[team,:,:] = new_population


        #total_time = sum(data[0])
        #average_time = total_time/len(data[0])

        #total_generations = sum(data[1])
        #average_gen = total_generations/len(data[1])

        #print("Total time: {}s, Total number of generations: {}, Average Time: {}, Average number of generations: {}".format(total_time,total_generations,average_time,average_gen))
