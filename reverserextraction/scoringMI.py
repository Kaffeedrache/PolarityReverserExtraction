#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 2.8.12

"""

"""

from operator import itemgetter
import math

import scoring



class MutualInformationScorer(scoring.AbstractComparisonCandidateScorer):
   """
   Score is the frequency relative to a comparison set by calculating Mutual Information.
   """
   
   
   def calculateSummand(self, C_ec, C_e, C_c):
      # All numbers must be floats!
      
      # If any part is 0, return 0 to avoid division by 0 or log 0
      if C_ec == 0 or C_e == 0 or C_c ==0 :
         return 0
         
      firstPart = C_ec / self.c_Total
      # put N in denominator
      frac = C_ec * self.c_Total / (C_e * C_c)
      result = firstPart * math.log(frac,2) 
      return result


   def initialize(self,candidates):
      """ 
      Abstract method.
      Called first thing in 'scoreCandidates'.
      May be overwritten by a Scorer to do any necessary initialization.
      """
      self.scoredCandidates = {}
      self.c_Total = self.c_CisNonrev + self.c_CisRev


   def scoreCandidateX(self,key,value):
      """
      Takes a candidate X and returns its score.
      Score is Mutual information of X and class "reversed".
      MI measures how much information the presence/absence 
      of a term contributes to making the correct classification 
      decision on c (reversed/nonreversed).
      Formula :
      MI (X, c) = SUM_e={0,1} SUM_c={REV,NONREV} P(X=e, C=c) log_2 [P(X=e, C=c) / P(X=e) * P(C=c)]
      where
      P(X=0, C=REV) how many examples that do NOT contain X are in class REV
      P(X=1, C=REV) how many examples that DO contain X are in class REV
         = count number of occurences of X in REV / #examples
      ...
      """
      #  print "key " + key
      
      # Get counts of X in nonrev/rev
      c_XinNonrev = self.comparisonSet.get(key)
      if c_XinNonrev == None:
         c_XinNonrev = float(0)
      c_XinNonrev = float(c_XinNonrev)
      c_XinRev = float(value)
      #  print "rev " + str(c_XinRev) + " nonrev " + str(c_XinNonrev) # TEST !!!
      
      # How many examples contain / not contain x
      c_x = c_XinRev + c_XinNonrev
      c_NOTx = self.c_Total - c_x
      #  print "x " + str(c_x) + " notx " + str(c_NOTx) # TEST !!!
      
      # Counts for NOT x in both classes
      c_notXinRev = self.c_CisRev - c_XinRev
      c_notXinNonrev = self.c_CisNonrev - c_XinNonrev
      #  print "c_notXinRev " + str(c_notXinRev) + " c_notXinNonrev " + str(c_notXinNonrev) # TEST !!!
      
      # Get parts of sum
      # X=1, C=REV
      first = self.calculateSummand(c_XinRev, c_x, self.c_CisRev)
      #  print "X=1, C=REV " + utils.strF3(first * 1000.0) # TEST !!!
      # X = 0, C = REV
      second = self.calculateSummand(c_notXinRev, c_NOTx, self.c_CisRev)
      #  print "X=0, C=REV " + utils.strF3(second * 1000.0) # TEST !!!
      # X = 1, C = NONREV
      third = self.calculateSummand(c_XinNonrev, c_x, self.c_CisNonrev)
      #  print "X=1, C=NONREV " + utils.strF3(third * 1000.0) # TEST !!!
      # X = 0, C = NONREV
      forth = self.calculateSummand(c_notXinNonrev, c_NOTx, self.c_CisNonrev)
      #  print "X=0, C=NONREV " + utils.strF3(forth * 1000.0) # TEST !!!
      
      mi = first + second + third + forth
      
      #  print "MI(" + key + ",REV) = " + utils.strF3(mi * 1000.0) # TEST !!!
      
      return mi * 1000.0



class MutualInformationOnlyRevScorer(MutualInformationScorer):


   def scoreCandidateX(self,key,value):

      mi = MutualInformationScorer.scoreCandidateX(self,key,value)

      # HACK
      # MI is nonnegative
      # MI gives features that can distinguish between classes,
      # not features that point to one class.
      # But we want features that point to class REVERSED!
      # - those that occur more often in reversed than nonrev
      # Solution: make score negative for those that ocurr
      # more often in nonrev contexts!
      score = mi
      c_XinNonrev = self.comparisonSet.get(key)
      if c_XinNonrev == None:
         c_XinNonrev = 0
      if c_XinNonrev > value:
         score *= (-1)
      
      return score


# Just some checking with numbers from information retrieval book
# Result should be 0.0001105 (see chap. 13.5.1, page 273)

#  miscorer = MutualInformationOnlyRevScorer()

#  miscorer.setNumberRevExamples (49+141)
#  miscorer.setNumberNonrevExamples (774106 + 27652)

#  miscorer.comparisonSet = {}
#  miscorer.comparisonSet["export"] = 27652

#  miscorer.initialize({})

#  finalscore = miscorer.scoreCandidateX("export", 49)
#  print "And the winner is " + utils.strF3(finalscore)