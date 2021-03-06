"""" Group 14: Eivind Stangebye Larsen and Torkild Sandnes Grøstad """

from Graph import Graph
from Edge import Edge
from Node import Node
import matplotlib.pyplot as plt
import numpy as np
import operator

class Calculator: 

    """ Task 4 """
    # Q: A specific node or all nodes?
    def degreeOfNodes(self, graph):

        degreeDict = dict()
        nodes = graph.getNodes()
        
        for key, value in nodes.items():
            thisNode = value
            thisNodesEdges = thisNode.getEdgeList()
            degreeDict[thisNode] = len(thisNodesEdges)
        return degreeDict # Will look like this: {node_1: degreeOfNode, node_2: degreeOfNode, ..., node_k: degreeOfNode}

    """ Part of task 11 """
    def sumOfDegrees(self, graph):
        thisDict = self.degreeOfNodes(graph)
        sum = 0
        for value in thisDict.items():
            sum += value[1]
        return sum
    
    def getProbability(self, graph, node):
        denominator = self.sumOfDegrees(graph)
        thisNodesEdge = node.getEdgeList()
        numerator = len(thisNodesEdge)
        fraction = float(numerator/denominator)
        return fraction

    """ Task 5 """
    def plotDegreeOfNodes(self, graph):

        nodes = self.degreeOfNodes(graph)
        maxDegree = max(nodes.values())
        degreeOfNode = [i for i in range(0, maxDegree+1)]  # Degree 0-max of degreeOfNdoes
        numberOfNodes = [0*i for i in range(0, maxDegree+1)]  # Number of nodes with this degree
        
        for i in range(0, len(degreeOfNode)+1):
            for key, value in nodes.items():
                if value == i: # If this nodes degree is equal to i
                    numberOfNodes[i] += 1
                
        maxNodes = max(enumerate(numberOfNodes), key=operator.itemgetter(1))[1]
        
        plt.figure(figsize = (40, 30))
        plt.bar(degreeOfNode, numberOfNodes, color ='blue', align='edge', width = 0.4)
        plt.xlabel('Degree of node', fontsize=15)
        plt.ylabel('Number of nodes', fontsize=15)
        plt.xticks([i for i in range(0, maxDegree+1)], fontsize = 7)
        #plt.yticks([i for i in range(0, maxNodes+1)])
        plt.yticks(np.arange(0, maxNodes+1, 5))
        plt.text(maxDegree, maxNodes, "Number of nodes in total: " + str(len(graph.getNodes())), size=12, ha="right", va="center",
         bbox=dict(boxstyle="round",ec=(1., 0.5, 0.5), fc=(1., 0.8, 0.8)))
        plt.grid()
        plt.show()

    """ Task 6 """
    def extractComponentsOfNode(self, node):

        c = [] # List of connected components found
        k = set(node.getNeighbours())  # The neighbours of this node
    
        while k:
            n = k.pop()
            group = {n} 
            queue = [n]
    
            while queue:
                n = queue.pop(0) 
                neighbours = set(n.getNeighbours()) 
                neighbours.difference_update(group)  
                k.difference_update(neighbours)  
                group.update(neighbours) 
                queue.extend(neighbours)  
            c.append(group) 
        return list(c[0])
    
    """ Task 7 """
    def extractComponentsOfGraph(self, graph):

        componentsOfGraph = [] # List of connected components found
        nodesInGraph = list(graph.getNodes().values()) # The neighbours of this node

        while nodesInGraph:
            n = nodesInGraph[0]
            componentsOfNode = self.extractComponentsOfNode(n)
            componentsOfGraph.append(componentsOfNode)
            for x in componentsOfNode:
                nodesInGraph.remove(x)
        return componentsOfGraph

    """ Task 8 """ 
    def plotSizesOfConnectedComp(self, graph):

        compOfGraph = self.extractComponentsOfGraph(graph)
        labels = []
        sizes = []

        for count, i in enumerate(range(0, len(compOfGraph)), 1): # Start counting from 1
            labels.append('Subgraph #' + str(count))
            sizes.append(len(compOfGraph[i]))
        
        plt.bar(labels, sizes, color ='blue', width = 0.2)
        plt.xlabel('Subgraph', fontsize=15)
        plt.ylabel('Size of subgraph', fontsize=15)
        plt.yticks([i for i in range(0, max(sizes)+2)])
        plt.grid()
        plt.show() 
    
    """ Task 9 """
    def shortestPathBFS(self, graph, start, goal): 
        explored = []  
        queue = [[start]] 
         
        if start == goal: 
            print("End") 
            return 

        while queue: 
            path = queue.pop(0) 
            node = path[-1] 
            
            if node not in explored: 
                neighbours = graph[node] 
                
                for neighbour in neighbours: 
                    newPath = list(path) 
                    newPath.append(neighbour) 
                    queue.append(newPath) 
                    
                    if neighbour == goal: 
                        return len(newPath)-1
                explored.append(node) 
        return False

    def distanceToAllNodes(self, graph, startNode):
        startNode = startNode.getName()
        dictGraph = graph.buildGraph()
        nodesInGraph = [key[0] for key in graph.getNodes().items()]
        nodesInGraph.remove(startNode)
        distanceDict = dict()
        
        for node in nodesInGraph:
            length = self.shortestPathBFS(dictGraph, startNode, node)
            distanceDict[node] = length
        return distanceDict 
        
    """ Task 10 """
    def diameterOfGraph(self,graph):
        
        dictGraph = graph.buildGraph()
        combDict = dict()
        nodesInGraph = [key[1] for key in graph.getNodes().items()]
   
        for node in nodesInGraph:
            dictWithDistances = self.distanceToAllNodes(graph, node)
            for n in dictWithDistances:
                combDict[node.getName() + " -> "+ n] = str("Diameter: "+str(dictWithDistances[n]))
        return list(max(combDict.items(), key = operator.itemgetter(1)))
