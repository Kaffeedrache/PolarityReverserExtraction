#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 11.6.12

"""

"""

import featureextractor

import sys
sys.path.append("../base")
import contextFinderTrees



class FeatureExtractorConstructions (featureextractor.FeatureExtractorWordWise):
   """ 
   Extract features from a training example.
   """
   
   
   def setReverserExtracter (self, reverserExtracter):
      self.reverserExtracter = reverserExtracter      


   def doExtraction(self, sentWord, tree, label):
      allcandidates = self.reverserExtracter.extractCandidatesFromContext(sentWord, tree)
      allcandidates.insert(0,self.reverserExtracter.createRepresentationSentWord(sentWord))
      return allcandidates

