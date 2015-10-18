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


    def create_individual(self, size, min_val, max_val):
        """
        create an individual with the number of traits size, with each trait in
        the range specified by min_val and max_val
        """
        return [random_trait(min_val, max_val) for x in range(size)]

    def fitness(self, individual):
        """

        A simple fitness function that simply sums up the values of the traits,
        producing a value to map that individual's chance of reproduction.
        """
        return sum(individual)


    def mutate_population(self, population, min_val, max_val):
        """
        A mutation funtion that mutates the individuals.
        """

        for individual in population:
            for position,trait in enumerate(individual):
                if random.randint(0,100) < self.mutation_rate:
                    individual[position] = random_trait(min_val, max_val)

    def random_trait(self, min_val, max_val):
        """
        creates random traits for the individuals
        """
        return random.randint(min_val,max_val)

    def reproduce(self, population, elitism=False):
        """
        Reproduces a population
        """

        #TODO: Move this outside
        scores = np.array([fitness(x) for x in population])
        if elitism:
            scores[np.argmax(scores)] *= 2

        #Normalize
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

    def run(self, num_teams, pop_size, gen_max, **kwargs):
        self.__dict__.update(kwargs)

        for run in range(self.runs):
            #get the start time
            start_time = time.time()

            #Create an initial population
            population = [create_individual(trait_number, min_val, max_val) for x in range(trait_number)]

            for gen_count in range(gen_max):
                new_population = reproduce(population)
                mutate_population(new_population, min_val, max_val)
                population = new_population
            else:
                print("The solution was not found")
                data[0][run] = time.time()-start_time
                data[1][run] = gen_max

        total_time = sum(data[0])
        average_time = total_time/len(data[0])

        total_generations = sum(data[1])
        average_gen = total_generations/len(data[1])

        print("Total time: {}s, Total number of generations: {}, Average Time: {}, Average number of generations: {}".format(total_time,total_generations,average_time,average_gen))
