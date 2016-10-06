#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 3.9.12

"""

"""

class LabelStatistics:


   labelTable = {}
   labelMappings = {}
   possibleLabels = []
   label1Name = ""
   label2Name = ""
   numberOfErrors = 0
   numberOfEntries = 0
   
  
   def __init__(self, possibleLabels, label1Name = "", label2Name = ""):
      self.possibleLabels = possibleLabels
      self.label1Name = label1Name
      self.label2Name = label2Name
      
      # Padding for output
      longestLabel = max(possibleLabels, key=len)
      self.pad = len(longestLabel)
   
   
   def setLabelMapping (self, labelMappings):
      self.labelMappings = labelMappings

   def getNumberOfErrors(self):
      return self.numberOfErrors
      
   def getNumberOfEntries(self):
      return self.numberOfEntries


   def printStatistics(self, name = ""):
      """
      Adds one instance of assignedLabel / goldLabel to the table.
      """
      
      
      if self.numberOfErrors > 0:
         print "Warning, had " + str(self.numberOfErrors) + " errors!!"
      
      #  debug1 = self.possibleLabels[0]
      #  debug2 = self.possibleLabels[len(self.possibleLabels)-1]
      #  print "DEBUg: classified as " + debug1 + ", really " + debug2 + ": " + str(self.labelTable.get(debug1 + " " + debug2))
      
      latexString = "LaTeX " +  self.possibleLabels[0] + " " + name.replace("_"," ") + " & " # LaTeX
      
      # Print table
      #  print ""
      row = " ".ljust(self.pad) + " | "
      for label1 in self.possibleLabels:
         row = row + label1.ljust(self.pad) + " | "
      print row +  "  > " + self.label2Name
      for label1 in self.possibleLabels:
         row = ""
         for label2 in self.possibleLabels:
            row = row + str(self.labelTable.get(label1 + " " + label2)).ljust(self.pad) + " | "
         print label1.ljust(self.pad) + " | " + row
      print " |-> " + self.label1Name
      print ""
      

      # === Calculate agreement / Accuracy ===
      agreed = 0
      total = 0
      for label1 in self.possibleLabels:
         for label2 in self.possibleLabels:
            value = self.labelTable.get(label1 + " " + label2)
            total += value
            if label1 == label2:
               agreed += value

      # Exit if there are no examples
      if total == 0:
         print "Total: 0 examples."
         print latexString + " 0 " + "  \\\\"
         return
      
      agreement = float(agreed)/float(total)
      print "Agreement/Accuracy = %i/%i = %.1f" % (agreed, total, round(agreement * 100,1))
      latexString += str(total) + " & " + str(round(agreement * 100,1)) + " & " # LaTeX


      # === Calculate Kappa ===
      
      # Probability of assignement for each class
      marginals = []
      for label1 in self.possibleLabels:
         marginalValue = 0
         for label2 in self.possibleLabels:
            # items rated as label1 by rater 1
            marginalValue += self.labelTable.get(label1 + " " + label2) 
            # items rated as label1 by rater 2
            marginalValue += self.labelTable.get(label2 + " " + label1)
         # calculate probability of this class (marginal totals / number of items rated)
         # TODO: here both annotators must have rated same amount!!
         p = float(marginalValue) / float(2 * total)
         marginals.append(p)
      
      # Probability of random agreement
      randomAgreement = 0
      for m in marginals:
         randomAgreement += (m * m)
      
      #  print "P(E) = " + str(randomAgreement)
      if randomAgreement != 1.0:
         kappa = (agreement - randomAgreement)  / (1.0 - randomAgreement)
      else:
         kappa = 0.0
      print "Kappa = %.3f" %  kappa 


      # === Calculate Precision, Recall, F-measure per class ===
      macroF = 0.0
      allTP = 0
      allFP = 0
      allFN = 0
      for label1 in self.possibleLabels:
         tp = self.labelTable.get(label1 + " " + label1)
         allTP += tp
         
         # Catch division by 0 error
         if tp == 0: 
            print "Class %s P=0.0 R=0.0 F1=0.0" % label1
            latexString += "0.0 & 0.0 & 0.0 & "  # LaTeX
            continue

         fn = 0
         fp = 0
         for label2 in self.possibleLabels:
            if label1 != label2:
               # classified as not label1, but is really label1
               index = label2 + " " + label1
               occurrences = self.labelTable.get(index)
               fn += occurrences
               # classified as label1, but is really not label1
               index = label1 + " " + label2
               occurrences = self.labelTable.get(index)
               fp += occurrences

         allFN += fn
         allFP += fp
         precision = float(tp) / float(fp + tp)
         recall = float(tp) / float(fn + tp)
         f1 = 2 * precision * recall / (precision + recall)
         macroF += f1
         print "Class %s P=%.1f R=%.1f F1=%.1f" % (label1, round(precision * 100,1), round(recall * 100,1), round(f1 * 100,1))
         latexString += str(round(precision * 100,1)) + " & " + str(round(recall * 100,1)) + " & " + str(round(f1 * 100,1)) + " & "  # LaTeX

      macroF = macroF * 100 / len(self.possibleLabels)
      print "Macro F1 = %.1f" % (macroF)
      latexString += str(round(macroF,1)) + "  \\\\"
      
      microP = float(allTP) / float(allFP + allTP)
      microR = float(allTP) / float(allFN + allTP)
      microF = 2 * microP * microR / (microP + microR)
      # with two classes microF is equivalent to Accuracy
      
      print latexString 
      #  print "LaTeX: & " +  utils.strF100(accuracy)  + " & " + utils.strF100(precisionPos) + " & " + utils.strF100(recallPos) + " & " + utils.strF100(f1Pos) + " & " + utils.strF100(precisionNeg) + " & " + utils.strF100(recallNeg) + " & " + utils.strF100(f1Neg) + " & " + utils.strF100((f1Pos + f1Neg)/2.0) + "\\\\"



   def initializeTable(self):
      """
      Initializes the table with count 0 in all cases.
      Overwrites any existing old table.
      """
      self.labelTable = {}
      for label1 in self.possibleLabels:
         for label2 in self.possibleLabels:
            self.labelTable[label1 + " " + label2] = 0



   def getLabelMapping(self, assignedLabel):
      """
      Check self.labelMappings and return mapping.
      """
      # Map labels (if a mapping is given)
      if assignedLabel in self.labelMappings:
         return self.labelMappings.get(assignedLabel)
      else:
         return assignedLabel



   def addToTable(self, assignedLabel, goldLabel):
      """
      Adds one instance of assignedLabel / goldLabel to the table.
      """
      
      # Errorcheck: Invalid label
      if assignedLabel not in self.possibleLabels:
         print "LABEL ERROR, invalid assigned label: " + str(assignedLabel)
         self.numberOfErrors += 1
         return
      if goldLabel not in self.possibleLabels:
         print "LABEL ERROR, invalid gold label: " + str(goldLabel)
         self.numberOfErrors += 1
         return
      
      # Normal case, add 1 to corresponding table entry
      index = assignedLabel + " " + goldLabel
      occurrences = self.labelTable.get(index)
      if occurrences != None:
         self.labelTable[index] = occurrences + 1
      else:
         self.labelTable[index] = 1
      self.numberOfEntries+= 1
   
   