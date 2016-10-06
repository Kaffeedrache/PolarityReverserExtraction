
# Settings for feature extraction and classification

# Do not change here, these are the default settings, do your changes below in SPECIAL SETTINGS

dataFolderRoot = ""


# ===== Corpus settings =====

corpusType = "HL"
#  corpusType = "DL"

# Hu Liu 2004 
# Ding Liu 2008 
sentencesParsedFile = {
   "HL" : "../files/HuLiu5productsSplitBut_Parsed.txt",
   "DL" :"../files/sentenceLabelsDingLiu_parsed.txt"
}

# Word-level labeled files
goldLabelsFile = {
   "HL" :  "../files/sentimentWordsAnnotated_HuLiu.txt",
   "DL" : "../files/sentimentWordsAnnotated_DingLiu.txt"
}


# ===== Sentiment dictionary settings =====

# Files containing sentiment dictionaries 
dictionaryLocations = {
   "WWH" : "../files/subjclueslen1-HLTEMNLP05.tff",
   "GI" : "../files/gi_dictionary",
   "Stanf" : "../files/stanfordWordsFeatureWeights.sc"
}

# Dictionary to use
# Affects the choice of parser and classes to read/write parse trees
# as well as the sentement dictionary.
# Possible choices are 
# WWH : Wilson Wiebe Hoffmann subjectivity clues
# GI: General Inquirer
# Stanf : Stanford Classifier
# WWH_Stanf : Wilson Wiebe Hoffmann subjectivity clues filtered with Stanford Classifier
# GI_Stanf : General Inquirer filtered with Stanford Classifier
dictionaryType = "WWH"

# POS tags to exclude from dictionary
posExcludeList = [] # don't exclude anything

# Use only words marked as 'strongsubj'
strongsubj = False

# If classifier filtering is used, set threshold for top n features to be used
classifierThreshold = 1000


# ===== Subjectivity classification settings =====

# Do not do subjectivity analysis by default (if this is false, ignore everything below)
analyseSubjectivity = False

# Set words with this POS to be ignored as sentiment word
posIgnore = False
posIgnoreAsSentimentWord =  [
   'IN', # prepositions or conjunctions
   'UH', # interjections ('yes', 'no')
   'DT', # determiners
   'CD', # numbers
   ]

# Should adverbs modifying sentiment words be ignored as polarity shifters
ignoreShifters = False

# Threshold for number of aspects to use
aspectsThreshold = 100

# If to calculate aspects or to load from file
# Possible values:
# Calculate: Calculate
# Save: calculate and save to file
# Load: load from file
# None: do not use aspects
aspectsMode = "None"

# File to save/load aspects from
aspectsFile = "../files/aspects.txt"


# ===== Reverser extraction settings =====

# Representation
representationPRCs = "AbstractedCompletePaths" # also AP
#  representationPRCs = "SimplePathsPOS" # also SP
#  representationPRCs = "Words"
#  representationPRCs = "Lemmas"

# Distance in parse-tree to check
windowsize = 3


# ===== Feature extraction settings =====

# Where to write feature files to (used in creation of trianing examples for classifier)
def getFeFilenamePrefix():
   return dataFolderRoot + "featurefiles/featureFile" + dictionaryType + corpusType + "_"


# Which features to extract = ReversingConstructions + id
featureExtractorNames = [
"Ikeda", # BoW
"Constructions", # BoC
"ReversingConstructionsGold", # BoPRC (PRC-gold)
"ReversingConstructionsMI",
"ReversingConstructionsRel",
"ReversingConstructionsMIExt", # BoPRC (PRC-system)
]


# ===== Feature extraction and Classification settings =====

# Load reversers from file
reverserFileGold = {
   "ReversingConstructionsGold" : "_files/reversingConstructions_gold2.txt",
   #  "ReversingConstructionsMI" : "_files/reversingConstructions_mi2.txt",
   #  "ReversingConstructionsMIExt" : "_files/reversingConstructions_miExt2.txt",
   "ReversingConstructionsMI" : "_files/reversingConstructions_MI.txt",
   "ReversingConstructionsMIExt" : "_files/reversingConstructions_MIExt.txt",
   "ReversingConstructionsRel" : "_files/reversingConstructions_Rel.txt",
   "Ikeda" : "_files/negationWords.txt",
}

# How many reverseres to load
cutoffThreshold = 70


# ===== Classification settings =====

# File to look up output of classifier
def getClassifierOutputFilename(classifierID): # type is only classifier
   return dataFolderRoot + "folds/featureFile" + dictionaryType + corpusType + "_" + classifierID + ".txt.output"
   
analyseConsistency = True

# Type of classifier to use
inconsistencyClassifierType = "None" # no reverser treatment, all words are consistent
#  inconsistencyClassifierType = "NegationVoting" # use negation cues in context
#  inconsistencyClassifierType = "Classifier" # classify with ml (lookup)

# Type of features
inconsistencyClassificationID = ""
#  inconsistencyClassificationID = "Ikeda"
#  inconsistencyClassificationID = "Constructions"
#  inconsistencyClassificationID = "ReversingConstructionsGold"
#  inconsistencyClassificationID = "MI"
#  inconsistencyClassificationID = "MIExt"


# Folder for significance output
def getEvalOutputFilename(classifierType,classifierID, sentences=True):
   prefix = dataFolderRoot + "eval/"
   suffix = dictionaryType + corpusType + "_"+ classifierType + classifierID + (str(windowsize) if inconsistencyClassifierType != "None" else "")  + getFilterString() + ".txt"
   if sentences:
      return prefix + "evaluations_" + suffix
   else:
      return prefix + "evaluationw_" + suffix

   

# ===== SPECIAL SETTINGS =====

# These overwrite the defaults set above
# For explanations see there

#  dictionaryType = "WWH"
#  dictionaryType = "GI"
#  dictionaryType = "Stanf"

#  representationPRCs = "AP"
#  representationPRCs = "SP"
#  representationPRCs = "CP"
#  representationPRCs = "Lemmas"

#  windowsize = 3

#  analyseSubjectivity = True # set this if you want any of the below three subjectivity analyzers
#  posIgnore = True
#  ignoreShifters = True
#  aspectsMode = "Load"

#  strongsubj = True
#  dictionaryType = "GI_Stanf"
#  dictionaryType = "WWH_Stanf"

#  corpusType = "HL"
#  corpusType = "DL"


#  analyseConsistency = False


#  inconsistencyClassifierType = "None" # no reverser treatment, all words are consistent
#  inconsistencyClassifierType = "NegationVoting" # use negation cues in context
#  inconsistencyClassifierType = "Classifier" # classify with ml (lookup)

# Type of classification
#  inconsistencyClassificationID = ""
#  inconsistencyClassificationID = "Ikeda"
#  inconsistencyClassificationID = "Constructions"
#  inconsistencyClassificationID = "Gold"
#  inconsistencyClassificationID = "MI"
#  inconsistencyClassificationID = "MIExt"




allOptionsBinary = ["dictionaryType", "corpusType", "inconsistencyClassifierType", "inconsistencyClassificationID", "windowsize", "domain", "aspects"]
allOptionsUnary = ["strongsubj", "POSignore", "intensifier"]


def setOption(name, value):
   
   print name + " = " + str(value)
   global dictionaryType
   
   if name == "dictionaryType":
      dictionaryType = value
      
   if name == "corpusType":
      global corpusType
      corpusType = value

   if name == "representationPRCs":
      global representationPRCs
      representationPRCs = value

   if name == "windowsize":
      global windowsize
      windowsize = int(value)


   if name == "intensifier":
      global ignoreShifters
      ignoreShifters = True

   if name == "POSignore":
      global posIgnore
      posIgnore = True

   if name == "aspects":
      global aspectsMode
      global aspectsThreshold
      aspectsMode = "Load"
      aspectsThreshold = int(value)
      
   global analyseSubjectivity
   if ignoreShifters or posIgnore or aspectsMode == "Load":
      analyseSubjectivity = True
      
      
   if name == "strongsubj":
      global strongsubj
      strongsubj = True
      
   if name == "domain":
      dictionaryType += "_Stanf"
      global classifierThreshold
      classifierThreshold = int(value)
      
      
   if name == "singletons":
      global candidateCleanup
      candidateCleanup = True
      
   if name == "POScat":
      global posExcludeList
      posExcludeList = []


   if name == "inconsistencyClassifierType":
      global inconsistencyClassifierType
      inconsistencyClassifierType = value

   if name == "inconsistencyClassificationID":
      global inconsistencyClassificationID
      inconsistencyClassificationID = value


def getFilterString():
   filtersstr = ""
   filtersstr += ("posIgnore " if posIgnore and analyseSubjectivity else "")
   filtersstr += ("intensifier " if ignoreShifters and analyseSubjectivity else "") 
   filtersstr += ("aspects" + str(aspectsThreshold) + " "  if aspectsMode == "Load" and analyseSubjectivity else "") 
   filtersstr += ("strongsubj " if strongsubj else "") 
   filtersstr += ("domain" + str(classifierThreshold) + " " if dictionaryType.find("_Stanf")>0 else "") 
   return filtersstr



