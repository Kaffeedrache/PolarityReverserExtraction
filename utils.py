#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 19.10.11

"""
Constants.
"""

from datetime import datetime


# Words/POS that should be ignored as possible candidates for reversers.
# "Words" may actually be lemmas.
#  filteredWords = []
filteredWords = [",", ".", "(", ")", "-", "!", "?", "_", ",","*",";","'", '"',"[","]","--",":","\\", "/", "-rrb-", "-lrb-", "~", "$", "...", "&"]
filteredPOS = ["CD"]

negativeLabel = "-1"
positiveLabel = "1"

# Assign following Ikeda et al.
labelReversed = "1"
labelNonreversed = "-1"


# Words that cannot be sentiment words and are
# ignored for the extraction of reversed words.
posIgnoreAsSentimentWord = [
   'IN', # conjunctions
   'UH', # interjections ('yes', 'no')
   'DT', # determiners
   ]


   
""" Key for attribute used for marking all nodes. """
posMarker = "_position"

""" Value for attribute self.posMarker for the sentiment node. """
posMarkerSW = "SENTWORD"

""" Going from child to parent, given as direction in self.markNode() """
treeMarkerUp = "<"

""" Going from parent to child, given as direction in self.markNode() """
treeMarkerDown = ">"






wordLabelInconsistent = "REVERSED"
wordLabelConsistent = "NONREVERSED"
wordLabelNoSent = "NOSENT"
wordLabelSentiment = "SENTIMENT"
wordLabelModify = "MODIFY"
sentenceLabelPositive = "POS"
sentenceLabelNegative = "NEG"
sentenceLabelNeutral = "NEU"

wordLabelsSubjectivity = [wordLabelNoSent, wordLabelSentiment]
wordLabelsConsistency = [wordLabelInconsistent, wordLabelConsistent]
sentenceLabels = [sentenceLabelPositive, sentenceLabelNegative]
labelMapSubjectivity ={
   wordLabelInconsistent : wordLabelSentiment,
   wordLabelConsistent : wordLabelSentiment,
   wordLabelModify : wordLabelNoSent,
}
labelMapConsistency = {
   wordLabelModify : wordLabelConsistent,
   wordLabelNoSent : wordLabelConsistent,
}
labelMapSentence = {
   sentenceLabelNeutral : sentenceLabelPositive
}






def filterAndNormalizeCandidate(candidate, pos = ""):
   """ 
   Filter by word.
   Filter by POS.
   Normalizes candidates (sets to lowercase).
   """
   if pos != "" and pos in filteredPOS:
      return ""
   
   if candidate in filteredWords:
      return ""
   
   return candidate.lower()
   



def strF3 (floatValue):
   return ("%.3f" % round(floatValue,3))
   
def strF100 (floatValue):
   return ("%.1f" % round(floatValue * 100,1))

   
   

class simpleLogger:
   
   fileOpen = False
   name = ""
   
   def __init__(self, name):
      self.name = name
   
   def log(self, tree, candidatesString):
      if not self.fileOpen:
         now = datetime.now()
         #  nowstr = str(now.year) + str(now.month) + str(now.day) + "." + str(now.hour) + str(now.minute) + str(now.second)
         nowstr = now.strftime("%y%m%d.%H%M%S")
         self.outputFileHandle = open("../logs/extraction_" + self.name + "_" + nowstr + ".log" , "w")
         self.fileOpen = True
         print "open " + "extraction_" + self.name + "_"+ nowstr + ".log"
      
      label = tree.findLabel()
      self.outputFileHandle.write(label + ": ")
      sentence = tree.getWholeSentenceMarkSentiment()
      for word in sentence:
         self.outputFileHandle.write(word)
         self.outputFileHandle.write(" ")
      self.outputFileHandle.write(" ## " + candidatesString)
      self.outputFileHandle.write("\n")
      
   def close(self):
      self.fileOpen = False