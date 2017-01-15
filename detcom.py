# -*- coding: utf-8 -*-
__author__ = 'Márcio Vinícius Dias'


import step1, step3, step4, step5, step6, step7


class Main():

    attribSelecteds = {}
    metaPath = []


    def __init__(self):
        pass

    def run(self):
        # ***********************************************************
        # STEP ONE INIT

        xmlFileSchema = 'dataset/esquema_rede_enronNetwork.xml'
        # verticesAndAttribFromSchema = step1.Etp1().getAllVerticesAndAttribFromSchema( xmlFileSchema)
        # print verticesAndAttribFromSchema

        self.metaPath.append('pessoa')
        self.metaPath.append('ocorrencia')

        self.attribSelecteds['pessoa'] = ['idade']
        self.attribSelecteds['ocorrencia'] = ['latitude', 'longitude', 'dataHora']

        xmlFileNetworkGi = 'dataset/rede_exemplo_abordagem.xml'
        nameOfNetwork = 'abordagemNetwork'
        targetVertice = 'pessoa'
        attrbToLabel = 'name'

        categorical = False
        isHomogeneousNetwork = False

        # print "Step1 done!"

        # STEP ONE END
        # ***********************************************************

        # ***********************************************************
        # STEP THREE INIT
        fileToSaveRecords = 'output/records.txt'
        #step3.Etp3().run(xmlFileNetworkGi, self.metaPath, self.attribSelecteds, fileToSaveRecords, isHomogeneousNetwork)

        # STEP THREE END
        # ***********************************************************

        # ***********************************************************
        # STEP FOUR INIT
        fileWithTreatedRecords = 'output/recordsForClustering.txt'
        #step4.Etp4().run(fileWithTreatedRecords, fileToSaveRecords, categorical, isHomogeneousNetwork)

        # STEP FOUR END
        # ***********************************************************

        # ***********************************************************
        # STEP FIVE INIT
        fileWithClusters = 'output/clusters.txt'
        fileInducedGraph = 'output/inducedGraph.txt'
        #step5.Etp5().run(fileWithClusters, fileToSaveRecords, fileInducedGraph, targetVertice, isHomogeneousNetwork)

        # STEP FIVE END
        # ***********************************************************

        # ***********************************************************
        # STEP SIX INIT
        #step6.Etp6().run(fileInducedGraph, targetVertice, nameOfNetwork, attrbToLabel, xmlFileNetworkGi)

        # STEP SIX END
        # ***********************************************************

        # ***********************************************************
        # STEP SEVEN INIT
        step7.Etp7().run(targetVertice, nameOfNetwork, attrbToLabel, xmlFileNetworkGi)

        # STEP SEVEN END
        # ***********************************************************


if __name__ == "__main__":
    print(__doc__)
    Main().run()