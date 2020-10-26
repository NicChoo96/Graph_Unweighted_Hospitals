class Graph_Reader:
    def __init__(self):
        self.graphFile = "roadNet-CA.txt"
        #self.graphFile = "as20000102.txt"
        self.hospitalFile = "hospitalnodes.txt"


    #takes in a textfile name as input, and returns a dictionary of node keys as output
    #each node key has a value: the value is a list of adjacent nodes i.e. the nodes that can be reached from the node key
    def readGraph(self):
        graphFile = open(self.graphFile,"rb")
        content = graphFile.read()

        content_list = content.decode().split('\n')
        graphFile.close()

        graph = {}

        content_list = content_list[:len(content_list)-1]

        for line in content_list:
            if '#' in line:
                continue

            linelist = line.split('\t')

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

        return graph

    #takes in a textfile name as input, and returns a list of hospital nodes as output
    #textfile must follow the format stated (from project2 pdf):
    # line 1:# numofhospitals   (note the hex and space after hex then your numofhospitals)
    # line 2:node#   (repeat line 2 for each hospital node)
    def readHospital(self):
        hospitalFile = open(self.hospitalFile,"rb")
        content = hospitalFile.read()
        content_list = content.decode().split('\n')
        hospitalFile.close()
        k_hospital = int(content_list[0][2:])
        hospital = []
        for line in range(k_hospital):
            hospital.append(int(content_list[line+1]))

        return hospital
