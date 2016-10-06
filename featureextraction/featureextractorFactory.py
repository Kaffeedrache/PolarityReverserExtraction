#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 14.11.12

"""
"""

import featureextractorIkeda
import featureextractorConstructions
import featureextractorReversingConstructions
import featureextractorLabelingOutput
import featureextractorTreeWriter
import featureextractorPlaintextOutput

import sys
sys.path.append("../base")
import contextFinderTrees


def createFeatureExtractor(name, featuresFilename, contextFinder, reverserFile = "", cutoff = "",):


   # Set feature extractors
   if name == "Ikeda":
      featureExtractor = featureextractorIkeda.FeatureExtractorIkeda()
      featureExtractor.setOutputFile(featuresFilename + "Ikeda" + ".txt")
      print "Feature extractor Ikeda"
      return featureExtractor
      
   if name == "Constructions":
      featureExtractor = featureextractorConstructions.FeatureExtractorConstructions()
      featureExtractor.setReverserExtracter(contextFinder)
      featureExtractor.setOutputFile(featuresFilename + "Constructions"+ ".txt")
      print "Feature extractor Constructions"
      return featureExtractor
   
   print name
   print reverserFile
   if name.startswith("ReversingConstructions"):
      #  id = name.replace("ReversingConstructions","")
      featureExtractor = featureextractorReversingConstructions.FeatureExtractorReversingConstructions()
      featureExtractor.setReverserExtracter(contextFinder)
      featureExtractor.setInputReversersFile(reverserFile, cutoff)
      featureExtractor.setOutputFile(featuresFilename + name + ".txt")
      print "Feature extractor Reversing Constructions ("  + featureExtractor.getName() + ") from file " + reverserFile + ", cutoff=" + str(cutoff)
      return featureExtractor
      
   #  if name == "LabelingOutput":
      #  featureExtractor = featureextractorLabelingOutput.FeatureExtractorLabelingOutput()
      #  featureExtractor.setOutputFile(featuresFilename + "labelingOutput"+ ".txt")
      #  featureExtractor.setPrintLabel(labelingOutputPrintLabel)
      #  return featureExtractor
      
   #  if name == "TreeWriter":
      
      #  parseWriterR = parseWriterBohnet.ParseWriterBohnet()
      #  parseWriterNR = parseWriterBohnet.ParseWriterBohnet()
      #  print "... created parse writers (" + getClassName(parseWriterR) + ")."
      #  featureExtractor = featureextractorTreeWriter.FeatureExtractorTreeWriter()
      #  featureExtractor.setParseWriterReversed(parseWriterR, reversedSentencesFile)
      #  featureExtractor.setParseWriterNonreversed(parseWriterNR, nonreversedSentencesFile)
      #  return featureExtractor

   #  if name == "PlaintextWriter":
      #  featureExtractor = featureextractorPlaintextOutput.FeatureExtractorPlaintextOutput()
      #  featureExtractor.setFileReversed(reversedSentencesPlaintextFile)
      #  featureExtractor.setFileNonReversed(nonreversedSentencesPlaintextFile)
      #  return featureExtractor
      
   print "ERROR!! Cannot create this Feature extractor: " + name