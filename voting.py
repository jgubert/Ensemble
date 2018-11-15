# -*- coding: utf-8 -*-

"""
  Este arquivo implementa a funcionalidade de votação
"""

"""
  Coleta os votos das árvores, e seleciona qual foi o mais frequente para fazer a classificação.
  Caso haja empate, retorna o 1º elemento mais frequente
  
  Entradas: votelist = lista de inteiros, contendo os votos de cada árvore do ensemble
            
  Saídas: valor = string, elemento mais frequente, caso tenha pelo menos 1 elemento na lista de votações
          -1 = inteiro, caso a lista de votações seja vazia
"""
# DONE. NEEDS TESTING!
def votingAnalysis(votelist):
	if(votelist):
		return (max(set(votelist), key=votelist.count))
	else:
		return -1
