import time
import utils
import tkinter as tk

start = time.time()
allPaths = {}
visitedNodePath = {}
nodesWithoutHospital = 0

def backtrack(parent, startNode, end):
    path = [end]
    while path[-1] != startNode:
        currentNode = parent[path[-1]]
        visitedNodePath[path[-1]] = True
        path.append(currentNode)
        newPath = path.copy()
        newPath.reverse()
        allPaths[currentNode] = newPath
        print("Completion: " + str(round(len(allPaths) / nodesWithoutHospital * 100, 6)) + "%")


def BFS(startNode, graph, hospital):
    visitedNode = {}
    queue = []
    parent = {}
    queue.append(startNode)
    visitedNode[startNode] = True
    while queue:
        currentNode = queue.pop(0)
        if currentNode in hospital:
            return backtrack(parent, startNode, currentNode)

        for i in range(len(graph[currentNode])):
            if graph[currentNode][i] not in visitedNode:
                parent[graph[currentNode][i]] = currentNode
                queue.append(graph[currentNode][i])
                visitedNode[graph[currentNode][i]] = True


def analyseGraphEdges(graph):
    edgeCounts = {}
    for key in graph:
        edgeCounts[key] = len(graph[key])

    utils.write_data_json_file("output/", "edgesCount.json", edgeCounts)

def run(graph, hospital, outputFile):
    global start
    global allPaths
    global visitedNodePath
    global nodesWithoutHospital

    start = time.time()
    allPaths = {}
    visitedNodePath = {}
    nodesWithoutHospital = len(graph) - len(hospital)

    topEdges = 4
    highKeys = []
    for key in graph:
        if len(graph[key]) >= topEdges and key not in hospital:
            highKeys.append(key)

    for key in highKeys:
        if key not in allPaths:
            BFS(key, graph, hospital)

    for key in graph:
        if key not in allPaths and key not in hospital:
            BFS(key, graph, hospital)

    utils.write_data_json_file("output/", outputFile, {"AlgoMethod":"Appending BFS", "hospitals": hospital, "paths": allPaths})
    return "File Write Completed"+"\n"+"Nodes Number:" + str(len(graph)) + "\n" + "Run Finished: " + str(time.time() - start)
