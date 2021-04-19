from __future__ import division
import time
from random import randint, random, sample, shuffle
import numpy as np
import operator
import re
from functions import *
import copy
GA_ELITRATE = 0.4
maxIterations = 16384
populationSize = 2048
GA_MUTATIONRATE = 0.3
nCitits = 0
initPoint,capacity, graph, demand, optimalValue, ncars = None,None,None,None,None,None
class Agent:
    def __init__(self, string, fitness):
        self.string = string
        self.fitness = fitness
        self.age = 0
        self.cars = 0


def roulette_selection(weights):
        # sort the weights in ascending order
        sorted_indexed_weights = sorted(enumerate(weights), key=operator.itemgetter(1));
        indices, sorted_weights = zip(*sorted_indexed_weights);
        # calculate the cumulative probability
        tot_sum=sum(sorted_weights)
        prob = [x/tot_sum for x in sorted_weights]
        cum_prob=np.cumsum(prob)
        # select a random a number in the range [0,1]
        random_num=random()

        for index_value, cum_prob_value in zip(indices,cum_prob):
            if random_num < cum_prob_value:
                return index_value

def initPop(population, buffer,graph):
    
    for i in range(populationSize):
        customers = createShuffledState(graph.keys())
        population.append(Agent(customers, 0))
        buffer.append(Agent("", 0))

def calcAvarage(population):
    ''' calculate avarage and Standard Deviation, then print'''
    Sum=0
    for i in population:
        Sum+= i.fitness
    avg = Sum/len(population)
    
    Sum=0
    for i in population:
        Sum+= (i.fitness-avg)**2
    
    SD = abs(Sum/len(population))
    print("Avarage is: ", avg, "Standard Deviation:", SD)



def getFitness(population,graph,demand,capacity,initPoint,nTrucks):
    Sum=0
    for agent in population:
        agent.age+=1
        state = agent.string
        tours = creatTrucksTour(state, graph, capacity, demand, nTrucks)
        fit = calculateDistance(graph, tours,initPoint)                    
        agent.fitness = fit
        Sum+= fit
    avg = Sum/len(population)
    Sum=0
    for i in population:
        Sum+= (i.fitness-avg)**2  
    SD = abs(Sum/len(population))
    print("Avarage is: ", avg, "Standard Deviation:", SD)



def twoPointCrossOver(population,buffer,esize):
    for i in range(esize, populationSize):
        i1 = randint(0, int(populationSize/2) - 1)
        i2 = randint(0, int(populationSize/2) - 1)       
        buffer[i].string = crossover(population[i1].string,population[i2].string)
    return buffer

    
def elitism(population, buffer, esize):
    return [Agent(x.string, x.fitness) for x in population[:esize]] + [x for x in buffer[esize:]]

def mutate(agent):
    def inversion_mutation(chromosome_aux):
            chromosome = agent.string
            
            index1 = randint(0,len(chromosome)-1)
            index2 = randint(index1,len(chromosome)-1)
            
            chromosome_mid = chromosome[index1:index2]
            chromosome_mid.reverse()
            
            chromosome_result = chromosome[0:index1] + chromosome_mid + chromosome[index2:]
            
            return chromosome_result
    def insertion_mutation(chromosome_aux):
            chromosome = agent.string            
            i1, i2 = getTwoIndexesFromState(chromosome)
            chromosome.insert(i2-1,chromosome.pop(chromosome.index(chromosome[i1]))) 
            
            return chromosome
    def swap_mutation(chromosome_aux):
            chromosome = agent.string            
            i1, i2 = getTwoIndexesFromState(chromosome)
            chromosome[i1], chromosome[i2] = chromosome[i2], chromosome[i1]
            
            return chromosome
    agent.string = inversion_mutation(agent.string)
def random_subroute(state):
    global initPoint,capacity, graph, demand, optimalValue, ncars
    routes =  creatTrucksTour(state, graph, capacity, demand, ncars)
    return routes[randint(0,len(routes)-1)]
################################################################
def crossover(parent1, parent2):
        global nCitits

        def simple_random_crossover( chrom1, chrom2):
            child = copy.deepcopy(chrom1)
            sub_route = random_subroute(chrom2)
            for x in sub_route:
                child.pop(child.index(x))
            pos=randint(1,len(chrom1)-1)
            return child[:pos] + sub_route + child[pos:]
        return  simple_random_crossover(parent1, parent1)
def ox(parent1, parent2):
    spos1 = randint(0, int(populationSize) - 1) % len(parent1)
    child = []
    for i in parent1:
        child.append(-1)
    for i in range(len(parent1)):
        if(parent1[i] < len(parent1)/2):
            child[i] = parent1[i]
    k = 0
    for j in range(len(parent1)):
        if parent2[j] >= len(parent1)/2:
            while child[k] != -1:
                k += 1
            child[k] = parent2[j]
    return child
def pmx(parent1,parent2):    
    spos1 = randint(0, int(populationSize) - 1) % len(parent1)
    child = []
    for i in parent1:
        child.append(i)
    for j in range(spos1):
        if parent1[j] == parent2[spos1]:
            child[j] = parent1[spos1]
            child[spos1] = parent1[j]
    return child
    
################################################################
def mate(population, buffer, choiceFunc, crossOverFunc):
    esize = int(populationSize * GA_ELITRATE)
    for i in range(esize):
        buffer[i] = population[i]
    for i in range(esize, populationSize):
        p1,p2 = choiceFunc(population, 25),choiceFunc(population, 25)
        buffer[i].string = ox(p1.string, p2.string)
        buffer[i].age = 0
        # Mate the rest
    
        if random() < GA_MUTATIONRATE:
            mutate(buffer[i])
    return buffer

def tournementSelection(population, size):
    pick1 = population[randint(0,populationSize-1)]     # pick first genom
    for i in range(size):
        pick2 = population[randint(0,populationSize-1)]     # pick second genom

        if pick1.fitness > pick2.fitness:   # find better genom
            pick1 = pick2

    return pick2



def RWS(population, buffer, size):
    '''Roulette wheel selection'''
    selections = []
    fitnesses = [(1/agent.fitness) for agent in population]
    for i in range(size):
        index = roulette_selection(fitnesses)
        selections.append(population[index])

    return selections + [i for i in buffer[size:]]

def aging(population, buffer, size):
    BestAge = 4
    for agent in population:
        agent.fitness += (agent.age-BestAge)**2   # add age bonus
    return RWS(population, buffer, size)
        
    

def startGenetic(path):
    global nCitits, initPoint,capacity, graph, demand, optimalValue, ncars
    startingTime = time.time()
    clocks = time.process_time()
    population = []
    buffer = []
    initPoint,capacity, graph, demand, optimalValue, ncars, problemName = getData(path)
    initPop(population, buffer, graph)
    nCitits = len(population[0].string)
    for i in range(maxIterations):
        iterStartingTime = time.time()
        
        getFitness(population,graph,demand,capacity,initPoint,ncars)
        population.sort(key= lambda x: x.fitness)  # sort population array by fitness
        print("Current best state cost: ", population[0].fitness)     # print string with best fitness
        if int(population[0].fitness) == int(optimalValue) or time.time() - startingTime >= ncars * 0.85:
            print("Elapsed time: ", time.time()-iterStartingTime,"Clock ticks: ",str(time.process_time() - clocks))
            print("")
            tour = creatTrucksTour(population[0].string, graph, capacity, demand, ncars)
            return tour, population[0].fitness, i
        
        buffer = mate(population, buffer, tournementSelection, twoPointCrossOver)  # mate
        population, buffer = buffer, population


            
        print("Elapsed time: ", time.time()-iterStartingTime,"Clock ticks: ",str(time.process_time() - clocks))
        clock = time.process_time()
        print("")


# startGenetic("E-n33-k4.txt")















