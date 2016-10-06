#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 11.6.12

"""

"""



class FeatureExtractor ():
   """ 
   Extract features from a training example.
   """

   separator = " "

   # --- Open/close files ---
   
   fileOpen = False
   doWriteToFile = False

   def getName(self):
      return self.__class__.__name__ 

   def setWriteToFile(self, doWriteToFile):
      self.doWriteToFile = doWriteToFile

   def setOutputFile(self, outputFile):
      self.outputFile = outputFile
      self.fileOpen = False


   def openFile(self):
      """ 
      Open input file.
      """
      if not self.fileOpen:
         self.outputFileHandle = open(self.outputFile, "w")
         self.fileOpen = True
         #  print "file " + self.outputFile + " is now open" # TEST !!!


   def writeToFile(self, label, featurevector):
      #  print "Write " + label + " / " + str(featurevector) + "[" + self.__class__.__name__ + "]" # TEST !!!
      
      self.openFile()
      
      string = ""
      
      if label != "":
         string = label + "\t"
         
      for feature in featurevector:
         string += feature
         string += self.separator

      self.outputFileHandle.write(string.strip() + "\n")
      self.outputFileHandle.flush()

   
   def cleanup(self):
      """ 
      Cleanup - close output file.
      For sentence-based extraction, extract last sentence
      (one last call to self.extractFeatures(None, None, None))
      """
      
      # let last sentence be extracted
      if self.sentenceAtATime:
         self.extractFeatures(None, None, None)
         
      # Close output file
      try:
         self.outputFileHandle.close()
      except AttributeError:
         # ignore
         pass
      self.fileOpen = False



   # --- Extract features ---

   
   def doExtraction(self, node, tree, label):
      """
      @return list of features
      """
      raise NotImplementedError('Method must be implemented in subclass')
      return []
      
   
   def extractFeatures(self, node, tree, label):
      """
      Label can be utils.labelReversed or utils.labelNoneversed
      Extract k words from left and right context.
      Feature vector:
         0 sentiment word
         1..3 k words left context
         4..6 k words right context
      @return list of features
      Set if write to file with setWriteToFile
      """
      candidates = self.doExtraction(node, tree, label)
      
      #  print "---" # TEST !!!
      #  print tree.getWholeSentence() # TEST !!!
      #  if tree.findLabel() == utils.positiveLabel: # TEST !!!
         #  print "POS" # TEST !!!
      #  else: # TEST !!!
         #  print "NEG" # TEST !!!
      #  print sentWord.getWord() # TEST !!!
      #  if label == utils.labelReversed: # TEST !!!
         #  print "REVERSED" # TEST !!!
      #  else: # TEST !!!
         #  print "NONREVERSED" # TEST !!!
      #  for c in allcandidates: # TEST !!!
         #  print str(c) # TEST !!!
      
      if self.doWriteToFile:
         self.writeToFile(label, candidates)
         
      return candidates


class FeatureExtractorSentenceWise (FeatureExtractor):
   sentenceAtATime = True
   
   

class FeatureExtractorWordWise (FeatureExtractor):
   sentenceAtATime = False
   