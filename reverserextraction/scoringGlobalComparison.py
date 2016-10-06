#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 19.10.11

"""

"""


import scoring

import sys
sys.path.append("..")
import utils


# ----- Scorers that need comparison data calculated once globally -----

class AbstractGlobalComparisonScorer(AbstractCandidateScorer):
   
   
   def calculateGlobalComparisonSet(self, corpusFilenames):
      """ 
      Calculates a set with candidates to compare to.
      Abstract method.
      """
      self.comparisonSet = {}


class GlobalComparisonScorerTfIdf(AbstractGlobalComparisonScorer):
   """
   Score is the frequency relative to a global comparison set.
   """
   
   def addWord(self, word):
      # Normalize
      candidate = utils.filterAndNormalizeCandidate(word)
      #  print "adding ---" + candidate + "---" # TEST
      
      # Ignore the empty string as a candidate
      if candidate == "":
         return
      # Count occurrences
      occurrences = self.comparisonSet.get(candidate)
      if occurrences != None: 
         #  word in candidates -> add 1 to count
         self.comparisonSet[candidate] = occurrences + 1
      else: # not in candidates -> set 1
         self.comparisonSet[candidate] = 1
      
   
   def calculateGlobalComparisonSet(self, corpusFilenames):
      """ 
      Calculates a set with candidates to compare to.
      Abstract method.
      """
      #  print "Calculate global set"
      self.comparisonSet = {}
      self.lineNo = 0
      for filename in corpusFilenames:
         inputFile = open(filename)
         for line in inputFile:
            line = line.strip()
            line = line.decode('latin-1','strict')
            line = line.encode('utf-8')
            
            if line == "" or line[0] == "*":
               continue
            
            parts = line.split("##")
            
            if len(parts) > 1: # label found -> tokenize
               sentence = parts[1]
               words = sentence.split()
            else: # title
               line = line.replace("[t]","")
               words = line.split()
            
            self.lineNo += 1
            
            # Add words, add every word only once per line
            # -> convert to set
            for word in set(words):
               self.addWord(word)
         
      #  for a in self.comparisonSet:
         #  print a + " -> " + str(self.comparisonSet.get(a))
      #  print self.lineNo
      
   
   def scoreCandidateX(self,key,value):
      """
      Takes a candidate X and returns its score.
      TODO
      """
      # Get word out of candidate representation
      parts = key.split("_")
      if len(parts) > 1: 
         word = parts[len(parts)-1]
      else:
         word = key
      #  print "search word "  + word + " for key " + key # TEST !!!
      compareValue = self.comparisonSet.get(word)
      if compareValue == None:
         compareValue = 0
      if compareValue != 0:
         # Calculate tf-idf:
         # tf = value
         # idf = log (N / compareValue), N = number of documents (i.e. lines)
         idf = float(self.lineNo) / float(compareValue)
         idf = math.log(idf,2) # log to base 2
         score = float(value) * idf
      else: # set score to 0
         score = 0
      #  print key + " : " + str(value) + " / " + str(compareValue) + " => " + str(score) # TEST !!!
      return score

