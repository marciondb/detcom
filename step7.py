# -*- coding: utf-8 -*-
__author__ = 'Márcio Vinícius Dias'

from sklearn.metrics.cluster import normalized_mutual_info_score
import gncd
import random
import step6
import snap
from igraph import *
from pandas import DataFrame

class Etp7():

    def makeVectorToNni(self, arryMni, listGraph):
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

    def makeNewNmi(self, nodesFromCompareAlg, nodesFromInductedGraph, vetNmiFromCompareAlg):
        newArrNmi = []

        for nodeFromIG in nodesFromInductedGraph:
            cont = 0
            for nodeFromCA in nodesFromCompareAlg:
                if nodeFromIG == nodeFromCA:
                    value = vetNmiFromCompareAlg[cont]
                    newArrNmi.append(value)
                    break
                cont += 1
        return newArrNmi

    def num(self,s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def getArrayFromStr(self, string, delimiter):

        aux = string.split(delimiter)
        temp = []

        for item in aux:

            temp.append(self.num(item))

        return temp

    def getOrinialidFromFile(self, fileWithOriginalIds):

        arrayIds = []

        with open(fileWithOriginalIds) as f:
            content = f.read().splitlines()
            for line in content:
                aux = int(line)
                arrayIds.append(aux)

        return arrayIds

    def getLouvainCResultFromFile(self, fileLouvainC):

        communitiesFromLouvainC = []
        with open(fileLouvainC) as f:
            content = f.read().splitlines()
            for line in content:
                aux = self.getArrayFromStr(line, ' ')
                communitiesFromLouvainC.append(aux)

        return communitiesFromLouvainC

    def communityFromLouvaincWithOriginalIds(self, communityFromLouvainC, arrayOriginalIds):

        louvaincWithOriginalIds = []

        for item in communityFromLouvainC:
            aux = arrayOriginalIds[item]
            louvaincWithOriginalIds.append(aux)
        return louvaincWithOriginalIds

    def getLouvainCResultFromFileToOriginalIds(self, fileLouvainC, fileWithOriginalIds):

        communitiesFromLouvainC = self.getLouvainCResultFromFile(fileLouvainC)
        arrayOriginalIds = self.getOrinialidFromFile(fileWithOriginalIds)
        louvaincWithOriginalIds = {}


        count = 0
        for community in communitiesFromLouvainC:
            aux = self.communityFromLouvaincWithOriginalIds(community, arrayOriginalIds)
            louvaincWithOriginalIds[count] = aux

            count += 1

        return louvaincWithOriginalIds

    def getResultsFromFile(self, fileOfResults):

        preResult = []
        results = []

        with open(fileOfResults) as f:
            content = f.read().splitlines()
            for line in content:

                graphInit = line.find("graph")
                if graphInit >= 0:

                    if(preResult.__len__() > 0):
                        results.append(preResult)
                    preResult = []
                    continue

                graphInit = line.find("GN")
                if graphInit >= 0:
                    results.append(preResult)
                    preResult = []
                    continue

                graphInit = line.find("{")
                if graphInit >= 0:
                    continue

                aux = self.getArrayFromStr(line, ',')
                preResult.append(aux)

        result2 = preResult

        return results, result2

    def saveGraph(self, graph, CmtyV, nameOfNetwork, attrbToLabel, xmlFileNetworkGi, targetVertice):

        dictLabel = step6.Etp6().createVectLabel(attrbToLabel, targetVertice, xmlFileNetworkGi)
        H = snap.TIntStrH()

        for Cmty in CmtyV:
            r = lambda: random.randint( 0,255 )
            community_color = "#%02X%02X%02X" % ( r(),r(),r() )

            for NI in CmtyV[Cmty]:
                H.AddDat( NI, '{}",style=filled, fillcolor="{}'.format(dictLabel[NI],community_color) )

        snap.DrawGViz(graph, snap.gvlSfdp,
                          "output/{}/graphLouvainCCommDetects.png".format(nameOfNetwork),
                          "Grafo com as comunidades detectadas por LouvainC", H)



    def getModularityFromLouvainC(self, nameOfNetwork, vetorNmi, nodesArray):

        g = Graph()
        for node in nodesArray:
            g.add_vertex(int(node))

        with open('dataset\grafo_metapath_{}.txt'.format(nameOfNetwork)) as f:
            content = f.read().splitlines()
            for line in content:
                edge = line.split(',')
                source = g.vs.select(name=int(edge[0])).indices[0]
                target = g.vs.select(name=int(edge[1])).indices[0]

                g.add_edges([(source, target)])

        modularity = g.modularity(vetorNmi)

        return modularity

    def getResultFromLouvainC(self, nameOfNetwork, nodesArray, attrbToLabel, xmlFileNetworkGi, targetVertice):

        fileLouvainC = "dataset\\louvainC_{}.txt".format(nameOfNetwork)
        fileWithOriginalIds = "dataset\\original_ids_{}.txt".format(nameOfNetwork)

        arrayToNmi = self.getLouvainCResultFromFileToOriginalIds(fileLouvainC, fileWithOriginalIds)
        vetorNmi = self.makeVectorToNni(arrayToNmi, nodesArray)

        nameOfFileToCompare = "dataset\grafo_metapath_{}.txt".format(nameOfNetwork)
        listGraph = []
        with open(nameOfFileToCompare) as f:
            content = f.read().splitlines()
            for line in content:
                listGraph.append(line)

        graphDet = gncd.Main().buildG(listGraph)

        self.saveGraph( graphDet, arrayToNmi, nameOfNetwork, attrbToLabel, xmlFileNetworkGi, targetVertice )

        density = gncd.Main().avgDensity(graphDet, arrayToNmi)

        modularity = self.getModularityFromLouvainC( nameOfNetwork, vetorNmi, nodesArray )

        result = [modularity, nodesArray, vetorNmi, density, arrayToNmi]

        return result

    def saveResultsToExcel(self, results, result2, result3, nameOfNetwork):

        col2_name = 'Nmi LouvainC'
        col6_name = 'Nmi GN'
        col3_name = 'M DetCom'
        col4_name = 'M LouvainC'
        col5_name = 'M GN'
        col7_name = 'D DetCom'
        col8_name = 'D LouvainC'
        col9_name = 'D GN'

        modularitiesDetCom = []
        modularitiesGN = []
        modularitiesLouvainC = []
        densitiesDetCom = []
        densitiesGN = []
        densitiesLouvainC = []
        nmisGN = []
        nmisLouvainC = []

        for result in results:

            # 0 = modularity
            # 1 = nodeArray
            # 2 = vetorNmi
            # 3 = density
            # 4 = detected communities/arrayToNmi

            vectorFromResult2 = self.makeNewNmi(result2[1], result[1], result2[2])

            vet1 = result[2]
            vet2 = vectorFromResult2
            nmiGN = normalized_mutual_info_score(vet1, vet2)
            nmisGN.append(nmiGN)

            vectorFromResult3 = self.makeNewNmi(result3[1], result[1], result3[2])
            vet1 = result[2]
            vet2 = vectorFromResult3
            nmiLouvainC = normalized_mutual_info_score(vet1, vet2)
            nmisLouvainC.append(nmiLouvainC)

            modularitiesDetCom.append(result[0])
            modularitiesGN.append(result2[0])
            modularitiesLouvainC.append(result3[0])

            densitiesDetCom.append(result[3])
            densitiesGN.append(result2[3])
            densitiesLouvainC.append(result3[3])

        df = DataFrame({col6_name: nmisGN,
                        col2_name: nmisLouvainC,
                        col5_name: modularitiesGN,
                        col4_name: modularitiesLouvainC,
                        col3_name: modularitiesDetCom,
                        col9_name: densitiesGN,
                        col8_name: densitiesLouvainC,
                        col7_name: densitiesDetCom})
        df.to_excel('result_{}.xlsx'.format(nameOfNetwork), sheet_name='comparacao', index=True)

        return 0

    def run(self, targetVertice, nameOfNetwork, attrbToLabel, xmlFileNetworkGi):

        fileOfResults = "output\\Results_{}.txt".format(nameOfNetwork)

        results, result2 = self.getResultsFromFile(fileOfResults)
        result3 = self.getResultFromLouvainC(nameOfNetwork, result2[1], attrbToLabel, xmlFileNetworkGi, targetVertice)

        self.saveResultsToExcel(results, result2, result3, nameOfNetwork)

        print "Step7 done!"

if __name__ == "__main__":
    print(__doc__)
    Etp7().run()

