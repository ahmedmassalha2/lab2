from functions import *
from functools import reduce
import numpy as np
import time
from numpy.random import choice

alpha = 2
beta = 5
sigma = 3
ro = 0.8
theta = 80
class ACO:
    def __init__(self,graph, demand, capacity, initPoint,
                  optimalValue, ncars, maxIter, maxTries):
        self.graph = graph
        self.demand = demand
        self.capacity = capacity
        self.initPoint = initPoint
        self.optimalValue = optimalValue
        self.ncars = ncars
        self.maxIter = maxIter
        self.limitTime = 0.6 * ncars
        self.maxTries = maxTries
        self.feromones, self.distances = self.createFeromonListAndDistanceList()
    def getEdge(self,v1,v2):
        return min(v1,v2), max(v1,v2)
    
    def createFeromonListAndDistanceList(self):
        feromonesList, distances = dict(), dict()
        for vertics1 in self.graph.keys():
            for vertics2 in self.graph.keys():
                first, second = self.getEdge(vertics1,vertics2)
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
        routes, cities = [], [i for i in self.graph.keys()]
        
        
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
                if currCapacity - self.demand[city] >= 0:
                    currentTruckPath.append(city)
                    cities.remove(city)
                    currCapacity -= self.demand[city]
                else:
                    finish = True
            routes.append(currentTruckPath)
                                                                                                               
        routesCost = calculateDistance(self.graph, routes,self.initPoint)
        
        return (routes, routesCost)
    
    
    def getBestAndUpdateferm(self, feromones, antsSol, bestState):
        avg = 0
        for el in antsSol:
            avg+=el[1]
        avg = avg/len(antsSol)
        
        #update feromones init
        for key in self.feromones.keys():
            self.feromones[key] = (ro + theta/avg)*self.feromones[key]

        antsSol.sort(key = lambda sol: sol[1])
        if(bestState==None):
            bestState = antsSol[0]
        else:
            if(antsSol[0][1] < bestState[1]):
                bestState = antsSol[0]
            for path in bestState[0]:
                for i in range(len(path)-1):
                    v1, v2 = self.getEdge(path[i],path[i+1])
                    self.feromones[(v1,v2)] = sigma/bestState[1] + self.feromones[(v1,v2)]
            
        for idx in range(sigma):
            routes, routesCost = antsSol[idx][0], antsSol[idx][1]
            for truck in routes:
                for i in range(len(truck)-1):
                    v1, v2 = self.getEdge(truck[i],truck[i+1])
                    self.feromones[(v1,v2)] = (sigma-(idx+1)/routesCost**(idx+1)) + self.feromones[(v1,v2)]
        return bestState
    
    def checkIterStopCond(self,startTime,iteration):
        if iteration > self.maxIter or (time.time() - startTime) > self.limitTime:
            return False
        else:
            return True
    def runAnts(self):     
        
        startTime = time.time()
        bestState, iteration = None, 0
        tryMax = self.maxTries
        while self.checkIterStopCond(startTime,iteration):
            antsSolutions = [ self.getNewState() for i in range(22)]
            newBest = self.getBestAndUpdateferm(self.feromones, antsSolutions, bestState)
            if bestState!= None:
                if newBest[1]<bestState[1]:
                    tryMax = self.maxTries
                    bestState = newBest
                else:
                    tryMax -= 1
                    if tryMax == 0:
                        break
            else:
                bestState = newBest
            print(bestState[1],time.time() - startTime,iteration)
            iteration += 1
        return bestState,time.time() - startTime,iteration

