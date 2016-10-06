#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 11.6.12

"""

"""

import utils
import featureextractor

import sys
sys.path.append("../base")
import contextFinderTrees


class FeatureExtractorIkeda (featureextractor.FeatureExtractorWordWise):
   """ 
   Extract features from a training example.
   Features are words in context
   """
 
   k = 3
   
   
   """
   Set to TRUE if the sentiment word itself should be included in the features.
   """
   useSentimentWord = True
   
   def doExtraction(self, node, tree, label):
      #  print tree.getWholeSentence()
      #  tree.printTree()
      sentimentWordID = node.getID()
      context = []
      if self.useSentimentWord:
         context.append(node.getWord())
      #  print node.getWord() + str(sentimentWordID)
      for i in range(sentimentWordID-self.k, sentimentWordID+self.k+1):
         newnode = tree.getNodeInSentence(i)
         #  print str(i) + " " + str(newnode)
         if newnode != None and i != sentimentWordID:
            word = newnode.getWord()
            context.append(word)
      #  print context
      return context
   
   