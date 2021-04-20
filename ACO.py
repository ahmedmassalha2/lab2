from functions import *
from functools import reduce
import numpy as np
from numpy.random import choice

alpha = 2
beta = 5
sigm = 3
ro = 0.8
th = 80
class ACO:
    def __init__(self,graph, demand, capacity, initPoint,
                  optimalValue, ncars, maxIter):
        self.graph = graph
        self.demand = demand
        self.capacity = capacity
        self.initPoint = initPoint
        self.optimalValue = optimalValue
        self.ncars = ncars
        self.maxIter = maxIter
        self.feromones, self.distances = self.createFeromonListAndDistanceList()
    def createFeromonListAndDistanceList(self):
        feromonesList, distances = dict(), dict()
        for vertics1 in self.graph.keys():
            for vertics2 in self.graph.keys():
                first = min(vertics1,vertics2)
                second = max(vertics1,vertics2)
                if vertics1 != vertics2:                    
                    feromonesList[(first, second)] = 1
                distances[(first, second)] = getDistance(self.graph[first],self.graph[second])
        return feromonesList, distances
    
    def getProbs(self,city, cities ):
        probs = []
        for c in cities:
            first, second = min(c,city), max(c,city)
            p = ((self.feromones[(first, second)])**alpha)*((1/self.distances[(first, second)])**beta)
            probs.append(p)

        return probs/np.sum(probs)
    
    
    
    #create route and calculate its cost
    def getNewState(self):
        routes, cities = [], [i for i in graph.keys()]
        
        
        while len(cities) != 0:
            
            currCapacity = self.capacity
            city = choice(cities, 1)[0]
            currentTruckPath = [city]
            currCapacity -= self.demand[city]
            cities.remove(city)

            #find cities to routes per truck
            finish = False
            while len(cities) != 0 and finish == False:
                probs = self.getProbs(city, cities)
                city = choice(cities, 1, p=probs)[0]
                if currCapacity - demand[city] >= 0:
                    currentTruckPath.append(city)
                    cities.remove(city)
                    currCapacity -= self.demand[city]
                else:
                    finish = True
            routes.append(currentTruckPath)
                                                                                                               
        routesCost = calculateDistance(self.graph, routes,self.initPoint)
        
        return (routes, routesCost)
    
    
    def updateFeromone(self, feromones, solutions, bestSolution):
        Lavg = reduce(lambda x,y: x+y, (i[1] for i in solutions))/len(solutions)
        self.feromones = { k : (ro + th/Lavg)*v for (k,v) in self.feromones.items() }
        solutions.sort(key = lambda x: x[1])
        if(bestSolution!=None):
            if(solutions[0][1] < bestSolution[1]):
                bestSolution = solutions[0]
            for path in bestSolution[0]:
                for i in range(len(path)-1):
                    self.feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = sigm/bestSolution[1] + self.feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
        else:
            bestSolution = solutions[0]
        for l in range(sigm):
            paths = solutions[l][0]
            L = solutions[l][1]
            for path in paths:
                for i in range(len(path)-1):
                    self.feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = (sigm-(l+1)/L**(l+1)) + self.feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
        return bestSolution
    
    def runAnts(self):     
        import time
        startTime = time.time()
        bestState = None
        for iteration in range(self.maxIter):
            antsSolutions = [ self.getNewState() for i in range(30)]
            newBest = self.updateFeromone(self.feromones, antsSolutions, bestState)
            if bestState!= None:
                if newBest[1]<bestState[1]:
                    bestState = newBest
            else:
                bestState = newBest
            print(bestState[1],time.time() - startTime)

initPoint,capacity, graph, demand, optimalValue, ncars, problemName = getData("E-n76-k10.txt")
a = ACO(graph, demand, capacity, initPoint,optimalValue, ncars, 100000)
a.runAnts()