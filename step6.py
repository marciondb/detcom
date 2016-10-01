__author__ = 'marcio'

from lxml import  objectify
import snap
import re

class Etp6():

    def __init__(self):
        pass

    # start the objectify from the xml network file
    def startRootNetwork(self, xmlFileName):

        with open(xmlFileName) as f:
            xml = f.read()

        rootNetworkXmlFile = objectify.fromstring(xml)

        return rootNetworkXmlFile

    def createVectLabel(self, attrbToLabel, vertice, xmlFileName):

        root = self.startRootNetwork(xmlFileName)
        temp = vertice.split('-')
        dictLabel = snap.TIntStrH()
        for metaNetwork in root.getchildren():
            for nodesType in metaNetwork.getchildren():
                for nodeclass in nodesType.getchildren():

                    nodeclassType = nodeclass.get("type")

                    if (nodeclassType != temp[0]):
                        continue

                    for node in nodeclass.getchildren():

                        verticeName = node.get("id")

                        if attrbToLabel == "mainId":
                            dictLabel[int(verticeName)] = verticeName
                            continue

                        for nodeProperties in node.getchildren():
                            for property in nodeProperties.getchildren():

                                # To include only attributes that the were selected in the var self.attribSelecteds
                                name = property.get('name')
                                value = property.get('value')

                                if name == attrbToLabel:
                                    dictLabel[int(verticeName)] = value


        return dictLabel

    def treatLine(self, line, targetVertice):

        aux = line.split(',')

        aux2 = aux[0].split(targetVertice)
        aux3 = aux[1].split(targetVertice)

        return aux2[1]+','+aux3[1]


    def sendGraphToDetect( self, algorithmChoose, fileInducedGraph, targetVertice, nameOfNetwork, attrbToLabel, GI ):

        numberOfGraph = -1
        flagChangeGraphControl = -1
        listGraph = []
        results = []
        dictLabel = self.createVectLabel(attrbToLabel, targetVertice, GI)

        with open(fileInducedGraph) as f:
            content = f.read().splitlines()
            for line in content:

                graphInit = line.find("graph")

                if graphInit >= 0 :
                    numberOfGraph += 1
                    continue
                else:

                    if flagChangeGraphControl < numberOfGraph:
                        flagChangeGraphControl = numberOfGraph

                        if listGraph.__len__() > 0:
                            #print ''
                            results.append(algorithmChoose.Main().run(listGraph, nameOfNetwork, numberOfGraph, dictLabel))

                        listGraph = []

                    lineToIncludeInList = self.treatLine(line, targetVertice)
                    listGraph.append(lineToIncludeInList)

            numberOfGraph += 1
            results.append( algorithmChoose.Main().run(listGraph, nameOfNetwork, numberOfGraph, dictLabel))

        listGraph = []

        nameOfFileToCompare = "dataset\grafo_metapath_{}.txt".format(nameOfNetwork)
        with open(nameOfFileToCompare) as f:
            content = f.read().splitlines()
            for line in content:
                listGraph.append(line)

        result2 = algorithmChoose.Main().run(listGraph, nameOfNetwork, 10000, dictLabel)

        fileOfResults = "output\\Results_{}.txt".format(nameOfNetwork)
        self.saveResults(results, result2, fileOfResults)

    def getStrFromArray(self, array):
        strLine = array.__str__()
        strLine = re.sub(r"/?\[", "", strLine)
        strLine = re.sub(r"/?\]", "", strLine)

        return strLine


    def saveResults(self, results, result2, fileName):

        file_ = open(fileName, 'w')

        numberOfGraph = 1
        for result in results:
            file_.write('graph {}\n'.format(numberOfGraph))
            numberOfGraph += 1

            for term in result:
                # 0 = modularity
                # 1 = nodeArray
                # 2 = vetorNmi
                # 3 = density
                # 4 = detected communities/arrayToNmi
                strLine = self.getStrFromArray(result[term])
                file_.write("{0}\n".format(strLine))

        #result From GN
        file_.write('GN\n')
        for term in result2:
            # 0 = modularity
            # 1 = nodeArray
            # 2 = vetorNmi
            # 3 = density
            # 4 = detected communities/arrayToNmi
            strLine = self.getStrFromArray(result2[term])
            file_.write("{0}\n".format(strLine))

        file_.close()

    def run(self, fileInducedGraph, targetVertice, nameOfNetwork, attrbToLabel, GI ):


        #list of algorithm to choose
        algorithm = {}

        algorithm[0] = ['GirvanNewman']

        #user choice
        algorithmChooseByUser = 0

        print "Algorithm to detect community selected was {}".format( algorithm[algorithmChooseByUser][0] )

        algorithmChoose = None
        if algorithmChooseByUser == 0 :
            import gncd

            algorithmChoose = gncd

        self.sendGraphToDetect( algorithmChoose, fileInducedGraph, targetVertice, nameOfNetwork, attrbToLabel, GI )

        print "Step6 done!"

