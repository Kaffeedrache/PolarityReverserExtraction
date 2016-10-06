#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 17.10.11

"""

"""

import parsetrees

sentimentMark = "Sent"

class ParseReaderBohnet:
   
   
   fileOpen = False
   sentimentMark = "Sent"
   
   
   # --- Getter/setter ---
      
      
   def setInputFile(self, inputFile):
      """ 
      Sets the output file.
      Expects a location.
      """
      self.inputFile = inputFile

   
   # --- Open/close files ---
   
   
   def cleanup(self):
      """ 
      Cleanup - close input file.
      """
      self.inputFileHandle.close()
      self.fileOpen = False
   
   
   def openFile(self):
      """ 
      Open input file.
      """
      if not self.fileOpen:
         self.inputFileHandle = open(self.inputFile)
         self.fileOpen = True
         #  print "file " + self.inputFile + " is now open" # TEST !!!
   
   
   
   # --- Reading parses ---
      
   def readSentence(self):
      """ 
      Reads a parse from the input file 
      and returns the sentence (list of words).
      @deprecated
      """
      self.openFile()
      
      line = "asdf"
      sentence = []
      while line != "":
         line = self.inputFileHandle.readline()
         line = line.strip()
         #  print "Line read: " + line # TEST !!!
         if line == "":
            break
         # Split line in parts, format is
         # ID word lemma ? ? POS ? ? ID_of_root ? relation ? ? sentimentmark
         parts = line.split("\t")
         #  print parts[0] + "---" + parts[1]
         word = parts[1]
         sentence.append(word)
         #  print "Sentence: " + str(sentence)
      
      return sentence
      
      
   def readParse(self):
      """ 
      Reads a parse from the input file.
      """
      self.openFile()
      
      line = "asdf"
      tree = parsetrees.ParseTree()
      tree.createTree()
      while line != "":
         line = self.inputFileHandle.readline()
         line = line.strip()
         #  print "Line read: " + line # TEST !!!
         if line == "":
            break
         # Split line in parts, format is
         # ID word lemma ? ? POS ? ? ID_of_root ? relation ? ? sentimentmark
         parts = line.split("\t")
         #  try:
         # TODO make here less error prone! check for length before access
            #  print parts[0] + "---" + parts[1] + "---" + parts[8] + "---" + parts[5]
         mark = False
         if parts[len(parts)-1] == self.sentimentMark:
            mark = True
         tree.addNode(int(parts[0]), int(parts[8]), {parsetrees.ParseTreeNode.keyWord: parts[1], parsetrees.ParseTreeNode.keyPos: parts[5], parsetrees.ParseTreeNode.keyLemma: parts[2], parsetrees.ParseTreeNode.keyRelation: parts[10], parsetrees.ParseTreeNode.keySentiment : mark})
         #  except IndexError:
            #  print "--- ERROR ----"
            #  print parts
            #  print len(parts)
         #  print "Tree: "
         #  tree.printTree()

      return tree
      

   def identifySentimentWord(self, sentence):
      """ 
      Identify word in uppercase in list.
      Returns -1 if none is found.
      """
      for s in range(len(sentence)):
         if sentence[s].isupper():
            return s
      
      return -1
      
      
   def identifySentimentWordInParse(self, parse):
      """ 
      Identify word in uppercase in parse.
      Returns -1 if none is found.
      """
      return parse.findSentimentWord()