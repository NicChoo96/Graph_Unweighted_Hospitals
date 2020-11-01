import graph_preprocessing as gp
import time
import random
import utils

# graph = gp.readGraph("as20000102.txt")
graph = gp.readGraph("roadNet-CA.txt")
# graph = gp.readGraph("test.txt")
print("Done Reading Graph")
start = time.time()
hospital = {}
number_hospitals = 10
nodes = {}
topK = 2
hospital_blocks = []
totalDistanceCount = 0

class HospitalBlock:
    def __init__(self, hospitalNodeID):
        self.hospitalNodeID = hospitalNodeID
        self.queue = [hospitalNodeID]
        self.visitedNode = {hospitalNodeID:True}
        self.parent = {}
        self.layer = 0
        self.isCompleted = False

    def store_data(self, queue, visitedNode, parent):
        self.visitedNode = visitedNode
        self.queue = queue
        self.parent = parent

    def addLayer(self):
        self.layer += 1
    def completed(self):
        self.isCompleted = True

def load_hospital_data():
    for h in range(number_hospitals):
        numb = random.randint(0, len(graph) - 1)
        while (numb in hospital and numb not in graph):
            numb = random.randint(0, len(graph) - 1)
        hospital[numb] = 1
        hospital_blocks.append(HospitalBlock(numb))
    print("List of Hospital:")
    print(hospital)

def backtrack(parent, startNode, end):
    path = [end]
    while path[-1] != startNode:
        currentNode = parent[path[-1]]
        path.append(currentNode)

    return path

def store_node_data(n, hospitalID, layerDist):
    global totalDistanceCount
    if n not in hospital:
        if n in nodes:
            if len(nodes[n]) < topK:
                # if not nodes[graph[layerNodes][i]][-1]["d"] == hospital_node_block.layer: visitedNode[graph[layerNodes][i]] = True
                nodes[n].append({"h": hospitalID, "d": layerDist})
                totalDistanceCount += 1
        # Add Hospital Distance to Node
        else:
            nodes[n] = []
            nodes[n].append({"h": hospitalID, "d": layerDist})
            totalDistanceCount += 1

hospitalCount = 0

def BFS(hospital_node_block):
    global hospitalCount
    currentLayer = []

    hospital_node_block.addLayer()

    while hospital_node_block.queue:
        currentLayer.append(hospital_node_block.queue.pop(0))
    if len(currentLayer) == 0:
        hospital_node_block.completed()
        hospitalCount += 1

    for layerNodes in currentLayer:
        # Issue one
        if layerNodes not in graph:
            print(layerNodes)
            print(hospital_node_block.layer)
        store_node_data(layerNodes, hospital_node_block.hospitalNodeID, hospital_node_block.layer-1)
        for i in range(len(graph[layerNodes])):
            if graph[layerNodes][i] not in hospital_node_block.visitedNode:
                hospital_node_block.parent[graph[layerNodes][i]] = layerNodes
                hospital_node_block.queue.append(graph[layerNodes][i])
                hospital_node_block.visitedNode[graph[layerNodes][i]] = True



load_hospital_data()
layer = 0
# hospital[0] = 1
# number_hospitals = 1
# hospital_blocks.append(HospitalBlock(0))
print(hospital_blocks)
while hospitalCount < number_hospitals:
    for h in hospital_blocks:
        if not h.isCompleted:
            BFS(h)
    layer += 1
    print("Layer " + str(layer) + ":")
    print(hospitalCount)
print(totalDistanceCount)
utils.write_data_json_file("output/", "pulseBFSOutput.json", nodes)


print("Number of Nodes:" + str(len(graph)))
print("BFS Completed => Time Completed in:")
print(time.time() - start)