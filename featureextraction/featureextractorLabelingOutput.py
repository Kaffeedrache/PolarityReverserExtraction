#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 11.6.12

"""

"""

import utils
import featureextractor



class FeatureExtractorLabelingOutput (featureextractor.FeatureExtractorSentenceWise):
   """ 
   """
   
   lastTree = None
   markedNodes = []
   markedNodesLabels = []

   def setPrintLabel(self, labelingOutputPrintLabel):
      self.printLabel = labelingOutputPrintLabel
   
   
   def extractFeatures(self, node, tree, label):
      """
      Label can be utils.labelReversed or utils.labelNonreversed
      """
      
      #  print "call for node " + node.getWord() + " ( " + str(label) 
      
      # First call: Save tree
      if self.lastTree == None:
         self.lastTree = tree
      
      # Remember all nodes to be labeled
      if tree == self.lastTree:
         self.markedNodes.append(node)
         self.markedNodesLabels.append(label)
         #  print "marked " + node.getWord() + " as " + label # TEST !!!
      
      else:
         # New tree, print old tree
         
         #  print "print sentence" # TEST !!!
         #  for n in self.markedNodes: # TEST !!!
            #  index = self.markedNodes.index(n) # TEST !!!
            #  print "marked " + n.getWord() + " as " + self.markedNodesLabels[index] # TEST !!!
         #  self.lastTree.printTree() # TEST !!!
         
         # New tree, construct sentence representation of old sentence
         currentSentence = ""
            
         iter = self.lastTree.getIterator()
         currentNode = iter.next()
         
         while currentNode != "":
            
            # Add word to sentence
            if currentNode in self.markedNodes:
               if self.printLabel == True:
                  index = self.markedNodes.index(currentNode)
                  reverserLabel = self.markedNodesLabels[index]
                  if reverserLabel == utils.labelReversed: # HACK TODO change
                     reverserLabel = "REVERSED"
                  elif reverserLabel == utils.labelNonreversed: # HACK TODO change
                     reverserLabel = "NONREVERSED"
                  currentSentence = currentSentence + " " + "<sentimentWord label=\"" + reverserLabel + "\">" + "__" + currentNode.getWord() + "__" + "</sentimentWord>"
               else:
                  currentSentence = currentSentence + " " + "__" + currentNode.getWord() + "__"
               
            else:
               currentSentence = currentSentence + " " + currentNode.getWord() 
               
            # Next node
            currentNode = iter.next()
            
         # Write old sentence
         sentenceLabel = ""
         if self.printLabel == True:
            sentenceLabel = self.lastTree.findLabel()
            if sentenceLabel == utils.negativeLabel: # HACK TODO change
               sentenceLabel = "NEG"
            elif sentenceLabel == utils.positiveLabel: # HACK TODO change
               sentenceLabel = "POS"
         
         self.writeToFile(sentenceLabel, [currentSentence])
         
         # Set everything to new tree
         self.lastTree = tree
         self.markedNodes = [] 
         self.markedNodesLabels = [] 
         
         # Save new node for new tree
         self.markedNodes.append(node)
         self.markedNodesLabels.append(label)
         #  print "marked " + node.getWord() + " as " + label # TEST !!!
         

      
      
      
   def extractFeaturesAndGiveme(self, node, tree, label):
      """
      """
