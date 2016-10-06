#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler,20.1.12


"""

"""

from operator import itemgetter

import dictionaryWWH
import dictionaryGI
import dictionaryStanfordClassifier
import checkWordOcurrences

import sys
sys.path.append("../PolarityReversers") 
import utils 


def getDictionaryGI (dictfile, positiveLabel, negativeLabel):
   dictionaryPositive = dictionaryGI.makeDictionaryPOS (dictfile, positiveLabel)
   dictionaryNegative = dictionaryGI.makeDictionaryPOS (dictfile, negativeLabel)
   #  print "... created dictionaries from file " + dictfile +  "."
   return dictionaryPositive, dictionaryNegative


def getDictionaryWWH (dictfile, positiveLabel, negativeLabel, strongsubj, posExcludeList):
   dictionaryPositive = dictionaryWWH.makeDictionaryPOS (dictfile, positiveLabel,strongsubj,posExcludeList)
   dictionaryNegative = dictionaryWWH.makeDictionaryPOS (dictfile, negativeLabel,strongsubj,posExcludeList)
   #  print "... created dictionaries from file " + dictfile + " (" + str(strongsubj) + "," + str(posExcludeList) + ")."
   return dictionaryPositive, dictionaryNegative


def getDictionaryStanfordClassifier (dictfile, threshold):
   dictionaryStanfordClassifier.setThreshold(threshold)
   dictionaryPositive, dictionaryNegative = dictionaryStanfordClassifier.makeDictionaryPOS (dictfile)
   return dictionaryPositive, dictionaryNegative


def compareDicts (dictWords, dictCompare):
   """
   """
   mydict = {}
   for word in dictWords:
      if dictCompare.get(word) != None:
         mydict[word] = dictWords.get(word)
   return mydict


def getDictionaryWWHStanfordFiltered (dictfileWWH, dictfileStanford, positiveLabel, negativeLabel, strongsubj, posExcludeList, threshold):
   posWWH, negWWH = getDictionaryWWH (dictfileWWH, positiveLabel, negativeLabel, strongsubj, posExcludeList)
   posStanf, negStanf = getDictionaryStanfordClassifier (dictfileStanford, threshold)

   # ==== Compare

   comparePos = compareDicts(posWWH,  posStanf)

   #  print "=== Positive words (filtered) ===" # TEST !!!
   #  for (entry,value) in sorted(comparePos.items()): # TEST !!!
      #  print entry + ": " + str(value) # TEST !!!
   #  print "Positive dict contains " + str(len(comparePos)) + " words."

   compareNeg = compareDicts(negWWH,  negStanf)

   #  print "=== Negative words (filtered) ===" # TEST !!!
   #  for (entry,value) in sorted(compareNeg.items()): # TEST !!!
      #  print entry + ": " + str(value) # TEST !!!
   #  print "Negative dict contains " + str(len(compareNeg)) + " words."

   return comparePos, compareNeg


def getDictionaryGIStanfordFiltered (dictfileGI, dictfileStanford, positiveLabel, negativeLabel):
   posGI, negGI = getDictionaryGI (dictfileGI, positiveLabel, negativeLabel)
   posStan, negStan = getDictionaryStanfordClassifier (dictfileStanford)

   # ==== Compare

   comparePos = compareDicts(posGI,  posStanf)

   #  print "=== Positive words (filtered) ===" # TEST !!!
   #  for (entry,value) in sorted(comparePos.items()): # TEST !!!
      #  print entry + ": " + str(value) # TEST !!!
   #  print "Positive dict contains " + str(len(comparePos)) + " words."

   compareNeg = compareDicts(negGI,  negStanf)

   #  print "=== Negative words (filtered) ===" # TEST !!!
   #  for (entry,value) in sorted(compareNeg.items()): # TEST !!!
      #  print entry + ": " + str(value) # TEST !!!
   #  print "Negative dict contains " + str(len(compareNeg)) + " words."

   return comparePos, compareNeg



def dictionaryFactory(dictionaryLocations, dictionaryType, strongsubj = True, posExcludeList = [], classifierThreshold = 500):

   # Create sentiment word dictionaries
   if dictionaryType == "WWH":
      dictionaryLocation = dictionaryLocations.get(dictionaryType)
      dictionaryPositive, dictionaryNegative = getDictionaryWWH(dictionaryLocation, utils.positiveLabel, utils.negativeLabel, strongsubj, posExcludeList)
   elif dictionaryType == "GI":
      dictionaryLocation = dictionaryLocations.get(dictionaryType)
      dictionaryPositive, dictionaryNegative = getDictionaryGI(dictionaryLocation, utils.positiveLabel, utils.negativeLabel)
   elif dictionaryType == "Stanf":
      dictionaryLocation = dictionaryLocations.get(dictionaryType)
      dictionaryPositive, dictionaryNegative = getDictionaryStanfordClassifier(dictionaryLocation, classifierThreshold)
   elif dictionaryType == "WWH_Stanf":
      dictfileWWH = dictionaryLocations.get("WWH")
      dictfileStanf = dictionaryLocations.get("Stanf")
      dictfile = dictfileWWH + " " + dictfileStanf
      dictionaryPositive, dictionaryNegative = getDictionaryWWHStanfordFiltered(dictfileWWH, dictfileStanf, utils.positiveLabel, utils.negativeLabel, strongsubj, posExcludeList, classifierThreshold)

   return dictionaryPositive, dictionaryNegative

