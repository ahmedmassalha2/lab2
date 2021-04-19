
from functions import prinSolution,calculateSolDistance,createShuffledState,getData,getTwoIndexesFromState,creatTrucksTour,calculateDistance,swap
import time
class tabuSearch:
    def __init__(self, initialState, graph, demand, capacity, initPoint,
                  optimalValue, ncars, maxIter, nNeighbors, maxTabuSize, nAttemps):
        self.state = initialState
        self.graph = graph
        self.demand = demand
        self.capacity = capacity
        self.initPoint = initPoint
        self.ncars = ncars
        self.maxIter = maxIter
        self.optimalValue = optimalValue
        self.tabuList = []
        self.nNeighbors = nNeighbors
        self.maxTabuSize = maxTabuSize
        self.nAttemps = nAttemps
        self.valueMaxRep = self.nAttemps*5
        
    def getFitness(self, state):
        return calculateSolDistance(self.initPoint, state, self.graph, self.capacity, self.demand, self.ncars)

    
    def run(self):
        startTime = time.clock()
        totalTime = time.time()
        sBest  = self.state
        bestCostRep = 0
        bestCandidate = [i for i in sBest]
        self.tabuList.append([i for i in sBest])
        valueMaxTries = self.valueMaxRep
        for iteration in range(self.maxIter):
            #create n neighbors to take the best
            neighbors = []
            for i in range(self.nNeighbors):
                i1, i2 = getTwoIndexesFromState(bestCandidate)                
                newNeighbor = swap(bestCandidate, i1, i2)
                neighbors.append(newNeighbor)
                
            bestCandidate = neighbors[0]
            for sCandidate in neighbors:
                if ( (sCandidate not in self.tabuList) and (self.getFitness(sCandidate) < self.getFitness(bestCandidate)) ):
                    bestCandidate = sCandidate
            
            if (self.getFitness(bestCandidate) < self.getFitness(sBest)):
                sBest = [i for i in bestCandidate]
            
            
            self.tabuList.append([i for i in bestCandidate])
            if len(self.tabuList) > self.maxTabuSize:
                self.tabuList = self.tabuList[50:]#self.tabuList[int(self.maxTabuSize/2):]
            
            bestCost = self.getFitness(sBest)
            print("Current best state cost: ",str(bestCost), "Clock ticks: ",str(time.clock() - startTime))
            startTime = time.clock()
            if int(bestCostRep) != int(bestCost) and int(bestCost) != int(self.optimalValue)  and time.time() - totalTime < self.ncars * 0.8:
                bestCostRep = bestCost
                valueMaxTries = self.valueMaxRep
            else:
                valueMaxTries -= 1
                if valueMaxTries == 0 or int(bestCost) == int(self.optimalValue) or time.time() - totalTime >= self.ncars * 0.8:
                    tour = creatTrucksTour(sBest, self.graph, self.capacity, self.demand, self.ncars)
                    return tour, bestCost, self.initPoint, iteration
                
                
            
        tour = creatTrucksTour(sBest, self.graph, self.capacity, self.demand, self.ncars)
        bestCost = self.getFitness(sBest)
        return tour, bestCost, self.initPoint
# initPoint,capacity, graph, demand, optimalValue, ncars = getData("a")
# initState = createShuffledState(graph.keys())
# alg = tabuSearch(initState,graph, demand,capacity,initPoint,optimalValue, ncars
#                          ,2000000,70, 200,30)
# bestState, bestCost, initPoint =  alg.run()
# prinSolution(bestState, bestCost)