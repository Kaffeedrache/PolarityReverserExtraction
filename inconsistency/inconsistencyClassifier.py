#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 21.9.12



import reverserFinder
import reverserFinderWordLevel


class InconsistencyClassifier():

   labelClassConsistent = -1
   labelClassInconsistent = 1
   classifierName = ""

   def getName(self):
      """
      Get name of classifier.
      """
      if self.classifierName == "":
         return self.__class__.__name__
      else:
         return self.classifierName
      
   def setName(self, classifierName):
      """
      Get name of classifier.
      """
      self.classifierName = classifierName 

   def getClassification(self, tree, sentimentWord):
      """
      Return classification confidence.
      > 0 reversed
      <= 0 nonreversed
      """
      raise NotImplementedError('Method must be implemented in subclass')




# === Standard majority voting (no inconsistency assessment) ===


class InconsistencyClassifierDummy (InconsistencyClassifier):
   """
   Classify all words as consistent/nonreversed.
   """
   
   def getName(self):
      return "Dummy classifier (all consistent)"

   def getClassification(self, tree, sentimentWord):
      """
      Always return -1 (nonreversed)
      """
      return self.labelClassConsistent # -1 = sure non-reversed



# === Negation voting (binary decision) ===



class NegationVotingClassifierAbstract (InconsistencyClassifier):
   """
   Classify word as reversed or nonreversed based on the number
   of reversers found in the vicinity.
   Subclasses specify "vicinity" by setting self.reverserFinder.
   Reversers are saved in a static dictionary.
   """
   
   """ Responsible for searching neighborhood for negation cues. """
   reverserFinder = None


   def makeReverserDictionary(self, reverserFile, cutoffThreshold):
      """
      Create static dictionary of negation cues.
      """
      self.reverserFinder.makeReverserDictionary(reverserFile, cutoffThreshold)


   def getClassification(self, tree, sentimentWord):
      """
      Classify word as reversed if odd number of negation cues found.
      """
      numberOfReversers = self.reverserFinder.findReversers(sentimentWord, tree)
      #  if numberOfReversers > 1:
         #  print "Got " + str(numberOfReversers) + " reversers!"
      if numberOfReversers % 2 == 1:
         return self.labelClassInconsistent # Reversed
      else:
         return self.labelClassConsistent # Nonreversed



class NegationVotingClassifierTrees (NegationVotingClassifierAbstract):
   """
   Vicinity = syntactic context.
   """

   def __init__ (self,contextFinder):
      self.reverserFinder = reverserFinder.ReverserFinder()
      self.reverserFinder.setReverserExtractor(contextFinder)

   def setReverserExtracter(self, reverserType):
      self.reverserFinder.setReverserExtracter(reverserType)
      


class NegationVotingClassifierWords (NegationVotingClassifierAbstract):
   """
   Vicinity = preceding/following words.
   """

   def __init__ (self,windowsize):
      self.reverserFinder = reverserFinderWordLevel.ReverserFinderWordLevel(windowsize)
      # Alternative: look only left of word
      #  self.reverserFinder = reverserFinderWordLevel.ReverserFinderWordLevelOnlyLeft()


# === Weighted consistency voting ===



class InconsistencyClassifierLookup(InconsistencyClassifier):
   """
   Read in a Stanford classifier file
   """   
   
   exampleDict = {}
   
   def __init__ (self, classifierFile, classifierID = ""):
      """
      """
      mydictionary = {}
      inputFile = open(classifierFile)
      i = 1
      for line in inputFile:
         line = line.strip()
         parts = line.split("\t")
         features = parts[0].strip()
         pair = mydictionary.get(features) 
         if pair != None: # TEST !!!
            if pair[0] != parts[2] or pair[1][0:4] != parts[3][0:4]: # TEST !!!
               print "have already in dict: " + features + str(mydictionary.get(features)) # TEST !!!
               print "adding now: " + parts[2] + " " + parts[3] # TEST !!!
         mydictionary[features] = (parts[2], parts[3])
         #  print "--" + features + "--" # TEST !!!
         #  print mydictionary.get(features) # TEST !!!
      self.exampleDict = mydictionary
      
      self.classifierID = classifierID


   def setFeatureExtractor(self, featureExtractor):
      self.extractor = featureExtractor


   def getClassification(self, tree, sentimentWord):
      """
      -1 : nonreversed
      1  : reversed
      """
      
      features = self.extractor.extractFeatures(sentimentWord, tree, "1")
      sentence = ""
      for i in features:
         sentence = sentence + " " + i
      sentence = sentence.strip()
      #  print sentimentWord.getWord() + " / " + sentence # TEST !!!
      
      classification  = self.exampleDict.get(sentence)
      #  print classification
      
      if classification != None:
         label = int(classification[0]) 
         # now labels are  (like Ikeda et al.)
         # -1 = nonreversed
         # 1 = reversed
         probability = float(classification[1])
         #  print "Have " + str(label) + " " + str(probability)
         #  print probability * label
         #  if label == -1: # TEST !!!
            #  print sentimentWord.getWord() + " -> nonreversed" # TEST !!!
         #  else: # TEST !!!
            #  print sentimentWord.getWord() + " -> reversed" # TEST !!!
         return probability * label 
      else:
         print "Look up: " + sentimentWord.getWord() + " / " + sentence
         print "ERROR ! DID NOT FIND FEATURE VECTOR!!!"
         return -200 # Error code
