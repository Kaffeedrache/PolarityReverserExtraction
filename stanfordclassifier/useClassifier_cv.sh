#!/bin/bash

# >sh useClassifier_cv.sh /fs/tmp-local/users/kesslewd/dataprcs/featurefiles/featureFile_Ikeda.txt


# Do k-fold cross-validation with Stanford classifier


if [ $# != 1 ] ; then
   echo "Usage: `basename $0` <all data filename>"
   echo "This script first creates 10 folds, then runs Stanford Classifier"
   exit 1
fi

BASEFILE=$1
FOLDS=10

STANFORDHOME="/home/users3/kesslewd/d7/Tools/stanford-classifier/stanford-classifier-2011-06-19"
PROPERTYFILE="/home/users3/kesslewd/Work/svnCode/PolarityReversers/stanfordclassifier/standardFeatures.prop"
MYPATH="/fs/tmp-local/users/kesslewd/dataprcs/folds/"


FILENAME="${BASEFILE##*/}"


# Split data into folds with python script
cp $BASEFILE $MYPATH
echo "--- Create cross validation folds for " $MYPATH/$FILENAME " ---"
python crossValidationSetup.py $MYPATH/$FILENAME $FOLDS

if [ ! -f $MYPATH/$FILENAME.1 ]; then
   echo "Error, file not found!"
   exit 1
fi


# Do classification with Stanford classifier
cd $STANFORDHOME

for i in `seq 1 $FOLDS`; # for each cv fold
do
   echo "--- Cross-validating fold" $i " ---"
   
   echo $MYPATH/$FILENAME
   
   # Create train and test files
   # Fold i is test
   # all other folds are train
   # First delete old files from previous run
   if [ -f $MYPATH/$FILENAME.test ]; then
      rm $MYPATH/$FILENAME.test
   fi
   #~ echo "moving " $MYPATH/$FILENAME.$i " to test" # TEST !!!
   cat $MYPATH/$FILENAME.$i > $MYPATH/$FILENAME.test
   
   if [ -f $MYPATH/$FILENAME.train ]; then
      rm $MYPATH/$FILENAME.train
   fi
   for j in `seq 1 $FOLDS`; 
   do
      if [ "$i" != "$j" ] ; then
         #~ echo "adding " $MYPATH/$FILENAME.$j" to train" # TEST !!!
         cat $MYPATH/$FILENAME.$j >> $MYPATH/$FILENAME.train
      fi
   done
   
   # Classify, output classifier, features, classified sentences
   if [ -f $MYPATH/$FILENAME.output.$i ]; then
      rm $MYPATH/$FILENAME.output.$i
   fi
   #~ java -cp stanford-classifier.jar edu.stanford.nlp.classify.ColumnDataClassifier -prop $PROPERTYFILE -trainFile $MYPATH/$FILENAME.train -testFile $MYPATH/$FILENAME.test -printTo $MYPATH/$FILENAME.features.$i > $MYPATH/$FILENAME.output.$i
   echo "java -cp stanford-classifier.jar edu.stanford.nlp.classify.ColumnDataClassifier -prop $PROPERTYFILE -trainFile $MYPATH/$FILENAME.train -testFile $MYPATH/$FILENAME.test > $MYPATH/$FILENAME.output.$i"
   java -cp stanford-classifier.jar edu.stanford.nlp.classify.ColumnDataClassifier -prop $PROPERTYFILE -trainFile $MYPATH/$FILENAME.train -testFile $MYPATH/$FILENAME.test > $MYPATH/$FILENAME.output.$i
   
   # Handle errors
   if [ $? -ne 0 ] ; then
      echo "ERROR !!! Fold creation failed with exit code $?"
      exit 1
   fi

done

cd $MYPATH

# Clean up
rm $MYPATH/$FILENAME.test
rm $MYPATH/$FILENAME.train

# Combine outputs into single file
if [ -f $MYPATH/$FILENAME.output ]; then
   rm $MYPATH/$FILENAME.output
fi
echo "--- Write outputs to " $FILENAME.output
for i in `seq 1 $FOLDS`;
do
   cat $MYPATH/$FILENAME.output.$i >> $MYPATH/$FILENAME.output
done


# Score
#~ echo "Score output file"
#~ python scoreOutput.py $MYPATH/$FILENAME.output

