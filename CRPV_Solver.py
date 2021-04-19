
from simulatedAnnealing import simulatedAnnealing
from tabuSearch import tabuSearch
from functions import *
from genetic import *
import time
import csv

def solve(algorithm, path):
    startTime = time.time()
    bestState, bestCost, initPoint = None, None, None
    initPoint,capacity, graph, demand, optimalValue, ncars, problemName = getData(path)
    initState = createShuffledState(graph.keys())
    if algorithm == 0:
        #SA
        alg = simulatedAnnealing(initState,graph, demand,capacity,initPoint,optimalValue, ncars
                         ,2000,2000000,30)
        bestState, bestCost, initPoint, iteration = alg.simulate()
        
    elif algorithm == 1:
        #tabu
        alg = tabuSearch(initState,graph, demand,capacity,initPoint,optimalValue, ncars
                         ,2000000,100, 300,30)
        bestState, bestCost, initPoint, iteration =  alg.run()
    elif algorithm == 2:
        bestState, bestCost, iteration = startGenetic(path)
        
    print("Total elapsed time: ",str(time.time() - startTime))
    prinSolution(bestState, bestCost,graph, initPoint)
    

pathForInput = input("Please enter path for the input file: ")
getAlgorithm = "To solve your problem, Please select one of the following algorithms:\n" +"Simulated Annealing = 1, Tabu Search = 2, Genetic = 3\n"
print("=======================================================================")
print("Welcome to CRVP solver")
algorithm = int(input(getAlgorithm)) - 1
solve(algorithm,pathForInput)