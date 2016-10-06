#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 19.10.11

"""
Provides implementations PRC representations.
Different smiple classes working only with words.
"""

from representation import PRCRepresentation

import sys
sys.path.append("..") 
from utils import filterAndNormalizeCandidate



class PRCRepresentationWords(PRCRepresentation):
   """ 
   Candidates are words (no lemmatization).
   """
   
   """ Name of the PRC representation (short string) """
   reName = "Word"
   
   def createRepresentation(self, candidate, sentWord):
      """
      Create as representation the word.
      Overloaded from super.
      """
      word = candidate.getWord() 
      pos = candidate.getPOS()
      candidateString = filterAndNormalizeCandidate(word, pos)
      return candidateString



class PRCRepresentationLemmas(PRCRepresentation):
   """ 
   Candidates are lemmata.
   """ 
   
   """ Name of the PRC representation (short string) """
   reName = "Lemma"
   
   def createRepresentation(self, candidate, sentWord):
      """
      Create as representation the lemma.
      Overloaded from super.
      """
      word = candidate.getLemma()
      pos = candidate.getPOS()
      candidateString = filterAndNormalizeCandidate(word, pos)
      return candidateString
