#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 21.12.11


"""

"""
from operator import itemgetter





def checkWordOcurrences (dictionary, file):
   """
   """
   mydict = {}
   
   # Read in file
   input_file = open(file)
   for line in input_file:
      
      line = line.strip()
      if line != "":
         
         # Split into parts
         parts = line.split(' ')
         
         # check every word if it is in the dictionary
         for word in parts:
            word = word.lower()
            if dictionary.get(word) != None:
               # Count occurrences
               occurrences = mydict.get(word)
               if occurrences != None: 
                  #  word in candidates -> add 1 to count
                  mydict[word] = occurrences + 1
               else: # not in candidates -> set 1
                  mydict[word] = 1
         
      
   # Positive dictionary - first entries
   #  itemno = 0
   #  for i in sorted(mydict.items(), key=itemgetter(1)):
      #  print i
   
   return mydict


