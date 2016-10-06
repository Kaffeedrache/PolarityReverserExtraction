#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 19.10.11

"""
Constants.
"""


posNoun = "N"
posVerb = "V"
posAdj = "ADJ"
posAdv = "ADV"
posJoker = "*"
posDet = "DT"
posCard = "CD"
posPrep = "PR"


tagsDictionary = {
   posNoun : ['NN','NNS'],
   posVerb : ['VB','VBN','VBD','VBG','VBZ','VBP', # be
                  'VH','VHN','VHD','VHG','VHZ','VHP' # have
                  'VV','VVN','VVD','VVG','VVZ','VVP' ], # other
   posAdj : ['JJ', 'JJS', 'JJR'],
   posAdv : ['RB','RBR','RBS'],
   posDet : ['DT'],
   posCard : ['CD'],
   posPrep : ['IN']
}


sentimentMark = "Sent"


def isOfGeneralPOS(questionPOS, generalPOS):
   if generalPOS == posJoker:
      return True
      
   theTags = tagsDictionary.get(generalPOS)
   if theTags != None and questionPOS in theTags:
      return True
   
   return False


def getGeneralPOS(questionPOS):
   for theTags in tagsDictionary:
      if questionPOS in tagsDictionary.get(theTags):
         return theTags
   return posJoker


