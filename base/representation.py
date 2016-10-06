#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 14.11.12

"""
Abstract class for representation of PRCs.
"""

import sys
sys.path.append("../../Utils") 
from parseutils import getGeneralPOS

sys.path.append("..")
from utils import posMarker
from utils import posMarkerSW
from utils import treeMarkerDown
from utils import treeMarkerUp


class PRCRepresentation:
   
   
   """ Key for attribute used for marking all nodes. """
   posMarker = posMarker

   """ Value for attribute self.posMarker for the sentiment node. """
   posMarkerSW = posMarkerSW

   """ Going from child to parent, given as direction in self.markNode() """
   treeMarkerUp = treeMarkerUp

   """ Going from parent to child, given as direction in self.markNode() """
   treeMarkerDown = treeMarkerDown
   

   """ Name of the PRC representation (short string) """
   reName = "AbstractPRC"
   
   
   def setPosMarker(self, marker):
      """
      The representation of a node is marked with the attribute self.posMarkerSW.
      Change to allow multiple annotations.
      """
      self.posMarker = marker
   

   def markSentimentWord(self, sentimentWord):
      """ 
      Marks the sentiment word in self.posMarker as the sentiment word
      (value is self.posMarkerSW).
      Existence of the mark may be used to check if a word
      has been processed before.
      Method may be overloaded.
      
      @param sentimentWord The node of the reversed sentimetn word.
      POST: sentimentWord has attribute self.posMarker
      """
      sentimentWord.mark ({self.posMarker: self.posMarkerSW})

   
   def markNode(self, originNode, direction, currentNode):
      """
      Marks 'currentNode' with a sign that it has been processed.
      Existence of the mark may be used to check if a word
      has been processed before.
      Every ReverserExtracter should overload this method to
      save information inside the nodes about the structure,
      e.g. path to this node from sentiment word.
      
      @param originNode The node previously processed on the path.
      @param direction The direction we need to go in the parse tree
            to get from 'originNode' to 'currentNode'
            (may be self.treeMarkerUp or self.treeMarkerDown).
      @param currentNode The node to be processed that is considered
            as a candidate reverser.
      POST: currentNode has attribute self.posMarker
      """
      currentNode.mark ({self.posMarker: ""})
   
   
   def createRepresentation(self, candidate, sentWord):
      """ 
      Abstract method.
      Create a representation of the candidate from the node.
      Return "" for invalid candidate.
      Every subclass must overload this method.
      
      @param candidate Node that is candidate
      @param sentWord The sentiment word in this sentence from
            where the reverser candidate has been extracted.
      @return 
      """
      raise NotImplementedError('Method must be implemented in subclass')
      return ""
   
   
   def createRepresentationSentWord(self, sentWord):
      """
      Create a representation of the sentiment word from the node.
      Return "" for invalid candidate.
      Default is return generalized POS.
      
      @param sentWord The sentiment word in this sentence from
            where the reverser candidate has been extracted.
      @return sentiment word generalized POS
      """
      return getGeneralPOS(sentWord.getPOS())
