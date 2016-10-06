#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 5.12.11


"""
Constructs a python dictionary from General Inquirer.
See http://www.wjh.harvard.edu/~inquirer/ for information.
"""

import sys
sys.path.append("../utils") 
import parseutils
sys.path.append("..") 
import utils


# See http://www.wjh.harvard.edu/~inquirer/homecat.htm for categories.
# Write in lowercase.
categoriesPositive = ['pos', 'pstv', 'posaff', 'pleasur', 'virtue', 'increas']
categoriesNegative = ['negativ', 'ngtv', 'negaff' , 'pain', 'vice', 'hostile' , 'fail' , 'enlloss' , 'wlbloss' , 'tran-loss']

# Categories as written in paper Choi & Cardie 2008
#  categoriesNegators = ['notlw','decreas']

# 'notlw' seems to be 'NOT' in our file (20 wirds)
# 'decreas' seems to be 'Decr' in our file (79 words)
categoriesNegators = ['not','decr']


posDictionary = {
   'noun' : parseutils.posNoun,
   'modif' : parseutils.posAdj,
   'supv' : parseutils.posVerb
}




def makeDictionaryPOS (dictionaryFile, label):
   """
   Insert all words from the file into the dictionary with sentiment "label",
   key is the word, value is the part of speech.
   Expected format: 
   ABOUT#5 H4Lvd Handels  | 8% idiom-verb: ""Bring (brought) about""--handled by ""bring""
   Word#Sense Categories* | Explanation
   Words are normalized to lowercase.
   
   @param dictionaryFile The file from which the dictionary will be read
   @param label The label the words should have (only words with this label
         will be inserted into the dictionary)
         should be either utils.negativeLabel or utils.positiveLabel
   """
   mydictionary = {}
   
   # Get list corresponding to label
   categoriesList = []
   if label==utils.negativeLabel:
      categoriesList = categoriesNegative
   if label==utils.positiveLabel:
      categoriesList = categoriesPositive
      
   #  if label==0:
      #  categoriesList = categoriesNegators
   
   # Read in dictionary
   firstLine = True
   input_file = open(dictionaryFile)
   for line in input_file:
      
      # Skip first line
      if firstLine:
         firstLine = False
         continue
      
      line = line.strip()
      # Split into before and after description
      parts = line.split('|')
      # Split into words and categories
      categories = parts[0].split()
      
      # Get word
      word = categories[0].lower()
      #  print "Word: " + word # TEST !!!
      
      # Remove senses
      # Senses are separated by a # and a number,
      # e.g. happy#2
      # Split on #, set word to be only the first part
      wordsplit = word.split("#")
      if len(wordsplit)>1:
         word = wordsplit[0]
      
      # Check for categories
      # categories[0] is the word, so start with [1]
      pos = []
      isCorrectCategory = False
      for category in categories[1:]:
         #  print "Category: " + category # TEST !!!
         
         # Check if the word is in one of the categories we want,
         if category.lower() in categoriesList:
            isCorrectCategory = True
         
         # Check if the category is a POS tag, if yes, save in 'pos'
         if category.lower() in posDictionary:
            if pos == []:
               pos = [posDictionary.get(category.lower())]
            else:
               pos.append(posDictionary.get(category.lower()))

      # Write to word to dictionary
      if isCorrectCategory:
         
         # Set POS to Joker if no POS was found
         if pos == []:
            pos = [parseutils.posJoker]
         
         # Word is already in dictionary, append all new pos
         previousPos = mydictionary.get(word)
         if previousPos != None:
            pos.extend(previousPos)
         
         # Set POS as entry in dict
         mydictionary[word] = pos
         
         #  print word + " " + str(mydictionary[word]) # TEST !!!
      
   return mydictionary




#  negdict = makeDictionaryPOS ("/mount/corpora11/d7/Data/Sentiment-Dictionary/gi_dictionary",utils.negativeLabel)

#  for n in sorted(negdict):
   #  if (len(negdict.get(n))) >= 2:
      #  print n + " " + str(negdict.get(n))

#  print "dict has " + str(len(negdict)) + " entries"
#  mergedlist = []

#  i = 0
#  for v in negdict.values():
   #  i+=1
   #  mergedlist.extend(v)
   #  print v
   #  print "=>" + str( mergedlist)
   #  if i>10:
      #  break
      
#  print len(v)

#  import itertools
#  a =  [i for i in itertools.chain.from_iterable(negdict.values())]

#  print len(a)
#  print a