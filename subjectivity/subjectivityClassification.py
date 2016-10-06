#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 6.9.12

"""

"""

import sys
sys.path.append("../Utils") 
import parsetrees
import parseutils


sys.path.append("../base")
import sentimentwords


class SubjectivityClassifier:
   
   # Set to default = do nothing
   aspectMode = "None"
   POSIgnored = []
   doCheckPOS = False
   modifierMode = False
   dictionaryPositive = []
   dictionaryNegative = []
   
   
   def setPOSIgnored(self, POSIgnored):
      self.POSIgnored = POSIgnored
      self.doCheckPOS = (len(POSIgnored) >= 1)

      
   def setModifierMode(self, modifierMode):
      self.doCheckModifiers = modifierMode


   def setAspectDictionary(self, dictionaryAspects):
      """
      Possible values: 
      """
      self.dictionaryAspects = dictionaryAspects
      self.doCheckAspects = (len(dictionaryAspects) >= 1)
      
      #  print "Aspects: " # TEST !!!
      #  for aspect in reversed(sorted(aspectDictionary.items(), key=itemgetter(1))): # TEST !!!
         #  print aspect # TEST !!!
      #  print "Aspect dict contains " + str(len(dictionaryAspects)) + " words." # TEST !!!


   def setSentimentDictionaries(self, dictionaryPositive, dictionaryNegative):
      self.dictionaryPositive = dictionaryPositive
      self.dictionaryNegative = dictionaryNegative



   
   def wordIsSubjective(self, node, tree):
      """
      
      """
      
      # Get word, lemma and POS in parse
      word = node.getWord()
      pos = node.getPOS()
      lemma = node.getAttribute(parsetrees.ParseTreeNode.keyLemma)
      
      if self.doCheckPOS:
         if self.checkIsPOSignore(pos):
            #  print "here we have POS to ignore for " + lemma  + " (" + pos + ")"# TEST !!!
            return False
         #  else:
            #  print "No POS to ignore for " + lemma  + " (" + pos + ")"# TEST !!!
      if self.doCheckModifiers:
         if self.checkIsModifier(pos, node, tree):
            #  print "here we have father issues for " + lemma  + " (" + pos + ")"# TEST !!!
            return False
         #  else:
            #  print "No Modifer for " + lemma  + " (" + pos + ")"# TEST !!!
      if self.doCheckAspects:
         if self.checkIsInAspect(lemma, node.getID(), tree):
            #  print "is in aspect " + lemma  + " (" + pos + ")"# TEST !!!
            return False
         #  else:
            #  print "No aspect for " + lemma  + " (" + pos + ")"# TEST !!!
      
      return True





   def checkIsPOSignore(self, pos):
      """
      Check if the word has a POS that is to be ignored.
      @returns True if this is a to-be-ignored POS,
         False otherwise.
      """
      if pos in self.POSIgnored:
         return True
      else:
         return False



   def checkIsModifier(self, pos, node, tree):
      """
      Check if the word modifies another sentiment word.
      Do this only for adverb.
      @returns True if this is a modifier word,
         False otherwise.
      """

      # Filter out polarity shifters, words that modify
      # other sentiment words.
      # Do this only for adverbs.
      # Maybe do this only for adverb/adjective
      # or adverb/verb or adverb/adverb.
      # Might do this for adj/noun, but there are
      # many problematic cases.

      if parseutils.isOfGeneralPOS(pos, parseutils.posAdv): #or parseutils.isOfGeneralPOS(pos, parseutils.posAdj) and parseutils.isOfGeneralPOS(fatherpos, parseutils.posNoun):
         
         # Check father
         fathernode = tree.getParentNode(node)
         if fathernode != 0:
         
            # Get father's word, lemma and POS in parse
            fatherword = fathernode.getWord()
            fatherpos = fathernode.getPOS()
            fatherlemma = fathernode.getAttribute(parsetrees.ParseTreeNode.keyLemma)
         
            # Check if the word/lemma of the parent node
            # is a sentiment word. If positive or negative doesn't
            # matter in this case.
            # If father is a sentiment word, the word is used
            # as a polarity shifter, it's not a sentiment word
            # on its own.
            if sentimentwords.isProperSentimentWord(fatherword, fatherpos, fatherlemma, self.dictionaryPositive):
               return True
            elif sentimentwords.isProperSentimentWord(fatherword, fatherpos, fatherlemma, self.dictionaryNegative):
               return True
      return False



   def checkIsInAspect(self, lemma, nodeId, tree):
      """
      Check if a word or its lemma is part of an aspect.
      Check only aspect bigrams.
      @returns True if this is a sentiment word in an aspect,
         False otherwise.
      """

      # Check if is in bigram with next node in sentence
      nextNode = tree.getNodeInSentence(nodeId + 1)
      if nextNode != None:
         nextLemma = nextNode.getLemma()
         bigram = lemma + " " + nextLemma
         #  print "Check bigram: " + bigram # TEST !!!
         isInThere = self.dictionaryAspects.get(bigram)
         if isInThere != None:
            #  print "Have bigram: " + bigram # TEST !!!
            return True
      
      # Check if is in bigram with previous node in sentence
      prevNode = tree.getNodeInSentence(nodeId - 1)
      if prevNode != None:
         prevLemma = prevNode.getLemma()
         bigram = prevLemma + " " +  lemma
         #  print "Check bigram: " + bigram # TEST !!!
         isInThere = self.dictionaryAspects.get(bigram)
         if isInThere != None:
            #  print "Have bigram: " + bigram # TEST !!!
            return True
      
      # Not in aspect - return false
      return False
   