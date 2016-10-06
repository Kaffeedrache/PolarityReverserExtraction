#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 21.12.11


"""

"""
from operator import itemgetter


import sys
sys.path.append("../Utils") 
import parseutils


threshold = 1000

  
def setThreshold(newThreshold):
   """ 
   Sets the threshold for considering to score a candidate.
   threshold=0 means no threshold.
   """
   print "Classifier threshold: " + str(newThreshold)
   global threshold 
   threshold = newThreshold


def isWord (word):
   """
   A string is a word if it contains only
      - alphanumeric characters [a-zA-z]
      - apostrophe [']
      - hyphen [-]
   """
   # Have to adjust for non-English letters
   # May allow . 
   for i in word:
      if not i.isalpha() and i != "'" and i != "-":
         return False
   return True


def makeDictionary (dictionaryFile):
   """
   Read in ALL values in file!
   """
   mydictionary = {}
   
   # Read in dictionary
   input_file = open(dictionaryFile)
   lineNo = 0
   for line in input_file:
      lineNo += 1
      
      # Skip first 3 lines
      if lineNo < 4:
         continue
      
      line = line.strip()
      if line != "":
         
         # Split into parts
         parts = line.split(' ')
         
         # Word is first part, remove preceding "1-SW-"
         word = parts[0][5:]
         if word == "" or not isWord(word):
            #  print "Is not a word: " + word  # TEST !!!
            continue
            
         # Value is last part, convert to float
         try:
            value = float(parts[len(parts)-1])
         except exceptions.ValueError:
            print "Value Error: " + parts[len(parts)-1]
            continue
         
         # Normalize word
         word = word.lower()
         # only 
         #  print word + " " + str(value) # TEST !!!
         mydictionary[word] = float(parts[len(parts)-1])
      
      #  if lineNo > 50: # TEST !!!
         #  break # TEST !!!
      
   return mydictionary
   
   

def makeDictionaryNumbers (dictionaryFile):
   """
   Return dictionaries of X most positive and X most
   negative features.
   Value is feature weight.
   """
   
   mydictionary = makeDictionary (dictionaryFile)

   # Positive dictionary - first entries
   myposdict = {}
   itemno = 0
   for i in sorted(mydictionary.items(), key=itemgetter(1)):
      myposdict[i[0]] = i[1]
      itemno += 1
      if itemno > threshold:
         break
   
   # Negative dictionary - last entries
   mynegdict = {}
   itemno = 0
   for i in reversed(sorted(mydictionary.items(), key=itemgetter(1))):
      mynegdict[i[0]] = i[1]
      itemno += 1
      if itemno > threshold:
         break
   
   return myposdict, mynegdict


def makeDictionaryPOS (dictionaryFile):
   """
   Return dictionaries of X most positive and X most
   negative features.
   Value is "anypos".
   """
   mydictionary = makeDictionary (dictionaryFile)
   
   # Positive dictionary - first entries
   myposdict = {}
   itemno = 0
   for i in sorted(mydictionary.items(), key=itemgetter(1)):
      myposdict[i[0]] = [parseutils.posJoker]
      itemno += 1
      if itemno > threshold:
         break
   
   # Negative dictionary - last entries
   mynegdict = {}
   itemno = 0
   for i in reversed(sorted(mydictionary.items(), key=itemgetter(1))):
      mynegdict[i[0]] = [parseutils.posJoker]
      itemno += 1
      if itemno > threshold:
         break
   
   return myposdict, mynegdict