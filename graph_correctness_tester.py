import json
import os

def read_data_json_file(output_directory, file_name):
    # Load in existing file record
    if os.path.isfile('./' + output_directory + file_name):
        with open(output_directory + file_name) as json_file:
            f_data = json.load(json_file)
            return f_data

graph_data = read_data_json_file("output/", "smallPP.json")


def test_end_node_correctness():
    correctCount = 0

    for path in graph_data["paths"]:
        if str(graph_data["paths"][path][-1]) in graph_data["hospitals"]:
            correctCount += 1

    print("Graph Correctness for end node: " + str(correctCount/len(graph_data["paths"])*100) + "%")

def test_graph_completion():
    totalNodes = 0
    for path in graph_data["paths"]:
        totalNodes += 1
    print("Total Nodes path found: " + str(totalNodes))
    print("Total Nodes in graph: 1965206")
    print("Completion Percentage: " + str(totalNodes/1965206*100) + "%")

test_graph_completion()