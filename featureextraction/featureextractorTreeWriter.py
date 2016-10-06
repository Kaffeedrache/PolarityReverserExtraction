#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 11.6.12

"""

"""

import utils
import featureextractor



class FeatureExtractorTreeWriter (featureextractor.FeatureExtractorWordWise):
   """ 
   Write parse tree for found sentiment word with the word marked.
   Note: Tree is written once for every word found.
   Reversed words are written to self.parseWriterReversed / outputFileReversed
   Nonreversed words are written to self.parseWriterNonreversed / outputFileNonreversed
   """

   #  def extractFeatures(self, node, tree, label):
      #  """
      #  Label can be utils.labelReversed or utils.labelNoneversed
      #  """
      
      #  self.writeToFile(label, tree.getWholeSentence())
   
   def setParseWriterReversed(self, parseWriter, outputFileReversed):
      """ 
      Sets a parse reader.
      Need to set outputFileReversed file first!
      """
      self.parseWriterReversed = parseWriter
      parseWriter.setOutputFile(outputFileReversed)
      
   def setParseWriterNonreversed(self, parseWriter, outputFileNonreversed):
      """ 
      Sets a parse reader.
      Need to set input file first!
      """
      self.parseWriterNonreversed = parseWriter
      parseWriter.setOutputFile(outputFileNonreversed)
   
   
   def extractFeatures(self, node, tree, label):
      """
      Label can be utils.labelReversed or utils.labelNonreversed
      Write parse tree to file
      """
      parseWriter = None
      if label == utils.labelReversed:
         parseWriter = self.parseWriterReversed
      elif label == utils.labelNonreversed:
         parseWriter = self.parseWriterNonreversed
      else:
         print "ERRROR, do not recognize label for feature extraction (FeatureExtractorTreeWriter): " + label
         return
      
      # We have a reversed word. Mark it
      node.markSentimentWord()
      # Write to file
      parseWriter.writeParse(tree)
      # Reverse the change for the next check
      node.unmarkSentimentWord()
      #  print word + "(" + lemma + "," + pos + ")" + " found in " + tree.getLabel() + ": " + tree.getWholeSentenceString() # TEST !!!
      
      
   def extractFeaturesAndGiveme(self, node, tree, label):
      """
      """
      
