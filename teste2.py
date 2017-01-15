import networkx as nx
from collections import Counter

GNX = nx.Graph()


def buildG(listGraph):
    edgesWithWeight = Counter(listGraph)

    for line in edgesWithWeight:

        weightFromLine = edgesWithWeight[line]

        col = line.split(',')

        nodeId1 = int(col[0])
        nodeId2 = int(col[1])

        GNX.add_edge(nodeId1, nodeId2, weight=float(weightFromLine))

    return GNX

listGraph = []

nameOfNetwork = "enron"+"Network"

nameOfFileToCompare = "dataset\\teste\\grafo_metapath_{}.txt".format(nameOfNetwork)

with open(nameOfFileToCompare) as f:
    content = f.read().splitlines()
    for line in content:
        listGraph.append(line)

buildG( listGraph )

print(nx.average_clustering(GNX))
