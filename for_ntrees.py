# -*- coding: utf-8 -*-

import main_teste
import sys

"""
  Como executar:

  > python3 for_ntrees.py <datafile.format>

"""

filename = str(sys.argv[1])


n_trees = [1, 5, 10, 15, 20]#, 25, 30]#, 50, 100]
for i in n_trees:
    main_teste.main(filename, i)

##main_teste.main(filename, 1)
