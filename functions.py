import math
from random import shuffle, randint
import numpy as np
import re
import matplotlib.pyplot as plt

def getData(fileName):
    
    f = open(fileName, "r")
    content = f.read()
    problemName = content.split("COMMENT")[0].split(" : ")[1].replace('\n','')
    cords = content.split("NODE_COORD_SECTION")[1].split("\n")
    i=1
    graph = {}
    for c in cords:
        if c!="" and c!="DEMAND_SECTION":
            c = c.split(" ")
            
            graph[i] = (int(c[1]), int(c[2]))
            i += 1
        if  c=="DEMAND_SECTION":
            break
            
    optimalValue = re.search("Optimal value: (\d+)", content, re.MULTILINE)
    if(optimalValue != None):
        optimalValue = optimalValue.group(1)
    else:
        optimalValue = re.search("Best value: (\d+)", content, re.MULTILINE)
        if(optimalValue != None):
            optimalValue = optimalValue.group(1)
    capacity = re.search("^CAPACITY : (\d+)$", content, re.MULTILINE).group(1)

    demand = re.findall(r"^(\d+) (\d+)$", content, re.MULTILINE)
    demand = {int(a):int(b) for a,b in demand}
    capacity = int(capacity)
    optimalValue = int(optimalValue)
    ncars = int(re.search("^DIMENSION : (\d+)$", content, re.MULTILINE).group(1))
    initPoint = graph[list(graph.keys())[0]]
###################################################
    #first point is the ware house, so remove it
    newGraph = dict()
    newDemand = dict()
    for key in graph.keys():
        if key != 1:
            newGraph[key-1] = graph[key]
    for key in demand.keys():
        if key != 1:
            newDemand[key-1] = demand[key]
    graph = newGraph
    demand = newDemand
###################################################    
    return initPoint,capacity, graph, demand, optimalValue, ncars, problemName




def getDistance(p1,p2):
    return np.linalg.norm(np.array(p2)-np.array(p1))
    return  math.sqrt((p2[0]- p1[0])**2 + (p2[1] - p1[1])**2)


def createShuffledState(state):
    newState = list([int(i) for i in state])
    shuffle(newState)
    return newState
    
def generateFirstState(graph,initPoint,demand):
    firstState = list([int(i) for i in graph.keys()])
    firstState.sort(key= lambda x: getDistance(graph[x],initPoint))  # sort population array by fitness
    firstState.reverse()
    return firstState
#create from the state a tours for each truk
def creatTrucksTour(state, graph, capacity, demand, nTrucks):
    trucks = 0
    currCap = capacity
    allTours = [[]]
    for city in state:
        cityDemand = demand[city]   
        if currCap >= cityDemand:
            currCap -= cityDemand
            allTours[len(allTours)-1].append(city)
        else:
            currCap = capacity - cityDemand
            allTours.append([city])
            trucks += 1
            
            if trucks > nTrucks:
                break
    return allTours


def calculateDistance(graph, tours,initPoint):
    #warehouse is the startiong initPoint
    distances = 0
    for tour in tours:
        prev = initPoint
        for city in tour:
            cityCord = graph[city]
            distances += getDistance(prev, cityCord)
            prev = cityCord
        #calculate back to ware house
        distances += getDistance(prev,initPoint)
    return distances

def getTwoIndexesFromState(state):
    i1,i2 = -1, -1
    while True:
        i1 = randint(0, len(state) - 1)
        i2 = randint(0, len(state) - 1)
        if i1 != i2:
            return i1, i2
def swap(state, i1, i2):
    copyState = [i for i in state]
    copyState[i1], copyState[i2] = copyState[i2], copyState[i1]
    return copyState
    
def calculateSolDistance(initPoint, state, graph, capacity, demand, nTrucks):
     tours = creatTrucksTour(state, graph, capacity, demand, nTrucks)
     return calculateDistance(graph, tours,initPoint)
 
def prinSolution(path, cost,graph, initPoint,startPoint = 0):
    print("=======================================================================")
    print("Solution cost: ",str(cost))
    for p in path:
        tour = str(startPoint)
        for i in p:
            tour += ' '+str(i)
        tour += ' '+str(startPoint)
        print(tour)
    print("=======================================================================")
    drawSol(path,graph, initPoint)

def drawSol(tours, graph, initPoint):
    colors = ["grey","red","blue","green","orange","yellow"]
    c = 0
    for tour in tours:
        first = initPoint
        for i in range(len(tour)):
            second = graph[tour[i]]
            x = [first[0],second[0]]
            y = [first[1],second[1]]
            plt.plot(x, y, marker='v',color=colors[c])
            first = second
        x = [first[0],initPoint[0]]
        y = [first[1],initPoint[1]]
        plt.plot(x, y, marker='v', color=colors[c])
        c = (c+1)%len(colors)
    
    plt.show()
