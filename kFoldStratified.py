# -*- coding: utf-8 -*-

"""
  Este arquivo implementa o K-Fold Estratificado
"""

from operator import itemgetter, attrgetter
import csv
import bootstrap
import header
import decisionTree


"""
  Faz a proporção de elementos

  Entradas: numelements = inteiro, quantidade arbitrária de elementos
            total = inteiro, quantidade total de elementos

  Saídas: número inteiro = é a proporção entre 'numelements' e 'total'
"""
def dataRatio(numelements, total):
    return (numelements / total)

"""
  Conta quantos valores diferentes de atributos-alvo existem

  Entradas: dataset = lista de listas, é o conj de dados

  Saídas: possible_attr = lista, contendo todos os possíveis atributos do conj de dados
"""
def countPossibleAttributes(dataset):
    possible_attr = []
    column_amount = len(dataset[0])
    
    for i in range(len(dataset)):
        if (possible_attr.count(dataset[i][column_amount-1]) == 0):
            possible_attr.append(dataset[i][column_amount-1])
    
    return possible_attr

"""
  Conta quantas ocorrências de cada valor do atributo alvo existem

  Entradas: dataset = lista de listas, é o conj de dados

  Saídas: lista de listas = concatenação de listas, que retorna as listas dos atributos "sim" e "nao"
"""
def countAttributesAmount(dataset):
    # coleta a coluna com atr alvo
    objattr = len(dataset[0])-1

    # classifica de acordo com a última coluna da matriz, que é o atributo alvo
    dataset = sorted(dataset, key = itemgetter(objattr))


    # contagem genérica de atributos-alvo
    possible_attr = countPossibleAttributes(dataset)
    list_classes = []
    
    for i in range(len(possible_attr)):
        list_classes.append([])
        
    for i in range(len(dataset)):
        for j in range(len(possible_attr)):
            if (dataset[i][objattr] == possible_attr[j]):
                list_classes[j].append(dataset[i])
    
    #print("LEN CLASSES")
    #print(len(list_classes))
    
    if (list_classes):
        return list_classes
    else:
        return -1

"""
  Faz o K-Fold Estratificado

  Entradas: dataset = lista de listas, é o conj de dados
            n_folds = inteiro, quantidade de folds a serem gerados
  Saídas: fold_list = lista de listas, é a lista de folds gerada
"""
def kFoldStratified(dataset, n_folds):
    fold_list = []

    # Conta quantas ocorrências de cada valor do atributo alvo existem
    list_attrs = countAttributesAmount(dataset)
    
    #print(*list_attrs)
    total_elems = len(dataset)

    idx = -1
    prop = 0
    temp_prop = 0
    list_prop = []
    
    #print(len(list_attrs))
    # Calcula a proporção de cada atributo alvo existente no dataset
    for i in range(len(list_attrs)):
        list_prop.append(dataRatio(len(list_attrs[i]), total_elems))
    
    #
    #print(*list_prop,sep="\n")
    
    # calcula a quantidade de elementos por fold
    elems_per_fold = total_elems // n_folds

    # Cria n folds de forma estratificada
    for i in range(n_folds):
        fold_list.append([])
        for j in range(len(list_attrs)):
            attr_amount = int(list_prop[j] * elems_per_fold)

            for k in range(attr_amount):
                if (list_attrs[j]):
                    fold_list[i].append(list_attrs[j][0])
                    list_attrs[j].remove(list_attrs[j][0])

    # DEBUG: impressão da lista de folds
    ''''
    for i in range(len(fold_list)):
        for j in range(len(fold_list[i])):
            print("\n")
            print(*fold_list[i],sep="\n")
    '''
    '''
    for i in fold_list:
        print(fold_list.index(i))
        print(*i, sep="\n")
    '''
    return (fold_list)

"""
  Faz o K-Fold Estratificado de forma iterativa

  Entradas: fold_list = lista de listas, é a lista de folds gerada
            n_folds = inteiro, quantidade de folds a serem gerados
  Saídas: ?
"""
def kFoldStratifiedIterations(fold_list, n_folds):

    for i in range(n_folds):
        aux_fold_list = []
        test_fold = []
        training_folds = []

        # copia a lista de folds para uma lista auxiliar
        aux_fold_list = list(map(list, fold_list))

        # pega o fold de teste
        test_fold = aux_fold_list[i]

        #print (*aux_fold_list,sep="\n")

        # pega os folds de treinamento
        aux_fold_list.remove(test_fold)

        # transforma lista de listas em uma lista só, para facilitar implementação
        for j in aux_fold_list:
            training_folds += j

        # DEBUG: impressão do test fold e dos training folds
        #print("\n ======== TEST FOLD ======== \n")
        #print(*test_fold,sep="\n")
        #print("\n ======== TRAINING FOLDS ======== \n")
        #print(*training_folds,sep="\n")

        # Funcao para fazer o bootstrap e criar a arvore
        #makeForest(training_folds, 1)
