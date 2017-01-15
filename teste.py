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

print isinstance( S1, int )

import time
strings = time.strftime("%Y,%m,%d,%H,%M,%S")
t = strings.split(',')
numbers = [ int(x) for x in t ]
print numbers

import numpy as np

X = np.loadtxt('output/x.txt')

min  = np.min(np.min(X, axis=1), axis=0)
max  = np.max(np.max(X, axis=1), axis=0)
value = min-(max-min)

print value
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

documents = (
"The sky is blue",
"The sun is bright",
"The sun in the sky is bright",
"We can see the shining sun, the bright sun"
)
tfidf_vectorizer = TfidfVectorizer(max_df=0.9, max_features=200000,
                                   min_df=0.1, analyzer='word', stop_words=None,
                                   use_idf=True)
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

affinity_matrix_ = -euclidean_distances(tfidf_matrix, tfidf_matrix)
print affinity_matrix_
print "---------------------------"


x= tfidf_matrix.todense()
years = []
for document in documents:
    years.append(1999)

c = np.hstack((x, np.atleast_2d(years).T))

er = -euclidean_distances(c, c)
print er"""

from wordcloud import WordCloud, STOPWORDS
import step5
detcom = ['13-22','13-26','13-33','14-27','23-27','25-27','27-31','26-27','27-31']
gn = ['11-12','11-13','11-14','11-22','11-26','11-27','11-31','11-32', '12-13','12-14','12-22','12-26','12-27','12-29','12-31','12-34','12-35','12-73','13-14','13-22','13-23','13-24','13-26','13-27','13-29','13-30','13-31','13-32','13-34','13-35','14-23','14-24','14-25','14-26','14-27','14-28','14-29','14-30','14-31','14-32','14-34','14-35','22-23','22-25','22-26','22-27','22-30','22-31','22-32','22-34','22-35','23-24','23-25','23-26','23-27','23-28','23-29','23-30','23-31','23-32','23-34','23-35','24-25','24-26','24-27','24-29','24-31','24-32','25-26','25-27','25-28','25-30','25-31','25-32','26-27','26-29','26-30','26-31','26-32','26-34','26-35','27-28','27-29','27-30','27-31','27-32','27-34','27-35','28-29','28-30','28-31','28-32','29-30','29-31','29-32','30-31','30-35','31-32','31-34','31-35','32-34','32-35','34-73','35-73','73-144']
"""
clusters = step5.Etp5().treatClustersFile('output/clusters.txt', 'output/records.txt', True)
#print clusters

testClusters = open('output/testClusters.txt', 'w')
count = 0
for cluster in clusters:
    listOfItens = clusters[cluster]

    count = count + 1
    edges = ''
    for item in listOfItens:
        if item:
            node1 = item[0]
            node2 = item[1]
            testClusters.write('{} | {}\n'.format(node1, node2))
graphInit = line.find("GN")
            if graphInit >= 0:
                results.append(preResult)
                preResult = []
                continue
graph 1
0.629009614043
0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 83, 84, 85, 86, 87, 88, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101, 102, 108, 109, 110, 111, 114, 116, 117, 118, 119, 121, 122, 123, 124, 126, 127, 128, 130, 131, 132, 133, 137, 140, 141, 143, 145, 147
2, 2, 2, 2, 2, 0, 2, 2, 7, 2, 1, 1, 1, 1, 4, 1, 4, 4, 0, 0, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 3, 0, 0, 0, 3, 3, 1, 0, 0, 2, 4, 1, 0, 1, 1, 0, 2, 2, 2, 2, 2, 2, 2, 3, 2, 7, 2, 2, 0, 0, 1, 4, 0, 0, 7, 4, 1, 0, 2, 3, 3, 6, 5, 5, 5, 5, 5, 2, 5, 5, 0, 0, 0, 6, 0, 9, 2, 7, 0, 9, 9, 0, 6, 7, 0, 4, 6, 0, 8, 0, 8, 8, 0, 3, 3, 0, 6, 6, 0, 8, 3, 4, 3, 3, 8
0.322105737175
{0: 130, 133, 6, 19, 20, 36, 37, 39, 40, 41, 45, 47, 51, 54, 69, 70, 73, 74, 78, 94, 95, 96, 98, 102, 110, 116, 119, 122, 126, 1: 11, 12, 13, 14, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 44, 50, 52, 53, 71, 77, 2: 0, 1, 2, 3, 4, 7, 8, 10, 48, 55, 56, 57, 58, 59, 60, 61, 63, 67, 68, 79, 90, 100, 3: 128, 38, 81, 42, 43, 140, 143, 80, 145, 62, 127, 4: 49, 72, 76, 141, 15, 17, 18, 21, 117, 5: 84, 85, 86, 87, 88, 91, 92, 6: 97, 131, 132, 111, 83, 118, 7: 64, 9, 114, 75, 101, 8: 123, 121, 147, 124, 137, 9: 99, 108, 109}

"""
def getCommunitiesFromInductedGraph( communitiesss, listGraphaux ):

    preCommunityEdges = {}
    for community in communitiesss:
        preList = []

        for line2 in listGraphaux:

            temp = line2.split('|')
            auxNodes = temp[0]
            nodes = auxNodes.replace('author,', '')

            node1 = int(nodes.split('-')[0])
            node2 = int(nodes.split('-')[1])

            if (not node1 in communitiesss[community]) and (not node2 in communitiesss[community]):
                continue
            #aux = 'author{},author{}'.format(node1, node2)
            aux = temp[1]
            preList.append(aux)

        preCommunityEdges[community] = preList

    return preCommunityEdges

import ast
def getResultsCommunitiesFile(fileOfResults):
    result2 = []
    result1 = []
    flagTemp = False
    with open(fileOfResults) as f:
        content = f.read().splitlines()
        for line in content:

            graphInit = line.find("graph")
            if graphInit >= 0:
                continue

            graphInit = line.find("GN")
            if graphInit >= 0:
                flagTemp = True

            graphInit = line.find("{")
            if not graphInit >= 0:
                continue

            if flagTemp:
                result2.append(ast.literal_eval(line))
                continue

            result1.append(ast.literal_eval(line))



    return result1, result2

fileOfResults = "output/Results_enronNetwork.txt"
communityList, communityListGN = getResultsCommunitiesFile(fileOfResults)


nameOfFileToCompare = "output/inducedGraph.txt"
listGraph = []
cont = -1
flag = False
communityEdges = {}
listGraph2 = []
with open(nameOfFileToCompare) as f:
    content = f.read().splitlines()
    for line in content:

        graphInit = line.startswith("graph")
        if graphInit:

            if cont >= 0:
                cont_ = communityList[cont]
                communityEdges[cont] = getCommunitiesFromInductedGraph(cont_, listGraph)

            cont+=1
            listGraph = []
            continue

        listGraph.append(line)
        listGraph2.append(line)


communityEdges[cont] = getCommunitiesFromInductedGraph(communityList[cont], listGraph)
communityEdgesGN = getCommunitiesFromInductedGraph(communityListGN[0], listGraph2)

from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer

stopwords = set(STOPWORDS)
sw = text.ENGLISH_STOP_WORDS.union(
        ['10', '11', '2001', 'amto', 'cc', 'know', 'just', 'like', 'friday', 'monday', 'fw', 'week', 'make', 'day',
         'don', 'today', 'use', 'questions', 'october', 'november', 'work', '08', '15', '26', 'time', '2002', 'gas',
         'contract', 'meeting', 'said', 'ees', 'EES', 'NA',
         'tuesday', 'wednesday', 'ect', 'com', 'new', 'let', 'need', 'hou', 'pm', 'pmto', 'mark', 'sent', 'subject',
         'thanks', 'message', 'want', 'thursday', 'think', '0003', '66', '199', '42', '688', '57', 'ga', 'corp',
         'agreement',
         'original', '00', '01', '02', '03', '04', '05', '09', '12', '20', '2000', '30', '646', '713', '853',
         'attached', 'going', 'll', 'mail', 'forward', 'forwarded', 'will', 'enron', 'energy', 'california', 'power',
         'EE', 'ET', 'ee', 'et'])

for wor in sw:
    stopwords.add(wor)
"""
saveImages = 'output/tagclouds/'
for communitys in communityEdges:
    communitiesFromGraph = communityEdges[communitys]

    for community in communitiesFromGraph:
        # Read the whole text.
        text = ''.join(communitiesFromGraph[community])
        wordcloud = WordCloud(stopwords=stopwords).generate(text)
        wordcloud.to_file("{}tagCloud_graph{}_community{}.png".format(saveImages, communitys, community))

        # take relative word frequencies into account, lower max_font_size
        wordcloud = WordCloud(max_words=1000, stopwords=stopwords, margin=10,
                              random_state=1).generate(text)
        wordcloud.to_file("{}tagCloud_graph{}_community{}_withFrenquencies.png".format(saveImages, communitys, community))

"""
saveImages = 'output/tagclouds/GN/'

for community in communityEdgesGN:
    # Read the whole text.
    text = ''.join(communityEdgesGN[community])
    wordcloud = WordCloud(stopwords=stopwords).generate(text)
    wordcloud.to_file("{}tagCloud_community{}.png".format(saveImages, community))

    # take relative word frequencies into account, lower max_font_size
    wordcloud = WordCloud(max_words=1000, stopwords=stopwords, margin=10,
                          random_state=1).generate(text)
    wordcloud.to_file("{}tagCloud_community{}_withFrenquencies.png".format(saveImages, community))














"""

textDetcom = []
with open('output/testClusters.txt') as f:
    content = f.read().splitlines()
    for line in content:
        partition = line.split('|')
        edge = partition[0]
        text = partition[1]
        edgeToCompare = edge.replace('author,','').strip()
        #print edgeToCompare

        if edgeToCompare in detcom:
            textDetcom.append(text)
print len(textDetcom)

stopwords = set(STOPWORDS)

sw = ['10', '11', '2001', 'amto', 'cc', 'know', 'just', 'like', 'friday', 'monday', 'fw', 'week', 'make', 'day',
         'don', 'today', 'use', 'questions', 'october', 'november', 'work', '08', '15', '26', 'time', '2002', 'gas',
         'contract', 'meeting', 'said', 'ees', 'EES', 'NA',
         'tuesday', 'wednesday', 'ect', 'com', 'new', 'let', 'need', 'hou', 'pm', 'pmto', 'mark', 'sent', 'subject',
         'thanks', 'message', 'want', 'thursday', 'think', '0003', '66', '199', '42', '688', '57', 'ga', 'corp',
         'agreement', 'yo', 'you', 'grop', 'yor', 'abot', 'stan', 'come',
         'original', '00', '01', '02', '03', '04', '05', '09', '12', '20', '2000', '30', '646', '713', '853',
         'attached', 'going', 'll', 'mail', 'forward', 'forwarded', 'will', 'enron', 'energy', 'california', 'power',
         'EE', 'ET', 'ee', 'et']

for wor in sw:
    stopwords.add(wor)

# Read the whole text.
text = ''.join(textDetcom)

# Generate a word cloud image
wordcloud = WordCloud(stopwords=stopwords).generate(text)
wordcloud.to_file("gn.png")
# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud)
plt.axis("off")

# take relative word frequencies into account, lower max_font_size
wordcloud = WordCloud(max_words=1000, stopwords=stopwords, margin=10,
               random_state=1).generate(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


"""


























