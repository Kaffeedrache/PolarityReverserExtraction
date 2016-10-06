# Polarity Reverser Extraction

Code for paper (Kessler and Schütze, 2012).

__WARNING__: This is research code, it was not written with anybody else in mind nor with the goal of applying it "in real life". So it is hacky and may not be usable at all.



## Prerequisites

Stuff you will need

* [Stanford classifier](http://nlp.stanford.edu/software/classifier.shtml). For the experiments in the paper I used version 2.1.1 / stanford-classifier-2011-06-19. Needed for polarity classification with classifier voting.
 * [MPQA Subjectivity Lexicon](http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/) and/or [General Inquirer sentiment dictionary](www.wjh.harvard.edu/~inquirer/)
 * [Hu and Liu 5 products dataset](https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#datasets) and/or [Ding, Liu and Yu 9 products dataset](https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#datasets). Do do the word-level evaluation, you will need to get the [files annotated at word level](http://wiltrud.hwro.de/research/data/wordconsistency.html)
 * [ProsCons datset](http://hdl.handle.net/11022/1007-0000-0000-8E6E-6) Needed for reverser extraction.
 * [MATE parser](https://code.google.com/archive/p/mate-tools/) Needed to parse all the data (or any other dependency parser that produces CoNLL format).
 
You can restrict yourself to one lexicon (MPQA or GI) and one dataset (Hu/Liu or Ding/Liu/Yu).


## Usage


### 1. Parse the data

Everything only works on files with parsed sentences in the CoNLL format (dependency parses).
I used the [MATE parser](https://code.google.com/archive/p/mate-tools/).


### 2. Extract reversing constructions

Adapt the paths in `settingsextraction.py` to your files:

    # File with parsed sentences
    sentencesParsedFile = "../files/camerasCellphonesProsCons.txt_parsed" 

    # Files containing sentiment dictionaries 
    dictionaryLocations = {
       "WWH" : "../files/subjclueslen1-HLTEMNLP05.tff",
       "GI" : "../files/gi_dictionary",
       "Stanf" : "../files/stanfordWordsFeatureWeights.sc"
    }

    # File to save/load aspects from
    aspectsFile = "../files/aspects.txt"

    # Labeled reversers for evaluation
    goldReversersFiles = {
       "AbstractedCompletePaths" : "../files/reversersAnnotated_AP.txt",
       "AP" : "../files/reversersAnnotated_AP.txt",
       "SimplePathsPOS" : "../files/reversersAnnotated_SP.txt",
       "SP" : "../reversersAnnotated_SP.txt",
       "Words" : "../files/reversersAnnotated_Lemmas.txt",
       "Lemmas" : "../files/reversersAnnotated_Lemmas.txt"
    }


Adapt any other settings you want to change in the part of the file starting from 

    # ===== SPECIAL SETTINGS =====

You can set the following things in the command line:
 * `dictionaryType` can be "WWH" (MPQA subjectivity lexicon) or "GI" (general inquirer).
 * `representationPRCs` can be "AP" (abstract paths), "SP" (simple paths) or "Lemmas".
 * `representationPRCs` can be "AP" (abstract paths), "SP" (simple paths) or "Lemmas".
 * `scorer` can be "Rel" (relative frequency), "MI" (Mutual Information) or "MIExt" (MI+).
 * `windowsize` is a number larger than 1.
 * Additionally you can add as many of the filters as you like.
    Filters without options:
    `strongsubj` `POSignore` `intensifier` `singletons`.
    Filters with one option (the number of features/aspects to consider):
    `domain` `aspects`


Run the extraction (example):

    python mainExtractReversers.py dictionaryType WWH representationPRCs Lemmas scorer Rel windowsize 3 POSignore aspects 70 singletons
    

Now you have a set of extracted polarity reversing constructions in the file `$ROOTFOLDER/filescreated/re_r`!


### 3. Create training examples of (in)consistent sentiment words for classifier [if you want to do classifier voting, otherwise skip]

Adapt the paths in `settingsclassification.py` to your files: 

    # Hu Liu 2004 
    # Ding Liu 2008 
    sentencesParsedFile = {
       "HL" : "../files/HuLiu5productsSplitBut_Parsed.txt",
       "DL" :"../files/sentenceLabelsDingLiu_parsed.txt"
    }
    
    # Files containing sentiment dictionaries 
    dictionaryLocations = {
       "WWH" : "../files/subjclueslen1-HLTEMNLP05.tff",
       "GI" : "../files/gi_dictionary",
       "Stanf" : "../files/stanfordWordsFeatureWeights.sc"
    }
    
    # File to save/load aspects from
    aspectsFile = "../files/aspects.txt"


Adapt any other settings you want to change in the part of the file starting from 

    # ===== SPECIAL SETTINGS =====


You can set the following things in the command line:
 * `dictionaryType` can be "WWH" (MPQA subjectivity lexicon) or "GI" (general inquirer).
 * `corpusType` can be "HL" (Hu and Liu 5 products dataset) or "DL" (Ding, Liu and Yu 9 products dataset).
 * `windowsize` is a number larger than 1.

Run the training example generation (example):

    python mainExtractTrainingExamples.py dictionaryType WWH corpusType DL

The feature files are saved in the folder specified by `settingsclassification.getFeFilenamePrefix()`, usually `$ROOTFOLDER/featurefiles/featureFile$DICTTYPE$CORPUSTYPE_$ID.txt`, where the variables refer to the dictionary type, corpus type and classifier ID respectively. Which IDs are extracted is set in `settingsclassification.featureExtractorNames`.


### 4. Train/apply classifier [if you want to do classifier voting, otherwise skip]

Run Stanford classifier in 10 fold cross validation setup (for feature file names see creation of training examples above):
    
    sh useClassifier_cv.sh <feature file name>


### 5. Do polarity and consistency classification

Adapt the paths in `settingsclassification.py` to your files: 

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
    
    # Files containing sentiment dictionaries 
    dictionaryLocations = {
       "WWH" : "../files/subjclueslen1-HLTEMNLP05.tff",
       "GI" : "../files/gi_dictionary",
       "Stanf" : "../files/stanfordWordsFeatureWeights.sc"
    }
    
    # File to save/load aspects from
    aspectsFile = "../files/aspects.txt"

Adapt any other settings you want to change in the part of the file starting from 

    # ===== SPECIAL SETTINGS =====
    

You can set the following things in the command line:
 * `dictionaryType` can be "WWH" (MPQA subjectivity lexicon) or "GI" (general inquirer).
 * `corpusType` can be "HL" (Hu and Liu 5 products dataset) or "DL" (Ding, Liu and Yu 9 products dataset).
 * `windowsize` is a number larger than 1.
 * For negation voting: `inconsistencyClassificationID` can be one of ("Ikeda" "ReversingConstructionsGold" "ReversingConstructionsMIExt" "ReversingConstructionsMI"  "ReversingConstructionsRel")
 * For classifier voting: `inconsistencyClassificationID` can be one of ("Ikeda" "Constructions" "ReversingConstructionsGold" "ReversingConstructionsMIExt" "ReversingConstructionsMI" "ReversingConstructionsRel")

    
Run the baselines (example):

    python mainPolarityCassification.py inconsistencyClassifierType None dictionaryType WWH corpusType HL


Run the negation voting (example):

    python mainPolarityCassification.py inconsistencyClassifierType NegationVoting inconsistencyClassificationID Ikeda dictionaryType WWH corpusType HL windowsize 3
    
Run the classifier voting (example):

    python mainPolarityCassification.py inconsistencyClassifierType Classifier inconsistencyClassificationID Ikeda dictionaryType WWH corpusType HL windowsize 3

The result is evaluated on both levels, word-level consistency information and sentence-leven polarity information.



## Information for developers

Main file for reverser extraction is `mainExtractReversers.py`, settings are in `settingsextraction.py`.

Main file for feature generation is `mainExtractTrainingExamples.py`, settings are in `settingsclassification.py`.

Main file for polarity and consistency classification is `mainPolarityClassification.py`, settings are in `settingsclassification.py`.

- `aspects`:
   Create and read aspect lists for aspect filter.
   Used in extraction and classification.
   
- `base`:
   Representations of syntactic constructions, sentiment words and finding them in the parse tree.
   Used everywhere.

- `featureextraction`:
   Extract features for classification.
   Used in feature generation.

- `inconsistency`:
   Inconsistency classification.
   Used in classification.

- `reverserextraction`:
   Scoring and evaluation of reverser extraction.
   Used in extraction.

- `sentimentDictionary`:
   Read sentiment dictionaries, filter for POS, subjectivity.

- `stanfordclassifier`:
   Everything to do with using the Stanford classifier to do cross-validation classification.

- `subjectivity`:
   Filter that have something to do with subjectivity, filter for POS, aspects, intensifier.

- `utils`:
   Read parse trees, do statistics, other useful stuff.


## Licence and References

(c) Wiltrud Kessler

This code is distributed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported license
[http://creativecommons.org/licenses/by-nc-sa/3.0/](http://creativecommons.org/licenses/by-nc-sa/3.0/)

Please cite:
Wiltrud Kessler and Hinrich Schütze (2012)
Classification of Inconsistent Sentiment Words Using Syntactic Constructions.
In Proceedings of the 24th International Conference on Computational Linguistics (COLING 2012), Mumbai, India, 10.-14. December 2012, pages 569-578.


