#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preprocess import cleanText
import networkx
import itertools
import math
import json

sentenceDictionary = {};

def getSimilarity(sentenceID1, sentenceID2):
    commonWordCount = len(set(sentenceDictionary[sentenceID1]) & set(sentenceDictionary[sentenceID2]))
    denominator = math.log(len(sentenceDictionary[sentenceID1])) + math.log(len(sentenceDictionary[sentenceID2]))
    return commonWordCount/denominator if denominator else 0

def generateGraph(nodeList):
    graph = networkx.Graph()
    graph.add_nodes_from(nodeList)
    edgeList = list(itertools.product(nodeList, repeat=2))
    for edge in edgeList:
        graph.add_edge(edge[0], edge[1], weight=getSimilarity(edge[0], edge[1]))
    return graph


def printDictionary():
    for key,val in sentenceDictionary.iteritems():
        print str(key) + " : " + " ".join(sentenceDictionary[key])

def textRankSimilarity(summarySentenceCount):
    fileName = "../Marathi/documents/doc1"
    global sentenceDictionary
    sentenceDictionary, sentences ,size = cleanText(fileName)
    #printDictionary()
    graph = generateGraph(list(sentenceDictionary.keys()))
    pageRank = networkx.pagerank(graph)
    return sorted(pageRank, key=pageRank.get, reverse=True)[:summarySentenceCount]


if __name__ == "__main__":
    print(textRankSimilarity(5))