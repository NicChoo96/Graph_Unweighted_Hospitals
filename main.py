import graph_preprocessing as gp
import time
import random
import json
import os
from numba import jit, cuda

# graph = {
#     1: [8, 3, 7],
#     2: [7],
#     3: [1, 5],
#     4: [5, 8],
#     5: [4,3],
#     6: [7],
#     7: [1, 2, 6],
#     8: [1, 4]
# }
# hospital = [8,6, 2, 7]
start = time.time()
graph_reader = gp.Graph_Reader()
graph = graph_reader.readGraph()
# hospital = graph_reader.readHospital()
hospital = {}
node = [5]
allPaths = {}
visitedNodePath = {}
number_hospitals = 250

for h in range(number_hospitals):
    numb = random.randint(0, len(graph) - 1)
    while (numb in hospital and numb not in graph):
        numb = random.randint(0, len(graph) - 1)
    hospital[numb] = 1
print("List of Hospital:")
print(hospital)

print("Done Reading Graphs: " + str(time.time() - start))
nodesWithoutHospital = len(graph) - number_hospitals


def write_data_json_file(output_directory, file_name, writePath):
    # Load in existing file record
    if os.path.isfile('./' + output_directory + file_name):
        with open(output_directory + file_name) as json_file:
            f_data = json.load(json_file)
            if len(f_data) != 0:
                data = f_data
    data = writePath

    with open(output_directory + file_name, 'w') as outfile:
        json.dump(data, outfile)


def backtrack(parent, startNode, end):
    path = [end]
    while path[-1] != startNode:
        currentNode = parent[path[-1]]
        visitedNodePath[path[-1]] = True
        path.append(currentNode)
        newPath = path.copy()
        newPath.reverse()
        allPaths[currentNode] = newPath
        #print(allPaths[currentNode])
        #print("Run" + str(currentNode) + " " + str(time.time() - start))
        print("Completion: " + str(round(len(allPaths) / nodesWithoutHospital * 100, 6)) + "%")

    path.reverse()
    return path


def BFS_Selected(startNode, hospitalNode):
    visitedNode = {}
    queue = []
    parent = {}
    queue.append(startNode)
    visitedNode[startNode] = True
    while queue:
        currentNode = queue.pop(0)
        if currentNode == hospitalNode:
            return backtrack(parent, startNode, currentNode)

        for i in range(len(graph[currentNode])):
            if graph[currentNode][i] not in visitedNode:
                if graph[currentNode][i] in allPaths:
                    return allPaths[graph[currentNode][i]]
                parent[graph[currentNode][i]] = currentNode
                queue.append(graph[currentNode][i])
                visitedNode[graph[currentNode][i]] = True


def BFS_Shortest(startNode):
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

# @jit
def BFS_ShortestCuda(startNode):
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


def analyseGraphEdges():
    edgeCounts = {}
    for key in graph:
        edgeCounts[key] = len(graph[key])

    write_data_json_file("output/", "edgesCount.json", edgeCounts)

topEdges = 4
highKeys = []
for key in graph:
    if len(graph[key]) >= topEdges and key not in hospital:
        highKeys.append(key)

for key in highKeys:
    if key not in allPaths:
        BFS_ShortestCuda(key)

for key in graph:
    if key not in allPaths and key not in hospital:
            BFS_ShortestCuda(key)

write_data_json_file("output/", "smallPP.json", {"hospitals": hospital, "paths": allPaths})
print("Nodes Number:" + str(len(graph)))
print("Run Finished: " + str(time.time() - start))
