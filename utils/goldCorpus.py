#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 6.9.12

"""
Get word labels from gold annotated corpus.
"""

import parsetrees
import parseutils


class Token:
   
   string = ""
   label = ""
   
   
   def __init__ (self, string):
      #  print "adding token " + string
      self.string = string
   
   def addLabel (self,label):
      #  print "adding label " + label
      self.label = label
   
   def hasLabel (self):
      if self.label == "":
         return False
      else:
         return True

   def getString(self):
      return self.string
      
   def getLabel(self):
      return self.label
      
   def __str__(self):
      #  print "---" + self.string +  "---" 
      #  print "---" + self.label +  "---" 
      if self.hasLabel():
         return self.string +" [" + str(self.label) + "]"
      else:
         return self.string




class GoldLabelProvider:
   
   
   endOfCorpusReached = False
   
   
   def __init__(self, labeledFileName):
      
      self.labeledFile = open(labeledFileName, "r")
      self.labelQueue = []
      self.currentSentence = []
      self.currentSentenceLabel = ""
      
      
   def getCurrentSentenceLabel(self):
      return self.currentSentenceLabel

   
   def getNextGoldLabel(self, currenttoken, currentsentence):
      """
      Return None if no more label.
      Token should be just the string, sentence a list of strings.
      """
      # if necessary read next sentence
      if self.labelQueue == []:
         line = self.labeledFile.readline().strip()
         if line != "":
            parts = line.split("\t") # cut off label
            self.currentSentenceLabel = parts[0].strip()
            self.readSentence(parts[1].strip())
         else:
            print "ERROR, no more sentences!!"
            self.endOfCorpusReached = True
            return None
         
         sent = []
         for token in self.currentSentence:
            sent.append(token.getString())
         #  print "  / " + str(sent) # TEST !!!
      
      # Get first labeled token in line
      mytoken = self.labelQueue.pop(0)
      #  print "My token is: " + str(mytoken) # TEST !!!
      
      # perform sanity check if what we got corresponds
      # to what we should have got
      if self.checkSanity(mytoken, self.currentSentence, currenttoken, currentsentence):
         return mytoken.getLabel()
      else:
         print "ERROR, sanity check failed!!"
         return None
   
   
   
   def readSentence(self, currentline):
      
      self.labelQueue = []
      self.currentSentence = []
      
      #  print "current line " + currentline
      
      while currentline != "":
         
         #  print "current line " + currentline
         
         foundSpace = currentline.find(" ")
         foundSW = currentline.find("<sentimentWord")
         
         if foundSW < foundSpace and foundSW >= 0:
            
            first = currentline.find(">__")
            last = currentline.find("__</sentimentWord>")
            #  print "first " + str(first)
            #  print "last " + str(last)
            current = currentline[first+3:last]
            #  print currentline[last:]
            goon = currentline[last:].find(">") + last + 1
            #  print "goon " + str(goon)
            labelstart = currentline.find("label=")
            label = currentline[labelstart+7:first-1]
            #  print "Token: " + current
            newtoken = Token(current)
            newtoken.addLabel(label)
            self.currentSentence.append(newtoken)
            self.labelQueue.append(newtoken)
            #  print "LABEL QUEUE:"
            #  for label in self.labelQueue:
               #  print label
               
            currentline = currentline[goon:].strip()
            
         elif foundSpace >= 0:
            current = currentline[0:foundSpace]
            currentline = currentline[foundSpace+1:]
            #  print currentline
            #  print "Token: " + current
            self.currentSentence.append(Token(current))
         
         else: # end of line and no space at the end
            current = currentline[0:]
            #  print "Token: " + current
            self.currentSentence.append(Token(current))
            currentline = ""
         
      #  print "Final: " + line
      
      #  print "RESULT:"
      #  for token in tokenlist:
         #  print token.getString()
         #  print token
      
      
      
      

   def checkSanity (self, token1, tokenlist1, string2,  stringlist2):
      """
      token1 / tokenlist1 is what we found by searching the next label.
      This is a Token() and list of Token() as defined above.
      string2 / stringlist2 is what we are supposed to find,
      this is just a string of the token (exact word form, not lemma!) and the 
      sentence as list of strings.
      Check sanity as in:
         - both tokens are the same
         - both sentences have same length
         - all tokens are the same in both sentences
      """
      
      length = len(tokenlist1)
      if len(stringlist2) != length:
         print "SENTENCE ERROR: different lengths!!"
         sent = []
         for token in tokenlist1:
            sent.append(token.getString())
         print "S: Len " + str(len(stringlist2)) + " " + str(stringlist2)
         print "F: Len " + str(length) + " " + str(sent)
         return False

      for i in range(0,length):
         if tokenlist1[i].getString() != stringlist2[i]:
            print "SENTENCE ERROR: " + tokenlist1[i].getString() +  " vs. " + stringlist2[i]
            return False
      
      if token1.getString() != string2:
         print "TOKEN ERROR: tokens do not match: " + token1.getString() + " vs. " + string2
         return False
      
      return True
      
      
      
      
   def cleanup(self):
      """ 
      Cleanup - close input file.
      """
      self.labeledFile.close()