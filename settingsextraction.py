
# Settings for reverser extraction

# Do not change here, these are the default settings, do your changes below in SPECIAL SETTINGS

dataFolderRoot = ""


# ===== Corpus settings =====

# File with parsed sentences
sentencesParsedFile = "../files/camerasCellphonesProsCons.txt_parsed"

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

# Remove singletons
candidateCleanup = False

# Representation
representationPRCs = "AbstractedCompletePaths" # also AP
#  representationPRCs = "SimplePathsPOS" # also SP
#  representationPRCs = "Words"
#  representationPRCs = "Lemmas"

# Distance in parse-tree to check
windowsize = 4

# for extracted reversers
reFilenamePrefix  = dataFolderRoot + "filescreated/re"

# Scorer
#  scorer = "RelativeFrequency"
#  scorer = "MI"
scorer = "MI+"


# Threshold for counting ocurrences of a reverser,
# minimum number of ocurrences, all below is ignored
scoringThreshold = 10
#  scoringThreshold = 5
#  scoringThreshold = 0

# Number of revesrers to be extracted
# 0 is equivalent to all
scoringN = 0

# Labeled reversers for evaluation
goldReversersFiles = {
   "AbstractedCompletePaths" : "../files/reversersAnnotated_AP.txt",
   "AP" : "../files/reversersAnnotated_AP.txt",
   "SimplePathsPOS" : "../files/reversersAnnotated_SP.txt",
   "SP" : "../reversersAnnotated_SP.txt",
   "Words" : "../files/reversersAnnotated_Lemmas.txt",
   "Lemmas" : "../files/reversersAnnotated_Lemmas.txt"
}

#  goldReversersFile = goldReversersFiles.get(representationPRCs)

# How many iterations to run for Reverser Extraction
#  iterations = 1

# Evaluate correctness of top k extracted reversers
#  evaluationThresholds = [10, 20,30,50,70,100]
#  evaluationThresholds = [10,20,30,40,50,70,100]
evaluationThresholds = [10,20,30,40,50,60,70]
#  evaluationThresholdsShort = [10,50,70]
evaluationThresholdsShort = evaluationThresholds 



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

#  scorer = "Rel"
#  scorer = "MI"
#  scorer = "MIExt"

#  windowsize = 4
#  scoringThreshold = 0

#  aspectsThreshold = 25


#  analyseSubjectivity = True # set this if you want any of the below three subjectivity analyzers
#  posIgnore = True
#  ignoreShifters = True
#  aspectsMode = "Load"

#  strongsubj = True
#  dictionaryType = "GI_Stanf"
#  dictionaryType = "WWH_Stanf"
#  classifierThreshold = 11000

#  candidateCleanup = True



allOptionsBinary = ["dictionaryType", "representationPRCs", "windowsize", "scorer", "domain", "aspects"]
allOptionsUnary = ["strongsubj", "POSignore",  "intensifier", "singletons", "POScat"]


def setOption(name, value):
   
   print name + " = " + str(value)
   global dictionaryType
   
   if name == "dictionaryType":
      dictionaryType = value

   if name == "representationPRCs":
      global representationPRCs
      representationPRCs = value

   if name == "windowsize":
      global windowsize
      windowsize = int(value)

   if name == "scorer":
      global scorer
      scorer = value


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




def getFilterString():
   filtersstr = ""
   filtersstr += ("posIgnore " if posIgnore and analyseSubjectivity else "")
   filtersstr += ("intensifier " if ignoreShifters and analyseSubjectivity else "") 
   filtersstr += ("aspects" + str(aspectsThreshold) + " "  if aspectsMode == "Load" and analyseSubjectivity else "") 
   filtersstr += ("strongsubj " if strongsubj else "") 
   filtersstr += ("domain" + str(classifierThreshold) + " " if dictionaryType.find("_Stanf")>0 else "") 
   filtersstr += ("singletons " if candidateCleanup else "") 
   return filtersstr





