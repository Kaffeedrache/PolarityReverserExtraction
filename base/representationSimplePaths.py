#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 19.10.11

"""
Provides implementations PRC representations.
Different classes working with simplified paths.
"""

from representation import PRCRepresentation

import sys
sys.path.append("..") 
from utils import filterAndNormalizeCandidate

sys.path.append("../../Utils") 
from parseutils import getGeneralPOS


class PRCRepresentationSimplePaths(PRCRepresentation):
   """ 
   Candidates are POSTITION_LEMMA.
   Where position from {DESCENDENT, SIBLING, ANCESTOR}.
   """


   """ Value for attribute self.posMarker for a descendent of the sentiment word. """
   posMarkerChild = "DESCENDENT"
   
   """ Value for attribute self.posMarker for an ancestor of the sentiment word. """
   posMarkerParent = "ANCESTOR"
   
   """ Value for attribute self.posMarker for a sibling (descendent of an ancestor,
   of the sentiment word. """
   posMarkerSibling = "SIBLING"
   
   """ Name of the ReverserExtracter (short string) """
   reName = "SimplePaths"
   
   
   def markNode(self, originNode, direction, currentNode):
      """
      Marks 'currentNode' with a simplified path from the sentiment word
      to the current node (only state if node is above, below or a sibling
      of sentiment word).
      Overloaded from super.
      """
      originMark = originNode.getAttribute(self.posMarker) 
      
      if direction == self.treeMarkerDown:
         
         # Go down and origin is also a child or the sentiment word -> child
         if originMark == self.posMarkerChild or originMark == self.posMarkerSW:
            currentNode.mark({self.posMarker: self.posMarkerChild})
         
         # Go down, but origin is not a child or the sentiment word -> sibling
         else:
            currentNode.mark({self.posMarker: self.posMarkerSibling})
      
      # Go up -> father
      elif direction == self.treeMarkerUp:
         currentNode.mark({self.posMarker: self.posMarkerParent})


   def createRepresentation(self, candidate, sentWord):
      """
      Create as representation the simplified path from the sentiment word
      to the candidate node, POSITION_LEMMA.
      Overloaded from super.
      """
      word = candidate.getLemma()
      pos = candidate.getPOS()
      word = filterAndNormalizeCandidate(word, pos)
      if word == "":
         return ""
      position = candidate.getAttribute(self.posMarker)
      candidateString = position + "_" + word
      return candidateString



class PRCRepresentationSimplePathsPOS(PRCRepresentationSimplePaths):
   """ 
   Candidates are SENTIMENTWORDPOS_POSTITION_LEMMA
   Where position from {DESCENDENT, SIBLING, ANCESTOR}
   """
   

   """ Name of the ReverserExtracter (short string) """
   reName = "SimplePathsPOS"
   

   def createRepresentation(self, candidate, sentWord):
      """
      Create as representation the simplified path from the sentiment word
      to the candidate node, SENTIMENTWORDPOS_POSTITION_LEMMA.
      Overloaded from super.
      """
      sentWordPOS = getGeneralPOS(sentWord.getPOS())
      word = candidate.getLemma()
      pos = candidate.getPOS()
      word = filterAndNormalizeCandidate(word, pos)
      if word == "":
         return ""
      position = candidate.getAttribute(self.posMarker)
      candidateString = sentWordPOS + "_" + position + "_" + word
      return candidateString

