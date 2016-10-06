#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 20.12.11

"""
"""


import sys
sys.path.append("..") 
from utils import posMarker
from utils import posMarkerSW
from utils import treeMarkerDown
from utils import treeMarkerUp



class TreeContextFinder:
   """ 
   Extracts as candidates all words with a distance smaller than DIST from 
   the sentiment word in the parse tree.
   The representation of the reverser is open.
   """
   
   
   """ Name of the ReverserExtracter (short string) """
   reName = "TreeContextFinder"
   

   
   
   def setWindowsize(self, windowsize):
      """
      Set maximum distance for checking neighborhood
      """
      self.windowsize = windowsize
      
   
   def setRepresentation(self, representation):
      """
      Used to create string from node.
      """
      self.representation = representation
   
   
   def createRepresentationSentWord(self, sentWord):
      """
      Use self.representation to create string from node.
      """
      return self.representation.createRepresentationSentWord(sentWord)
   
   
   def extractCandidatesFromContext(self, sentWord, tree):
      """
      Go through tree, find all nodes that are children, parents 
      and siblings (children of parents) of the sentiment word
      with distance smaller than windowsize from the sentiment word.
      Nodes are considered candidates for reversers.
      Sentiment word is marked with self.representation.markSentimentWord().
      Every found node is marked with self.representation.markNode().
      For all candidates the representation is extracted with
      self.representation.createRepresentation().
      """
      
      
      # Mark with marker attribute unique to this node
      currentMarker = posMarker + str(sentWord.getID())
      self.representation.setPosMarker(currentMarker)     
      
      
      # Get all words in parse tree around sentiment word.
      # Save candidates in 'allcandidates'.
      # Mark the sentimetn word, because we want to delete
      # it afterwards.
      self.representation.markSentimentWord(sentWord)
      allcandidates = [sentWord]
      
      # Get candidates below sentiment word.
      level = self.windowsize
      nextInLine = []
      toBeProcessed = [sentWord]
      while level > 0 and toBeProcessed:
         for current in toBeProcessed:
            children = tree.getChildNodes(current)
            for c in children:
               #  print "Bringing " + str(c) + " to the kindergarden" # TEST !!!
               #  print current.getAttribute(posMarker) + treeMarkerDown + c.getWord() # TEST !!!
               self.representation.markNode(current, treeMarkerDown, c)
               allcandidates.append(c)
               nextInLine.append(c)
         toBeProcessed = nextInLine
         nextInLine = []
         level = level - 1
      
      #  print "All candidates up to now (children): " # TEST !!!
      #  for a in allcandidates: # TEST !!!
         #  print a # TEST !!! 
      #  print "--" # TEST !!!
      
      # Get candidates above sentiment word and their children.
      currentnode = sentWord
      level = self.windowsize
      while level > 0 and not currentnode.getID() == 0 and not currentnode.getParentID() == 0:
         #  print "node " + str(currentnode) + " at level " + str(level) # TEST !!!
         father = tree.getParentNode(currentnode)
         if father == 0: # The currentnode was root, no more parents/siblings
            break
            
         # Mark parent node and add to candidates
         allcandidates.append(father)
         self.representation.markNode(currentnode, treeMarkerUp, father)

         # Get children of parent (= siblings)
         # tmpLevel is level - 1 (= distance in parse tree)
         # because we have already the path to the parent as #level steps.
         # Do not add nodes that already have a attribute for posMarker,
         # these have been processed in a step before
         # (e.g. original sentiment node and its children).
         tmpLevel = level - 1
         nextInLine = []
         toBeProcessed = [father]
         while tmpLevel > 0 and toBeProcessed:
            for current in toBeProcessed:
               children = tree.getChildNodes(current)
               for c in children:
                  #  print "Child of " + father.getWord() + ": " + c.getWord() # TEST !!!
                  if c.getAttribute(currentMarker) == None:
                     # Do not overwrite an existing mark 
                     # (that would be sentiment node or child of it)
                     # also do not process this node further
                     #  print father.getAttribute(self.posMarker) + self.treeMarkerDown + c.getWord() # TEST !!!
                     self.representation.markNode(current, treeMarkerDown, c)
                     allcandidates.append(c)
                     nextInLine.append(c)
                  #  else: # TEST !!!
                     #  print "do not extract " + c.getWord() # TEST !!!
            toBeProcessed = nextInLine
            nextInLine = []
            tmpLevel = tmpLevel - 1
         
         
         # Next loop
         level = level - 1
         currentnode = father
         
      #  TEST !!!
      #  print "All candidates up to now (parent): " # TEST !!!
      #  for a in allcandidates: # TEST !!!
         #  print a # TEST !!!
      #  print "--" # TEST !!!

      # Remove sentiment word itself
      allcandidates.remove(sentWord)

      #  TEST !!!
      #  print "All candidates (total): " # TEST !!!
      #  for a in allcandidates: # TEST !!!
         #  print a # TEST !!!
      #  print "--" # TEST !!!
   
      
      # Insert representations in result list
      result = []
      for a in allcandidates:
         candidate = self.representation.createRepresentation(a, sentWord)
         if candidate != "":
            result.append(candidate)
      
      # Remove markers (go through all nodes, not only close nodes - inefficient)
      iter = tree.getIterator()
      node = iter.next()
      while node != "":
         node.unmark(currentMarker)
         node = iter.next()
      
      return result
      