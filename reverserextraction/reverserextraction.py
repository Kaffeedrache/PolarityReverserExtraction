#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 10.10.11

"""
Provides a class for extracting polarity reversers.
"""


from operator import itemgetter


class ReverserExtracter:
   """ 
   Provides a class for extracting polarity reversers.
   """
   
   candidates = {}
   
   sentWordThreshold = 1
   
   # --- Constructor ---
   
   def __init__(self):
      self.candidates = {}
      self.candidateSentWords = {}
      self.reverserScoringDictionary = None


   def cleanup(self):
      self.candidates = {}
      self.candidateSentWords = {}
      self.parseReader.cleanup()


   # --- Getter/setter ---
   
   def setContextFinder(self, contextFinder):
      """ 
      """
      self.contextFinder = contextFinder
      
   def getCandidates(self):
      """ 
      """
      return self.candidates


   def setVerboseMode(self, mode):
      """ 
      Suppresses debug output.
      """
      self.verboseMode = mode
      
      
   def setReverserScoringDictionary(self, reverserScoringDictionary):
      """ 
      """
      self.reverserScoringDictionary = reverserScoringDictionary
      

   # --- Methods ---
   

   def insertCandidateOccurrence(self, candidate, sentWord):
      """ 
      Adds an occurrence of candidate to self.candidates.
      Should be overridden in subclasses to filters candidates.
      Normalization should be done beforehand.
      The sentiment word is stored separately and used later for cleaning.
      """
      candidate = candidate.strip()
      # Ignore the empty string as a candidate
      if candidate == "":
         return
         
      # Count occurrences
      # and add modified sentiment word to list
      occurrences = self.candidates.get(candidate)
      if occurrences != None: 
         #  word in candidates -> add 1 to count
         self.candidates[candidate] = occurrences + 1
         self.candidateSentWords[candidate].add(sentWord)
      else: # not in candidates -> set 1
         self.candidates[candidate] = 1
         self.candidateSentWords[candidate] = set([sentWord])
      
      #  print candidate + " " + str(self.candidates.get(candidate)) # TEST !!!
      #  print candidate + " " + str(self.candidateSentWords.get(candidate)) # TEST !!!


   def cleanupCandidateSet(self):
      """
      Delete all candidates that modify only one sentiment word
      (= 1 ocurrence or multiple always with same word).
      """
      toDelete = []
      for c in self.candidates:
         #  if self.verboseMode:
            #  print c + ": " + str(self.candidates.get(c)) + " ocurrences with " +  str(len(self.candidateSentWords.get(c))) + " words." # TEST !!!
            #  print self.candidateSentWords.get(c) # TEST !!!
         if len(self.candidateSentWords.get(c)) <= self.sentWordThreshold:
            toDelete.append(c) # Mark entry for deletion
      
      
      # Delete entries
      for d in toDelete:
         if self.candidates.get(d) > 5:
            print d + " " + str(self.candidates.get(d))  + " " + str(self.candidateSentWords.get(d)) # TEST !!!
         del self.candidates[d]





   def extractCandidates(self, sentimentWord, tree):
      """ 
      """
      contextList = self.contextFinder.extractCandidatesFromContext(sentimentWord, tree)
      
      
      if self.reverserScoringDictionary != None:
         
         # Select only one reverser per sentence,
         # insert only this one into self.candidates
         #  print tree.getWholeSentenceMarkSentiment() # TEST !!!
         candidatesString = ""
         maxScore = 0
         bestCandidate = ""
         for a in contextList:
            score = self.reverserScoringDictionary.get(candidate)
            #  print "candidate " + candidate + " score " + str(score) + "(" + str(maxScore) # TEST !!!
            if bestCandidate == "" or score >= maxScore:
               #  print "new best candidate: " + candidate # TEST !!!
               bestCandidate = candidate
               maxScore = score
            candidatesString = candidatesString + " " + candidate # log
            
         if bestCandidate != "" and maxScore != None:
            candidatesString = candidatesString + " >>> " + bestCandidate # log
            self.insertCandidateOccurrence(bestCandidate, sentWord.getLemma())
         else:
            candidatesString = candidatesString + " " + ">> ERROR, no best candidate!!" # log
            #  print ">> ERROR, no best candidate!!"
            
      
      
      candidatesString = ""
      for c in contextList:
         self.insertCandidateOccurrence(c, sentimentWord.getLemma())
         candidatesString = candidatesString + " " + c # log

      return sentimentWord.getWord() + " ## " + candidatesString # TEST !!!
