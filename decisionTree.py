# -*- coding: utf-8 -*-
#readFromFile created by João Gubert
#31/08/18

import fileinput
import csv
import tree
import header
import math
import bootstrap
import voting
import errorMeasures

'''
 ######################## FUNÇÕES AUXILIARES #######################
'''

"""
    Função que identifica colunas onde os atributos são continuos e
    calcula o valor médio da coluna.
    Este valor é armazenado na primeira linha da coluna, onde ficava o
    identificador do tipo de atributo.

    Entradas: matriz = dataset onde será calculado as médias de colunas
                        de atributos continuos.
    Não possui saídas.
"""
def collumnAverage(matriz):
    totalrows = len(matriz) #sum(1 for row in matriz)
    for collumn in range(len(matriz[0])):
        if int(matriz[0][collumn]) == 1:
            average = 0
            for row in range(2,totalrows):
                average += float(matriz[row][collumn])
            average = average/(totalrows-2)
            matriz[0][collumn] = round(average,3)


"""
    Função que calcula a entropia da matriz.
    É usada para calcular o Ganho total da matriz.
    Esse valor depois será usada para o cálculo do ID3 de cada atributo.

    Entradas: matriz = dataset onde será calculado o ID3.
    Saídas: info_gain = valor do ID3 da matriz.
"""
def info(matriz):
    value_counter = []
    value_list = []

    for i in range(2,len(matriz)):
        if(value_list.count(matriz[i][len(matriz[1])-1]) == 0):
            value_list.append(matriz[i][len(matriz[1])-1])
            value_counter.append(1)
        else:
            value_counter[value_list.index(matriz[i][len(matriz[1])-1])] += 1

    lines = len(matriz)-2
    collumns =  len(matriz[1])-1

    for i in range(len(value_counter)):
        if value_counter[i] == 0:
            return 1

    info_gain = 0
    for i in range(len(value_counter)):
        info_gain = info_gain -(value_counter[i]/lines)*math.log2(value_counter[i]/lines)


    return info_gain


"""
    Função que calcula o ganho ID3 de um subconjunto.

    Entradas: matriz = dataset onde será calculado os ID3
            atributo = Número da coluna que será calculado o ID3.
    Saídas: info_gain_atrib = valor do ID3 corresponde ao atributo calculado.
"""
def infoGain(matriz, atributo):
    value_counter = []
    value_list = []
    atrib = []
    lines = len(matriz)-2
    collumns =  len(matriz[1])-1



    for i in range(2, lines+2):
        if (value_list.count(matriz[i][collumns]) == 0):
            value_list.append(matriz[i][collumns])



    # Contador de ocorrencias de Sim e Nao para atributos Discretos
    if(float(matriz[0][atributo]) == 0):
        for i in range(2, lines+2):
            if (atrib.count(matriz[i][atributo]) == 0):
                atrib.append(matriz[i][atributo])
                value_counter.append([])

        # cria a matriz para a contagem
        # dimensões são numero de valores para o alvo, por numero
        # de valores para o atributo
        for i in range(len(value_counter)):
            value_counter[i] = [0]*len(value_list)

        # faz a contagem
        for j in value_list:
            for i in range(2, lines+2):
                if (matriz[i][collumns] == j):
                    value_counter[atrib.index(matriz[i][atributo])][value_list.index(j)] += 1



    # Contador de ocorrencias de Sim e Nao para atributos Continuos
    # ESTE AINDA PRECISA ARRUMAR =========================================
    elif(float(matriz[0][atributo]) != 0):
        # append() para iniciar com 2 os contadores
        # indices 0 contadores para menores que Média
        # indices 1 contadores para maiores que média

        #atrib.append(0)
        #atrib.append(0)
        value_counter.append([])
        value_counter.append([])

        for i in range(len(value_counter)):
            value_counter[i] = [0]*len(value_list)
        '''
        yes_counter.append(0)
        yes_counter.append(0)
        no_counter.append(0)
        no_counter.append(0)
        '''
        for i in range(2, lines+2):
            if(float(matriz[i][atributo]) < float(matriz[0][atributo])):
                for j in range(len(value_list)):
                    if(matriz[i][collumns] == value_list[j]):
                        value_counter[0][value_list.index(matriz[i][collumns])] += 1
            elif(float(matriz[i][atributo]) >= float(matriz[0][atributo])):
                for j in range(len(value_list)):
                    if(matriz[i][collumns] == value_list[j]):
                        value_counter[1][value_list.index(matriz[i][collumns])] += 1

    info_gain_atrib = 0

    for i in range(len(value_counter)):
        occurrences = 0
        occurrences = sum(value_counter[i])

        aux = 0
        for j in range(len(value_counter[i])):
            if value_counter[i][j] == 0:
                continue
            aux = aux -(value_counter[i][j]/occurrences)*math.log2(value_counter[i][j]/occurrences)

        info_gain_atrib = info_gain_atrib + (occurrences/lines) * aux

    info_gain_total = info(matriz)
    info_gain_atrib = info_gain_total - info_gain_atrib

    #print("Ganho matriz: " + str(info_gain_total))
    #print("Ganho atrib: " + str(info_gain_atrib))

    return info_gain_atrib



"""
    Função que constrói a árvore de decisão.
    Árvore e feita de forma recursiva, utilizando o algoritmo de ID3
    para encontrar o melhor atributo para cada nodo da árvore.

    Entradas: matriz = dataset que será usada para a construção da árvore.
            node = Node raiz da árvore
    Não tem saída.
"""
def makeTreeAux(matriz, node):
    #yes_counter = 0
    #no_counter = 0

    # lista com os valores para os atributos alvos
    value_list = []
    # lista de contadores para os atributos alvos
    value_counter = []

    # Neste for está engessado "Sim" e "Nao", para os outros datasets
    # teremos que mudar isso
    for i in range(2,len(matriz)):
        if(value_list.count(matriz[i][len(matriz[1])-1]) == 0):
            value_list.append(matriz[i][len(matriz[1])-1])
            value_counter.append(1)
        else:
            value_counter[value_list.index(matriz[i][len(matriz[1])-1])] += 1


    # Quando chega nos nodos folhas, return
    for i in value_list:
        if len(value_counter) == 1:
            node.setValue(i)
            node.setType("Leaf")
            return



    # Encontra o atributo com maior Ganho de Informação
    attrib_chosen = 0
    enthalpy_chosen = 0
    for i in range(len(matriz[1])-1):
        attrib_gain = infoGain(matriz, i)
        if (enthalpy_chosen < attrib_gain):
            attrib_chosen = i
            enthalpy_chosen = attrib_gain


    #DEBUG:
    #print("Atributo escolhido: " + str(matriz[1][attrib_chosen]))
    #print("Entalpia: " + str(enthalpy_chosen) + "\n")


    # caso nodo impuro seta o valor com a maior ocorrencia
    if(enthalpy_chosen == 0):
        value = max(value_list)
        node.setValue(value)
        node.setType("Leaf")
        return



    # Seta valor e tipo do Nodo
    node.setValue(matriz[1][attrib_chosen])
    if float(matriz[0][attrib_chosen]) == 0:
        node.setType("Discrete")
    elif float(matriz[0][attrib_chosen]) != 0:
        node.setType("Continuos")

    # Caso nodo seja Discreto
    if(node.attribType == "Discrete"):
        #popula filhos
        sons = []
        for i in range(2, len(matriz)):
            if (sons.count(matriz[i][attrib_chosen]) == 0):
                sons.append(matriz[i][attrib_chosen])

        #chama função de forma recursiva para os filhos
        for son_key in sons:
            #print(son_key)
            new_data = list(map(list, matriz))

            son_node = tree.Node()
            node.addSon(son_node, son_key)

            # exclui linhas que não tem son_key de new_data
            aux_remove = []
            for i in range(2, len(new_data)):
                if(new_data[i][attrib_chosen] != son_key):
                    aux_remove.append(i)
            for i in reversed(aux_remove):
                new_data.pop(i)


            # exclui coluna do atributo selecionado
            for i in range(len(new_data)):
                new_data[i].pop(attrib_chosen)

            makeTreeAux(new_data, son_node)

    elif(node.attribType == "Continuos"):

        new_data_great = list(map(list, matriz))
        new_data_less = list(map(list, matriz))

        son_node_great = tree.Node()
        son_node_less = tree.Node()

        node.addSon(son_node_less, matriz[0][attrib_chosen])
        node.addSon(son_node_great, matriz[0][attrib_chosen])

        # Deixa na matriz apenas valores menores que a Média
        aux_remove = []
        for i in range(2, len(new_data_less)):
            if (float(new_data_less[i][attrib_chosen]) >= new_data_less[0][attrib_chosen]):
                aux_remove.append(i)
        for i in reversed(aux_remove):
            new_data_less.pop(i)

        for i in range(0, len(new_data_less)):
            new_data_less[i].pop(attrib_chosen)

        # Deixa na matriz apenas os valores maiores ou iguais que a Média
        aux_remove2 = []
        for i in range(2, len(new_data_great)):
            if (float(new_data_great[i][attrib_chosen]) < new_data_great[0][attrib_chosen]):
                aux_remove2.append(i)
        for i in reversed(aux_remove2):
            new_data_great.pop(i)

        for i in range(0, len(new_data_great)):
            new_data_great[i].pop(attrib_chosen)


        makeTreeAux(new_data_less, son_node_less)
        makeTreeAux(new_data_great, son_node_great)


"""
    Chamada para ser usada fora do escopo decisionTree.
    Função é chamada para criar uma árvore de decisão a partir de um
    dataset.
    Antes de fazer a criação, é feita a média dos atributos continuos.

    Entradas: matriz = dataset que será usada para criar a árvore.
            node = Nodo raiz da árvore.
    Não tem saída.
"""
def makeTree(matriz, node):
    collumnAverage(matriz)
    '''
    print("DEBUG: Impressão da Matriz")
    print(*matriz,sep="\n")
    '''
    makeTreeAux(matriz,node)


"""
    Percorre a árvore de decisão, classificando uma nova entrada.

    Entradas: node = Nodo raiz da árvore a ser percorrida.
            entry = Entrada de teste a ser classificada.
    Saídas = Retorna uma string, a classificação "Sim" ou "Não".
"""
def classify(node, entry):
    if(node.attribType == "Leaf"):
        return (node.value)

    index = -1
    index2 = -1
    for i in range(len(entry[0])):
        if(entry[1][i] == node.value):
            index = i
            #print(node.value)
    if node.attribType == "Discrete":
        for son_key in node.sons_index:
            if entry[2][index] == son_key:
                index2 = node.sons_index.index(son_key)
                #print("\t->" + node.sons_index[index2])
                break
    elif node.attribType == "Continuos":
        for son_key in reversed(range(len(node.sons_index))):
            if(float(entry[2][index]) >= float(node.sons_index[son_key])):
                index2 = 1
                #print("\t->" + "  >= " + str(node.sons_index[son_key]))
                break
            elif(float(entry[2][index]) < float(node.sons_index[son_key])):
                index2 = 0
                #print("\t->" + "  < " + str(node.sons_index[son_key]))
                break
    if(index == -1 and index2 == -1):
        return ("Inconclusivo")
    return classify(node.sons[index2], entry)

"""
    Faz a chamada do bootstrap N vezes, com o conjunto de dados dataset.

    Entradas: dataset = fold contendo os dados de treinamento
    Saídas = Lista com N árvores
"""
def makeForest(dataset, n, header):
    #print(" === Função makeForest")
    list_trees = []
    bootstrap_list = []

    #print("Dataset:")
    #print (*dataset,sep="\n")

    for i in range(n):
        #print("Criando Bootrap")
        bootstrap_list.append(bootstrap.bootstrap(dataset,len(dataset)))
        #print("Bootstrap criado")
        new_tree = tree.Node()
        bootstrap_list[i] = header.getHeader(bootstrap_list[i])
        #print(" ======== Conteudo do bootstrap list ========")
        #print (*bootstrap_list,sep="\n")
        #print("===============================================")

        makeTree(bootstrap_list[i], new_tree)

        #print("Arvore Criada")

        list_trees.append(new_tree)

    return list_trees

"""
    Recebe uma lista de árvores gerada, passando o classificador em cada uma,
    armazenando os resultados das classificações em uma lista

    Entradas: dataset = fold contendo os dados de treinamento
              list_trees = lista de árvores gerada
    Saídas = Lista com N votos
"""
def startClassification(testsetoriginal, list_trees, header, value_classes):
    votelist = []   # lista contendo as votações das árvores para cada instância do conj de teste
    final_votes = []    # lista contendo as votações finais das árvores
    target_attrs_from_testset = []
    target_test = []
    testset = list(map(list, testsetoriginal))
    
    # coleta dos atributos alvo do conj de teste, armazenando em uma lista auxiliar, removendo-os do conj de treinamento
    rowsize = len(testset[0])-1

    for i in range(len(testset)):
        target_attrs_from_testset.append([testset[i][rowsize]])
        testset[i].pop(rowsize)

    # processamento das classificações das árvores, obtendo seus votos, analisando-os
    for i in range(len(testset)):

        # inicializa as listas vazias
        votelist.append([])
        final_votes.append([])

        target_test = [testset[i]]

        # colocando o cabeçalho em cada entrada de teste
        testset[i] = header.getHeader(target_test)

        for j in range(len(list_trees)):
            # cria a lista de votações de cada árvore da floresta
            votelist[i].append(classify(list_trees[j], testset[i]))

        # coleta as votações finais de cada árvore, para todas as instâncias do conj de teste
        final_votes[i].append(voting.votingAnalysis(votelist[i]))

    '''
    print("TARGET ATTRS:")
    print(*target_attrs_from_testset, sep="\n")
    print("FINAL VOTES:")
    print(*final_votes, sep="\n")
    print("VOTE LIST:")
    print(*votelist, sep="\n")
    '''

    errorMeasures.processConfusionMatrix(target_attrs_from_testset, final_votes, value_classes)
    
    #errorMeasures.printConfusionMatrix()
    
    '''
    # DEBUG: impressão das medidas de erro
    print(errorMeasures.accuracy(len(testset)))
    print(errorMeasures.error(len(testset)))
    print(errorMeasures.recall())
    print(errorMeasures.precision())
    '''
    '''
    DEBUG: Impressão de 'votelist'
    print("================ VOTELIST: ================")
    print(*votelist,sep="\n")
    '''
    '''
    DEBUG: Impressão de 'final_votes'
    print("================ FINALVOTES: ================")
    print(*final_votes,sep="\n")
    '''
    return (final_votes)
