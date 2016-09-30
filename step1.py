__author__ = 'marcio'

from lxml import  objectify

class Etp1():

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

