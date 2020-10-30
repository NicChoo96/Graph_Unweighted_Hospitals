import graph_preprocessing as gp
import time
import random
import json
import math
import os
import threading

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
allPaths = {}
visitedNodePath = {}
number_hospitals = 344
numOfThreads = 8
top_k_hospital = 3
numGraphPerThread = 1

class BFS_threads(threading.Thread):
    def __init__(self, threadID, name, nodeList):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.nodeList = nodeList
    def run(self):
        for nodes in self.nodeList:
            BFS_thread_process(nodes)
            # print("T"+str(self.threadID) + ":" + str(round(len(allPaths)/numOfThreads/numGraphPerThread*100, 6)) + "%")
            print("T" + str(self.threadID) + ":" + str(len(allPaths)))


def load_graph_data():
    global numGraphPerThread

    for h in range(number_hospitals):
        numb = random.randint(0, len(graph) - 1)
        while (numb in hospital and numb not in graph):
            numb = random.randint(0, len(graph) - 1)
        hospital[numb] = 1
    print("List of Hospital:")
    print(hospital)

    nodesWithoutHospital = len(graph) - number_hospitals

    numGraphPerThread = nodesWithoutHospital/numOfThreads

    print("Done Reading Graphs: " + str(time.time() - start))

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
        path.append(currentNode)
    path.reverse()
    allPaths[startNode].append(path)

def BFS_thread_process(startNode):
    allPaths[startNode] = []
    visitedNode = {}
    queue = []
    parent = {}
    queue.append(startNode)
    visitedNode[startNode] = True
    hospitalCount = 0
    while queue:
        currentNode = queue.pop(0)
        if currentNode in hospital:
            backtrack(parent, startNode, currentNode)
            hospitalCount += 1
            if hospitalCount == top_k_hospital:
                return

        for i in range(len(graph[currentNode])):
            if graph[currentNode][i] not in visitedNode:
                parent[graph[currentNode][i]] = currentNode
                queue.append(graph[currentNode][i])
                visitedNode[graph[currentNode][i]] = True

def multiThreading_BFS():
    threads = []
    threadsNodes = []
    nodesPerThread = math.ceil(len(graph)/numOfThreads)
    nodesArr = []
    for key in graph:
        nodesArr.append(key)
        if len(nodesArr) == nodesPerThread:
            threadsNodes.append(nodesArr.copy())
            nodesArr = []
    threadsNodes.append(nodesArr.copy())

    for i in range(len(threadsNodes)):
        threads.append(BFS_threads(i+1, "BFS_T" + str(i+1), threadsNodes[i]))

    for i in range(len(threadsNodes)):
        threads[i].start()

    for i in range(len(threadsNodes)):
        threads[i].join()

load_graph_data()
multiThreading_BFS()
print(len(allPaths))

write_data_json_file("output/", "Multi_Thread_NormalBFS.json", {"hospitals": hospital, "paths": allPaths})
print("Nodes Number:" + str(len(graph)))
print("Top " + str(top_k_hospital) + " hospitals")
print("Number of Threads:  " + str(numOfThreads))
print("Run Finished: " + str(time.time() - start))