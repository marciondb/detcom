__author__ = 'marcio'


class Etp5():

    file_ = None

    def __init__(self):
        pass

    def transformListToSpecificString(self, list):

        newList = []
        for item in list:
            aux = item.split(',')

            aux2 = aux[0] + aux[1]
            newList.append(aux2)

        return newList


    def returnLineFromRecordsFile(self, lineToCompare, fileRecords):
        from string import whitespace
        import hashlib

        countLine = 0
        with open(fileRecords) as f:
            content = f.read().splitlines()
            for line in content:
                partition = line.split('|')

                lineFromRecords = hashlib.md5(partition[1].translate(None, whitespace)).hexdigest()
                lstrip = hashlib.md5(lineToCompare.translate(None, whitespace)).hexdigest()
                if lstrip == lineFromRecords:

                    partitionEdge = partition[0].split('-')

                    if countLine in self.lineToCompareSaver:
                        countLine+=1
                        continue
                    self.lineToCompareSaver[countLine] = partitionEdge

                    return partitionEdge
                    #return partition
                countLine += 1


    lineToCompareSaver = {}

    # compare the item and return an specific line in the original records file
    def compareSpecificLineInRecords(self, lineToCompare, fileRecords, isHomogeneousNetwork):

        if isHomogeneousNetwork:
            return self.returnLineFromRecordsFile(lineToCompare, fileRecords)

        contLine = 0
        with open(fileRecords) as f:
            content = f.read().splitlines()
            for line in content:
                partition = line.split('|')

                """
                TO treat the line, need to transform the number in the same "decimal size"
                But for now is only number, have to treat for all the cases...
                futures works...
                """
                arrayFromClusterFile = lineToCompare.split(" ")
                temp = partition[1].split("   ")
                arrayThisLine = []
                for x in temp:
                    if x != '':
                        arrayThisLine.append("%.5e" % float(x))

                if arrayFromClusterFile == arrayThisLine:

                    # BRIL
                    if contLine in self.lineToCompareSaver:
                        contLine += 1
                        continue

                    partitionEdge = partition[0].split('-')

                    # BRIL
                    self.lineToCompareSaver[contLine] = partitionEdge

                    return partitionEdge
                else:
                    contLine+=1
        return None


    #treat the original output file
    #to the cluster file with the records file
    def treatClustersFile(self, fileWithClusters, fileRecords, isHomogeneousNetwork):

        numberOfClusters = -1
        cluterDict = {}
        listCluster = []

        with open(fileWithClusters) as f:
            content = f.read().splitlines()
            for line in content:

                clusterInit = line.find("cluster")

                if clusterInit >= 0 :
                    if numberOfClusters > -1:
                        cluterDict[numberOfClusters] = listCluster
                        listCluster = []

                    numberOfClusters = numberOfClusters + 1
                    continue
                else:

                    lineToIncludeInList = self.compareSpecificLineInRecords(line, fileRecords, isHomogeneousNetwork)
                    #if lineToIncludeInList is None:
                        #continue
                    listCluster.append(lineToIncludeInList)

        cluterDict[numberOfClusters] = listCluster

        return cluterDict

    def getItemTarget(self, itenToCompare, targetVertice):

        for item in itenToCompare:

            aux = item.split(',')

            if aux[0] == targetVertice:
                return aux[0]+aux[1]

    def testIfTailIsTheTargetVertice(self, tail, targetVertice):
        tailToCheck = tail.split(',')

        if tailToCheck[0] == targetVertice:
            return True

    def saveInducedGraphInFile(self, edges):

        for item in edges:
            self.file_.write( item + '\n')

    def createEdge(self, item, clusters, targetVertice):

        auxClusters = clusters[:]
        auxClusters.remove(item)
        
        itemToCheck = item[item.__len__()-1]
        if (self.testIfTailIsTheTargetVertice(itemToCheck, targetVertice)):
            itemToCheck = item[0]

        edges = []
        for itemToCompare in auxClusters:

            tail = itemToCompare[itemToCompare.__len__()-1]

            if self.testIfTailIsTheTargetVertice(tail, targetVertice):
                tail = itemToCompare[0]

            if tail == itemToCheck:

                newEdge = self.getItemTarget(item, targetVertice) + ',' + self.getItemTarget(itemToCompare, targetVertice)

                edges.append(newEdge)

        return edges


    def inducedEdges(self, clusters, targetVertice):

        count = 0
        for cluster in clusters:
            listOfItens = clusters[cluster]

            self.file_.write( 'graph {}'.format(count) + '\n')
            count = count +1
            #print "graph"+count.__str__()

            edges = []
            for item in listOfItens:

                edgeList = self.createEdge(item, listOfItens, targetVertice)

                for edge in edgeList:
                   edges.append(edge)

            #print edges
            self.saveInducedGraphInFile(edges)



    def run(self, fileWithClusters, fileRecords, fileInducedGraph, targetVertice, isHomogeneousNetwork):

        clusters = self.treatClustersFile(fileWithClusters, fileRecords, isHomogeneousNetwork)
        #print clusters
        self.file_ = open(fileInducedGraph, 'w')
        if isHomogeneousNetwork:
            self.saveInducedGraphInFileFromHomogeneousNetwork(clusters)
        else:
            self.inducedEdges( clusters, targetVertice )
        self.file_.close()

        print "Step5 done!"

    def saveInducedGraphInFileFromHomogeneousNetwork(self, clusters):

        count = 0
        for cluster in clusters:
            listOfItens = clusters[cluster]

            self.file_.write('graph {}'.format(count) + '\n')
            count = count + 1

            for item in listOfItens:
                node1 = item[0].replace(",","")
                node2 = item[1].replace(",","")
                self.file_.write('{},{}\n'.format(node1,node2))





