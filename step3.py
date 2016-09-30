# coding=utf-8
__author__ = 'marcio'

from lxml import  objectify

class Etp3():

    rootNetworkXmlFile = None
    vectorVertices = {}
    attribSelecteds = {}
    metaPath = []
    metaPathLen = 0
    file_ = None


    def __init__(self):
        pass

    #check if a property is in the variable self.attribSelecteds
    def checkIfIsInTheAtrrbSelectedList(self, attribSelecteds, property):

        for attrib in attribSelecteds:
            if(attrib == property):
                return True

        return  False

    # Get all from specific type of vertice from the network
    def getVertices(self, vertice):

        root = self.rootNetworkXmlFile
        attributes = self.attribSelecteds[vertice]
        vectorVertice = {}
        #normalizationYear = 0.6855670 #((1949 - 1816)/(2010 - 1816))

        # this "gambarra" is to solve the case when is put a same verticeType in the metaPath
        # as is a Dictionary, the key must be unique, so this is de workaround...
        temp = vertice.split('-')

        for metaNetwork in root.getchildren():
            for nodesType in metaNetwork.getchildren():
                for nodeclass in nodesType.getchildren():

                    nodeclassType = nodeclass.get("type")

                    if ( nodeclassType != temp[0]):
                        continue

                    for node in nodeclass.getchildren():

                        verticeName = node.get("id")

                        for nodeProperties in node.getchildren():

                            attribList = {}

                            if (len(attributes) != 0):

                                for property in nodeProperties.getchildren():

                                    # To include only attributes that the were selected in the var self.attribSelecteds
                                    name = property.get('name')

                                    if (not self.checkIfIsInTheAtrrbSelectedList(attributes, name)):
                                        continue

                                    value = property.get('value')
                                    #numberValue = float(value)
                                    #if name == "styear":

                                        #if numberValue >= normalizationYear:0):
                                            #break

                                    attribList[name] = value

                                #if len(attribList) == 0:
                                    #continue

                            vectorVertice[verticeName] = attribList

        return vectorVertice

    # start the objectify from the xml network file
    def startRootNetwork(self, xmlFileName):

        with open(xmlFileName) as f:
            xml = f.read()

        self.rootNetworkXmlFile = objectify.fromstring(xml)

    # build a vector of all vertice for each type of vertice in the metaPath
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

        aux = ""
        #to keep the order of the list self.attribSelecteds
        for attribSelecteds in self.attribSelecteds[verticeType]:
            aux = aux + "   " + attributes[attribSelecteds]

        return aux


    #check if the ids in listToCheck has link and
    #get all attributes only of those ids that has link
    # And save in the file
    def auxBuildRecords(self, listToCheck ):

        for item in listToCheck:

            arrayItem = item.split("-")

            attribOfPairOfItem = []
            for index in range(0, arrayItem.__len__()-1):

                fristItem = arrayItem[index]
                secondItem = arrayItem[index + 1]

                firstVerticeType = self.metaPath[index]
                temp = firstVerticeType.split('-')
                firstVerticeType = temp[0]

                secondVerticeType = self.metaPath[index+1]
                temp = secondVerticeType.split('-')
                secondVerticeType = temp[0]

                #check if has link between the two vertices
                haslink = self.haslink(firstVerticeType, fristItem, secondVerticeType, secondItem)

                if (not haslink):
                    attribOfPairOfItem = []
                    break

                #firstVerticeType = self.metaPath[index]
                #secondVerticeType = self.metaPath[index+1]

                attribFristItem = self.getAttributesFromVertice(firstVerticeType, fristItem)
                attribOfPairOfItem.append(attribFristItem)

                if index == (arrayItem.__len__()-2):
                    attribSecondItem = self.getAttributesFromVertice(secondVerticeType, secondItem)
                    attribOfPairOfItem.append(attribSecondItem)

            if (haslink):

                aux = ""
                for index in range(0, arrayItem.__len__()):

                    itemId = arrayItem[index]
                    verticeType = self.metaPath[index]
                    aux = aux + "-" + verticeType + "," + itemId

                line = "{}|{}".format(aux[1:], ''.join(attribOfPairOfItem))

                #print line
                self.file_.write( line + '\n')

    # build the records
    def buildRecords(self):

        idItensFromVertices = []

        for path in self.metaPath:
            vertice = self.vectorVertices[path]

            preList = []
            for item in vertice:
                preList.append(item)
                preList.sort()

            idItensFromVertices.append(preList)

        # now combine all the item in the variable idItensFromVertices, so begin generate the records
        l3 = idItensFromVertices[0]
        for index in range(1, idItensFromVertices.__len__()):

            l1 = l3
            l2 = idItensFromVertices[index]
            l3 = [ i + "-" + j for i in l1 for j in l2 ]

        self.auxBuildRecords(l3)

    def buildRecordsForHomogeneousNetwork(self, fileToSaveRecords):

        #TODO mover para uma forma genérica
        attrbLink = ['bagOfWords','year']
        root = self.rootNetworkXmlFile

        for metaNetwork in root.getchildren():
            for nodesTypes in metaNetwork.getchildren():

                nodesType = nodesTypes.tag

                # to interact only inside of networks, where the links is.
                if (nodesType != "networks"):
                    continue

                for network in nodesTypes.getchildren():
                    for links in network.getchildren():
                        source = links.get("source")
                        target = links.get("target")
                        for properties in links.getchildren():
                            prelist = []
                            for property in properties.getchildren():

                                name = property.get('name')

                                if name in attrbLink:
                                    value = property.get('value')
                                    prelist.append(value)
                            aux = ''
                            for item in prelist:
                                aux += '   '+item

                            line = 'author,{0}-author,{1}|{2}'.format(source, target, aux)
                            self.file_.write(line + '\n')

    def run(self, xmlFileNetworkGi, metaPath, attribSelecteds, fileToSaveRecords, isHomogeneousNetwork):

        import time
        strings = time.strftime("%Y,%m,%d,%H,%M,%S")
        t = strings.split(',')
        numbers = [int(x) for x in t]
        print 'INICIO{}'.format(numbers)

        self.startRootNetwork(xmlFileNetworkGi)
        if not isHomogeneousNetwork:
            self.metaPath = metaPath
            self.attribSelecteds = attribSelecteds
            self.metaPathLen = self.metaPath.__len__()

            self.buildVectorVertices(self.metaPath)
            #print self.vectorVertices

        self.file_ = open(fileToSaveRecords, 'w')
        if isHomogeneousNetwork:
            self.buildRecordsForHomogeneousNetwork(fileToSaveRecords)
        else:
            self.buildRecords()
        self.file_.close()

        print "Step3 done!"
        strings = time.strftime("%Y,%m,%d,%H,%M,%S")
        t = strings.split(',')
        numbers = [int(x) for x in t]
        print 'FIM{}'.format(numbers)