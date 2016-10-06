#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 14.10.11

"""

"""

class ParseTreeNode:
   # encapsulate node
   
   # Keys
   keyPos = "pos"
   keyWord = "word"
   keySentiment = "sent"
   keyLemma = "lemma"
   keyRelation = "relation"
   
   # Fields
   id = 0
   parentID = 0
   attributes = {}
   
   def __init__(self, nodeID, parentID, attributes):
      self.id = nodeID
      self.parentID = parentID
      self.attributes = attributes

   def getID(self):
      return self.id
      
   def getParentID(self):
      return self.parentID
   
   def getWord(self):
      return self.attributes.get(self.keyWord)
      
   def getLemma(self):
      return self.attributes.get(self.keyLemma)
      
   #  def setWord(self, value):
      #  self.attributes[self.keyWord] = value
      
   def getPOS(self):
      return self.attributes.get(self.keyPos)
      
   def getAttribute(self, key):
      return self.attributes.get(key)
      

   def __str__(self):
      return "Node: ID " + str(self.id) + ", parent " + str(self.parentID) + ", attributes " + str(self.attributes)

   def mark(self, markerAttributes, overwrite = True):
      for a in markerAttributes:
         if self.attributes.get(a) == None or overwrite:
            #  print "marking " + a + " as " + markerAttributes.get(a)
            self.attributes[a] = markerAttributes.get(a)
         #  else:
            #  print "Marker exists!"

   def unmark(self, markerAttribute):
      #  print "unmark " + self.getWord()
      if self.attributes.get(markerAttribute) != None:
         #  print "unmarking " + str(self.attributes)
         del(self.attributes[markerAttribute])
         #  print "unmarking " + str(self.attributes)

            
   def markSentimentWord(self):
      self.mark({self.keySentiment : True})
      # TODO write this in parse
      #  self.attributes[self.keyWord] = self.getWord().upper() # HACK

   def unmarkSentimentWord(self):
      self.mark({self.keySentiment : False})
      # TODO write this in parse
      #  self.attributes[self.keyWord] = self.getWord().lower() # HACK
      
   def isSentimentWord(self):
      if self.attributes.get(self.keySentiment) == True:
         return True
      else:
         return False

class ParseTree:

   tree = {}
   label = ""
   

   def createTree(self):
      self.tree = {}
      self.label = ""
      
   
   # int, int, dictionary
   def addNode(self, nodeID, fatherID, attributes):
      #  print "add node " + str(nodeID)
      
      # Hack for non-working labels in Bohnet Parser
      # TODO delete this
      if nodeID == 1:
         word = attributes.get(ParseTreeNode.keyWord)
         word = word.strip()
         # HACK Format 1: Labels are marked as 1:/-1: before sentence
         if word[len(word)-1] == ":": # This is a label
            self.label = word[0:len(word)-1]
            #  print "Label set to " + self.label
            return 
         # HACK Format 2: Labels are just 1/-1 before sentence
         if word == "1" or word == "-1":
            self.label = word
            return
            
      # TODO change label for father to 0 if father doesn't exist??
      
      # Normal nodes
      node = ParseTreeNode(nodeID, fatherID, attributes)
      self.tree[nodeID] = node    
   
   def isEmpty(self):
      return not self.tree
   
      
   def printTree(self):
      for nodeID in self.tree:
         print self.tree[nodeID]
         
         
      
   def findSentimentWord(self):
      for nodeID in self.tree:
         node = self.tree[nodeID]
         word = node.getWord()
         if node.isSentimentWord():
            return node
         # Old Hack
         #  if word.isupper():
            #  return node
         
      return -1
      
      
   def getParentNode(self, node): # TODO not return 0 but empty node
      nodeID = node.getID()
      if nodeID == 0:
         return 0
      node = self.tree[nodeID]
      father = node.getParentID()
      #  print "This node is " + str(node.getID()) + " " + str(father) # TEST !!!
      #  print self.getWholeSentence()
      if father == 0: # 0 is ROOT
         return 0
      if father == 1: # HACK because sometimes 1 == label because Label doesn't work
         try:
            #  print "father is 1"
            fathernode = self.tree[father]
            return fathernode
         except KeyError:
            #  print "error, return 0"
            return 0
      fathernode = self.tree[father]
      #  print "Papa is " + str(fathernode.getID()) # TEST !!!
      return fathernode
      
      
   def getChildNodes(self, node):
      #  return [i for (i, tok) in enumerate(tokenlist) if tok==token]
      nodeID = node.getID()
      return [n for n in self.tree.values() if n.getParentID()==nodeID]
      #  idlist = []
      #  for (id, father, attributes) in self.tree:
         #  if father == nodeID:
            #  idlist.append(id)
      #  return idlist

   
   def getAllChildNodes(self, node, level):
      toBeProcessed = [node]
      kindergarden = []
      #  print "Working at level " + str(level) + " with [" + str(node.getID()) + "] to be processed " # TEST !!!
      
      while level > 0 and toBeProcessed:
         #  tbd = ""  # TEST !!!
         #  for i in toBeProcessed: # TEST !!!
            #  tbd = tbd + " " + str(i.getID()) # TEST !!!
         #  print "Working at level " + str(level) + " with [" + tbd + "] to be processed " # TEST !!!

         # Get direct children for every element in current list
         # Add them to the list of all children (kindergarden)
         # and to the list to be processed in the next round
         nextInLine = []
         for current in toBeProcessed:
            children = self.getChildNodes(current)
            for c in children:
               #  print "Bringing " + str(c) + " to the kindergarden"
               kindergarden.append(c)
               nextInLine.append(c)
         toBeProcessed = nextInLine
         level = level - 1
         
         # Could add something for more efficiency
      
      return kindergarden
   
   
   def getWholeSentence(self):
      sentence = []
      for nodeID in self.tree:
         node = self.tree[nodeID]
         sentence.insert(node.getID(), node.getWord())
      return sentence
      
   def getWholeSentenceMarkSentiment(self):
      sentence = []
      for nodeID in self.tree:
         node = self.tree[nodeID]
         if node.isSentimentWord():
            sentence.insert(node.getID(), "__" + node.getWord() + "__")
         else:
            sentence.insert(node.getID(), node.getWord())
      return sentence
      
   def getWholeSentenceString(self):
      sentence = ""
      for nodeID in self.tree:
         node = self.tree[nodeID]
         sentence = sentence + node.getWord() + " "
      return sentence.strip()
      
   def isWordMarked(self,word):
      if word[0:1] == "__":
         print "anfang"
         if word[len(word)-2,len(word)-1] == "__":
            print "ende"
            return True
      return False
      
   def findLabel(self): 
      return self.label
      
   def getLabel(self): 
      return self.label
      
   def getIterator(self):
      return ParseTreeIterator(self.tree)
         
   def getNodeInSentence(self, nodeID):
      if nodeID >= min(self.tree.keys()) and nodeID <=  max(self.tree.keys()):
         return self.tree[nodeID]
      else:
         return None
      
      
   
class ParseTreeIterator:
   
      
   def __init__(self, tree):
      self.iterator = min(tree.keys())-1 # -1 because I increment before access in next
      self.tree = tree
      self.max = max(tree.keys())
      
   def next(self):
      self.iterator = self.iterator+1
      if self.iterator > self.max:
         #  print "iterator : " + str(self.iterator)
         return ""
      else:
         #  print "iterator : " + str(self.iterator) + " node: " + str(self.tree[self.iterator])
         return self.tree[self.iterator]