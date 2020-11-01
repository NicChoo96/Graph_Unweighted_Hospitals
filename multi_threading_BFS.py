import time
import math
import threading
import utils

allPaths = {}
visitedNodePath = {}
numOfThreads = 8
numGraphPerThread = 1
graph = {}
hospital = []
topK = 1
nodes = {}
isRecordPath = 0

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

def store_node_data(n, hospitalID, layerDist):
    if n not in hospital:
        if n in nodes:
            nodes[n].append({"h": hospitalID, "d": layerDist})
        # Add Hospital Distance to Node
        else:
            nodes[n] = []
            nodes[n].append({"h": hospitalID, "d": layerDist})


def backtrack(parent, startNode, end):
    path = [end]
    while path[-1] != startNode:
        currentNode = parent[path[-1]]
        path.append(currentNode)
    path.reverse()
    if startNode not in hospital:
        allPaths[startNode].append(path)

def backtrack_dist(parent, startNode, end):
    path = [end]
    while path[-1] != startNode:
        currentNode = parent[path[-1]]
        path.append(currentNode)

    if startNode not in nodes:
        nodes[startNode] = []
    nodes[startNode].append({"h": end, "dist": len(path)})

def BFS_thread_process(startNode):
    if startNode in hospital:
        allPaths[startNode] = ["Hospital"]
    else:
        allPaths[startNode] = []
    visitedNode = {}
    queue = []
    parent = {}
    queue.append(startNode)
    visitedNode[startNode] = True
    hospitalCount = 0
    while queue:
        currentNode = queue.pop(0)
        if currentNode in hospital and startNode not in hospital:
            if isRecordPath:
                backtrack(parent, startNode, currentNode)
            else:
                backtrack_dist(parent, startNode, currentNode)
            hospitalCount += 1
            if hospitalCount == topK:
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

def run(graphData, hospitalData, k, outputFile, isRecord):
    global graph
    global hospital
    global topK
    global allPaths
    global visitedNodePath
    global numOfThreads
    global numGraphPerThread
    global isRecordPath
    global nodes

    nodes = {}
    isRecordPath = isRecord
    allPaths = {}
    visitedNodePath = {}
    numOfThreads = 8
    numGraphPerThread = 1
    graph = graphData
    hospital = hospitalData
    topK = k
    start = time.time()
    nodesWithoutHospital = len(graph) - len(hospital)
    numGraphPerThread = nodesWithoutHospital/numOfThreads
    multiThreading_BFS()
    print("Top " + str(topK) + " hospitals")
    if isRecordPath:
        utils.write_data_json_file("output/", outputFile, {"algoMethod": "Multi_Thread BFS", "hospitals": hospital, "paths": allPaths})
    else:
        utils.write_data_json_file("output/", outputFile, {"algoMethod": "Multi_Thread BFS", "hospitals": hospital, "nodes": nodes})
    return "Nodes Number:" + str(len(graph)) + "\n" + "Number of Threads:  " + str(numOfThreads) + "\n" + "Run Finished: " + str(time.time() - start)