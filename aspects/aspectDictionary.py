#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 20.1.12


"""

"""


# parsing things
import sys
sys.path.append("../Utils") 
import parseReaderBohnet
import parseutils

from operator import itemgetter


class AspectDictionary:


   # Bigram patterns for extracted aspect
   bigramPOS = [
         #  (parseutils.posAdj, parseutils.posNoun), 
         (parseutils.posNoun, parseutils.posNoun), 
         #  (parseutils.posVerb, parseutils.posNoun)
         ]
   # Trigram patterns,
   # extracted aspects must conform to trigram
   # pattern, but only last two tokens are extracted
   # as a bigram
   trigramPOS = [
         (parseutils.posCard, parseutils.posAdj, parseutils.posNoun),
         (parseutils.posAdj, parseutils.posAdj, parseutils.posNoun),
         (parseutils.posPrep, parseutils.posAdj, parseutils.posNoun),
         ]



   threshold = 70


   def __init__(self):
      """
      Initialize aspects set.
      """
      self.aspectSet = {}
      
      
   def cleanup(self):
      """
      Delete aspects set, cleanup parse reader.
      """
      self.candidates = {}
      self.parseReader.cleanup()
   
   
   def setParseReader(self, parseReader, inputFile):
      """ 
      Sets a parse reader.
      """
      self.parseReader = parseReader
      self.parseReader.setInputFile(inputFile)


   def setThreshold(self, newThreshold):
      """ 
      Sets the threshold for considering to score a candidate.
      threshold=0 means no threshold.
      """
      #  print "Aspect threshold: " + str(newThreshold)
      self.threshold = newThreshold
      

   def addBigram (self, node1, node2):
      """
      Insert a bigram to self.aspectSet or increase count of seen bigram.
      Checks if the bigram is in the list of POS-patterns to extract
      and normalizes bigrams to lowercase and lemma.
      """
   
      #  print node1.getWord() + " - " + node2.getWord()
      
      # Check if POS pattern matches
      pos1 = node1.getPOS()
      pos2 = node2.getPOS()
      isGood = False
      for bigramPOSlist in self.bigramPOS:
         if parseutils.isOfGeneralPOS(pos1,bigramPOSlist[0]):
            if parseutils.isOfGeneralPOS(pos2,bigramPOSlist[1]):
               isGood = True
      
      # Not in list of patterns
      if not isGood:
         return

      # Insert bigram
      # Normalize to lowercase and lemma
      #  candidate = node1.getWord().lower() + " " + node2.getWord().lower()
      candidate = node1.getLemma().lower() + " " + node2.getLemma().lower()
      
      # Ignore the empty string as a candidate
      if candidate == "":
         return
      
      # Count occurrences
      occurrences = self.aspectSet.get(candidate)
      if occurrences != None: 
         #  word in candidates -> add 1 to count
         self.aspectSet[candidate] = occurrences + 1
      else: # not in candidates -> set 1
         self.aspectSet[candidate] = 1




   def addTrigram (self, node1, node2, node3):
      """
      Insert a bigram to self.aspectSet or increase count of seen bigram.
      Checks if the bigram is in the list of trigram POS-patterns to extract
      and normalizes bigrams to lowercase and lemma.
      The first word of the trigram pattern is discarded for insertion,
      but must be matched.
      """
   
      #  print node1.getWord() + " - " + node2.getWord()
      
      # Check if POS pattern matches
      pos1 = node1.getPOS()
      pos2 = node2.getPOS()
      pos3 = node3.getPOS()
      isGood = False
      for trigramPOSlist in self.trigramPOS:
         if parseutils.isOfGeneralPOS(pos1,trigramPOSlist[0]):
            if parseutils.isOfGeneralPOS(pos2,trigramPOSlist[1]):
               if parseutils.isOfGeneralPOS(pos3,trigramPOSlist[2]):
                  isGood = True
      
      # Not in list of patterns
      if not isGood:
         return

      # Insert trigram
      # Normalize to lowercase and lemma
      #  candidate = node1.getWord().lower() + " " + node2.getWord().lower()
      #  candidate = node1.getLemma().lower() + node1.getPOS() + " " + node2.getLemma().lower() + " " + node3.getLemma().lower()
      candidate = node2.getLemma().lower() + " " + node3.getLemma().lower()
      
      # Ignore the empty string as a candidate
      if candidate == "":
         return
      
      # Count occurrences
      occurrences = self.aspectSet.get(candidate)
      if occurrences != None: 
         #  word in candidates -> add 1 to count
         self.aspectSet[candidate] = occurrences + 1
      else: # not in candidates -> set 1
         self.aspectSet[candidate] = 1
        


   def findAspects (self, parsedCorpusFilenames):
      """ 
      Find bigrams that occur often in review text and
      extracts them as aspects.
      Works on parsed files.
      """
      self.aspectSet = {}
      sentenceNo = 0
      
      for filename in parsedCorpusFilenames:
         inputFile = open(filename)
      
         weWant = True
         
         while weWant:
            
            # Read sentence
            tree = self.parseReader.readParse()         
            #  print tree.getWholeSentence() # TEST !!!
            
            # Catch end of file
            if tree.isEmpty(): 
               break
            
            sentenceNo += 1
            
            #  words = tree.getWholeSentence() # TEST !!!
            
            # Iterate through tree
            treeIterator = tree.getIterator()
            
            # Count all bigrams
            previousNode = ""
            prepreviousNode = ""
            currentNode = treeIterator.next()
            while currentNode != "":
               
               if previousNode != "":
                  self.addBigram(previousNode, currentNode)
                  
               if prepreviousNode != "":
                  self.addTrigram(prepreviousNode, previousNode, currentNode)
               
               prepreviousNode = previousNode
               previousNode = currentNode
               currentNode = treeIterator.next() 
            
            #  for i in range(1,len(words)-1):
               #  addBigram(words[i-1], word[i])
         
      #  for a in self.aspectSet:
         #  print a + " -> " + str(self.aspectSet.get(a))
      
      itemno = 1
      returnAspectSet = {}
      for i in reversed(sorted(self.aspectSet.items(), key=itemgetter(1))):
         #  print i # TEST !!!
         returnAspectSet[i[0]] = i[1]
         itemno += 1
         if itemno > self.threshold:
            break
      
      print len(self.aspectSet) # TEST !!!
      #  print sentenceNo # TEST !!!
      
      
      return returnAspectSet


   def saveAspectDictionary (self, aspectSet, aspectSetFilename):
      """
      Write extracted aspect set to file.
      """
      outputFile = open(aspectSetFilename, "w")
      itemno = 1
      for i in reversed(sorted(self.aspectSet.items(), key=itemgetter(1))):
         outputFile.write(i[0] + "\t" + str(i[1]) + "\n")
         itemno += 1
         if itemno > self.threshold: # write only number threshold
            break
         


   def loadAspectDictionary (self, aspectSetFilename):
      """
      Load aspects from file.
      Note: we load #self.threshold aspects, no matter how many are 
      in the file.
      """
      aspectSet = {}
      itemno = 1
      for line in open(aspectSetFilename):
         parts = line.split("\t")
         if len(parts)>1:
            key = parts[0].strip()
            value = int(parts[1].strip())
            aspectSet[key] = value
            itemno += 1
            if itemno > self.threshold: # assume sorted!!
               break
      if itemno < self.threshold:
         print "I wanted to load " + str(self.threshold) + " aspects, but there were only " + str(itemno-1) + " in the file!"
      return aspectSet
      

# -- MAIN --


#  corpusFolder = "../../Data/parsedCorpora/"
#  parsedFilename = corpusFolder +"camerasCellphonesProsCons_Parsed.txt" # pros/cons cellphones and cameras

#  parseReader = parseReaderBohnet.ParseReaderBohnet()
#  aspectFinder = AspectDictionary()
#  aspectFinder.setParseReader(parseReader, parsedFilename)

#  aspects = aspectFinder.findAspects ([parsedFilename])

#  for aspect in reversed(sorted(aspects.items(), key=itemgetter(1))):
   #  print aspect