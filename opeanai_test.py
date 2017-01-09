import random
import sys
import time
import numpy as np

from pybrain.structure import LinearLayer, SigmoidLayer, FeedForwardNetwork, FullConnection
from pybrain.structure.networks import NeuronDecomposableNetwork

import gym

# ---- TASKS
class ClassifyTask(object):

    def get_problem_size(self):
        """Returns the number of individuals to be scored simultaneously"""
        return 1

    def fitness(self, individual, n=10):
        """Maps individuals to scores"""
        shape = (n, individual.net.indim)
        patterns = np.reshape(np.random.randint(
            low=0, high=10, size=shape[0] * shape[1]), shape)

        score = 0

        for p in patterns:

            # Definition of problem
            true_output = np.zeros((individual.net.outdim, 1))
            true_output[0] = 1 if p[0] > 5 else 0

            result = individual.net.activate(p)

            # Scoring of problem
            score += 100 / (np.linalg.norm(result - true_output) + 1)

        individual.score = score / n

    def max_score(self):
        return 100


class AIGymTask(object):

    def __init__(self, env):
        self.env = env

    def fitness(self, individual, steps, trials, render=False):
        total_score = 0

        for t in range(trials):
            observation = self.env.reset()
            for s in range(steps):
                if(render):
                    self.env.render()
                action = np.argmax(individual.net.activate(observation))
                observation, reward, done, info = self.env.step(action)
                total_score += reward
                if done:
                    break

        individual.score = total_score / trials


class Individual(object):
    """Associates a network with the components which created it"""

    def __init__(self, net, components, gen_num):
        self.net = net
        self.components = components
        self.gen_num = gen_num
        self.score = 0


class GeneticNetworkOptimizer(object):
    """
    Optimizes a network for an external, decomposing the network 
    using ESP. Each individual is a combination of independantly
    evolved neurons. These are evolved in separate populations.
    """

    # Population stats
    pop_size = 25
    runs = 1
    elitism = 10

    # The mutation rate, in percent
    mutation_rate = 1

    def __init__(self, template_net):
        """Initializes the optimizer"""
        self.template_net = template_net
        self._generate_populations()
        self.gen_num = 0

    def _mutate_population(self, population):
        """A mutation funtion that mutates a population."""

        for individual in population:
            for position, trait in enumerate(individual):
                if random.randint(0, 100) < self.mutation_rate:
                    individual[position] += np.random.normal()

    # ---- HELPER FUNCTIONS
    def _reproduce(self, scores, population, elitism=False):
        """
        Reproduces a population
        """

        # If we're elitest, give the best performing individual an advantage
        if elitism:
            scores[np.argmax(scores)] *= elitism

        # Make scores positive
        min_score = np.min(scores)
        if(min_score <= 0):
            scores = np.add(scores, min_score+1)        

        # Normalize scores into probabilities
        total_score = sum(scores)
        scores /= total_score

        if (np.nan in scores):
            print("Error")
            print(scores)


        # Choose parents
        choices = np.random.choice(
            range(population.shape[0]),
            (len(population), 2),
            p=scores
        )

        # Make new population
        new_pop = np.zeros(population.shape)

        # ---- CROSS OVER
        # Generate cross-over points
        raw_cross_over_points = np.random.normal(
            loc=population.shape[1] / 2,
            scale=population.shape[1] / 6,
            size=(population.shape[0])
        )
        cross_over_points = np.clip(
            np.rint(raw_cross_over_points), 0, population.shape[1])

        for index, parents in enumerate(choices):
            cp = int(cross_over_points[index])
            new_pop[index, :] = np.concatenate(
                (population[parents[0], :cp], population[parents[1], cp:]))

        return new_pop

    def _generate_populations(self):
        """Generate populations based on the template net"""
        template_decomposition = self.template_net.getDecomposition()
        self.num_populations = len(template_decomposition)

        self.populations = []

        for i in range(self.num_populations):
            shape = (self.pop_size, len(template_decomposition))
            population = np.reshape(np.random.normal(
                size=shape[0] * shape[1]), shape)

            self.populations.append(population)

    # ---- EXTERNAL INTERFACE
    def generate_individuals(self, num_individuals):
        """Generates individuals from this generation for use in testing"""
        shape = (num_individuals, len(self.populations))
        combinations = np.reshape(np.random.randint(
            0, self.pop_size, size=shape[0] * shape[1]), shape)

        individuals = []
        for i, cb in enumerate(combinations):
            net = self.template_net.copy()
            net.setDecomposition([pop[cb[k], :] for k, pop in enumerate(self.populations)])

            individuals.append(Individual(net, cb, self.gen_num))

        return individuals

    def run_generation(self, individuals):
        """Use scoring of individuals to define fitness of the network 
        components, and evolve them"""

        # Accumulate scores
        scores = np.zeros((len(self.populations), self.pop_size))
        count = np.zeros((len(self.populations), self.pop_size))

        for i, individual in enumerate(individuals):
            assert(individual.gen_num == self.gen_num)
            for pop, comp in enumerate(individual.components):
                scores[pop, comp] += individual.score
                count[pop, comp] += 1
        
        with np.errstate(divide='ignore', invalid='ignore'):
            norm_scores = np.divide(scores, count)            
            norm_scores[norm_scores == np.inf] = 0
            norm_scores = np.nan_to_num(norm_scores)
        
        print("Generation: {}, Average score: {:.3f} Max score: {:.3f}".format(
            self.gen_num, norm_scores.mean(), np.nanmax(norm_scores)))

        for p in range(len(self.populations)):
            new_population = self._reproduce(
                norm_scores[p, :], self.populations[p])
            self._mutate_population(new_population)
            self.populations[p] = new_population

        self.gen_num += 1

def get_dim(space):
    if(isinstance(space, gym.spaces.Discrete)):
        return space.n
    else:
        return space.shape[0]


def main():

    env = gym.make('CartPole-v0')
    in_dim = get_dim(env.observation_space)
    out_dim = get_dim(env.action_space)

    # Create the network
    net = FeedForwardNetwork()

    # Interface layers
    inLayer = LinearLayer(in_dim)
    outLayer = LinearLayer(out_dim)

    # Internal Layers
    hiddenLayer1 = SigmoidLayer(6)

    net.addInputModule(inLayer)
    net.addModule(hiddenLayer1)
    net.addOutputModule(outLayer)

    net.addConnection(FullConnection(inLayer, hiddenLayer1))
    net.addConnection(FullConnection(hiddenLayer1, outLayer))

    network = NeuronDecomposableNetwork.convertNormalNetwork(net)
    network.sortModules()

    optimizer = GeneticNetworkOptimizer(network)
    task = AIGymTask(env)

    gen_count = 10000
    epsilon = 0.01

    for gen in range(gen_count):
        pop = optimizer.generate_individuals(100)

        for p in pop:
            task.fitness(p, steps=200, trials=10)

        optimizer.run_generation(pop)


if (__name__ == "__main__"):
    main()
