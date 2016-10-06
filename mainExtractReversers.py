#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 10.10.11

"""
MAIN for reverser extraction
"""

import settingsextraction as settings
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
import sentimentwords
import representationFactory

sys.path.append("reverserextraction")
import reverserextraction
import scoringFactory
import evaluationReverserDirect

sys.path.append("subjectivity")
import subjectivityClassification

from operator import itemgetter
import itertools


debug = False
#  debug = True


# ---- SETTINGS ---

sys.argv.pop(0) # remove first
while len(sys.argv) >= 1:
   value = ""
   name = sys.argv.pop(0)
   if name in settings.allOptionsBinary and len(sys.argv) >= 1:
      value = sys.argv.pop(0)
   settings.setOption(name,value)

#  print settings.getFilterString()

# ---- INITIALIZATION ---


# Initialize parser for data corpus
parseReader = parseReaderBohnet.ParseReaderBohnet()
parseReader.setInputFile(settings.sentencesParsedFile)
print "+ Data from file " + settings.sentencesParsedFile



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


# Initialize Reverser Extractor
re = reverserextraction.ReverserExtracter()
re.setVerboseMode(False)
print "+ Create reverser extractor:"
representationPRCs = representationFactory.createPRCRepresentation(settings.representationPRCs)
print "Representation is " + str(settings.representationPRCs)
contextFinder = contextFinderTrees.TreeContextFinder()
contextFinder.setWindowsize(settings.windowsize)
contextFinder.setRepresentation(representationPRCs)
print "Context finder is " + contextFinder.__class__.__name__ + " with window size " + str(settings.windowsize)
re.setContextFinder(contextFinder)
print "Candidate cleanup is " + str(settings.candidateCleanup)


# Scoring
reScorer = scoringFactory.createScorer(settings.scorer, settings.scoringThreshold, settings.scoringN)
compareWithNonreversed = reScorer.isComparisonScorer()
print "+ Scorer is " + reScorer.__class__.__name__ + ", threshold " + str(settings.scoringThreshold) + ", N=" + str(settings.scoringN) + " ."
if compareWithNonreversed:
   comparisonExtracter = reverserextraction.ReverserExtracter()
   comparisonExtracter.setVerboseMode(False)
   comparisonExtracter.setContextFinder(contextFinder)
   #  print "Do compare with nonreversed."




# ---- PROCESSING ---
print "===== Extract reversers ====="


numberSentences = 0
numberAvailableSentences = 0
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
   #  if sentencePolarity == utils.negativeLabel: # TEST !!!
   #  if sentencePolarity == utils.positiveLabel: # TEST !!!
      #  continue # TEST !!!

   iter = tree.getIterator()
   node = iter.next()
   foundSentimentWord = False
   
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
      foundSentimentWord = True
      
      # Debug
      if debug: print str(numberIstances) + ". word " + word + " (" + wordPolarity + ")" + " => reversed: " + str(sentencePolarity != wordPolarity) # TEST !!!
      
      # Extract the reversed / nonreversed words
      if sentencePolarity == wordPolarity: 
         # Extract as nonreversed example
         wordsNonreversed += 1
         #  if debug: print word +"-> is nonreversed" # TEST !!!
         if compareWithNonreversed:
            # Extract candidates from context for comparison
            candidateString = comparisonExtracter.extractCandidates(node, tree)
            if debug: print candidateString
         
      else:
         # Extract as reversed example
         wordsReversed += 1
         #  if debug: print word +"-> is reversed" # TEST !!!
         candidateString = re.extractCandidates(node, tree)
         if debug: print candidateString


      
      # Next node
      node = iter.next()


   #  if numberSentences >= 2000: # TEST !!!
      #  break # TEST !!!

   if foundSentimentWord:
      numberAvailableSentences += 1


# 3. Delete unwanted candidates
if settings.candidateCleanup:
   re.cleanupCandidateSet()
   print "... cleaned up candidate set."



# 4. Score extracted reversers

reScorer.setNumberRevExamples(wordsReversed)
reScorer.setNumberNonrevExamples(wordsNonreversed)

if compareWithNonreversed:
   scorerNonreversed = scoringFactory.createScorer("RawFrequency", 0, 0)
   resultingNonreversers = scorerNonreversed.scoreCandidates(comparisonExtracter.getCandidates(), settings.reFilenamePrefix + "_nr", False)
   reScorer.setComparisonSet(resultingNonreversers)
   print "... scored comparison candidates (output written to " + settings.reFilenamePrefix + "_nr" + ")."

resultingReversers = reScorer.scoreCandidates(re.getCandidates(), settings.reFilenamePrefix + "_r", debug)
print "... scored candidates (output written to " + settings.reFilenamePrefix + "_r" + ")."

# Debug
print "Extracted Reversers:"
for pair in reversed(sorted(resultingReversers.items(), key=itemgetter(1))):
   #  print pair[0] + " " + str(pair[1])
   print pair[0] + " " + ("%.2f" % round(pair[1],2))


# TODO Iterative processing


# LaTeX
latexString = settings.dictionaryType
tikzString = ""
latexString += " & " + settings.representationPRCs
latexString += " & " + settings.scorer
latexString += " & " + str(settings.windowsize)
latexString += " & " + settings.getFilterString()

# 5. Evaluate extracted reversers
directEvalScores = []
goldFile = settings.goldReversersFiles.get(settings.representationPRCs)
if goldFile != None:
   isLast = False
   for t in settings.evaluationThresholds:
      if debug: print "... evaluate reversers against " + goldFile + " at t=" + str(t)
      evaluationReverserDirect.reverserThreshold = t
      if t == settings.evaluationThresholds[-1]:
         isLast = True
         print "--- check ---"
      correct, incorrect, nolabel = evaluationReverserDirect.evaluate (settings.reFilenamePrefix + "_r", goldFile, debug or isLast)
      directEvalScores.append((correct, incorrect, nolabel, t))
      precision = float(correct)/float(t)
      if t in settings.evaluationThresholdsShort:
         latexString +=  " & " + "%.2f " % (round(precision,2))
         tikzString += "(%d, %.2f) " % (t, round(precision,2))
      if isLast:
         latexString += " & " +  str(correct)
         latexString += " & " +  str(nolabel)
         print "!!Result & %.2f " % (round(precision,2))

   print "... evaluate reversers against " + goldFile
   print "Scores (correct, incorrect, nolabel, threshold)"
   print directEvalScores


# Some statistics
print "... processed " + str(numberSentences) + " sentences, "  + str(numberAvailableSentences) + " contained sentiment words, " + str(numberIstances) + " sentiment words found."
print "... " + str(wordsNonreversed) + " words in them are not reversed ( = " + str(float(wordsNonreversed)/float(numberIstances)) + ")."
print "... " + str(wordsReversed) + " words in them are reversed ( = " + str(float(wordsReversed)/float(numberIstances)) + ")."

print "==eval=="
print "% " + str(directEvalScores)
print latexString + " \\\\ \n"



print "==tikz=="
print "\\addplot plot coordinates {" + tikzString + "};"
print "\\addlegendentry{%s %s %s %s %s}" % (settings.dictionaryType, settings.representationPRCs, settings.scorer, settings.windowsize, settings.getFilterString())


# Clean up
parseReader.cleanup()

