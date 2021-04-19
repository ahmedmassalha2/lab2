import random
import math
import numpy as np
import time
from functions import prinSolution,calculateSolDistance,createShuffledState,getData,getTwoIndexesFromState,creatTrucksTour,calculateDistance,swap
#[9,7,5,2,1,6,13,11,4,3,8,10,17,20,18,15,12,14,21,19,16]#
#[9,7,5,2,1,6,13,11,4,3,8,10,17,20,18,15,12,14,21,19,16]#
class simulatedAnnealing:
    def __init__(self, initialState, graph, demand, capacity, initPoint,
                  optimalValue, ncars, initTemp, maxIter, nAttemps):
        self.state = initialState
        self.graph = graph
        self.demand = demand
        self.capacity = capacity
        self.initPoint = initPoint
        self.optimalValue = optimalValue
        self.ncars = ncars
        self.initTemp = initTemp
        self.maxIter = maxIter
        self.nAttemps = nAttemps
        self.valueMaxRep = self.nAttemps*5
        
    
    def updateTemp(self,temp):
        return random.uniform(0, 1) * temp
    
    def simulate(self):
        totalTime = time.time()
        startTime = time.clock()
        temp = self.initTemp
        currState, bestState = self.state, [i for i in self.state]
        valueMaxTries = self.valueMaxRep
        bestCostRep = 0
        for iteration in range(self.maxIter):
            for j in range(self.nAttemps):
                i1, i2 = getTwoIndexesFromState(currState)
                
                nextState = swap(currState, i1, i2)
                
                currCost, nextCost = calculateSolDistance(self.initPoint, currState, self.graph, self.capacity, self.demand, self.ncars),calculateSolDistance(self.initPoint, nextState, self.graph, self.capacity, self.demand, self.ncars)
                cost_diff = nextCost - currCost
    
                
                if cost_diff < 0:
                    currState = [i for i in nextState]
                    bestCost = calculateSolDistance(self.initPoint, bestState, self.graph, self.capacity, self.demand, self.ncars)
                    currCost = calculateSolDistance(self.initPoint, currState, self.graph, self.capacity, self.demand, self.ncars)
                    if currCost < bestCost:
                       bestState =  [i for i in currState]
                else:
                    try:
                        ans = np.exp(-cost_diff / temp)
    
                    except OverflowError:
                        ans = float('inf')
                    if random.uniform(0, 1) < ans:
                        currState = [i for i in nextState]
            

            bestCost = calculateSolDistance(self.initPoint, bestState, self.graph, self.capacity, self.demand, self.ncars)
            print("Current best state cost: ",str(bestCost),"Clock ticks: ",str(time.clock() - startTime))
            startTime = time.clock()
            if bestCostRep != bestCost and int(bestCost) != int(self.optimalValue) and time.time() - totalTime < self.ncars * 0.6:
                bestCostRep = bestCost
                valueMaxTries = self.valueMaxRep
            else:
                valueMaxTries -= 1
                if valueMaxTries == 0 or int(bestCost) == int(self.optimalValue) or time.time() - totalTime >= self.ncars * 0.6:
                    tour = creatTrucksTour(bestState, self.graph, self.capacity, self.demand, self.ncars)
                    return tour, bestCost, self.initPoint, iteration
                     
                
            
            temp = temp * 0.95
        bestCost = calculateSolDistance(self.initPoint, bestState, self.graph, self.capacity, self.demand, self.ncars)
        return bestState, bestCost, self.initPoint
    
# initPoint,capacity, graph, demand, optimalValue, ncars = getData("a")
# initState = createShuffledState(graph.keys())
# alg = simulatedAnnealing(initState,graph, demand,capacity,initPoint,optimalValue, ncars
#                          ,2000,2000000,30)
# bestState, bestCost, initPoint = alg.simulate()
# # print(res[0])
# # print(res[1])
# # print(res[2])
# prinSolution(bestState, bestCost)