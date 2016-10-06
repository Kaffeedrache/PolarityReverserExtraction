#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 19.10.11

"""
Provides implementations PRC representations.
Different classes working with paths.
"""

from representation import PRCRepresentation

import sys
sys.path.append("..") 
from utils import filterAndNormalizeCandidate

sys.path.append("../../Utils") 
from parseutils import getGeneralPOS



class PRCRepresentationCompletePaths(PRCRepresentation):
   """ 
   Candidates are complete paths, > for down the tree, < for up
   """
   
   """ Name of the PRC representation (short string) """
   reName = "CompletePaths"


   def markSentimentWord(self, sentimentWord):
      """ 
      Marks the sentiment word in self.posMarker as the sentiment word
      (value is generalized sentWord POS).
      Overloaded from super.
      """
      sentWordPos = getGeneralPOS(sentimentWord.getPOS())
      #  sentimentWord.mark ({self.posMarker: self.posMarkerSW + sentimentWord.getPOS()})
      sentimentWord.mark ({self.posMarker: sentWordPos})
   
   
   def markNode(self, originNode, direction, currentNode):
      """
      Marks 'currentNode' with the complete path from the sentiment word
      to the current node.
      Overloaded from super.
      """
      currentNode.mark({self.posMarker: originNode.getAttribute(self.posMarker) + direction + currentNode.getLemma() + "_" + getGeneralPOS(currentNode.getPOS())})


   def createRepresentation(self, candidate, sentWord):
      """
      Create as representation the complete path from the sentiment word
      to the candidate node.
      Overloaded from super.
      """
      word = candidate.getLemma()
      pos = candidate.getPOS()
      word = filterAndNormalizeCandidate(word, pos)
      if word == "":
         return ""
      candidateString = candidate.getAttribute(self.posMarker)
      return candidateString


class PRCRepresentationAbstractedCompletePaths(PRCRepresentation):
   """ 
   Candidates are complete paths, > for down the tree, < for up.
   Nodes on the path are represented by POS.
   """
   
   """ Name of the PRC representation (short string) """
   reName = "AbstractedCompletePaths"

   tmpPosMarker = "__"


   def setPosMarker(self, marker):
      """
      The representation of a node is marked with the attribute self.posMarkerSW.
      Change to allow multiple annotations.
      Overloaded from super to allow for tmpPosMarker.
      """
      self.posMarker = marker
      self.tmpPosMarker = "__" + marker


   def markSentimentWord(self, sentimentWord):
      """ 
      Marks the sentiment word in self.posMarker as the sentiment word
      (value is self.posMarkerSW + sentWord POS).
      Overloaded from super.
      """
      sentWordPos = getGeneralPOS(sentimentWord.getPOS())
      sentimentWord.mark ({self.posMarker: sentWordPos})
      sentimentWord.mark ({self.tmpPosMarker: sentWordPos})
   
   
   def markNode(self, originNode, direction, currentNode):
      """
      Marks 'currentNode' with the complete path from the sentiment word
      to the current node. Words are abstracted to POS.
      Overloaded from super.
      """
      currentNode.mark({self.tmpPosMarker: originNode.getAttribute(self.tmpPosMarker) + direction + getGeneralPOS(currentNode.getPOS())})
      currentNode.mark({self.posMarker: originNode.getAttribute(self.tmpPosMarker) + direction + currentNode.getLemma() + "_" + getGeneralPOS(currentNode.getPOS())})


   def createRepresentation(self, candidate, sentWord):
      """
      Create as representation the complete path from the sentiment word
      to the candidate node.
      Overloaded from super.
      """
      word = candidate.getLemma()
      pos = candidate.getPOS()
      word = filterAndNormalizeCandidate(word, pos)
      if word == "":
         return ""
      candidateString = candidate.getAttribute(self.posMarker)
      return candidateString
