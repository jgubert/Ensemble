# -*- coding: utf-8 -*-

"""
  Este arquivo tem as funções que calculam erros para atributos discretos e contínuos
"""

"""
  Alguns dados precisam ser coletados da matriz de confusão. Talvez a mesma possa ser representada como
  confusionMatrix[2][2] de inteiros
"""

confusionMatrix = []
resultMatrix = []

"""
  Calcula a acurácia (accuracy) do modelo
  Entradas: n = tamanho do conjunto de dados
  Saídas: número real
"""
# DONE. NEEDS TESTING!
def accuracy(n, num_classes):
    VP = 0
    VN = 0
    total_classes = len(num_classes) 
    for i in range(total_classes):
        VP += resultMatrix[i][0][0]
        VN += resultMatrix[i][1][1]
        
    return ((VP + VN) / (n * total_classes))

"""
  Calcula a taxa de erro (error) do modelo
  Entradas: n = tamanho do conjunto de dados
  Saídas: número real
"""
def error(n, num_classes):
    return (1 - accuracy(n, num_classes))

"""
  Calcula a revocação (recall) do modelo
  Saídas: número real
"""
def recall(num_classes):
    VP = 0
    FN = 0
    aux = 0
    total_classes = len(num_classes)
    
    if (total_classes == 2):
        VP = confusionMatrix[0][0]
        FN = confusionMatrix[0][1]
        return (VP / (VP + FN))
    else:        
        for i in range(total_classes):
            VP = 0
            FN = 0
            VP += resultMatrix[i][0][0]
            FN += resultMatrix[i][0][1]
            aux += (VP / (VP + FN))
        
        return (aux / total_classes)


"""
  Calcula a precisão (precision) do modelo
  Saídas: número real
"""
def precision(num_classes):
    VP = 0
    FP = 0
    aux = 0
    total_classes = len(num_classes) 
    
    if (total_classes == 2):
        VP = confusionMatrix[0][0]
        FP = confusionMatrix[1][0]
        return (VP / (VP + FP))
    else:
        for i in range(total_classes):
            VP = 0
            FP = 0
            VP += resultMatrix[i][0][0]
            FP += resultMatrix[i][1][0]
            aux += (VP / (VP + FP))
        
        return (aux / total_classes)

"""
  Calcula o F-Measure do modelo
  Entradas: prec = número real, resultado da chamada da função 'prec()'
            rev = número real, resultado da chamada da função 'rev()'
            beta = número real, ênfase do problema (prec ou rev)
  Saídas: número real
"""
def FMeasure(prec, rev, beta):
    return (1 + beta**2) * (prec * rev) / ((beta**2 * prec) + rev)

"""
  Calcula as células da matriz de confusão (cumulativamente)
  Entradas: target_attrs_from_testset = lista de strings, são os atributos alvo do conj de teste
            final_votes = lista de strings, são as votações das árvores geradas no ensemble
  Saídas: matriz, contendo os valores em suas células
"""
def processConfusionMatrix(target_attrs_from_testset, final_votes, value_classes):
    #print(len(value_classes))
    #print(final_votes)
    
    ## É ISSO?! NÃO PODE SER TÃO SIMPLES ASSIM!
    for i in range(len(final_votes)):
        confusionMatrix[value_classes.index(target_attrs_from_testset[i][0])][value_classes.index(final_votes[i][0])] += 1

"""
  Compacta as células da matriz de confusão em uma matriz de resultados
  Entradas: class_num = lista de strings, são os diferentes atributos alvo do conj de teste
  Saídas: matriz, contendo os valores acumulados em suas células
"""
def compactConfusionMatrix(class_num):
    
    #print(len(resultMatrix))
    #print(len(class_num))
    if (len(resultMatrix) == len(class_num)):
        resetResultMatrix()
    
    #print(resultMatrix)
    #print(len(resultMatrix))
    
    for k in range(len(class_num)):
        
        initResultMatrix()
        
        for i in range(len(confusionMatrix)):
            for j in range(len(confusionMatrix)):
                # VP
                if (i == k and j == k):
                    resultMatrix[k][0][0] += confusionMatrix[k][k]
                # VN
                if (i != k and j != k):
                    resultMatrix[k][1][1] += confusionMatrix[i][j]
                # FP
                if (i == k and j != k):
                    resultMatrix[k][1][0] += confusionMatrix[i][j]
                # FN
                if (i != k and j == k):
                    resultMatrix[k][0][1] += confusionMatrix[i][j]

# Funções para Confusion Matrix
def printConfusionMatrix():
    print(*confusionMatrix,sep="\n")

def initConfusionMatrix(num_classes):
    for i in range(num_classes):
        confusionMatrix.append([])
        for j in range(num_classes):
            confusionMatrix[i].append(0)
      
def resetConfusionMatrix(num_classes):
    while(len(confusionMatrix)):
        confusionMatrix.pop()
'''
    for i in range(num_classes):
        for j in range(num_classes):
            confusionMatrix[i][j] = 0
'''

# Funções para Result Matrix
def printResultMatrix():
    print(*resultMatrix,sep="\n")
    
def initResultMatrix():
    resultMatrix.append([[0,0],[0,0]])

def resetResultMatrix():
    while(len(resultMatrix)):
        resultMatrix.pop()
