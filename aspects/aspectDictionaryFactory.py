#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 6.9.12


"""

"""


import aspectDictionary


def createAspectDictionary(aspectsMode, aspectsFile, aspectsThreshold):
   # Credit aspect dictionary
   dictionaryAspects = {}
   aspectFinder = aspectDictionary.AspectDictionary()
   if aspectsMode == "Calculate" or aspectsMode == "Save":
      aspectFinder.setThreshold(aspectsThreshold)
      aspectFinder.setParseReader(parseReader, parsedFilename)
      dictionaryAspects = aspectFinder.findAspects ([parsedFilename])
      aspectFinder.cleanup()
      #  print "... created aspect dictionary from file " + parsedFilename + "."
      if aspectsMode == "Save":
         aspectFinder.saveAspectDictionary(dictionaryAspects, aspectsFile)
         #  print "... saved aspect dictionary to file " + aspectsFile + "."
   elif aspectsMode == "Load":
      aspectFinder.setThreshold(aspectsThreshold)
      dictionaryAspects = aspectFinder.loadAspectDictionary(aspectsFile)
      #  print "... loaded aspect dictionary from file " + aspectsFile + "."
      
   #  print "Aspects: " # TEST !!!
   #  for aspect in reversed(sorted(dictionaryAspects.items(), key=itemgetter(1))): # TEST !!!
      #  print aspect # TEST !!!
   #  print "Aspect dict contains " + str(len(dictionaryAspects)) + " words." # TEST !!!

   return dictionaryAspects




#  corpusFolder = "../../Data/parsedCorpora/"
#  parsedFilename = corpusFolder +"camerasCellphonesProsCons_Parsed.txt" # pros/cons cellphones and cameras

#  parseReader = parseReaderBohnet.ParseReaderBohnet()
#  aspectFinder = AspectDictionary()
#  aspectFinder.setParseReader(parseReader, parsedFilename)

#  aspects = aspectFinder.findAspects ([parsedFilename])

#  for aspect in reversed(sorted(aspects.items(), key=itemgetter(1))):
   #  print aspect