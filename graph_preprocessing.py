import os
import randomgraphout
import random
import sys

# takes in a textfile name as input, and returns a dictionary of node keys as output
# each node key has a value: the value is a list of adjacent nodes i.e. the nodes that can be reached from the node key

def readGraph(graphInfo):
    graphFile = open(graphInfo, "rb")
    content = graphFile.read()

    content_list = content.decode().split('\n')
    graphFile.close()

    graph = {}

    content_list = content_list[:len(content_list) - 1]

    for line in content_list:
        if '#' in line:
            continue

        linelist = line.split('\t')
        try:
            if int(linelist[0]) in graph:
                if int(linelist[1]) not in graph[int(linelist[0])]:
                    graph[int(linelist[0])].append(int(linelist[1]))
            else:
                graph[int(linelist[0])] = [int(linelist[1])]

            if int(linelist[1]) in graph:
                if int(linelist[0]) not in graph[int(linelist[1])]:
                    graph[int(linelist[1])].append(int(linelist[0]))
            else:
                graph[int(linelist[1])] = [int(linelist[0])]
        except:
            return False

    return graph

# takes in a textfile name as input, and returns a list of hospital nodes as output
# textfile must follow the format stated (from project2 pdf):
# line 1:# numofhospitals   (note the hex and space after hex then your numofhospitals)
# line 2:node#   (repeat line 2 for each hospital node)
def readHospital(hospitalInfo):
    hospitalFile = open(hospitalInfo, "rb")
    content = hospitalFile.read()
    content_list = content.decode().split('\n')
    hospitalFile.close()
    try:
        k_hospital = int(content_list[0][2:])
    except:
        return False
    hospital = []
    for line in range(k_hospital):
        hospital.append(int(content_list[line + 1]))

    return hospital


# creates an unweighted, undirected, unsigned simple graph that allows self loops with 200 vertices, and each vertice can have 0-40 edges
# exports a tsv file to current working directory (address printed)
# returns a dictionary data structure containing the random graph data
def generateRandomGraph():
    randomgraphout.run()
    randomGraph = readGraph(os.getcwd() + "\\randomgraph.tsv")
    return randomGraph


# taking in random graph with default 200 vertices, create a hospital file with default 30 hospitals (can be changed using numHospitals)
# exports a txt file with name "hospitalnodes" to working directory
# CAUTION: WILL OVERWRITE FILE WITH SAME NAME IF EXISTS IN DIRECTORY
# returns a list data structure containing the hospital data
def generateRandomHospital(randomGraph, numHospitals=20):
    randomNodes = []
    for node in randomGraph:
        randomNodes.append(node)
    random.shuffle(randomNodes)
    randomNodes = randomNodes[:numHospitals]
    randomNodes.sort()

    hospitalNodes = open("hospitalnodes.txt", "w")
    hospitalNodes.write("# ")
    hospitalNodes.write(str(numHospitals))
    for hospital in randomNodes:
        hospitalNodes.write('\n' + str(hospital))
    hospitalNodes.close()

    return randomNodes


randomGraph = generateRandomGraph()
randomNodes = generateRandomHospital(randomGraph)
print(len(randomNodes))
print(randomNodes)