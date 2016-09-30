# -*- coding: utf-8 -*-
__author__ = 'Márcio Vinícius Dias'

import snap
import random
import os
from collections import Counter
import networkx as nx
import gncdNX

class Main():

    Graph = snap.PUNGraph.New()
    GraphDet = snap.PUNGraph.New()
    GNX = nx.Graph()
    nodesArray = []
    dictWeightEdges = {}

    def __init__(self):
        pass


    def buildG(self, listGraph):

        edgesWithWeight = Counter(listGraph)

        for line in edgesWithWeight:

            weightFromLine = edgesWithWeight[line]

            col = line.split(',')

            nodeId1 = int( col[0] )
            nodeId2 = int( col[1] )


            if not self.Graph.IsNode(nodeId1):
                self.Graph.AddNode( nodeId1 )
                self.GraphDet.AddNode( nodeId1 )
                self.nodesArray.append(nodeId1)


            if not self.Graph.IsNode(nodeId2):
                self.Graph.AddNode( nodeId2 )
                self.GraphDet.AddNode( nodeId2 )
                self.nodesArray.append(nodeId2)

            self.GNX.add_edge(nodeId1, nodeId2,weight=float(weightFromLine))
            self.Graph.AddEdge( nodeId1, nodeId2 )
            self.GraphDet.AddEdge( nodeId1, nodeId2 )

        return self.GraphDet

    def makeVectorToNmi(self, arryMni, listGraph):
        dictMni = {}

        for commuLabel in arryMni:
            vetNodesInCommu = arryMni[commuLabel]

            for node in vetNodesInCommu:
                index = listGraph.index(node)
                dictMni[ index ] = commuLabel

        vetTemp = []
        for item in dictMni:
            vetTemp.append(dictMni[item])

        return vetTemp

    #because the !@@#$@ copy.copy or deepcopy DOESN'T WORK!!!!
    # for snap.graphs
    def graphCopy(self, graphToCopy):

        newGraph = snap.PUNGraph.New()

        for nodeFromGraphToCopy in graphToCopy.Nodes():
            newGraph.AddNode( nodeFromGraphToCopy.GetId() )

        for edgesFromGraphToCopy in graphToCopy.Edges():
            ed = edgesFromGraphToCopy.GetId()
            nd1 = ed[0]
            nd2 = ed[1]
            newGraph.AddEdge(nd1, nd2)

        return newGraph


    def density(self, graphToCopy, nodesFromCommunity):

        newGraphToUse = self.graphCopy(graphToCopy)

        listOfNodesToRemoveFrom = snap.TIntV()

        for nodeFromNewGraph in newGraphToUse.Nodes():
            idNodeFromOriginalGraph = nodeFromNewGraph.GetId()

            if not idNodeFromOriginalGraph in nodesFromCommunity:
                listOfNodesToRemoveFrom.Add(idNodeFromOriginalGraph)

        snap.DelNodes(newGraphToUse, listOfNodesToRemoveFrom)

        na = newGraphToUse.GetEdges()
        n  = len(nodesFromCommunity)
        nt = (n*(n-1))/2

        if nt == 0:
            den = 0
        else:
            den = float(na) / float(nt)

        return den

    densityByCommunity = []
    def avgDensity(self, graphToCopy, dictOfNodesFromCommunity):

        sumDen = 0.0
        for nodesFromCommunity in dictOfNodesFromCommunity.items():
            density = self.density(graphToCopy, nodesFromCommunity[1])
            self.densityByCommunity.append( density )
            sumDen += density

        avgDen = sumDen / len(dictOfNodesFromCommunity)

        return avgDen

    def run(self, listGraph, fileWithCommunitiesDetects, nameOfNetwork, numberOfGraph, dictLabel):

        self.Graph = snap.PUNGraph.New()
        self.GraphDet = snap.PUNGraph.New()
        self.GNX = nx.Graph()
        self.nodesArray = []
        self.buildG( listGraph )
        self.nodesArray.sort()
        H = snap.TIntStrH()

        directory = 'output/'+ nameOfNetwork
        if not os.path.exists(directory):
            os.makedirs(directory)

        resultFromNX = gncdNX.main(self.GNX)

        #snap.DrawGViz( self.Graph, snap.gvlSfdp, "{}/graph{}Original{}.png".format(directory, numberOfGraph, nameOfNetwork), "Grafo{} Original {}".format(numberOfGraph, nameOfNetwork), dictLabel )

        #CmtyV = snap.TCnComV()
        #modularity = snap.CommunityGirvanNewman( self.Graph, CmtyV )
        modularity = resultFromNX[0]
        CmtyV = resultFromNX[1]
        if modularity < 0:
            modularity = modularity*(-1)

        #print len(CmtyV)

        cont = 0
        arryToNmi = {}
        for Cmty in CmtyV:
            r = lambda: random.randint( 0,255 )
            community_color = "#%02X%02X%02X" % ( r(),r(),r() )

            vetNodes = []
            for NI in Cmty:
                H.AddDat( NI, '{}",style=filled, fillcolor="{}'.format(dictLabel[NI],community_color) )
                #H.AddDat(NI, community_color)
                vetNodes.append(NI)

            arryToNmi[cont] = vetNodes

            cont+=1

        # print result
        snap.DrawGViz(self.GraphDet, snap.gvlSfdp,
                      "{}/graph{}CommDetects{}.png".format(directory, numberOfGraph, nameOfNetwork),
                      "Grafo{} {} com as comunidades detectadas por DetCon".format(numberOfGraph,
                                                                                         nameOfNetwork), H)
        # print "A modularidade da Rede foi? %f" % modularity

        density = self.avgDensity(self.GraphDet, arryToNmi)

        result = {}
        result[0] = modularity
        result[1] = self.nodesArray
        result[2] = self.makeVectorToNmi(arryToNmi, self.nodesArray)
        result[3] = density
        result[4] = arryToNmi
        #result[5] = self.densityByCommunity

        return result



