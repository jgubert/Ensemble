# -*- coding: utf-8 -*-

class Header:
    def __init__(self):
        self.header = []

    def setHeader(self, dataset):
        self.header.append(dataset[0])
        self.header.append(dataset[1])
        dataset.remove(dataset[1])
        dataset.remove(dataset[0])
        #print(*dataset,sep="\n")

    def getHeader(self, dataset):
        new_dataset = []
        new_dataset = list(map(list, self.header))

        #print(*dataset,sep="\n")

        new_dataset += dataset

        #print(*new_dataset,sep="\n")

        #print(*new_dataset,sep="\n")

        #print(self.header)

        return new_dataset
