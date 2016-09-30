# -*- coding: utf-8 -*-
__author__ = 'Márcio Vinícius Dias'

import snap
import os
import random
import gncd
import networkx as nx
import gncdNX

class Main():

    Graph = snap.PUNGraph.New()
    GNX = nx.Graph()

    def buildG(self, file_name):

        input_f = file_name
        data_set = open(input_f)
        lines = data_set.readlines()

        for line in lines:
            col = line.strip().split(';')

            if col[0] == "Vertices":
                self.is_vertice = True
                continue

            if col[0] == "Edges":
                self.is_vertice = False
                continue

            if self.is_vertice:
                self.Graph.AddNode(int(col[0]))
            else:
                self.Graph.AddEdge(int(col[0]), int(col[1]))

    def makeVectorToNni(self, arryMni, nodesArray):
        dictMni = {}

        for commuLabel in arryMni:
            vetNodesInCommu = arryMni[commuLabel]

            for node in vetNodesInCommu:
                index = nodesArray.index(node)
                dictMni[index] = commuLabel

        vetTemp = []
        for item in dictMni:
            vetTemp.append(dictMni[item])

        return vetTemp

    def temp(self, originalGraph, commuNodes, dictLabel, numberOfGraph, numberOfCommu ):

        self.Graph = snap.PUNGraph.New()
        fileName = "dataset/{}".format(originalGraph)
        self.buildG(fileName)

        H = snap.TIntStrH()

        directory = "output/resultados/temp/grafo{}".format( numberOfGraph)
        if not os.path.exists(directory):
            os.makedirs(directory)

        listOfNodesFromInductedGraph = commuNodes
        listOfNodesToRemoveFromThisOriginalGraph = snap.TIntV()

        for nodeFromOriginalGraph in self.Graph.Nodes():

            idNodeFromOriginalGraph = nodeFromOriginalGraph.GetId()

            if not idNodeFromOriginalGraph in listOfNodesFromInductedGraph:
                listOfNodesToRemoveFromThisOriginalGraph.Add(idNodeFromOriginalGraph)

        snap.DelNodes(self.Graph, listOfNodesToRemoveFromThisOriginalGraph)

        GraphDet = snap.PUNGraph.New()

        for node in self.Graph.Nodes():
            nodeNE = node.GetId()
            GraphDet.AddNode(nodeNE)

        for edge in self.Graph.Edges():
            newEdge = edge.GetId()
            GraphDet.AddEdge(newEdge[0], newEdge[1])

        CmtyV = snap.TCnComV()
        modularity = snap.CommunityGirvanNewman(self.Graph, CmtyV)
        # print len(CmtyV)

        cont = 0
        arryToMni = {}
        for Cmty in CmtyV:
            r = lambda: random.randint(0, 255)
            community_color = "#%02X%02X%02X" % (r(), r(), r())

            vetNodes = []
            for NI in Cmty:
                H.AddDat(NI, '{}",style=filled, fillcolor="{}'.format(dictLabel[NI], community_color))
                vetNodes.append(NI)

            arryToMni[cont] = vetNodes
            cont += 1

        # this is the case when there are no edges
        if len(arryToMni) == 0:
            numberOfNodes = GraphDet.Nodes()
            cont = 0
            for nodeNE in numberOfNodes:
                nodeNE = nodeNE.GetId()
                arryToMni[cont] = [nodeNE]
                cont += 1

        if arryToMni.__len__() == 1:
            snap.DrawGViz(GraphDet, snap.gvlSfdp, "{}/graph{}{}.png".format(directory, numberOfGraph, numberOfCommu),
                          "Grafo{}, comunidade {}".format(numberOfGraph, numberOfCommu))
        else:
            snap.DrawGViz(GraphDet, snap.gvlSfdp, "{}/graph{}{}.png".format(directory, numberOfGraph, numberOfCommu), "Grafo{}, comunidade {}".format(numberOfGraph, numberOfCommu), H)

        result = {}
        result[0] = 0
        result[1] = listOfNodesFromInductedGraph
        result[2] = self.makeVectorToNni(arryToMni, listOfNodesFromInductedGraph)

        density = gncd.Main().avgDensity(GraphDet, arryToMni)

        result[3] = density

        return result

    def run(self, result, originalGraph, nameOfNetwork, numberOfGraph, dictLabel ):

        self.Graph = snap.PUNGraph.New()
        fileName = "dataset/{}".format(originalGraph)
        self.buildG(fileName)
        self.GNX = nx.Graph()


        H = snap.TIntStrH()

        directory = "output/resultados/{}/{}grafo{}".format(nameOfNetwork, nameOfNetwork, numberOfGraph)
        if not os.path.exists(directory):
            os.makedirs(directory)

        snap.DrawGViz(self.Graph, snap.gvlSfdp, "{}/graphOriginal{}.png".format(directory, nameOfNetwork), "Grafo Original {}".format(nameOfNetwork), dictLabel)

        listOfNodesFromInductedGraph = result[1]
        listOfNodesToRemoveFromThisOriginalGraph = snap.TIntV()

        for nodeFromOriginalGraph in self.Graph.Nodes():

            idNodeFromOriginalGraph = nodeFromOriginalGraph.GetId()

            if not idNodeFromOriginalGraph in listOfNodesFromInductedGraph:
                listOfNodesToRemoveFromThisOriginalGraph.Add(idNodeFromOriginalGraph)

        snap.DelNodes(self.Graph, listOfNodesToRemoveFromThisOriginalGraph)

        GraphDet = snap.PUNGraph.New()

        for node in self.Graph.Nodes():
            nodeNE = node.GetId()
            GraphDet.AddNode(nodeNE)

        for edge in self.Graph.Edges():
            newEdge = edge.GetId()
            GraphDet.AddEdge(newEdge[0], newEdge[1])
            self.GNX.add_edge(newEdge[0], newEdge[1], weight=1.0)


        #snap.DrawGViz(self.Graph, snap.gvlSfdp, "{}/graphOriginal{}{}DetCon.png".format(directory, nameOfNetwork, numberOfGraph),
         #             "Grafo {} apenas com nos do DetCom".format(nameOfNetwork), dictLabel)

        #CmtyV = snap.TCnComV()
        #modularity = snap.CommunityGirvanNewman(self.Graph, CmtyV)
        resultFromNX = gncdNX.main(self.GNX)
        modularity = resultFromNX[0]
        CmtyV = resultFromNX[1]

        if modularity == -1:
            modularity = 0

        #print len(CmtyV)

        cont = 0
        arryToMni = {}
        for Cmty in CmtyV:
            r = lambda: random.randint(0, 255)
            community_color = "#%02X%02X%02X" % (r(), r(), r())

            vetNodes = []
            for NI in Cmty:
                H.AddDat(NI, '{}",style=filled, fillcolor="{}'.format(dictLabel[NI], community_color))
                vetNodes.append(NI)

            arryToMni[cont] = vetNodes
            cont += 1

        #this is the case when there are no edges
        if len(arryToMni) == 0:
            numberOfNodes = GraphDet.Nodes()
            cont = 0
            for nodeNE in numberOfNodes:
                nodeNE = nodeNE.GetId()
                arryToMni[cont] = [nodeNE]
                cont+=1

        snap.DrawGViz(GraphDet, snap.gvlSfdp,
                      "{}/graph{}CommDetects{}.png".format(directory, numberOfGraph, nameOfNetwork),
                      "Grafo{} {} com as comunidades detectadas por GirvanNewman".format(numberOfGraph, nameOfNetwork),
                       H)

        result = {}
        result[0] = modularity
        result[1] = listOfNodesFromInductedGraph
        result[2] = self.makeVectorToNni(arryToMni, listOfNodesFromInductedGraph )

        density = gncd.Main().avgDensity(GraphDet, arryToMni)

        result[3] = density



        return result

if __name__ == "__main__":
    print(__doc__)
    Main().run( "", "dataset/grafo_metapath_conflitosNetwork.txt", "conflitosNetwork", 1)
