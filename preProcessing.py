# -*- coding: utf-8 -*-

"""
  Este arquivo implementa funções de pré-processamento para os arquivos de dados
"""

import csv

"""
  Lê informações de um arquivo de dados
  
  Entradas: datafile = string, nome e formato do arquivo de dados
            
  Saídas: reader = lista de dados lida do arquivo
          -1 = caso dê problema ao criar a lista
"""
# DONE. NEEDS TESTING!
def openDataFile(datafile):
	with open(datafile, newline='') as f:
		delim = csv.Sniffer().sniff(f.read(1024))
		f.seek(0)
		reader = csv.reader(f, delim)
		reader = list(reader)
	
	if (reader):
		return reader
	else:
		return -1
