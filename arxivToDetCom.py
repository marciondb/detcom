__author__ = 'marcio'

from lxml import  objectify


def writeBeginFile(file):
    file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>' + '\n')
    file.write('<DynamicNetwork xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation = "DyNetML.xsd">' + '\n')
    file.write('<MetaNetwork>' + '\n')

def writeBeginNodeFile(file):
    file.write('<nodes>' + '\n')
    file.write('<nodeclass type = "author" id = "author" >' + '\n')

def writePrintNode(file, id, name):
    file.write('<node id="{0}">'.format(id) + '\n')
    file.write('<properties>' + '\n')
    file.write('<property name="name" type="string" value="{0}"/>'.format(name) + '\n')
    file.write('</properties>' + '\n')
    file.write('</node>' + '\n')
    # arquivo com as ids originais
    fileOriginalIds.write('{0}'.format(id) + '\n')

def writeCloseNodeFile(file):
    file.write('</nodeclass >' + '\n')
    file.write('</nodes>' + '\n')

def writeOpenNetworks(file):
    file.write('<networks>' + '\n')
    file.write('<network sourceType = "author" targetType = "author" id = "author x author" isDirected = "false">' + '\n')

def writeOpenLink(file, source, target):
    file.write('<link source="{0}" target="{1}">'.format(source, target) + '\n')
    file.write('<properties>' + '\n')
    #para imprimir o arquivo para usar no LouvianC
    fileLouvianC.write('{0} {1}'.format(source, target) + '\n')
    #para gerar o grafo simples, usado para comparar os algo
    fileSimpleGraph.write('{0},{1}'.format(source, target) + '\n')

def writeLinkProperty (file, property, name):
    file.write('<property name="{0}" type="string" value="{1}"/>'.format(name, property) + '\n')

def writeClosetLink(file):
    file.write('</properties>' + '\n')
    file.write('</link>' + '\n')

def writeCloseNetworks(file):
    file.write('</network>' + '\n')
    file.write('</networks>' + '\n')

def writeCloseFile(file):
    file.write('</MetaNetwork>' + '\n')
    file.write('</DynamicNetwork>' + '\n')

def getIdFromDict(nodeDict, value):

    for item in nodeDict:
        if nodeDict[item] == value:
            return item

def treatBagOfWords(bagOfWords):

    str = bagOfWords.text
    str = str.replace('\'', '')
    str = str.replace('set(', '')
    str = str.replace(')', '')
    str = str.replace('u', '')
    str = str.replace(',', '')
    str = str.replace('[', '')
    str = str.replace(']', '')

    return str

def filterYear(arrayProperty, year):

    for links in arrayProperty:
        key = links.get("key")
        if key != "d2":
            continue

        yearToCompare = int(links)

        if yearToCompare == year:
            return True

    return False
"""
file_ = open('dataset/predataset/rede_arxivNetwork.xml', 'w')
fileLouvianC = open('dataset/predataset/hetero.net', 'w')
fileSimpleGraph = open('dataset/predataset/grafo_metapath_arxivNetwork.txt', 'w')
fileOriginalIds = open('dataset/predataset/original_ids_arxivNetwork.txt', 'w')

with open('dataset/predataset/arxiv.txt') as f:"""

year = 1999
nodeDict = {}
nodeCount = 0
file_ = open('dataset/predataset/rede_enronNetwork.xml', 'w')
fileLouvianC = open('dataset/predataset/hetero.net', 'w')
fileSimpleGraph = open('dataset/predataset/grafo_metapath_enronNetwork.txt', 'w')
fileOriginalIds = open('dataset/predataset/original_ids_enronNetwork.txt', 'w')

with open('dataset/predataset/enron.txt') as f:
    xml = f.read()

root = objectify.fromstring(xml)


### TREAT EDGES INIT
#1-verificar source==target
verticesToNotInclude = []
verticesToInclude = []
for graph in root.getchildren():
    for element in graph.getchildren():
        node = element.get("id")

        if not node:

            #make a filter by year
            #if not filterYear(element.getchildren(), year):
                #continue

            source = element.get("source")
            target = element.get("target")

            if source not in verticesToInclude:
                verticesToInclude.append(source)
            if target not in verticesToInclude:
                verticesToInclude.append(target)

            if source == target:
                if source not in verticesToNotInclude:
                    verticesToNotInclude.append(source)

#2- verficar se outra aresta usa quem esta em verticesToNotInclude
temp2 = []
for graph in root.getchildren():
    for element in graph.getchildren():
        node = element.get("id")

        if not node:

            #make a filter by year
            #if not filterYear(element.getchildren(), year):
                #continue

            source = element.get("source")
            target = element.get("target")

            if (source != target):
                if(source in verticesToNotInclude):
                    verticesToNotInclude.remove(source)
                if target in verticesToNotInclude:
                    verticesToNotInclude.remove(target)



temp = []
for node in verticesToInclude:
    if node not in verticesToNotInclude:
        temp.append(node)

verticesToInclude = temp

for node in verticesToInclude:
    nodeDict[nodeCount] = node
    nodeCount += 1
nodeCount = 0
#print verticesToNotInclude
### TREAT EDGES END

writeBeginFile(file_)

writeBeginNodeFile(file_)

for node in verticesToInclude:
    writePrintNode(file_, nodeCount, node)
    nodeCount += 1

print nodeCount

writeCloseNodeFile(file_)

writeOpenNetworks(file_)

for graph in root.getchildren():
    for element in graph.getchildren():
        node = element.get("id")

        if not node:

            #make a filter by year
            #if not filterYear(element.getchildren(), year):
                #continue

            preSource = element.get("source")
            preTarget = element.get("target")

            if (preSource not in verticesToInclude) or (preTarget not in verticesToInclude) or (preSource == preTarget):
                continue

            source = getIdFromDict(nodeDict, preSource)
            target = getIdFromDict(nodeDict, preTarget)
            writeOpenLink(file_, source, target)

            for links in element.getchildren():
                key = links.get("key")
                if key == "d1" or key == "d3":
                    continue

                if key =="d0":
                    #bagOfWords = treatBagOfWords(links)
                    bagOfWords = links
                    writeLinkProperty(file_, bagOfWords, 'bagOfWords')
                if key =="d2":
                    writeLinkProperty(file_,links, 'year')

            writeClosetLink(file_)

writeCloseNetworks(file_)

writeCloseFile(file_)

file_.close()
fileLouvianC.close()
fileOriginalIds.close()
fileSimpleGraph.close()