#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 19.10.11

"""

"""

from operator import itemgetter
import math


class AbstractCandidateScorer:
   """
   Abstract class where every scorer inherits from.
   Goes through the list of candidates, scores every one and
   writes the n candidates with the highest score to the outputFile.
   N can be set.
   Main method to call is of course 'scoreCandidates',
   if you want to compare to another set, use
   'setComparisonSet' beforehand.
   """
   
   
   scoredCandidates = {}
   
   def setN(self, newN):
      """ 
      Sets the N for extraction of N best candidates.
      N=0 means extract all.
      """
      #  print "Number of reversers: " + str(newN) # TEST !!!
      self.n = newN
      
   def setThreshold(self, newThreshold):
      """ 
      Sets the threshold for considering to score a candidate.
      threshold=0 means no threshold.
      """
      #  print "Scoring threshold: " + str(newThreshold) # TEST !!!
      self.threshold = newThreshold

   def setNumberRevExamples (self, number):
      """ 
      Set number of reversed examples seen.
      """
      self.c_CisRev = float(number)
   
   def setNumberNonrevExamples (self, number):
      """ 
      Set number of nonreversed examples seen.
      """
      self.c_CisNonrev = float(number)
      
   def isComparisonScorer (self):
      """ 
      Return True if needs comparison set for scoring,
      else False.
      If this is true, you need to set the comparison set
      with self.setComparisonSet()
      """
      return isinstance(self,AbstractComparisonCandidateScorer)
   
   def scoreCandidateX(self,key,value):
      """ 
      Abstract method.
      Every Scorer must implement this method.
      Takes a candidate X and returns its score.
      """
      raise NotImplementedError('Method must be implemented in subclass')
      return 0

   def initialize(self,candidates):
      """ 
      Abstract method.
      Called first thing in 'scoreCandidates'.
      May be overwritten by a Scorer to do any necessary initialization.
      """
      self.scoredCandidates = {}
   

   def scoreCandidates(self, candidates, outputFile, printout = False):
      """ 
      Goes through the list of candidates, scores every one and
      writes the n candidates with the highest score to the outputFile.
      """
      self.initialize(candidates)
      
      # In the candidates dictionary is the raw frequency.
      # Score candidates and write to scored dict.
      i=0
      for key,value in sorted(candidates.items()):
         if value > self.threshold:
            score = self.scoreCandidateX(key,value)
            self.scoredCandidates[key]=score
         #  print key + " " + str(score) + " (from " + str(value) + ")" # TEST !!!
      #  print "test=" + str(len(self.scoredCandidates))
      
      # Print N candidates with highest score to file and to result set
      resultSet = {}
      outputFileHandle = open(outputFile, "w")
      i = 1
      for pair in reversed(sorted(self.scoredCandidates.items(), key=itemgetter(1))):
         
         # Extract only the top n candidates
         if i > self.n and self.n != 0:
            break
         
         # Actual result
         result = pair[0] + " " + ("%.2f" % round(pair[1],2))
         
         # This is only for printing it out nicely, 
         # getting ocurrences in compared vs. comparison set
         comparison =  " / " + str(candidates.get(pair[0]))  # TEST !!!
         if isinstance(self,AbstractComparisonCandidateScorer):
            comparison +=  " vs " # TEST !!!
            if self.comparisonSet: # TEST !!!
               # TODO broke this, fix if want to use global comparison set
               # Get word out of candidate representation
               #  parts = pair[0].split("_")
               #  if len(parts) > 1 and isinstance(self,AbstractGlobalComparisonScorer):
                  #  word = parts[len(parts)-1]
               #  else:
                  #  word = pair[0]
               comparison  += str(self.comparisonSet.get(pair[0])) # TEST !!!
            
         # Write it to file
         if printout:
            print result + comparison # TEST !!!
         resultSet[pair[0]] = pair[1]
         outputFileHandle.write(result + comparison + "\n")
         
         i += 1
      
      # Cleanup
      outputFileHandle.close()
      
      # Give back whole set of scored candidates
      print "total number of scored candidates: " + str(len(self.scoredCandidates))
      #  return self.scoredCandidates
      return resultSet


   def cleanup(self):
      """
      Delete scores from previous computation.
      """
      self.scoredCandidates = {}
      


# ----- Simple scorers (need no comparison) -----


class RawFrequencyScorer(AbstractCandidateScorer):
   """
   Score is just the raw frequency.
   """

   def scoreCandidateX(self,key,value):
      """
      Takes a candidate X and returns its score.
      Score is just the raw frequency
      """
      return value


class RawFrequencyScorerNormalized(AbstractCandidateScorer):
   """
   Score is the raw frequency divided by a maximum value.
   """

   def initialize(self,candidates):
      """ 
      Abstract method.
      May be overwritten by a Scorer to do any necessary initialization.
      """
      self.scoredCandidates = {}
      self.max = max(candidates.values())

   def scoreCandidateX(self,key,value):
      """
      Takes a candidate X and returns its score.
      Score is  the raw frequency divided by a maximum value.
      """
      return float(value) / float(self.max)




# ----- Scorers that need comparison dataset -----

class AbstractComparisonCandidateScorer(AbstractCandidateScorer):
   
      
   def setComparisonSet(self, comparisonSet):
      """ 
      Sets a set with candidates to compare to.
      """
      self.comparisonSet = comparisonSet



class RelativeFrequencyScorer(AbstractComparisonCandidateScorer):
   """
   Score is the frequency relative to a comparison set.
   """
     
   
   def scoreCandidateX(self,key,value):
      """
      Takes a candidate X and returns its score.
      TODO
      """
      compareValue = self.comparisonSet.get(key)
      if compareValue == None:
         compareValue = 0
      if compareValue != 0:
         score = float(value) / float(compareValue)
      else: # don't divide by 0
         score = float(value) # equiv compareValue = 1
      #  print key + " : " + str(value) + " / " + str(compareValue) + " => " + str(score) # TEST !!!
      return score


class RelativeFrequencyScorerLog(AbstractComparisonCandidateScorer):
   """
   Score is the frequency relative to a comparison set.
   score = log_2 (c_reversed / c_nonreversed)
   """
   
   def scoreCandidateX(self,key,value):
      """
      Takes a candidate X and returns its score.
      TODO
      """
      compareValue = self.comparisonSet.get(key)
      if compareValue == None:
         compareValue = 0
      if compareValue != 0:
         score = float(value) / float(compareValue)
      else: # don't divide by 0
         score = float(value) # equiv compareValue = 1
      score = math.log(score,2) # log to base 2
      #  print key + " : " + str(value) + " / " + str(compareValue) + " => " + str(score) # TEST !!!
      return score


class RelativeFrequencyScorerLogSum(AbstractComparisonCandidateScorer):
   """
   Score is the frequency relative to a comparison set.
   score = log_2 (c_reversed / c_reversed + c_nonreversed)
   """
   
   def scoreCandidateX(self,key,value):
      """
      Takes a candidate X and returns its score.
      TODO
      """
      compareValue = self.comparisonSet.get(key)
      if compareValue == None:
         compareValue = 0
      if compareValue != 0:
         score = float(value) / float(value + compareValue)
      else: # don't divide by 0
         score =  float(value) / float(value + 1) # equiv compareValue = 1
      score = math.log(score,2) # log to base 2
      #  print key + " : " + str(value) + " / " + str(compareValue) + " => " + str(score) # TEST !!!
      return score


class RelativeFrequencyScorerPlusAbsolute(AbstractComparisonCandidateScorer):
   """
   Score is the frequency relative to a comparison set.
   """
   
   def initialize(self,candidates):
      """ 
      Abstract method.
      May be overwritten by a Scorer to do any necessary initialization.
      """
      self.scoredCandidates = {}
      self.max = max(candidates.values())/5

   
   def scoreCandidateX(self,key,value):
      """
      Takes a candidate X and returns its score.
      TODO
      """
      compareValue = self.comparisonSet.get(key)
      if compareValue == None:
         compareValue = 0
      if compareValue != 0:
         relativeScore = float(value) / float(compareValue)
      else: # don't divide by 0
         relativeScore = float(value) # equiv compareValue = 1
      relativeScore = math.log(relativeScore,2) # log to base 2
      normalizedAbsoluteScore = float(value) / float(self.max)
      score = relativeScore + normalizedAbsoluteScore
      #  print key + " : " + str(value) + " / " + str(compareValue) + " => " + str(relativeScore) + " + " + str(normalizedAbsoluteScore)  + " => "+ str(score) # TEST !!!
      return score






