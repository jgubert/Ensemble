# -*- coding: utf-8 -*-

"""
  Função main()
"""

import fileinput
import csv
import math
import sys

import bootstrap
import decisionTree
import errorMeasures
import header
import kFoldStratified
import preProcessing
import tree
import voting
import random
import sampling

"""
  Como executar:

  > python3 main_teste.py <datafile.format> <num_trees>

"""
def main(filename, n_trees):
    # coletando os argumentos
    #filename = str(sys.argv[1])
    #n_trees = int(sys.argv[2])

    n_folds = 10
    list_forest = []

    # definindo seed
    random.seed(1)

    # abrindo o arquivo
    #datafile = preProcessing.openDataFile(filename)

    # TO DO: FIX THIS PIECE OF CODE
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        datafile = list(csv_reader)

    #print("\n============= DATA FILE =============")
    #print (*datafile,sep="\n")

    m = math.ceil(math.sqrt(len(datafile[1])))


    # Fazendo amostragem para as m colunas com maior ganho
    if m > len(datafile[0]):
        print("valor m é maior que quantidade de atributos")
        return -1

    datafile = sampling.sampleAttributes(datafile, m)
    

    # Setando o cabeçalho
    dataheader = header.Header()

    dataheader.setHeader(datafile)



    # Lista que vai armazenar os folds
    fold_list = []
    fold_list = kFoldStratified.kFoldStratified(datafile, n_folds)

    # Quantidade de entradas testadas é o tamanho de um fold
    # vezes a quantidade de testes que sera feito
    tam_testfold = len(fold_list[0]) * n_folds

    '''
    print("\n============= FOLD lIST =============")
    for i in range(n_folds):
        print("\nFold N " + str(i))
        print(*fold_list[i], sep="\n")
    '''
    # inicializa a matriz de confusão
    value_classes = kFoldStratified.countPossibleAttributes(datafile)
    errorMeasures.initConfusionMatrix(len(value_classes))
    
    # chamando o bootstrap (K-Fold posteriormente)
    for i in range(n_folds):
        aux_fold_list = []
        test_fold = []
        training_folds = []

        # copia a lista de folds para uma lista auxiliar
        aux_fold_list = list(map(list, fold_list))

        # pega o fold de teste
        test_fold = aux_fold_list[i]
        
        # DEBUG
        #print(*test_fold,sep="\n")
        #print("\n")
        #

        #print (*aux_fold_list,sep="\n")

        # pega os folds de treinamento
        aux_fold_list.remove(test_fold)

        # transforma lista de listas em uma lista só, para facilitar implementação
        for j in aux_fold_list:
            training_folds += j

        list_forest.append(decisionTree.makeForest(training_folds, n_trees, dataheader))
        final_votes = decisionTree.startClassification(test_fold, list_forest[i], dataheader, value_classes)


    # DEBUG: impressão das medidas de erro
    errorMeasures.compactConfusionMatrix(value_classes)
    print("\n\n ===========================================")
    print("Num Folds: " + str(n_folds))
    print("Num Trees: " + str(n_trees))
    print("RESULT MATRIX:")
    errorMeasures.printResultMatrix()
    print("CONFUSION MATRIX:")
    errorMeasures.printConfusionMatrix()
    print("Accuracy: ")
    print(errorMeasures.accuracy(tam_testfold,value_classes))
    print("Error: ")
    print(errorMeasures.error(tam_testfold,value_classes))
    print("Recall: ")
    print(errorMeasures.recall(value_classes))
    print("Precision: ")
    print(errorMeasures.precision(value_classes))
    print("FMeasure: ")
    print(errorMeasures.FMeasure(errorMeasures.precision(value_classes), errorMeasures.recall(value_classes), 1))
    print("===========================================")

    # Limpando Matriz de Confusão
    errorMeasures.resetConfusionMatrix(len(value_classes))

    '''
    #(*)
    # DEBUG: impressão das florestas

    for i in range(len(list_forest)):
        for j in range(len(list_forest[i])):
            #for k in range(len(list_forest[i][j])):
                #tree.printTree(list_forest[i][j][k])
            tree.printTree(list_forest[i][j])
    '''

'''
  Executando a main()
'''
#main()
