#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 30.11.11

import reverserFinder


class ReverserFinderWordLevel (reverserFinder.ReverserFinder):
   """
   Go through sentence, check all words closer than self.windowsize 
   on both sides of the sentiment word
   against the dictionary if one of them is a reverser.
   """
   
   def __init__ (self,windowsize):
      self.windowsize = windowsize

   def findReversers(self, sentimentWord, tree):
      """
      Go through sentence, check all words closer than self.windowsize 
      on both sides of the sentiment word
      against the dictionary if one of them is a reverser.
      Return number of reversers found in vicinity.
      """
      
      #  print tree.getWholeSentence()
      sentimentWordID = sentimentWord.getID()
      numberOfReversers = 0
      for i in range(sentimentWordID-self.windowsize, sentimentWordID+self.windowsize+1):
         newnode = tree.getNodeInSentence(i)
         #  print str(i) + " " + str(newnode)
         if newnode != None and i != sentimentWordID:
            word = newnode.getWord()
            if word in self.reverserDict:
               numberOfReversers += 1
               #  print word + " is in dict"
               self.reverserDict[word] += 1
      
      return numberOfReversers




class ReverserFinderWordLevelOnlyLeft (reverserFinder.ReverserFinder):
   """
   Go through sentence, check all words closer than self.windowsize 
   on the left of the sentiment word
   against the dictionary if one of them is a reverser.
   Return number of reversers found in vicinity.
   """

   def __init__ (self,windowsize):
      self.windowsize = windowsize


   def findReversers(self, sentimentWord, tree):
      """
      Go through sentence, check all words closer than self.windowsize 
      on the left of the sentiment word
      against the dictionary if one of them is a reverser.
      """
      
      #  print tree.getWholeSentence()
      sentimentWordID = sentimentWord.getID()
      numberOfReversers = 0
      for i in range(sentimentWordID-self.windowsize, sentimentWordID):
         newnode = tree.getNodeInSentence(i)
         #  print str(i) + " " + str(newnode)
         if newnode != None and i != sentimentWordID:
            word = newnode.getWord()
            if word in self.reverserDict:
               numberOfReversers += 1
               #  print word + " is in dict"

      return numberOfReversers