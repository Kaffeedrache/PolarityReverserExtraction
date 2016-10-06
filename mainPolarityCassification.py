#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 3.9.12

"""
MAIN for polarity classification (word and sentence level)
"""

import settingsclassification as settings
import utils

import sys

sys.path.append("utils") 
import parsetrees
import parseReaderBohnet
import statistics
import parseutils
import goldCorpus

sys.path.append("sentimentDictionary") 
import sentimentDictionary

sys.path.append("aspects") 
import aspectDictionaryFactory


sys.path.append("base") 
import contextFinderTrees
import sentimentwords
import representationFactory

sys.path.append("subjectivity")
import subjectivityClassification

sys.path.append("inconsistency")
import inconsistencyClassification

from operator import itemgetter
import itertools



def convertToNumberStr(label):
   if label == utils.sentenceLabelPositive:
      return "1"
   elif label == utils.sentenceLabelNegative:
      return "-1"
   else:
      return "0"

def convertToNumberWordStr(label):
   if label == utils.wordLabelConsistent:
      return "1"
   elif label == utils.wordLabelInconsistent:
      return "-1"
   else:
      return "0"


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


# Initialize gold label corpus
goldLabelProvider = goldCorpus.GoldLabelProvider(settings.goldLabelsFile.get(settings.corpusType))
print "Labels from file " + settings.goldLabelsFile.get(settings.corpusType)



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
#  print "+ Create context extractor:"
#  representationPRCs = representationFactory.createPRCRepresentation(settings.representationPRCs)
#  print "Representation is " + str(settings.representationPRCs)
#  contextFinder = contextFinderTrees.TreeContextFinder()
#  contextFinder.setWindowsize(settings.windowsize)
#  contextFinder.setRepresentation(representationPRCs)
#  print "Context finder is " + contextFinder.__class__.__name__ + " with window size " + str(settings.windowsize)


# Initialize inconsistency classifier
if settings.analyseConsistency:
   print settings.inconsistencyClassificationID
   print settings.reverserFileGold.get(settings.inconsistencyClassificationID)
   inconsistencyClassifier = inconsistencyClassification.getClassifier(settings.inconsistencyClassifierType, settings.inconsistencyClassificationID, settings.representationPRCs, settings.windowsize, settings.reverserFileGold.get(settings.inconsistencyClassificationID), settings.cutoffThreshold, settings.getClassifierOutputFilename(settings.inconsistencyClassificationID) ) 
   print "+ Inconsistency classifier: " + inconsistencyClassifier.getName()


# Initialize evaluation table (contingency matrix)
wordLabelTableSubjectivity = statistics.LabelStatistics(utils.wordLabelsSubjectivity, "assigned", "gold")
wordLabelTableSubjectivity.initializeTable()
wordLabelTableSubjectivity.setLabelMapping(utils.labelMapSubjectivity)
wordLabelTableConsistency = statistics.LabelStatistics(utils.wordLabelsConsistency, "assigned", "gold")
wordLabelTableConsistency.initializeTable()
wordLabelTableConsistency.setLabelMapping(utils.labelMapConsistency)
sentenceLabelTable = statistics.LabelStatistics(utils.sentenceLabels, "assigned", "gold")
sentenceLabelTable.initializeTable()
sentenceLabelTable.setLabelMapping(utils.labelMapSentence)


doPrintout = True
#  doPrintout = False
if doPrintout:
   outFilenameSents = settings.getEvalOutputFilename(settings.inconsistencyClassifierType,settings.inconsistencyClassificationID, True)
   outFilenameWords = settings.getEvalOutputFilename(settings.inconsistencyClassifierType,settings.inconsistencyClassificationID, False)
   print "+ Evaluation output to " + outFilenameSents + " and " + outFilenameWords

# Output (in Stanford classifier format)
if doPrintout:
   outFileSentences = open(outFilenameSents, "w")
   outFileWords = open(outFilenameWords, "w")



# ---- PROCESSING ---

numberSentences = 0
numberPolarSentences = 0
numberIstances = 0
labelDistributionGold = {}
labelDistributionSystem = {}


print "===== Begin polarity classification ====="

while True:
   tree = parseReader.readParse()
   if tree.isEmpty(): 
      break
   
   sentence = tree.getWholeSentence()
   numberSentences += 1
   sentenceLabel = tree.getLabel()
   if debug: print str(sentenceLabel) + " / " + " ".join(sentence) # TEST !!!
   
   if sentenceLabel == 0: # ignore neutral sentences
      continue
      
   positivityScore = float(0)
   foundWord = False
   
   iter = tree.getIterator()
   node = iter.next()
   
   while node != "": 
      
      word = node.getWord()
      pos = node.getPOS()
      lemma = node.getAttribute(parsetrees.ParseTreeNode.keyLemma)
      wordPolarity = 0
      
      # 1. Check if this is a sentiment word
      if sentimentwords.isProperSentimentWord(word, pos, lemma, dictionaryPositive):
         wordPolarity = 1
         foundWord = True
      elif sentimentwords.isProperSentimentWord(word, pos, lemma, dictionaryNegative):
         wordPolarity = -1
         foundWord = True
      
      if wordPolarity != 0:         
         
         # Get gold label
         goldLabel = goldLabelProvider.getNextGoldLabel(word, sentence)
      
         # treat no gold label as 'ERROR'
         if goldLabel == None:
            goldLabel = "ERROR"
         
         # 2. Classify word 
         # If I don't analyze subjectivity, I assume all words are subjective
         # If I don't analyze consistency, I assume all words are consistent
         isSubjective = True
         assignedLabel = utils.wordLabelConsistent
         
         # 2a) Subjectivity (subjective / nonsubjective )
         if settings.analyseSubjectivity:
            isSubjective = subjectivityClassifier.wordIsSubjective(node, tree)
            if isSubjective:
               assignedLabel = utils.wordLabelSentiment
            else:
               assignedLabel = utils.wordLabelNoSent

            assignedLabelSubj = wordLabelTableSubjectivity.getLabelMapping(assignedLabel)
            goldLabelSubj = wordLabelTableSubjectivity.getLabelMapping(goldLabel)
            wordLabelTableSubjectivity.addToTable(assignedLabelSubj, goldLabelSubj)
         
         # 2b) Consistency (consistent / inconsistent)
         if isSubjective and settings.analyseConsistency:
            classificationResult = inconsistencyClassifier.getClassification(tree, node)
            if classificationResult == -200:  # Hack: Error code
               assignedLabel = "ERROR"
            else:
               
               # Classify
               if classificationResult > 0:
                  assignedLabel = utils.wordLabelInconsistent
               else:               
                  assignedLabel = utils.wordLabelConsistent
                  
               # Add to table
               assignedLabelCons = wordLabelTableConsistency.getLabelMapping(assignedLabel)
               goldLabelCons = wordLabelTableConsistency.getLabelMapping(goldLabel)
               wordLabelTableConsistency.addToTable(assignedLabelCons, goldLabelCons)
               
               # Do significance output on word level
               if doPrintout:
                  #  sentenceStr = ""
                  #  for s in sentence:
                     #  sentenceStr += " " + s
                  #  sentenceStr = sentenceStr.strip()
                  outFileWords.write(word + "\t" + convertToNumberWordStr(goldLabelCons) + "\t" + convertToNumberWordStr(assignedLabelCons) + "\t" + str(classificationResult) + "\n")
            
               # 3. Add to positivity score on sentence level
               # reversedScore is > 0 if the word is reversed
               # <0 if the word is not reversed
               if wordPolarity == 1: # positive
                  positivityScore = positivityScore - classificationResult
               else: # negative
                  positivityScore = positivityScore + classificationResult
   
         # Debug
         numberIstances += 1
         if debug: print str(numberIstances) + ". word " + word + " => " + str(assignedLabel) + " [" + str(goldLabel) + "]" # TEST !!!
   
         # Collect distributions [DEBUG]
         a = labelDistributionGold.get("WORD_" + goldLabel)
         labelDistributionGold["WORD_" + goldLabel] = (a+1) if a != None else 1
         a = labelDistributionSystem.get("WORD_" + assignedLabel)
         labelDistributionSystem["WORD_" + assignedLabel] = (a+1) if a != None else 1


      # Next node
      node = iter.next()


   # TODO
   # sentence classification
   if foundWord:
      
      numberPolarSentences += 1
      
      if positivityScore >= 0:
         assignedSentenceLabel = utils.sentenceLabelPositive
      else:
         assignedSentenceLabel = utils.sentenceLabelNegative
         
      assignedLabelSentence = sentenceLabelTable.getLabelMapping(assignedSentenceLabel)
         
      # Compare to Hiwi annotation
      #  goldLabelSentence = sentenceLabelTable.getLabelMapping(goldLabelProvider.getCurrentSentenceLabel())
      
      # Compare to extracted sentence level
      if sentenceLabel == "1":
         goldLabelSentence = utils.sentenceLabelPositive
      else:
         goldLabelSentence = utils.sentenceLabelNegative
      
      # Collect distributions [DEBUG]
      a = labelDistributionGold.get("SENTENCE_" + goldLabelSentence)
      labelDistributionGold["SENTENCE_" + goldLabelSentence] = (a+1) if a != None else 1
      a = labelDistributionSystem.get("SENTENCE_" + assignedSentenceLabel)
      labelDistributionSystem["SENTENCE_" + assignedSentenceLabel] = (a+1) if a != None else 1
      
      sentenceLabelTable.addToTable(assignedLabelSentence, goldLabelSentence)
      if debug: print "Sentence score: " + str(positivityScore)  + " => " + str(assignedSentenceLabel) + " [" + str(goldLabelSentence) + "]" # TEST !!!
      
      # Do significance output on sentence level
      if doPrintout:
         sentenceStr = ""
         for s in sentence:
            sentenceStr += " " + s
         sentenceStr = sentenceStr.strip()
         outFileSentences.write(sentenceStr + "\t" + convertToNumberStr(goldLabelSentence) + "\t" + convertToNumberStr(assignedLabelSentence) + "\t" + str(positivityScore) + "\n")



   #  if numberSentences >= 2000 : # TEST !!!
      #  break # TEST !!!
      
   #  if  goldLabelProvider.endOfCorpusReached: # TEST !!!
      #  break # TEST !!!


# print evalation metrics and statistics
print "... " + str(numberSentences) + " sentences, "  + str(numberPolarSentences) + " sentences with sentword, " + str(numberIstances) + " sentiment words."
print "label distribution gold:"
print labelDistributionGold
print "label distribution system:"
print labelDistributionSystem
linelabel = settings.dictionaryType  + " " + settings.corpusType + " " + inconsistencyClassifier.getName() + " " + str(settings.windowsize) + " " + settings.getFilterString()

print "\n===== wordLabelTableSubjectivity ====="
errors = wordLabelTableSubjectivity.getNumberOfErrors()
total = wordLabelTableSubjectivity.getNumberOfEntries()
if errors < (numberIstances/2) and total != 0 :
   wordLabelTableSubjectivity.printStatistics(linelabel)
else:
   print "Got %d entries and %d errors" % (total, errors)
   
print "\n===== wordLabelTableConsistency ====="
errors = wordLabelTableConsistency.getNumberOfErrors()
total = wordLabelTableConsistency.getNumberOfEntries()
if errors < (numberIstances/2) and total != 0 :
   wordLabelTableConsistency.printStatistics(linelabel)
else:
   print "Got %d entries and %d errors" % (total, errors)
   
print "\n===== sentenceLabelTable ====="
sentenceLabelTable.printStatistics(linelabel)



# Cleanup
parseReader.cleanup()
outFileSentences.close()
outFileWords.close()
