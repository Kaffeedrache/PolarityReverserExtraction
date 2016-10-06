#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 25.11.11

"""
Checks if a word is a proper sentiment word.
"""

import sys
sys.path.append("../../Utils") 
import parseutils


def isProperSentimentWord(word, pos, lemma, dictionary):
   """
   Check if a word or its lemma is in the dictionary and 
   if it has a POS tag that corresponds to the entry in the dictionary.
   @returns False if the word or its lemma is 
            a) not in the dictionary or
            b) doesn't have the POS tag like the dictionary entry.
         True if the entry corresponds.
   """
   
   # Add all dictionary entries for word and lemma
   # to a set
   # (use set to avoid multiple entries)
   # (use a different data structure to avoid
   # manipulating dictionary entries / call by references!)
   sentimentPOSSet = set([])
   
   # Check dictionary for word,
   # Add POS tags of word to set
   sentimentPOSList1 = dictionary.get(word)
   if sentimentPOSList1 != None:
      sentimentPOSSet |= set(sentimentPOSList1)

   # We wouldn't gain anything from looking up the
   # lemma if it's the same.
   # If lemma is different from word form.
   # Search lemma in sentiment dictionary
   # and add found entries to set.      
   if word != lemma:
      sentimentPOSList2 = dictionary.get(lemma)
      if sentimentPOSList2 != None:
         sentimentPOSSet |= set(sentimentPOSList2)
   
   # Check if word or lemma was in the dictionary of sentiment words
   if sentimentPOSSet:
      #  if printing:
         #  print "Check " + "(" + lemma + "," + pos + ") in " + str(sentimentPOSSet) # TEST !!!
      #  print word + "(" + pos + ")" + " in dictionary" # TEST !!!
      
      # Check if the word's POS is equivalent to the POS in the set
      # (POS in dictionary are more general than the specific tagset)
      for sentimentPOS in sentimentPOSSet:
         if parseutils.isOfGeneralPOS(pos,sentimentPOS):
            # Word has correct POS
            return True
   
   return False


