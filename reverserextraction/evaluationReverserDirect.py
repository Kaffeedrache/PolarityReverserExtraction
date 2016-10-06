#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 26.4.12

"""
Check extracted reversers against manually annotated gold standard.
"""



labelReverser = "REVERSER"
labelNoReverser = "NOREVERSER"
labelUnsure = "UNSURE"

#  toPrintOut = [labelReverser, labelNoReverser, labelUnsure]

reverserThreshold = 30


def strF3 (floatValue):
   return ("%.3f" % round(floatValue,3))

def evaluate (reverserFileName, labeledFilename, debug = False):

   if not debug:
      toPrintOut = []
   else:
      toPrintOut = [labelReverser, labelNoReverser, labelUnsure]
      

   # Read dictionary of labeled reversers

   annotatedReversers = {}

   for line in open(labeledFilename, "r"):
      line = line.strip()
      line = line.decode('utf8','strict')
      parts = line.split("\t")
      if len(parts)>1:
         annotatedReversers[parts[0]] = parts[1]

   #  for a in annotatedReversers: # TEST !!!
      #  print a + " : " + annotatedReversers.get(a) # TEST !!!


   # Check extracted reversers against labels

   #  print "====== Begin evaluation! ======"

   lineNo = 0
   correct = 0
   incorrect = 0
   noLabel = 0
   unsure = 0

   for line in open(reverserFileName, "r"):
      line = line.strip()
      line = line.decode('utf8','strict')
      
      if line == "": # End of file
         break
      
      if lineNo >= reverserThreshold: # No. of extracted reversers
         break
      
      lineNo += 1
      
      parts = line.split(" ")
      candidate = parts[0]
      #  print candidate # TEST !!!
      
      # Check if candidate has already been annotated
      label =  annotatedReversers.get(candidate)
      if label == labelReverser:
         correct += 1
         if labelReverser in toPrintOut:
            print candidate.encode("utf-8") + " -> correct!"
      elif label == labelNoReverser:
         incorrect += 1
         if labelNoReverser in toPrintOut:
            print candidate.encode("utf-8") + " -> incorrect!"
      elif label == labelUnsure:
         unsure += 1
         if labelUnsure in toPrintOut:
            print candidate.encode("utf-8") + " -> unsure!"
      elif label == None:
         noLabel += 1
         if labelUnsure in toPrintOut:
            print candidate.encode("utf-8") + " -> no label!"
         

   if debug:
      print "Evaluated " + str(lineNo) + " extracted reversers."
      print "Correct: " + str(correct) + " (" + strF3(float(correct)/float(lineNo)) + ")"
      print "Incorrect: " + str(incorrect) + " (" + strF3(float(incorrect)/float(lineNo)) + ")"
      print "Unsure: " + str(unsure) + " (" + strF3(float(unsure)/float(lineNo)) + ")"
      print "Not labeled: " + str(noLabel) + " (" + strF3(float(noLabel)/float(lineNo)) + ")"

   return correct, incorrect, noLabel

