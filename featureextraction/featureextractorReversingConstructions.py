#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 11.6.12

"""

"""

import utils
import featureextractorConstructions



class FeatureExtractorReversingConstructions (featureextractorConstructions.FeatureExtractorConstructions):
   """ 
   Extract features from a training example.
   """
   
   filename = ""
   
   def getName(self):
      return self.__class__.__name__ + self.filename
      sys.exit()
   
   def makeReverserDictionary (self, dictionaryFile, cutoffThreshold):
      """
      May be overwritten in subclass.
      Read in #cutoffThreshold reversers from file (assume sorted!)
      Expected format:
      <candidate> <tab> <REVERSER>
      SIBLING_not REVERSER
      """
      mydictionary = {}
      inputFile = open(dictionaryFile)
      i = 1
      for line in inputFile:
         if i>cutoffThreshold and cutoffThreshold != 0:
            break
         line = line.strip()
         parts = line.split()
         key = parts[0]
         check = mydictionary.get(key)  # TEST !!!
         if check != None: # TEST !!!
            print "have already in dict: " + key
         mydictionary[key] = 0
         #print str(i) + " " + key # TEST !!!
         i += 1
      self.reverserDict = mydictionary
   
   
   def setInputReversersFile (self, inputReversersFile, threshold = 0):
      self.makeReverserDictionary (inputReversersFile, threshold)
      a = inputReversersFile.rfind("/")
      if a == -1: # not found -> use 0
         a = 0
      a2 = inputReversersFile.rfind("_",a)
      if a2 == -1: # not found -> use / (which may be 0)
         a2 = a
      b = inputReversersFile.rfind(".",a2)
      if b == -1:  # not found -> use last index
         b = len(inputReversersFile)-1
      self.filename = inputReversersFile[a2:b]

   
   def filterListWithReversers (self, sentWord, candidatesList):
      
      list = []
      list.append(self.reverserExtracter.createRepresentationSentWord(sentWord))
      for candidate in candidatesList:
         if candidate != "" and (self.reverserDict.get(candidate) != None):
            list.append(candidate)
      return list
   
      
      
   def doExtraction(self, sentWord, tree, label):
      """
      Label can be utils.labelReversed or utils.labelNonreversed
      """
      
      allcandidates = self.reverserExtracter.extractCandidatesFromContext(sentWord, tree)
         
      #  print "unfiltered"
      #  for c in allcandidates: # TEST !!!
         #  print str(c) # TEST !!!
         
      filteredCandidates = self.filterListWithReversers(sentWord, allcandidates)
      
      #  print "filtered"
      #  for c in filteredCandidates: # TEST !!!
         #  print str(c) # TEST !!!

      return filteredCandidates
