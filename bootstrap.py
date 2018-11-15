# -*- coding: utf-8 -*-

"""
  Este arquivo implementa o bootstrap (com reposição)
"""

import random

"""
  Faz o bootstrap
  Entradas: dataset = lista, representa informações do arquivo de dados lido
            setsize = inteiro positivo, tamanho da lista de treinamento do bootstrap a ser gerada
  Saídas: traininglist = lista de treinamento
          -1 = caso dê problema ao criar as listas
"""
def bootstrap(dataset, setsize):
	traininglist = []	# lista de elementos para treinamento, que armazenará instâncias do .csv

	# adiciona elementos selecionados aleatoriamente (com reposição) da tabela .csv para a lista de Treinamento
	traininglist = random.choices(dataset, k = setsize)
	
	# DEBUG: impressão de elementos de 'traininglist'
	#print("\n\n ==== TRAININGLIST ====\n")
	#print(*traininglist,sep='\n')
	
	if (traininglist):
		return traininglist
	else:
		return -1

"""
  Faz o bootstrap N vezes
  Entradas: dataset = lista, representa informações do arquivo de dados lido
            setsize = inteiro positivo, tamanho da lista de treinamento do bootstrap a ser gerada
            num_iterations = inteiro positivo, número de vezes que o bootstrap será executado
  Saídas: bootstrap_list = lista de bootstraps gerados
          -1 = caso dê problema ao criar as listas
"""
def bootstrapIteration(dataset, setsize):
    bootstrap_list = []
    
    for i in range(setsize):
        bootstrap_list.append(bootstrap(dataset, setsize))
        
    if (bootstrap_list):
        return (bootstrap_list)
    else:
        return -1
