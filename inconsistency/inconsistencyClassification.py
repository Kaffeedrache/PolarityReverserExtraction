#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 11.6.12

"""

"""

import inconsistencyClassifier
import reverserFinder
import reverserFinderWordLevel

import sys
sys.path.append("../base") 
import contextFinderTrees
import representationFactory

sys.path.append("featureextraction") 
import featureextractorIkeda
import featureextractorConstructions
import featureextractorReversingConstructions
import featureextractorLabelingOutput
import featureextractorTreeWriter
import featureextractorPlaintextOutput


classifierTypeNone = "None" # no reverser treatment
classifierTypeML = "Classifier" # classify with ml (lookup)
classifierTypeNegVoting = "NegationVoting" # use negation cues in context



#  representationConstructions = extractioncompletepaths.ReverserExtractionAbstractedCompletePaths()




def getClassifier(classifierType, classifierID, representationPRCs, windowsize, reverserFile = "", cutoffThreshold = "", classificationResultsFile = ""):
   """
   classifierType can be one of None / Classifier / NegationVoting
   classifierID can be arbitrary, influences 
      - reverserFile
      - classificationResultsFile
      - type of features to extract:
         "Ikeda" = featureextractorIkeda.FeatureExtractorIkeda
         "Constructions" = featureextractorConstructions.FeatureExtractorConstructions
         every thing else = featureextractorReversingConstructions.FeatureExtractorReversingConstructions
   
   
   Possible kwargs:
   For negation voting:
   - negationVotingType : Words (check words in sentence with no syntactic processing) /
         Syntax (check words/constructions in syntactic context)
   - cutoffThreshold : how many reversers to read from file to dictionary, 0 means all
   - reverserFile + classifierID : file from where to read reversers
   For classifier:
   - classificationResultsFile + classifierID : file from where to read classification results
   - reverserFile + classifierID : file from where to read reversers (if any)
   - cutoffThreshold : how many reversers to read from file to dictionary, 0 means all
   """

   # Do nothing, consider all words as consistent
   if classifierType == classifierTypeNone:
      print "dummy"
      return inconsistencyClassifier.InconsistencyClassifierDummy()

   # For those that use tree context (i.e., all but Dummy and Ikeda), create a context finder
   if  classifierID != "Ikeda":
      print "+ Create context extractor:"
      myrepresentationPRCs = representationFactory.createPRCRepresentation(representationPRCs)
      print "Representation is " + str(representationPRCs)
      contextFinder = contextFinderTrees.TreeContextFinder()
      contextFinder.setWindowsize(windowsize)
      contextFinder.setRepresentation(myrepresentationPRCs)
      print "Context finder is " + contextFinder.__class__.__name__ + " with window size " + str(windowsize)

   # Classify by looking for negation cues in the vicinity
   if classifierType == classifierTypeNegVoting:
      
      #  cutoffThreshold = kwargs.get('cutoffThreshold')
      #  reverserFile = kwargs.get('reverserFile' + classifierID)
      print "negation voting for : " + str(classifierID) + " " + str(cutoffThreshold) + " reversers from file " +  str(reverserFile)+ " window size " +  str(windowsize) # TEST 
      
      if classifierID == "Ikeda":
         createdClassifier = inconsistencyClassifier.NegationVotingClassifierWords(windowsize)
         createdClassifier.makeReverserDictionary(reverserFile, cutoffThreshold)

      else: # Reversing constructions
         createdClassifier = inconsistencyClassifier.NegationVotingClassifierTrees(contextFinder)
         #  createdClassifier.setReverserExtracter(representationConstructions)
         createdClassifier.makeReverserDictionary(reverserFile, cutoffThreshold)
         
         originalName = createdClassifier.getName() # TEST !!!
         createdClassifier.setName(originalName + "_" + classifierID) # TEST !!!

   
   # Stanford classifier result lookup
   elif classifierType == classifierTypeML:
      
      #  classificationResultsFile = kwargs.get('classificationResultsFile' + classifierID)
      print "lookup classifier for : " + classificationResultsFile # TEST 
      createdClassifier = inconsistencyClassifier.InconsistencyClassifierLookup(classificationResultsFile, classifierID)
         
      # Ikeda / Words
      if classifierID == "Ikeda":
         fe = featureextractorIkeda.FeatureExtractorIkeda()
      # Constructions
      elif classifierID == "Constructions":
         fe = featureextractorConstructions.FeatureExtractorConstructions()
         fe.setReverserExtracter(contextFinder)
      # Reversing constructions
      else:
         fe = featureextractorReversingConstructions.FeatureExtractorReversingConstructions()
         fe.setReverserExtracter(contextFinder)
         #  reverserFile = kwargs.get('reverserFile' + classifierID)
         #  cutoffThreshold = kwargs.get('cutoffThreshold')
         fe.setInputReversersFile(reverserFile, cutoffThreshold)
      
      createdClassifier.setFeatureExtractor(fe)

      originalName = createdClassifier.getName() # TEST !!!
      createdClassifier.setName(originalName + "_" + classifierID) # TEST !!!


   # Unknown arguments
   else:
      print "ERROR, do not recognize reversed words classifier type: classifierType"
      createdClassifier = None


      
   #  print "Consistency Classifier: " + id
   return createdClassifier


   
   

