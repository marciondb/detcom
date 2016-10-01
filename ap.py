print(__doc__)

from sklearn.cluster import AffinityPropagation
import numpy as np
import math
import collections

def getNumberFromDiference(S1, S2):
    difference = list(S1.symmetric_difference(S2))
    result = (len(S1)+len(S2))-len(difference)

    return result

def bagOfWordsDistance(line1, line2):
    value = 0.0
    for index in range(0, len(line1) - 1):
        if isinstance( line1[index], int):
            value += (line1[index] - line2[index]) ** 2
        else:
            value += getNumberFromDiference(line1[index], line2[index])

    result = math.sqrt(value)

    return result

def categoricalDist(line1, line2, isHomogeneousNetwork):

    if isHomogeneousNetwork:
        return bagOfWordsDistance(line1, line2)

    value = 0.0
    for index in range(0, len(line1)-1):
        #is categorical
        if isinstance( line1[index], int ) and isinstance( line2[index], int ):
            if (line1[index] == line2[index]):
                value += 0.0
            else:
                value += 1.0
        else:
            value += (line1[index]-line2[index])**2

    result = math.sqrt(value)

    return result

def getLineFromList(list, indexLine):

    cont = 0
    for line in list:

        if cont == indexLine:
            return line
            break
        cont+=1

    return "erro"


def makeCategoricalX(X_temp, isHomogeneousNetwork):

    squareMatriz = np.zeros(shape=(len(X_temp),len(X_temp)))
    contLine = 0
    contCol = 0

    for line in squareMatriz:

        X_line1 = getLineFromList(X_temp, contLine)

        for col in line:

            if contCol == contLine:
                squareMatriz[contLine, contCol] = 0.0
            else:
                X_line2 = getLineFromList(X_temp, contCol)
                squareMatriz[contLine, contCol] = categoricalDist(X_line1, X_line2, isHomogeneousNetwork)

            contCol+=1
        contCol = 0
        contLine+=1
    #print squareMatriz
    return squareMatriz

def recoveryClusterFromX(X,class_members):

    cont = 0
    cluster = []
    for index in class_members:
        if index:
            cluster.append(X[cont])
        cont+=1

    return cluster


def saveToTxtBagOfWords(file, newCluser_k):

    for item in newCluser_k:
        aux=''
        for col in item:
            aux += col.__str__()+' '

        file.write('{0}\n'.format(aux.rstrip()))



def ap(file_name, categorical, isHomogeneousNetwork):

    ##############################################################################
    # Generate data
    if categorical:
        loadFromFile = True
        X_temp = buildAsCategorical(file_name)

        if loadFromFile:
            X = np.loadtxt('output/x.txt')
        else:
            X = makeCategoricalX(X_temp, isHomogeneousNetwork)
            np.savetxt('output/x.txt',X, fmt='%1.3e')
    else:
        X = _buildV(file_name)

    ##############################################################################
    # Compute Affinity Propagation
    #af = AffinityPropagation(preference=-15, damping=0.9, convergence_iter=200, max_iter=2000).fit(X)
    if categorical:
        af = AffinityPropagation(affinity='precomputed',preference=-3, damping=0.9, convergence_iter=200, max_iter=2000).fit(X)
    else:
        af = AffinityPropagation(preference=-15, damping=0.9, convergence_iter=200, max_iter=2000).fit(X)

    cluster_centers_indices = af.cluster_centers_indices_
    #affinity_matrix = af.affinity_matrix_
    #print affinity_matrix
    labels = af.labels_
    n_clusters_ = len(cluster_centers_indices)

    print('Estimated number of clusters: %d' % n_clusters_)

    ##############################################################################
    # Plot result
    #import matplotlib.pyplot as plt
    from itertools import cycle

    #plt.close('all')
    #plt.figure(1)
    #plt.clf()

    file = open("output/clusters.txt", "w")

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        class_members = labels == k
        #cluster_center = X[cluster_centers_indices[k]]
        #plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
        #plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
        #         markeredgecolor='k', markersize=14)

        #print("\nCluster: %d\n" % k)

        file.write('cluster: {0}\n'.format(k))

        if not categorical:
            cluster_k = X[class_members]
            np.savetxt(file, cluster_k, fmt='%1.5e')

            #print cluster_k
        else:
            newCluser_k = recoveryClusterFromX(X_temp, class_members)
            if isHomogeneousNetwork:
                saveToTxtBagOfWords(file, newCluser_k)
            else:
                np.savetxt(file, newCluser_k, fmt='%1.5e')



            #print newCluser_k

        #for x in X[class_members]:
        #   plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

    file.close()

    #plt.title('Estimated number of clusters: %d' % n_clusters_)
    #plt.show()

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def RepresentsFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def treatStringVetToNumber(vet):

    newVet = []
    for item in vet:
        if RepresentsInt(item):
            newVet.append(int(item))
        elif RepresentsFloat(item):
            newVet.append(float(item))
        else:
            newVet.append(eval(item))

    return newVet

#as is possible to have categorical values and noncategorical values, need to create this matrix
# for the categoricalDist function
#_buildV transform all values to float, but I want int (categorical) and float (noncategorical)
def buildAsCategorical(file_):

    vetResult = []
    with open(file_) as f:
        content = f.read().splitlines()
        for line in content:
            partitionList = line.split('   ')
            partitionList.pop(0)

            partitionList = treatStringVetToNumber(partitionList)
            vetResult.append(partitionList)

    return vetResult


def _buildV(file_):
    darry = np.loadtxt(file_)

    return darry

if __name__ == "__main__":
    ap()
