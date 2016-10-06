#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 20.11.12

"""
Factory class for scorer
"""

import scoring
import scoringMI


def createScorer(name, threshold, numberOfPRCsToExtract):
   
   scorer = None
   
   if name == "RawFrequency":
      scorer = scoring.RawFrequencyScorer()
   elif name == "RelativeFrequency" or name == "Rel":
      scorer = scoring.RelativeFrequencyScorerLog()
   elif name == "MI":
      scorer = scoringMI.MutualInformationScorer()
   elif name == "MI+" or name == "MIExt":
      scorer = scoringMI.MutualInformationOnlyRevScorer()
      
   # TODO include others
   
   #  scorer = scoring.RawFrequencyScorerNormalized() 
   #  scorer = scoring.RelativeFrequencyScorer()
   #  scorer = scoring.RelativeFrequencyScorerLogSum()
   #  scorer = scoring.RelativeFrequencyScorerPlusAbsolute()
   
   # Global scorer is broken, fix in scoring first
   #  scorer = scoring.GlobalComparisonScorerTfIdf()
   
   # Set threshold & number of PRCs to extract
   scorer.setThreshold(threshold)
   scorer.setN(numberOfPRCsToExtract)
   
   
   if scorer != None:
      return scorer
   else:
      # Error
      print "Error, do not know this representation"
      return None


