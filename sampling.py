# -*- coding: utf-8 -*-

"""
  Este arquivo implementa a funcionalidade de amostragem de n atributos mais relevantes, de acordo com o ganho de informação calculado para cada um deles
"""

import decisionTree

"""
  Coleta todas as colunas da matriz, faz um ordenamento baseado no ganho de informação, e obtém os 'n' mais relevantes

  Entradas: dataset = lista de listas, representa as informações do arquivo de dados lido
            n = inteiro positivo, representa a quantidade de colunas com maiores ganhos de informação
  Saídas: sampleList = lista de listas, corresponde às 'n' colunas mais relevantes de acordo com o cálculo do ganho de informação, ordenadas de forma decrescente
          -1 = inteiro, caso dê problema ao criar as listas
"""
def sampleAttributes(dataset, n):

    # devemos retornar uma lista de n colunas mais relevantes, ou somente a coluna mais relevante (ver enunciado)?
    sampleList = []

    # lista que guarda os indices das colunas com maior ID3
    index_greater_ID3 = []


    ordened_ID3 = []
    ordened_ID3.append(0)

    # lista que guarda o ID3 de cada coluna
    ID3_collunm = []

    decisionTree.collumnAverage(dataset)

    for i in range(len(dataset[1])-1):
        ID3_collunm.append(decisionTree.infoGain(dataset, i))

    for i in range(len(ID3_collunm)):
        for j in range(len(ordened_ID3)):
            if ID3_collunm[i] >= ordened_ID3[j]:
                ordened_ID3.insert(j, ID3_collunm[i])
                break


    for i in range(len(ordened_ID3)-1):
        index_greater_ID3.append(ID3_collunm.index(ordened_ID3[i]))


    while (int(n) < int(len(index_greater_ID3))):
        index_greater_ID3.pop()


    for i in range(len(dataset)):
        sampleList.append([])
        for j in index_greater_ID3:
            sampleList[i].append(dataset[i][j])

    for i in range(1,len(dataset)):
        sampleList[i].append(dataset[i][len(dataset[0])])


    if(sampleList):
        return sampleList
    else:
        return -1
