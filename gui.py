import json
import tkinter as tk
import graph_preprocessing as processing
from tkinter.filedialog import askopenfilename
import os
import re
import appending_BFS
import multi_threading_BFS

def openFile(varSetter, dataSetter):
    tk.Tk().withdraw()
    filename = askopenfilename()
    if filename == "" or not re.search(".txt$", filename):
        return 0
    else:
        varSetter.set(os.path.basename(filename))
        dataSetter.set(filename)

def printLogs(logs_ui, root, text):
    logs_ui.config(state=tk.NORMAL)
    if isinstance(text, str):
        logs_ui.insert(tk.END, str(text) + "\n\n")
    else:
        for i in text:
            logs_ui.insert(tk.END, str(i) + "\n")
        logs_ui.insert(tk.END, "\n")
    logs_ui.config(state=tk.DISABLED)
    logs_ui.yview_moveto(1)
    root.update()

def main_gui():
    root = tk.Tk()
    root.title("Algorithm Program")

    ##############################################################################################
    # Frames
    fileFrame = tk.Frame(root)
    radioFrame = tk.Frame(fileFrame)
    logsFrame = tk.Frame(root)

    int_var = tk.IntVar()
    algoSelector_var = tk.IntVar()
    recordPath_var = tk.IntVar()
    graphText = tk.StringVar()
    hospitalText = tk.StringVar()
    graphData = tk.StringVar()
    hospitalData = tk.StringVar()
    savefilename = tk.StringVar()

    fileFrame.grid(row=0,column=0)
    radioFrame.grid(row=4, column=1)
    logsFrame.grid(row=0,column=3)

    # log file
    scroll = tk.Scrollbar(root)
    text = tk.Text(root, state=tk.DISABLED, width=40)
    text.grid(row=0, column=5, padx=10, pady=20)
    scroll.grid(row=0, column=10, sticky='ns')
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)

    # Logs Frame GUI
    logsLabel = tk.Label(logsFrame, text="Logs")

    # File Frame GUI
    graphText.set("No file")
    tk.Label(fileFrame, text = "Graph file").grid(row=0)
    tk.Label(fileFrame, text = "Graph file", textvariable=graphText).grid(row=0, column=1)
    graphFileOpenButton = tk.Button(fileFrame, text="Import Graph File",
                               command=lambda: openFile(graphText, graphData))
    graphFileOpenButton.grid(row=0, column=2)

    hospitalText.set("No file")
    tk.Label(fileFrame, text="Hospital file").grid(row=1)
    tk.Label(fileFrame, textvariable=hospitalText).grid(row=1, column=1)
    hospitalFileOpenButton = tk.Button(fileFrame, text="Import Hospital File",
                                    command=lambda: openFile(hospitalText, hospitalData))
    hospitalFileOpenButton.grid(row=1, column=2)

    numOfNodes = tk.IntVar()
    numOfNodes.set(200)
    tk.Label(fileFrame, text="Number of Nodes for Random").grid(row=5)
    numbOfHospitalEntry = tk.Entry(fileFrame, textvariable=numOfNodes).grid(row=5, column=1)

    numOfHospital = tk.IntVar()
    numOfHospital.set(20)
    tk.Label(fileFrame, text="Number of Hospitals for Random").grid(row=6)
    numbOfHospitalEntry = tk.Entry(fileFrame, textvariable=numOfHospital).grid(row=6, column=1)

    k = tk.IntVar()
    k.set(1)
    tk.Label(fileFrame, text = "Top K Hospitals").grid(row=7)
    kHospitalEntry = tk.Entry(fileFrame, textvariable = k).grid(row=7, column=1)

    tk.Label(fileFrame, text = "Save file name").grid(row=8)
    saveEntry = tk.Entry(fileFrame, textvariable = savefilename).grid(row=8, column=1)
    tk.Label(fileFrame, text = ".json").grid(row=8,column=2)

    traverseButton = tk.Button(fileFrame, text = "Traverse", command=lambda:
    main_algo(algoSelector_var.get(),int_var.get(),graphData.get(),hospitalData.get(),numOfNodes.get(),numOfHospital.get(),k.get(),savefilename.get(), root, text, recordPath_var.get()))

    traverseButton.grid(row=9,column=1)

    # Radio Frame GUI
    int_var.set(1)
    tk.Label(radioFrame, text = "Random Generation?").grid(row=2, column=0)
    yesSelect = tk.Radiobutton(radioFrame, text = "Yes", variable = int_var, value = 1).grid(row=2, column=1)
    noSelect = tk.Radiobutton(radioFrame, text = "No", variable = int_var, value = 0).grid(row=2, column=2)

    recordPath_var.set(1)
    tk.Label(radioFrame, text="Record (For Multi_threading BFS)").grid(row=3, column=0)
    pathSelector = tk.Radiobutton(radioFrame, text="Path", variable=recordPath_var, value=1).grid(row=3, column=1)
    distSelector = tk.Radiobutton(radioFrame, text="Dist", variable=recordPath_var, value=0).grid(row=3, column=2)

    # Radio Frame GUI
    algoSelector_var.set(1)
    tk.Label(radioFrame, text="Algorithm Selector").grid(row=4, column=0)
    algoSelectAppending = tk.Radiobutton(radioFrame, text="Appending BFS", variable=algoSelector_var, value=1).grid(row=4, column=1)
    algoSelectMultithread = tk.Radiobutton(radioFrame, text="Multi Threading BFS", variable=algoSelector_var, value=0).grid(row=4, column=2)

    logsLabel.pack()
    ##############################################################################################
    root.mainloop()

def main_algo(algoSelector, isRandom, graphFile, hospitalFile, num_nodes, num_hospitals, k, saveFile, root, logs_ui, isRecordPath):
    #this is how the main algo shd run (pseudocode)\
    if saveFile == "":
        printLogs(logs_ui, root, "Please enter a save file name")
        return
    if k > num_hospitals:
        printLogs(logs_ui, root, "Error 69: Top K is more than number of hospitals in graph!")
        return
    if k == 0:
        printLogs(logs_ui, root, "Error 69420: Top K cannot be 0")
        return
    #num of hosp set as 20
    if isRandom:
        if num_hospitals == 0:
            printLogs(logs_ui, root, "Error 000: Enter a number of hospitals more than 0")
            return
        if num_nodes == 0:
            printLogs(logs_ui, root, "Error 000: Enter a number of nodes more than 0")
            return
        print("random ran")
        graph = processing.generateRandomGraph(numVertices=num_nodes)
        print("graph done")
        hosp = processing.generateRandomHospital(graph,num_hospitals)
        if len(hosp) > len(graph):
            printLogs(logs_ui, root, "Error 9001: You have more hospitals than graph nodes")
            return
        printLogs(logs_ui, root, "Running Algorithm...\nNumber of Nodes: " + str(num_nodes) + "\nNumber of Hospitals: " + str(num_hospitals))
        print("hosp done")
    #   generate random graph for both graph and hospital
    #   read random graph into data structure
        #insert BFS algo here
        printLogs(logs_ui, root, "Running Algorithm From Randomized Graph")
        if algoSelector:
            if k > 1:
                printLogs(logs_ui, root, "Error sAd: This algorithm cannot run more than top 1 hospitals")
                return
            printLogs(logs_ui, root,"Running Appending BFS...")
            printLogs(logs_ui, root, appending_BFS.run(graph, hosp, saveFile + ".json"))
            printLogs(logs_ui, root, "File saved to " + saveFile+".json")
        else:
            printLogs(logs_ui, root,"Running Multi Threading BFS...")
            printLogs(logs_ui, root, multi_threading_BFS.run(graph, hosp, k, saveFile+".json", isRecordPath))
            printLogs(logs_ui, root, "File saved to " + saveFile+".json")
    else:
    #   check if graphFile and hospitalFile input is valid
    #   read graphs into data structure
        if graphFile == "" or hospitalFile == "":
            printLogs(logs_ui, root, "Error 420: Either there is no graph file or hospital file imported!")
            return
        printLogs(logs_ui, root, "Running Algorithm From Imported Files...")
        graph = processing.readGraph(graphFile)
        if not graph:
            printLogs(logs_ui, root, "File Error: Wong Graph file input")
            return
        print("graph done")
        hosp = processing.readHospital(hospitalFile)
        if not hosp:
            printLogs(logs_ui, root, "File Error: Wong Hospital file input")
            return
        if len(hosp) > len(graph):
            printLogs(logs_ui, root, "Error 9001: You have more hospitals than graph nodes")
            return
        # print(hosp)
        printLogs(logs_ui, root, "Running Files from " + graphFile + " and " + hospitalFile)
        #insert BFS here
        if algoSelector:
            if k > 1:
                printLogs(logs_ui, root, "Error sAd: This algorithm cannot run more than top 1 hospitals")
                return
            printLogs(logs_ui, root,"Running Appending BFS...")
            printLogs(logs_ui, root, appending_BFS.run(graph, hosp, saveFile + ".json"))
            printLogs(logs_ui, root, "File saved to " + saveFile+".json")
        else:
            printLogs(logs_ui, root,"Running Multi Threading BFS...")
            printLogs(logs_ui, root, multi_threading_BFS.run(graph, hosp, k, saveFile+".json", isRecordPath))
            printLogs(logs_ui, root, "File saved to " + saveFile+".json")
    #check if k and saveFile input is valid
    #call the algorithm function using all the parameters (graph, hospital, k, savefile) - note that graph, hospital refers to the data structures read from the textfiles


main_gui()
