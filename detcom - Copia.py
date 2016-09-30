# -*- coding: utf-8 -*-
__author__ = 'Márcio Vinícius Dias'

from lxml import  objectify

import treatRecordsFile

import etapa2


class Main():

    rootNetworkXmlFile = None
    vectorVertices = {}
    attribSelecteds = {}
    metaPath = []
    metaPathLen = 0
    file_ = None


    def __init__(self):
        pass


    # Get all vertices from the schema
    def getAllVerticesAndAttribFromSchema(self, xmlFileName):

        verticesAndAttrib = {}

        with open(xmlFileName) as f:
            xml = f.read()

        root = objectify.fromstring(xml)

        for metaNetwork in root.getchildren():
            for nodesType in metaNetwork.getchildren():
                for nodeclass in nodesType.getchildren():
                    for node in nodeclass.getchildren():

                        verticeName = node.get("id")

                        for nodeProperties in node.getchildren():

                            attribList = []

                            for property in nodeProperties.getchildren():

                                name = property.get('name')
                                attribList.append(name)
                                #print "%s => %s" % (verticeName, property.attrib)

                            verticesAndAttrib[verticeName] = attribList

        return verticesAndAttrib

    # Get all from specific type of vertice from the network
    def getVertices(self, vertice):

        root = self.rootNetworkXmlFile

        vectorVertice = {}

        for metaNetwork in root.getchildren():
            for nodesType in metaNetwork.getchildren():
                for nodeclass in nodesType.getchildren():

                    nodeclassType = nodeclass.get("type")

                    if ( nodeclassType != vertice):
                        continue

                    for node in nodeclass.getchildren():

                        verticeName = node.get("id")

                        for nodeProperties in node.getchildren():

                            attribList = {}

                            for property in nodeProperties.getchildren():

                                name = property.get('name')
                                value = property.get('value')

                                attribList[name] = value

                            vectorVertice[verticeName] = attribList



        return vectorVertice

    # start the objectify from the xml network file
    def startRootNetwork(self, xmlFileName):

        with open(xmlFileName) as f:
            xml = f.read()

        self.rootNetworkXmlFile = objectify.fromstring(xml)

    # build the a vector of all vertice for each type of vertice in metaPath
    def buildVectorVertices(self, metaPath):

        for meta in metaPath:
            self.vectorVertices[meta] = self.getVertices(meta)

    #check if has link between the two itens
    #auxiliary function of haslink
    def checkIfHasLink(self, links, fristItem, secondItem ):

        for link in links:

            source = link.get("source")
            target = link.get("target")

            if ( ( source == fristItem ) and ( target == secondItem) ):
                return True

        return False

    #check if has link between the two vertices
    def haslink(self, firstVerticeType, fristItem, secondVerticeType, secondItem):

        root = self.rootNetworkXmlFile

        for metaNetwork in root.getchildren():
            for nodesTypes in metaNetwork.getchildren():

                nodesType = nodesTypes.tag

                # to interact only inside of networks, where the links is.
                if (nodesType != "networks"):
                    continue

                for links in nodesTypes.getchildren():

                    #get only the selected network

                    networkSourceType = links.get("sourceType")
                    networkTargetType = links.get("targetType")

                    #as can accept graph that is not directed, the order doesn't matter
                    # source-target or target-source is the same for a not direct graph. (actually, doesn't exist target and source)
                    if( (networkSourceType == firstVerticeType) and (networkTargetType == secondVerticeType) ):

                        if (self.checkIfHasLink(links.getchildren(), fristItem, secondItem)):
                            return True

                    elif ( (networkSourceType == secondVerticeType) and (networkTargetType == firstVerticeType) ):

                        if (self.checkIfHasLink(links.getchildren(), secondItem, fristItem)):
                            return True

        return False

    # get the attributes selected by the user
    def getAttributesFromVertice(self, verticeType, verticeId):

        attributesFromTypeOfVertice = self.vectorVertices[verticeType]

        attributes = attributesFromTypeOfVertice[verticeId]

        #print self.attribSelecteds

        aux = ""
        for attribute in attributes:

            for attribSelected in self.attribSelecteds[verticeType]:

                if( attribute == attribSelected):
                    aux = aux + "   " + attributes[attribute]

        return aux



    # auxiliary function
    def auxBuildRecords(self, firstVerticeType, fristItem, metaPathItem):

        vertices = self.vectorVertices.values()[metaPathItem]

        for secondItem in vertices:

            secondVerticeType = self.metaPath[metaPathItem]

            #check if has link between the two vertices
            haslink = self.haslink(firstVerticeType, fristItem, secondVerticeType, secondItem)

            if(not haslink):
                continue

            aux1 = firstVerticeType + "," + fristItem + "-" + secondVerticeType + "," + secondItem

            aux2 = self.getAttributesFromVertice(firstVerticeType, fristItem)
            aux3 = self.getAttributesFromVertice(secondVerticeType, secondItem)

            aux4 = aux1 + "|" + aux2 + aux3

            print aux4

            self.file_.write( aux4 + '\n')

    # build the records
    def buildRecords(self, metaPathCount):

        if(metaPathCount == self.metaPathLen-1):
            return

        vertices1 = self.vectorVertices.values()[metaPathCount]

        for item in vertices1:
            verticeType = self.metaPath[metaPathCount]
            self.auxBuildRecords(verticeType, item, metaPathCount+1)

        self.buildRecords(metaPathCount+1)




    def run(self):

        xmlFileSchema = 'dataset/esquema_exemplo_abordagem.xml'
        verticesAndAttribFromSchema = self.getAllVerticesAndAttribFromSchema( xmlFileSchema)

        print verticesAndAttribFromSchema

        self.metaPath.append('pessoa')
        self.metaPath.append('ocorrencia')
        #self.metaPath.append('item')
        self.metaPathLen = self.metaPath.__len__()

        self.attribSelecteds['pessoa'] = ['idade']
        self.attribSelecteds['ocorrencia'] = ['latitude', 'longitude', 'dataHora']

        xmlFileNetworkGi = 'dataset/rede_exemplo_abordagem.xml'
        etapa2.Etp2.run(xmlFileNetworkGi)


        #treatRecordsFile.treat("output/clusterFromAP.txt")


if __name__ == "__main__":
    print(__doc__)
    Main().run()