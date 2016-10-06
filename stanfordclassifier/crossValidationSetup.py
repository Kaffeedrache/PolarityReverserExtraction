#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 11.6.12

"""
Read in file to memory.
Make k folds.
Randomized.
Same label balance in all folds as in original data.
"""

import random
import sys


def getBoolean(v):
   return v.lower() in ("yes", "true", "t", "1")

# Get parameters

allDataFileName = ""
if (len(sys.argv) > 1):
   allDataFileName = sys.argv[1]
else:
   print "no data file!!"
   exit(1)
   
folds = 0
if (len(sys.argv) > 2):
   folds = int(sys.argv[2])
else:
   folds = 10

if (len(sys.argv) > 3):
   doShuffle = getBoolean(sys.argv[3])
else:
   doShuffle = True

print "processing: " + allDataFileName
print "folds: " + str(folds)
print "shuffle: " + str(doShuffle)


# Read in original data
lines = {}
i = 0
for line in open(allDataFileName):
   parts = line.split("\t")
   label = parts[0].strip()
   features = line.strip()
   bla = lines.get(label)
   if bla == None:
      lines[label] = [features]
   else:
      bla.append(features)
      
   if line == "1" or line == "-1":
      print "ERROR!! in line" + str(i) + ": " + line
      
   i = i+1

print "Read " + str(i) + " lines."

if doShuffle:
   #Shuffle lines
   for key in lines.keys():
      random.shuffle(lines[key])
      print "Label " + key + " has " + str(len(lines[key])) + " lines"

# Create folds
i = 0
for foldno in range(1,folds+1):
   linesInFold = []
   debug = ""
   # Every fold has the same number of lines of one label
   for label in lines.keys():
      size = len(lines[label])/folds
      linesAdded = size
      if foldno == folds: # last fold, take all remaining data
         linesInFold.extend(lines[label][i*size:len(lines[label])])
         linesAdded = len(lines[label]) - i*size
      else:
         linesInFold.extend(lines[label][i*size:(i+1)*size])
      debug = debug + " " + str(label) + "=" + str(linesAdded) + ";"
   i = i+1
   print "FOLD " + str(foldno) + " :" + str(debug) # TEST !!!
   if doShuffle:
      # Write lines to file in randomized order
      random.shuffle(linesInFold)
   outfile = open(allDataFileName + "." + str(foldno), "w")
   for line in linesInFold:
      outfile.write(line + "\n")
   outfile.close()

print "Created " + str(folds) + " balanced, randomized folds from file " + allDataFileName


