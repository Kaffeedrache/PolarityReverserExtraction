#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 14.11.12

"""
Factory class for representation of PRCs.
"""

import representation
import representationWords
import representationSimplePaths
import representationCompletePaths



def createPRCRepresentation(name):
   
   # Words
   if name == "Words":
      return representationWords.PRCRepresentationWords()
   elif name == "Lemmas":
      return representationWords.PRCRepresentationLemmas()
      
   # Simple paths
   elif name == "SimplePaths":
      return representationSimplePaths.PRCRepresentationSimplePaths()
   elif name == "SimplePathsPOS" or name == "SP":
      return representationSimplePaths.PRCRepresentationSimplePathsPOS()
      
   # Complete paths
   elif name == "CompletePaths" or name == "CP":
      return representationCompletePaths.PRCRepresentationCompletePaths()
   elif name == "AbstractedCompletePaths" or name == "AP":
      return representationCompletePaths.PRCRepresentationAbstractedCompletePaths()
   
   # Error
   print "Error, do not know this representation"
   return None


