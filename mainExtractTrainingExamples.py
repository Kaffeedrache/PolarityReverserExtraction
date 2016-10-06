#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 10.10.11

"""
Create feature files for reversed/non-reversed words.
"""

import settingsclassification as settings
import utils

import sys

sys.path.append("utils") 
import parsetrees
import parseReaderBohnet
import parseutils

sys.path.append("sentimentDictionary") 
import sentimentDictionary

sys.path.append("aspects") 
import aspectDictionaryFactory


sys.path.append("base")
import contextFinderTrees
import representationFactory
import sentimentwords

sys.path.append("subjectivity")
import subjectivityClassification

sys.path.append("featureextraction")
import featureextractorFactory

import itertools


#  debug = False
debug = True


# ---- SETTINGS ---

sys.argv.pop(0) # remove first
while len(sys.argv) >= 1:
   value = ""
   name = sys.argv.pop(0)
   if name in settings.allOptionsBinary and len(sys.argv) >= 1:
      value = sys.argv.pop(0)
   settings.setOption(name,value)



# ---- INITIALIZATION ---


# Initialize parser for data corpus
parseReader = parseReaderBohnet.ParseReaderBohnet()
parseReader.setInputFile(settings.sentencesParsedFile.get(settings.corpusType))
print "+ Data from file " + settings.sentencesParsedFile.get(settings.corpusType)



# Initialize sentiment dictionary
dictionaryPositive, dictionaryNegative = sentimentDictionary.dictionaryFactory(settings.dictionaryLocations, settings.dictionaryType, settings.strongsubj, settings.posExcludeList, settings.classifierThreshold)
#  dictionaryPositive = {} # TEST !!!
#  dictionaryNegative = {} # TEST !!!
print "+ Created dictionary type "  + settings.dictionaryType  + " (only strong " + str(settings.strongsubj) + ", exclude " + str(settings.posExcludeList) + "):"
#  print "Positive words:" # TEST !!!
#  for (entry,value) in dictionaryPositive.items(): # TEST !!!
   #  print entry + ": " + str(value) # TEST !!!
print "Positive dict contains " + str(len(dictionaryPositive)) + " words, a total of " + str(len( [i for i in itertools.chain.from_iterable(dictionaryPositive.values())]))  +" entries."
#  print "Negative words:" # TEST !!!
#  for (entry,value) in dictionaryNegative.items(): # TEST !!!
   #  print entry + ": " + str(value) # TEST !!!
print "Negative dict contains " + str(len(dictionaryNegative)) + " words, a total of " + str(len( [i for i in itertools.chain.from_iterable(dictionaryNegative.values())]))  +" entries."
print "Entries in both dictionaries:" # TEST !!!
for (entry,value) in sorted(dictionaryPositive.items()): # TEST !!!
   if entry in dictionaryNegative: # TEST !!!
      print entry + ": " + str(value) + " " + str(dictionaryNegative.get(entry)) # TEST !!!


# Initialize subjectivity classifier
if settings.analyseSubjectivity:
   print "+ Analyse subjectivity:"
   subjectivityClassifier = subjectivityClassification.SubjectivityClassifier()
   subjectivityClassifier.setSentimentDictionaries(dictionaryPositive, dictionaryNegative)
   if settings.posIgnore:
      print "Ignore POS " + str(settings.posIgnoreAsSentimentWord) + " as sentiment words." # TEST !!!   
      subjectivityClassifier.setPOSIgnored(settings.posIgnoreAsSentimentWord)
   print "Check shifters is " + str(settings.ignoreShifters) + "."# TEST !!!
   subjectivityClassifier.setModifierMode(settings.ignoreShifters)
   print "Aspect mode is " + settings.aspectsMode + " for threshold " + str(settings.aspectsThreshold) + " and file " + settings.aspectsFile + "." # TEST !!!
   aspectDictionary = aspectDictionaryFactory.createAspectDictionary(settings.aspectsMode, settings.aspectsFile, settings.aspectsThreshold)
   #  print "Aspects: " # TEST !!!
   #  for aspect in reversed(sorted(aspectDictionary.items(), key=itemgetter(1))): # TEST !!!
      #  print aspect # TEST !!!
   print "Aspect dict contains " + str(len(aspectDictionary)) + " words." # TEST !!!
   subjectivityClassifier.setAspectDictionary(aspectDictionary)
else:
   print "+ Do not analyse subjectivity."


# PRC representation
print "+ Create context extractor:"
representationPRCs = representationFactory.createPRCRepresentation(settings.representationPRCs)
print "Representation is " + str(settings.representationPRCs)
contextFinder = contextFinderTrees.TreeContextFinder()
contextFinder.setWindowsize(settings.windowsize)
contextFinder.setRepresentation(representationPRCs)
print "Context finder is " + contextFinder.__class__.__name__ + " with window size " + str(settings.windowsize)



# FeatureExtractor
featureExtractors = []
print "+ Create feature extractors, outfiles in "  + settings.getFeFilenamePrefix()
for feName in settings.featureExtractorNames:
   fe = featureextractorFactory.createFeatureExtractor(feName, settings.getFeFilenamePrefix(), contextFinder, settings.reverserFileGold.get(feName), settings.cutoffThreshold)
   fe.setWriteToFile(True)
   featureExtractors.append(fe)





# ---- PROCESSING ---


print "Extract features........"


numberSentences = 0
numberIstances = 0
wordsNonreversed = 0
wordsReversed = 0


while True:
   tree = parseReader.readParse()
   if tree.isEmpty(): 
      break
   
   sentence = tree.getWholeSentence()
   numberSentences += 1
   sentencePolarity = tree.getLabel()
   if debug: print str(sentencePolarity) + " / " + str(sentence) # TEST !!!
   
   if sentencePolarity == 0: # ignore neutral sentences
      continue
      
   # Use only negative / positive sentences # TEST !!!
   #  if label == utils.negativeLabel: # TEST !!!
      #  continue # TEST !!!

   iter = tree.getIterator()
   node = iter.next()
   
   while node != "": 
      
      
      word = node.getWord()
      pos = node.getPOS()
      lemma = node.getAttribute(parsetrees.ParseTreeNode.keyLemma)
      
      # 1. Find sentiment word.
      # 2. Extract as nonreversed if sentence polarity = word polarity
      #     Extract as reversed if sentence polarity != word polarity
      
      wordPolarity = 0
      
      # Negative words
      if sentimentwords.isProperSentimentWord(word, pos, lemma, dictionaryNegative):
         #  if debug: print word +"-> is negative" + utils.negativeLabel # TEST !!!
         wordPolarity = utils.negativeLabel
         
      # Positive words
      if sentimentwords.isProperSentimentWord(word, pos, lemma, dictionaryPositive):
         #  if debug: print word +"-> is positive" + utils.positiveLabel # TEST !!!
         if wordPolarity != 0:
            # Word is in both dictionaries
            # Set to sentence polarity, default is nonreversed
            wordPolarity = sentencePolarity
            #  wordPolarity = sentencePolarity * (-1) # extract as reversed # TODO REMOVE
         else:
            wordPolarity = utils.positiveLabel
         
      # Neutral words / not in dictionary
      if wordPolarity == 0:
         node = iter.next()
         continue
      
      # If subjectivity is analysed and the example is not subjective,
      # ignore this word
      if settings.analyseSubjectivity:
         if not subjectivityClassifier.wordIsSubjective(node, tree):
            node = iter.next()
            if debug: print word +"-> is not subjective" # TEST !!!
            continue
         
      numberIstances += 1
      
      # Extract the reversed / nonreversed words
      if sentencePolarity == wordPolarity: 
         #  if debug: print word +"-> is nonreversed" # TEST !!!
         label = utils.labelNonreversed
         wordsNonreversed += 1
      else:
         #  if debug: print word +"-> is reversed" # TEST !!!
         label = utils.labelReversed
         wordsReversed += 1
   
      # Do something for this node with the feature extractors
      # that have been registered
      for extractor in featureExtractors:
         ftrs = extractor.extractFeatures(node, tree, label)
         if debug: print "extract with " + extractor.getName() + ": " + word + " / " + label + " / " + str(ftrs) # TEST !!!


      # Debug
      if debug: print str(numberIstances) + ". word " + word + " => " + str(label) # TEST !!!
      
      # Next node
      node = iter.next()


print "... processed " + str(numberSentences) + " sentences, " + str(numberIstances) + " sentiment words."
print "... " + str(wordsNonreversed) + " words in them are not reversed ( = " + str(float(wordsNonreversed)/float(numberIstances)) + ")."
print "... " + str(wordsReversed) + " words in them are reversed ( = " + str(float(wordsReversed)/float(numberIstances)) + ")."


# Clean up
for extractor in featureExtractors:
   print "do cleanup of " + str(extractor.__class__.__name__)
   extractor.cleanup()
parseReader.cleanup()

