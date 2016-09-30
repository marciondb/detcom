__author__ = 'marcio'
#import itertools

"""
#L1 = [['1', '0'], ['1', '1'], ['1', '2'], ['1', '3'], ['1', '4'], ['1', '5'], ['1', '6'], ['2', '0'], ['2', '1'], ['2', '2'], ['2', '3'], ['2', '4'], ['2', '5'], ['2', '6'], ['3', '0'], ['3', '1'], ['3', '2'], ['3', '3'], ['3', '4'], ['3', '5'], ['3', '6'], ['4', '0'], ['4', '1'], ['4', '2'], ['4', '3'], ['4', '4'], ['4', '5'], ['4', '6'], ['5', '0'], ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5'], ['5', '6'], ['6', '0'], ['6', '1'], ['6', '2'], ['6', '3'], ['6', '4'], ['6', '5'], ['6', '6'], ['7', '0'], ['7', '1'], ['7', '2'], ['7', '3'], ['7', '4'], ['7', '5'], ['7', '6'], ['8', '0'], ['8', '1'], ['8', '2'], ['8', '3'], ['8', '4'], ['8', '5'], ['8', '6']]
L1 = ['1', '2']
L2 = ['1', '2', '3']



def t(L1, L2):
    #L3 = [ i + (j,) for i in L1 for j in L2 ]

    #L3 = [ i + (j,) for i in L1 for j in L2 ]

    #print L3

    #L3 = [ i + "-" + j for i in L1 for j in L2 ]

    return [ i + "-" + j for i in L1 for j in L2 ]


L3 = t(L1,L2)
print L3
print "novo"
L4 = ['4','6','7']
print t(L3,L4)

__author__ = 'marcio'
#import itertools
#L1 = [ (i,j) for i in range(1,3) for j in range(1,5) ]
L1 = [('1', '0'), ('1', '1'), ('1', '2'), ('1', '3'), ('1', '4'), ('1', '5'), ('1', '6'), ('2', '0'), ('2', '1'), ('2', '2'), ('2', '3'), ('2', '4'), ('2', '5'), ('2', '6'), ('3', '0'), ('3', '1'), ('3', '2'), ('3', '3'), ('3', '4'), ('3', '5'), ('3', '6'), ('4', '0'), ('4', '1'), ('4', '2'), ('4', '3'), ('4', '4'), ('4', '5'), ('4', '6'), ('5', '0'), ('5', '1'), ('5', '2'), ('5', '3'), ('5', '4'), ('5', '5'), ('5', '6'), ('6', '0'), ('6', '1'), ('6', '2'), ('6', '3'), ('6', '4'), ('6', '5'), ('6', '6'), ('7', '0'), ('7', '1'), ('7', '2'), ('7', '3'), ('7', '4'), ('7', '5'), ('7', '6'), ('8', '0'), ('8', '1'), ('8', '2'), ('8', '3'), ('8', '4'), ('8', '5'), ('8', '6')]
print type(L1)
print L1.__len__()

#L2 = range(1,5)
L2 = ['1', '2', '3']
print type(L2)
print L2.__len__()

L3 = [ i + (j,) for i in L1 for j in L2 ]
#L3 = list(itertools.product(L1,L2))
print L3
print L3.__len__()

print "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
L2 = range(0,3)
print L2

#from sklearn.metrics.cluster import normalized_mutual_info_score

#print normalized_mutual_info_score([2, 2, 3, 1, 3, 1, 1, 0, 0, 0, 0, 0], [13, 13, 6, 6, 6, 6, 6, 12, 5, 12, 5, 5])

from igraph import *

#g = Graph.Read_Ncol('dataset\grafo_igrapg_metapath_conflitosNetwork.txt', names=True,  directed=False)

#print g.modularity([0, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1, 2, 1, 2, 1, 1, 1, 1, 1, 0, 0, 2, 2, 1, 1, 0, 2, 2, 0, 2, 2])

#def get

x = [0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 6, 7, 5, 0, 5, 0, 1, 1, 1, 1, 2, 0, 3, 0, 0, 2, 2, 3, 0, 0, 0, 0, 0]
nodes = [2, 20, 100, 130, 135, 200, 210, 211, 220, 350, 355, 360, 365, 530, 630, 640, 651, 652, 663, 666, 700, 710, 713, 731, 732, 750, 770, 775, 800, 840, 850, 900, 920]
g = Graph()
for node in nodes:
    g.add_vertex(int(node))

with open('dataset\grafo_metapath_conflitosNetwork.txt') as f:
    content = f.read().splitlines()
    for line in content:
        edge = line.split(',')
        source = g.vs.select(name=int(edge[0])).indices[0]
        target = g.vs.select(name=int(edge[1])).indices[0]

        g.add_edges([(source, target)])


print g.modularity(x)
print g.modularity([0, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1, 2, 1, 2, 1, 1, 1, 1, 1, 0, 0, 2, 2, 1, 1, 0, 2, 2, 0, 2, 2])


str = "set([u'astro-ph', u'gr-qc'])"

str = str.replace('\'','')
str = str.replace('set([','')
str = str.replace('])','')
str = str.replace('u','')
print str

L1 = "set(['a', 'b', 'c', 'd'])"
L2 = ['c', 'b', 'd', 'e','g']
S1 = eval(L1)#set(L1)
S2 = set(L2)
difference = list(S1.symmetric_difference(S2))
print difference
import math
print math.sqrt(8)

print isinstance( S1, int )"""

import time
strings = time.strftime("%Y,%m,%d,%H,%M,%S")
t = strings.split(',')
numbers = [ int(x) for x in t ]
print numbers
