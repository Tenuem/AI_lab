import random
from telnetlib import NOP

import numpy as np
from utils import fitness


class Genetic:
    def __init__(self, coords, population_size=100, elite_size=10, mutation_rate=0.01):
        self.coords = coords
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate

    def population_fitness(self, population):
        population_fitness = {}
        for i, individual in enumerate(population):
            # 1/fitness -> change to maximization problem
            population_fitness[i] = 1/fitness(self.coords, individual)

        return {k: v for k, v in sorted(population_fitness.items(), key=lambda item: item[1], reverse=True)}

    def best_solution(self, population):
        population_fitness = list(self.population_fitness(population))
        best_ind = population_fitness[0]
        #print(population_fitness[0])
        return population[best_ind]

    def initial_population(self):
        population = []
        # Create initial population
        for i in range(self.population_size):
            solution = np.random.permutation(len(self.coords))
            population.append(solution)

        return population

    def selection(self, population):
        # TODO: implement selection
        selection = []
        popFitness = self.population_fitness(population)
        sumFitness = 0
        for key, value in popFitness.items():
            sumFitness += value
        probability = {}
        prevProbability = 0
        for k, v in popFitness.items():
            probability[k] = prevProbability + (v/sumFitness)
            prevProbability = probability[k]
        
        
        for i in range(0, len(population)):
            r = random.random()
            for k, v in probability.items():
                if r <= v or i > 90:
                    selection.append(population[k])
                    break

        #print(len(selection))
        return selection

    def crossover_population(self, population):
        # TODO: implement crossover
        cross = []
        length = len(population[0])
        for i in range(self.population_size):
            if i > 90:
                cross.append(population[i])
               
            else:
                l = random.randrange(0, length)
                r = random.randrange(l, length)
                father = population[random.randint(0, len(population)-1)]
                mother = population[random.randint(0, len(population)-1)]
                sample = []
                for j in range(abs(r-l)):
                    sample.append(father[l+j])
                sample = father[l:r]
                mother = np.array([a for a in mother if a not in sample])
                mother = np.append(mother, sample)
                '''
                for element in mother:
                    if element in sample:
                        np.delete(mother, element, axis=None)
                    np.insert(mother, l, sample, axis=None)
'''
                #cross.append(father)
                cross.append(mother)
        return cross

    def mutate_population(self, population):
        # TODO: implement mutation
        for i in range(len(population)):
            chance = random.random()
            if chance <= self.mutation_rate:
                a = random.randint(0, len(population[0])-1)
                while True:
                    b = random.randint(0, len(population[0])-1)
                    if b != a:
                        break
                tmp = population[i][a]
                population[i][a] = population[i][b]
                population[i][b] = tmp

        return population

    def next_generation(self, population):
        selection = self.selection(population)
        children = self.crossover_population(selection)
        next_generation = self.mutate_population(children)
        return next_generation
