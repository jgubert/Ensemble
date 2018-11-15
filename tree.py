# -*- coding: utf-8 -*-

class Node:
    def __init__(self):
        self.value = None
        self.sons_index = []
        self.sons = []
        self.attribType = None

    def setValue(self, value):
        self.value = value

    def setType(self, type):
        self.attribType = type

    def addSon(self, Node, key):
        self.sons_index.append(key)
        self.sons.append(Node)

    def __repr__(self):
        return '%s' % (self.value)

"""
  Função para printar a arvore
  
  "Node" é node a ser printado, "level" é a profundidade em que
  este nodo se encontra, "key" é o valor da aresta para os seus filhos
  e "dict" é o dicionario para os valores discretos convertidos em continuos
"""
def printTree(Node):
    if(Node.attribType == "Discrete"):
        printTreeDiscrete(Node, 0, "")
    elif(Node.attribType == "Continuos"):
        printTreeContinuos(Node, 0, "", 0)

def printTreeDiscrete(Node, level, key):
    s = ""
    for i in range(level):
        s = s + "\t"
    s = s + key + " -> "
    if (level == 0):
        s = ""
    print(s + str(Node.value) + " (" + Node.attribType + ")")
    if Node.attribType == "Discrete":
        if (len(Node.sons) != 0):
            for j in range(len(Node.sons)):
                printTreeDiscrete(Node.sons[j], level + 1, Node.sons_index[j])
    elif Node.attribType == "Continuos":
        if (len(Node.sons) != 0):
            for j in range(len(Node.sons)):
                printTreeContinuos(Node.sons[j], level + 1, Node.sons_index[j], j)

def printTreeContinuos(Node, level, key, index_son):
    s = ""
    for i in range(level):
        s = s + "\t"
    if(index_son == 0):
        s = s + "< " + str(key) + " -> "
    elif(index_son == 1):
        s = s + ">= "+ str(key) + " -> "

    if (level == 0):
        s = ""
    print(s + str(Node.value) + " (" + Node.attribType + ")")
    if Node.attribType == "Discrete":
        if (len(Node.sons) != 0):
            for j in range(len(Node.sons)):
                printTreeDiscrete(Node.sons[j], level + 1, Node.sons_index[j])
    elif Node.attribType == "Continuos":
        if (len(Node.sons) != 0):
            for j in range(len(Node.sons)):
                printTreeContinuos(Node.sons[j], level + 1, Node.sons_index[j], j)
