#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 11.6.12

"""

"""

import utils
import featureextractor



class FeatureExtractorPlaintextOutput (featureextractor.FeatureExtractorWordWise):
   """ 
   Write sentence in plain text for found sentiment word with the word marked.
   Note: Tree is written once for every word found.
   Reversed words are written to self.reversedSentencesPlaintextFile
   Nonreversed words are written to self.nonreversedSentencesPlaintextFile
   """
   
   lastTree = None
   markedNodes = []
   
   
   def setFileReversed (self, reversedSentencesPlaintextFile):
      """ 
      Sets .
      """
      self.reversedSentencesPlaintextFile = open(reversedSentencesPlaintextFile, "w")
      

   def setFileNonReversed (self, nonreversedSentencesPlaintextFile):
      """ 
      Sets .
      """
      self.nonreversedSentencesPlaintextFile = open(nonreversedSentencesPlaintextFile, "w")
   
   
   def extractFeatures(self, node, tree, label):
      """
      Label can be utils.labelReversed or utils.labelNonreversed
      Is called
      """
      
      outputfile = None
      if label == utils.labelReversed:
         outputfile = self.reversedSentencesPlaintextFile
      elif label == utils.labelNonreversed:
         outputfile = self.nonreversedSentencesPlaintextFile
      else:
         print "ERRROR, do not recognize label for feature extraction (FeatureExtractorPlaintextOutput): " + label
         return

      
      # Find label
      sentenceLabel = tree.findLabel()
      currentSentence = str(sentenceLabel) + ":"

      iter = tree.getIterator()
      currentNode = iter.next()
         
      while currentNode != "":
         
         #  Add word to sentence
         if currentNode.getID() == node.getID():
            currentSentence = currentSentence + " " + "__" + currentNode.getWord() + "__"
         else:
            currentSentence = currentSentence + " " + currentNode.getWord() 
            
         #  Next node
         currentNode = iter.next()

      outputfile.write(currentSentence + "\n")
      outputfile.flush()
      
      
   def extractFeaturesAndGiveme(self, node, tree, label):
      """
      """
