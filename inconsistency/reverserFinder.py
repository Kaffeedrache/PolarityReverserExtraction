#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 25.11.11


class ReverserFinder:
   

   
   """ Dictionary of reversers """
   reverserDict = {}
   
   

   def setReverserExtractor(self, reverserExtractor):
      """
      Method for extracting reversers.
      Note that not all representations work with all extraction methods.
      """
      self.reverserExtractor = reverserExtractor


   def findReversers(self, sentimentWord, tree):
      """
      Check all words in vicinity against reverser dictionary.
      Return number of reversers found in vicinity.
      """
      mycandidates = self.reverserExtractor.extractCandidatesFromContext(sentimentWord, tree)
      numberOfReversers = 0
      for candidate in mycandidates:
         if self.reverserDict.get(candidate) != None:
            #  print "reversed with " + candidate # TEST !!!
            # Count occurrences into reverser dictionary
            self.reverserDict[candidate] += 1
            # 1 reverser found -> + 1
            numberOfReversers += 1
      return numberOfReversers


   def makeReverserDictionary (self, dictionaryFile, cutoffThreshold):
      """
      Static dictionary of negation cues.
      Read in #cutoffThreshold reversers from file (assume sorted!)
      Set cutoff to 0 to read all.
      Expected format:
      <candidate> <space> <score> <various other information>
      SIBLING_not 1.86 / 29 vs 8
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
         check = mydictionary.get(key)  
         if check != None: 
            print "have already in dict: " + key
         mydictionary[key] = 0
         #  print str(i) + " " + key # TEST !!!
         i += 1
      self.reverserDict = mydictionary
      print "Reverser Dictionary contains " + str(i-1) + " entries."
