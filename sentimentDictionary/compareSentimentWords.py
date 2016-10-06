#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 21.12.11


"""
@DEPRECATED
"""

from operator import itemgetter

import dictionaryWWH
import dictionaryGI
import dictionaryStanfordClassifier
import checkWordOcurrences

import utils

corpusFile = "../../Data/parsedCorpora/cellphonesProsConsAll.txt"
stanfordFile = "featureWeights.sc"

# --- Language of the files to process. --- 
# Affects the choice of parser and classes to read/write parse trees
# as well as the sentement dictionary.
# Possible choices are 
# EN : English
# DE : German
# ES : Spanish
language = "EN"

# Files containing sentiment dictionaries for different languages
dictfiles = {
   "EN" : "../../Data/subjclueslen1-HLTEMNLP05.tff",
   "EN2" : "/mount/corpora11/d7/Data/Sentiment-Dictionary/gi_dictionary",
   "DE" : "asdf"
}

# --- Settings for dictionary --- 
# POS tags to exclude from dictionary
posExcludeList = [] # don't exclude anything
#  posExcludeList = [utils.posVerb, utils.posAdj, utils.posNoun]  # only Adv
#  posExcludeList = [utils.posVerb, utils.posAdv, utils.posNoun, utils.posJoker]  # only Adj
#  posExcludeList = [utils.posJoker] # all but anypos
#  posExcludeList = [utils.posVerb] # all but verbs
#  posExcludeList = [utils.posNoun] # all but noun
#  posExcludeList = [utils.posAdj] # all but adj
#  posExcludeList = [utils.posAdv] # all but adv
#  posExcludeList = [utils.posAdv,utils.posJoker] # all but adv, anypos
# Use only words marked as 'strongsubj'
#  strongsubj = True
strongsubj = False



def compareDicts (dictWords, dictCompare):
   """
   """
   mydict = {}
   for word in dictWords:
      if dictCompare.get(word) != None:
         mydict[word] = dictWords.get(word)
   return mydict




# ==== Create sentiment word dictionaries

dictfile = dictfiles.get(language)
if language == "EN":
   dictionaryPositive = dictionaryWWH.makeDictionaryPOS (dictfile, utils.positiveLabel,strongsubj,posExcludeList)
   dictionaryNegative = dictionaryWWH.makeDictionaryPOS (dictfile, utils.negativeLabel,strongsubj,posExcludeList)
elif language == "EN2":
   dictionaryPositive = dictionaryGI.makeDictionaryPOS (dictfile, utils.positiveLabel)
   dictionaryNegative = dictionaryGI.makeDictionaryPOS (dictfile, utils.negativeLabel)
print "... created dictionaries from file " + dictfile + " (" + str(strongsubj) + "," + str(posExcludeList) + ")."

#  print "Positive words (manual dictionary):" # TEST !!!
#  for (entry,value) in dictionaryPositive.items(): # TEST !!!
   #  print entry + ": " + str(value) # TEST !!!
#  print "Positive dict contains " + str(len(dictionaryPositive)) + " words."

#  print "Negative words (manual dictionary)::" # TEST !!!
#  for (entry,value) in sorted(dictionaryNegative.items()): # TEST !!!
   #  print entry + ": " + str(value) # TEST !!!
#  print "Negative dict contains " + str(len(dictionaryNegative)) + " words."

# ==== Get only words that ocurr in corpus

#  dictionaryPositiveOcc = checkWordOcurrences.checkWordOcurrences(dictionaryPositive, corpusFile)
#  dictionaryNegativeOcc = checkWordOcurrences.checkWordOcurrences(dictionaryNegative, corpusFile)

# Hack: Print POS of dictionaryPositive instead of value, but keep that dictionary to be able to sort by frequency.... change that

#  print "Positive words (manual dictionary, occurrence filtered):" # TEST !!!
#  for (entry,value) in  reversed(sorted(dictionaryPositiveOcc.items(), key=itemgetter(1))): # TEST !!!
   #  print entry + " " + str(dictionaryPositive.get(entry))  + ": " + str(value) # TEST !!!
#  print "Positive dict contains " + str(len(dictionaryPositiveOcc)) + " words."

#  print "Negative words (manual dictionary, occurrence filtered):" # TEST !!!
#  for (entry,value) in  reversed(sorted(dictionaryNegativeOcc.items(), key=itemgetter(1))): # TEST !!!
   #  print entry + " " + str(dictionaryNegative.get(entry))  + ": " + str(value) # TEST !!!
#  print "Negative dict contains " + str(len(dictionaryNegativeOcc)) + " words."



# ==== Get Stanford classifier features

pos, neg = dictionaryStanfordClassifier.makeDictionary (stanfordFile)

#  print "=== Positive words (Stanford classifier) ===" # TEST !!!
#  for (entry,value) in sorted(pos.items(), key=itemgetter(1)): # TEST !!!
   #  print entry + ": " + str(value) # TEST !!!
#  print "Positive dict contains " + str(len(pos)) + " words." 
   
#  print "=== Negative words (Stanford classifier) ===" # TEST !!!
#  for (entry,value) in reversed(sorted(neg.items(), key=itemgetter(1))): # TEST !!!
   #  print entry + ": " + str(value) # TEST !!!
#  print "Negative dict contains " + str(len(neg)) + " words."


# ==== Compare

comparePos = compareDicts(dictionaryPositive,  pos)

print "=== Positive words (filtered) ===" # TEST !!!
for (entry,value) in sorted(comparePos.items()): # TEST !!!
   print entry + ": " + str(value) # TEST !!!
print "Positive dict contains " + str(len(comparePos)) + " words."

compareNeg = compareDicts(dictionaryNegative,  neg)

print "=== Negative words (filtered) ===" # TEST !!!
for (entry,value) in sorted(compareNeg.items()): # TEST !!!
   print entry + ": " + str(value) # TEST !!!
print "Negative dict contains " + str(len(compareNeg)) + " words."